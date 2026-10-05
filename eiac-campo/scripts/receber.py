"""Recebimento humano de material preparado; não consulta APIs externas."""
import argparse
import datetime
import fcntl
import hashlib
import json
import pathlib
import re
import canais as K


def instante(valor):
    K.texto(valor)
    data = datetime.datetime.fromisoformat(valor.replace('Z', '+00:00'))
    K.exigir(data.tzinfo is not None, 'data da origem/coleta precisa ter fuso')
    return data


def receber(arquivo, manifesto, autor=None, nova_versao=None):
    st, pb = K.contexto(autor)
    origem = json.loads(K.seguro(manifesto, 'rascunho/entrada').read_text())
    K.exigir(isinstance(origem, dict), 'manifesto precisa ser objeto')
    obrigatorios = {'ferramenta', 'objeto_id', 'conteiner_id', 'modificado_em', 'coletado_em'}
    K.exigir(obrigatorios <= set(origem) <= obrigatorios | {'submissao_id', 'campos_ocultos'}, 'campos do manifesto inválidos')
    K.exigir(origem['ferramenta'] in K.CONTEINER and origem['ferramenta'] != 'calendar', 'ferramenta de entrada inválida')
    K.id_externo(origem['objeto_id']); K.id_externo(origem['conteiner_id'])
    K.exigir(instante(origem['coletado_em']) >= instante(origem['modificado_em']), 'coleta anterior à modificação')
    candidatos = [c for c in K.G.selecionar(pb, st['etapa_atual'], 'entrada')
                  if c['ferramenta'] == origem['ferramenta']
                  and c['ids'][K.CONTEINER[c['ferramenta']]] == origem['conteiner_id']]
    K.exigir(len(candidatos) == 1, 'origem não declarada para entrada na etapa corrente')
    canal = candidatos[0]
    if canal['filtro']:
        K.exigir(isinstance(origem.get('campos_ocultos'), dict)
                 and origem['campos_ocultos'].get(canal['filtro']['campo']) == canal['filtro']['valor'], 'filtro de outro caso ou ausente')
        K.id_externo(origem.get('submissao_id'))
    else:
        K.exigir('submissao_id' not in origem and 'campos_ocultos' not in origem, 'metadados de formulário incompatíveis')
    p = K.seguro(arquivo, 'rascunho/entrada')
    K.exigir(p.is_file(), 'arquivo ausente')
    conteudo = p.read_bytes(); sha = hashlib.sha256(conteudo).hexdigest()
    index = K.seguro('registro/recebimentos.json')
    registro = json.loads(index.read_text()) if index.exists() else {'schema': 1, 'recebimentos': []}
    eventos = [e for e in K.E.eventos() if e.get('evento') == 'MaterialRecebido']
    K.exigir(isinstance(registro, dict) and registro.get('schema') == 1
             and isinstance(registro.get('recebimentos'), list), 'manifesto de recebimentos inválido')
    K.exigir(bool(index.exists()) == bool(eventos), 'manifesto e trilha de recebimento divergentes')
    if eventos:
        K.exigir(eventos[-1].get('registro_sha256') == hashlib.sha256(index.read_bytes()).hexdigest(), 'manifesto de recebimentos adulterado')
    anteriores = [r for r in registro['recebimentos'] if r['sha256'] == sha
                  or (r['origem']['conteiner_id'], r['origem']['objeto_id']) == (origem['conteiner_id'], origem['objeto_id'])]
    decisao = None
    if anteriores:
        K.exigir(nova_versao is not None, 'hash ou objeto já recebido; nova versão exige decisão humana')
        decisao = json.loads(K.seguro(nova_versao, 'rascunho').read_text())
        K.exigir(isinstance(decisao, dict) and decisao.get('decisor') == st['responsavel'], 'decisor deve ser responsável nomeado')
        K.texto(decisao.get('motivo')); datetime.date.fromisoformat(decisao['data'])
        K.exigir(decisao.get('recebimento_anterior') == anteriores[-1]['id'], 'decisão não identifica o recebimento anterior vigente')
    else:
        K.exigir(nova_versao is None, 'nova versão sem recebimento anterior')
    agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ident = f"REC-{len(registro['recebimentos'])+1:06d}"
    K.exigir(bool(re.fullmatch('[a-z0-9-]+', canal['finalidade'])), 'finalidade incompatível com destino estável')
    extensao = p.suffix.lower() if re.fullmatch(r'\.[a-zA-Z0-9]{1,10}', p.suffix) else '.bin'
    destino = K.seguro(f"fontes/{canal['finalidade']}/{agora[:10]}-{ident}{extensao}")
    K.exigir(not destino.exists(), 'destino já existe')
    ref = dict(id=ident, arquivo=str(destino), sha256=sha, finalidade=canal['finalidade'],
               etapa=st['etapa_atual'], origem=origem, autor=st['responsavel'], data=agora,
               canais_versao=K.G.carregar(pb)['versao'], decisao_nova_versao=decisao)
    backup = index.read_bytes() if index.exists() else None
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destino.open('xb') as f: f.write(conteudo)
        K.exigir(hashlib.sha256(destino.read_bytes()).hexdigest() == sha, 'hash diverge após cópia')
        registro['recebimentos'].append(ref); K.escrever(index, registro)
        K.E.evento('MaterialRecebido', autor=st['responsavel'], recebimento=ident, arquivo=str(destino),
                   sha256=sha, origem=origem, registro_sha256=hashlib.sha256(index.read_bytes()).hexdigest())
    except Exception:
        destino.unlink(missing_ok=True)
        if backup is None: index.unlink(missing_ok=True)
        else: index.write_bytes(backup)
        raise
    return ref


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--arquivo', required=True); ap.add_argument('--manifesto', required=True)
    ap.add_argument('--autor'); ap.add_argument('--nova-versao')
    ap.add_argument('--aprovacao', help='testemunho conferido pela guarda da sessão')
    a = ap.parse_args()
    try:
        with K.seguro('registro/.canais.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            resultado = receber(a.arquivo, a.manifesto, a.autor, a.nova_versao)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        K.E.evento('TentativaNegada', autor=(K.E.ler() or {}).get('responsavel'), operacao='receber-material', motivo=str(exc))
        ap.exit(1, 'Recusado: '+str(exc)+'\n')


if __name__ == '__main__': main()
