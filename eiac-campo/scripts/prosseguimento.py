"""Decisão humana de F0. Executar no terminal, fora da sessão do agente.

Uso: python3 prosseguimento.py --entrada rascunho/prosseguimento.json
Nova decisão exige a versão seguinte; cada registro anterior é preservado.
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import pathlib
import sys
import canais as K

E = K.E
X = __import__('estrutura')
DIRETORIO = 'registro/prosseguimento'
VIGENTE = DIRETORIO + '/vigente.yaml'
CAMPOS = {'versao', 'decisor', 'data', 'desfecho', 'motivo', 'ficha'}


def carregar():
    p = K.seguro(VIGENTE)
    eventos = [e for e in E.eventos() if e.get('evento') == 'ProsseguimentoDecidido']
    if not p.exists():
        K.exigir(not eventos, 'registro vigente ausente após decisão')
        return None
    b = p.read_bytes()
    K.exigir(eventos and eventos[-1].get('sha256') == hashlib.sha256(b).hexdigest()
             and eventos[-1].get('arquivo') == VIGENTE, 'integridade da decisão diverge da trilha')
    dados = X.carregar_yaml(b.decode('utf-8'))
    schema = json.loads(K.seguro('registro/prosseguimento.schema.json').read_text())
    K.exigir(not X.validar(dados, schema, 'registro'), 'registro de prosseguimento inválido')
    K.exigir(E.pessoa_nomeada(dados['decisor']) and E.pessoa_nomeada(dados['autor']), 'autoria nominal inválida')
    K.exigir(type(dados['versao']) is int and dados['versao'] > 0, 'versão inválida')
    historico = K.seguro(f"{DIRETORIO}/decisao-{dados['versao']:04d}.yaml")
    K.exigir(historico.read_bytes() == b, 'registro vigente difere da decisão preservada')
    return dados


def gravar(entrada):
    st, pb = K.contexto()
    K.exigir(any(a['id'] == 'decidir-prosseguimento' for a in pb['decisoes_humanas']),
             'ato não declarado no contrato deste caso')
    K.exigir(st['etapa_atual'] == 'F0' or
             (st['etapa_atual'] == 'P1' and st['cumprimentos'].get('F0', {}).get('cumprido')
              and not st['cumprimentos'].get('P1', {}).get('cumprido')), 'decisão somente em F0 ou antes de iniciar P1')
    K.exigir(st.get('nivel') in pb['niveis'], 'nível precisa ser apurado antes da decisão')
    dados = json.loads(K.seguro(entrada, 'rascunho').read_text())
    K.exigir(isinstance(dados, dict) and set(dados) == CAMPOS, 'campos da decisão inválidos')
    schema = json.loads(K.seguro('registro/prosseguimento.schema.json').read_text())
    erros = X.validar(dados, schema, 'decisao')
    K.exigir(not erros, '; '.join(erros))
    for campo in ('decisor', 'data', 'desfecho', 'motivo', 'ficha'):
        K.texto(dados[campo])
    K.exigir(E.pessoa_nomeada(dados['decisor']), 'decisor precisa ser pessoa nomeada')
    datetime.date.fromisoformat(dados['data'])
    K.exigir(type(dados['versao']) is int and dados['versao'] > 0, 'versão precisa ser inteiro positivo')
    ficha = K.seguro(dados['ficha'], 'caso')
    K.exigir(ficha.is_file() and bool(ficha.read_text().strip()), 'ficha E1 preparada ausente ou vazia')
    anterior = carregar()
    K.exigir(dados['versao'] == (anterior['versao'] + 1 if anterior else 1), 'versão deve suceder a decisão vigente')
    novo = dict(dados, autor=st['responsavel'], ficha_sha256=hashlib.sha256(ficha.read_bytes()).hexdigest())
    b = ('\n'.join(k + ': ' + json.dumps(v, ensure_ascii=False) for k, v in novo.items()) + '\n').encode()
    historico = K.seguro(f"{DIRETORIO}/decisao-{novo['versao']:04d}.yaml")
    K.exigir(not historico.exists(), 'decisão anterior não pode ser sobrescrita')
    p = K.seguro(VIGENTE)
    backup = p.read_bytes() if p.exists() else None
    try:
        historico.write_bytes(b)
        p.write_bytes(b)
        E.evento('ProsseguimentoDecidido', autor=st['responsavel'], decisor=dados['decisor'],
                 data=dados['data'], desfecho=dados['desfecho'], motivo=dados['motivo'],
                 versao=dados['versao'], arquivo=VIGENTE, historico=str(historico),
                 sha256=hashlib.sha256(b).hexdigest(), ficha_sha256=novo['ficha_sha256'])
    except Exception:
        if backup is None: p.unlink(missing_ok=True)
        else: p.write_bytes(backup)
        historico.unlink(missing_ok=True)
        raise
    return novo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--entrada', required=True)
    a = ap.parse_args()
    try:
        pasta = K.seguro(DIRETORIO); pasta.mkdir(parents=True, exist_ok=True)
        with K.seguro(DIRETORIO + '/.lock').open('a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            resultado = gravar(a.entrada)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        E.evento('TentativaNegada', autor=(E.ler() or {}).get('responsavel'),
                 operacao='decidir-prosseguimento', motivo=str(exc))
        ap.exit(1, 'Recusado: ' + str(exc) + '\n')


if __name__ == '__main__': main()
