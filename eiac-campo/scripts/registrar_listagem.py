"""Registro humano de listagem MCP limitada a contêiner declarado."""
import argparse
import datetime
import fcntl
import hashlib
import json
import re
import canais as K
import escopo_externo as S


def registrar(entrada, autor=None):
    st, pb = K.contexto(autor)
    dados = json.loads(K.seguro(entrada, 'rascunho/entrada').read_text())
    K.exigir(isinstance(dados, dict) and set(dados) == {'ferramenta_externa', 'argumentos', 'conteiner_id', 'objetos', 'coletado_em'}, 'manifesto de listagem inválido')
    cfg = S.contrato(pb)
    regras = [r for r in cfg['regras'] if re.fullmatch(r['padrao'], dados['ferramenta_externa']) and r.get('operacao') == 'listar']
    K.exigir(len(regras) == 1, 'ferramenta não declarada como listagem')
    erro = S.conferir(pb, dados['ferramenta_externa'], dados['argumentos'])
    K.exigir(erro is None, erro)
    escopos = [a for a in regras[0]['argumentos'] if a['tipo'] in ('id_de_canal', 'expressao')]
    K.exigir(any(dados['conteiner_id'] in S.ids(pb, a) and (
        S.argumento(dados['argumentos'], a['campo']) == dados['conteiner_id'] if a['tipo'] == 'id_de_canal'
        else bool(re.fullmatch(a['expressao'].replace('{id}', re.escape(dados['conteiner_id'])), S.argumento(dados['argumentos'], a['campo'])))) for a in escopos),
        'contêiner não corresponde à chamada de listagem')
    K.exigir(isinstance(dados['objetos'], list) and len(set(dados['objetos'])) == len(dados['objetos']), 'lista de objetos inválida')
    for ident in dados['objetos']: K.id_externo(ident)
    instante = datetime.datetime.fromisoformat(dados['coletado_em'].replace('Z', '+00:00'))
    K.exigir(instante.tzinfo is not None, 'data da listagem exige fuso')
    p = K.seguro(pb['escopo_ferramentas_externas']['listagens'])
    if p.exists(): S.ids_listados(pb)
    reg = json.loads(p.read_text()) if p.exists() else {'schema': 1, 'listagens': []}
    reg['listagens'].append(dict(dados, autor=st['responsavel']))
    K.escrever(p, reg)
    K.E.evento(pb['escopo_ferramentas_externas']['evento_listagem'], autor=st['responsavel'],
               conteiner_id=dados['conteiner_id'], sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    return dados


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--entrada', required=True); ap.add_argument('--autor')
    ap.add_argument('--aprovacao', help='testemunho conferido pela guarda da sessão')
    a = ap.parse_args()
    try:
        with K.seguro('registro/.canais.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            resultado = registrar(a.entrada, a.autor)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        K.E.evento('TentativaNegada', autor=(K.E.ler() or {}).get('responsavel'), operacao='registrar-listagem', motivo=str(exc))
        ap.exit(1, 'Recusado: '+str(exc)+'\n')


if __name__ == '__main__': main()
