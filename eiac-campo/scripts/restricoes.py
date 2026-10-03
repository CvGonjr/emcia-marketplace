"""Vínculos humanos de RH-xx a fontes curadas; EMCIA-HAB-01 §3.4 e CTX-01 §3.7.

Executar no terminal do engenheiro. Revisões exigem --nova-versao com JSON
{restricao, versao_anterior, decisor, motivo, data} em rascunho/.
"""
import argparse
import copy
import datetime
import fcntl
import hashlib
import json
import pathlib
import re
import sys
import canais as K

E = K.E
X = __import__('estrutura')


def habilitacao():
    p = K.seguro('registro/habilitacao.json')
    dados = json.loads(p.read_text())['vigente']
    itens = dados['restricoes']
    K.exigir(isinstance(itens, list), 'restrições importadas inválidas')
    K.exigir((dados['desfecho'] == 'prosseguir' and not itens) or
             (dados['desfecho'] == 'prosseguir com restrição' and bool(itens)), 'desfecho e restrições divergentes')
    ids = []
    for r in itens:
        K.exigir(isinstance(r, dict) and bool(re.fullmatch(r'RH-\d+', r.get('id', '')))
                 and r['id'] not in ids, 'RH inválido ou duplicado')
        for campo in ('item', 'motivo', 'restricao'): K.texto(r.get(campo))
        ids.append(r['id'])
    return dados


def fonte(ident):
    K.exigir(isinstance(ident, str) and bool(re.fullmatch(r'F-\d{3,}', ident)), 'fonte inválida: '+str(ident))
    p = K.seguro('contexto/fontes/'+ident+'.yaml')
    K.exigir(p.is_file(), 'fonte não existe curada: '+ident)
    d = X.carregar_yaml(p.read_text())
    schema = json.loads(K.seguro('registro/contexto.schema.json').read_text())
    K.exigir(isinstance(d, dict) and d.get('id') == ident and not X.validar(d, schema, 'fonte'), 'fonte sem contrato curado: '+ident)
    K.exigir(E.pessoa_nomeada(d.get('registrado_por')) and E.pessoa_nomeada(d.get('responsavel')), 'fonte sem autoria nominal: '+ident)
    K.exigir(any(e.get('evento') == 'ObjetoContextoCurado' and e.get('id') == ident
                 and e.get('arquivo') == str(p) for e in E.eventos()), 'fonte não existe curada na trilha: '+ident)
    return d


def carregar(hab=None):
    p = K.seguro('registro/restricoes.json')
    if not p.exists():
        K.exigir(not any(e.get('evento') in ('RestricaoVinculada','RestricaoDispensada') for e in E.eventos()), 'registro de restrições ausente após ato registrado')
        return dict(schema=1, vigentes=[], historico=[])
    d = json.loads(p.read_text())
    K.exigir(isinstance(d, dict) and set(d) == {'schema', 'vigentes', 'historico'} and d['schema'] == 1
             and isinstance(d['vigentes'], list) and isinstance(d['historico'], list), 'registro de restrições inválido')
    eventos = [e for e in E.eventos() if e.get('evento') in ('RestricaoVinculada', 'RestricaoDispensada')]
    K.exigir(eventos and eventos[-1].get('registro_sha256') == hashlib.sha256(p.read_bytes()).hexdigest(), 'integridade do registro de restrições diverge da trilha')
    ids = []
    for r in d['vigentes']:
        K.exigir(r['restricao'] not in ids, 'restrição vigente duplicada')
        ids.append(r['restricao'])
        K.exigir(E.pessoa_nomeada(r['autor']) and isinstance(r['versao'], int) and r['versao'] > 0, 'autoria ou versão inválida')
        K.exigir((r['estado'] == 'vinculada' and isinstance(r['fontes'], list) and bool(r['fontes']) and r['motivo'] is None)
                 or (r['estado'] == 'dispensada' and r['fontes'] == [] and isinstance(r['motivo'], str) and bool(r['motivo'].strip())), 'vínculo ou dispensa inválidos')
        if hab is not None: K.exigir(r['importacao'] == hab['id'], 'vínculo refere importação anterior')
    return d


def pendentes(hab, registro):
    return [r['id'] for r in hab['restricoes'] if not any(v['restricao'] == r['id'] and v['importacao'] == hab['id'] for v in registro['vigentes'])]


def gravar(operacao, ident, fontes=None, motivo=None, autor=None, nova_versao=None):
    st, pb = K.contexto()  # Autoria fixada no responsável do caso.
    K.exigir(autor is None or E.pessoa_nomeada(autor), 'autor precisa ser pessoa nomeada')
    K.exigir(autor is None or autor == st['responsavel'], 'autor deve ser responsável nomeado do caso')
    hab = habilitacao()
    rh = next((r for r in hab['restricoes'] if r['id'] == ident), None)
    K.exigir(rh is not None, 'RH inexistente na habilitação importada: '+ident)
    reg = carregar(hab)
    anterior = next((r for r in reg['vigentes'] if r['restricao'] == ident), None)
    decisao = None
    if anterior:
        K.exigir(nova_versao is not None, 'nova versão de vínculo exige decisão explícita')
        decisao = json.loads(K.seguro(nova_versao, 'rascunho').read_text())
        K.exigir(isinstance(decisao, dict) and decisao.get('restricao') == ident and
                 decisao.get('versao_anterior') == anterior['versao'], 'decisão não identifica a versão anterior')
        K.exigir(decisao.get('decisor') == st['responsavel'] and E.pessoa_nomeada(decisao.get('decisor')), 'decisor precisa ser responsável nomeado')
        K.texto(decisao.get('motivo')); datetime.date.fromisoformat(decisao['data'])
    else:
        K.exigir(st['etapa_atual'] == 'P2' and not st['cumprimentos'].get('P2', {}).get('cumprido'), 'vínculo inicial só na etapa corrente P2')
        K.exigir(nova_versao is None, 'nova versão sem vínculo anterior')
    K.exigir(st['etapa_atual'] == 'P2' or (anterior is not None and st['cumprimentos'].get('P2', {}).get('cumprido')),
             'revisão fora de P2 exige P2 encerrada e decisão explícita')
    if operacao == 'vincular':
        K.exigir(isinstance(fontes, list) and bool(fontes) and len(set(fontes)) == len(fontes), 'lista de fontes vazia ou duplicada')
        for ident_fonte in fontes: fonte(ident_fonte)
        estado = 'vinculada'; motivo = None
    else:
        K.exigir(isinstance(motivo, str) and bool(motivo.strip()), 'dispensa exige motivo')
        estado = 'dispensada'; fontes = []
    agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    novo = dict(restricao=ident, importacao=hab['id'], estado=estado, fontes=fontes, motivo=motivo,
                autor=st['responsavel'], data=agora, versao=(anterior['versao']+1 if anterior else 1), decisao=decisao)
    if anterior:
        reg['historico'].append(copy.deepcopy(anterior)); reg['vigentes'].remove(anterior)
    reg['vigentes'].append(novo)
    p = K.seguro('registro/restricoes.json'); backup = p.read_bytes() if p.exists() else None
    try:
        K.escrever(p, reg)
        E.evento('RestricaoVinculada' if estado == 'vinculada' else 'RestricaoDispensada',
                 autor=st['responsavel'], restricao=ident, versao=novo['versao'], fontes=fontes, motivo=motivo,
                 importacao=hab['id'], registro_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    except Exception:
        if backup is None: p.unlink(missing_ok=True)
        else: p.write_bytes(backup)
        raise
    return novo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('operacao', choices=['vincular', 'dispensar'])
    ap.add_argument('--restricao', required=True); ap.add_argument('--fontes')
    ap.add_argument('--motivo'); ap.add_argument('--autor'); ap.add_argument('--nova-versao')
    a = ap.parse_args()
    try:
        with K.seguro('registro/.restricoes.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            K.exigir((a.operacao == 'vincular' and a.fontes is not None and a.motivo is None)
                     or (a.operacao == 'dispensar' and a.fontes is None), 'argumentos incompatíveis com a operação')
            resultado = gravar(a.operacao, a.restricao, a.fontes.split(',') if a.fontes is not None else None,
                              a.motivo, a.autor, a.nova_versao)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        E.evento('TentativaNegada', autor=(E.ler() or {}).get('responsavel'), operacao='vincular-restricao', motivo=str(exc))
        ap.exit(1, 'Recusado: '+str(exc)+'\n')



def fontes_contexto(ident):
    """Resolve ids por relações explícitas de objetos já curados, sem inferir."""
    import fontes_registro as F
    if re.fullmatch(r'F-\d{3,}', ident):
        fonte(ident)
        return {ident}
    if re.fullmatch(r'REC-\d+', ident):
        pb = json.loads(K.seguro('registro/playbook.json').read_text())
        F.conferir(pb, ident)
        encontrados = []
        for p in K.seguro('contexto/fontes').glob('F-*.yaml'):
            d = X.carregar_yaml(K.seguro(p).read_text())
            if isinstance(d, dict) and ident in d.get('recebimentos', []):
                fonte(d['id']); encontrados.append(d['id'])
        K.exigir(encontrados, 'relação de fonte ausente para '+ident)
        return set(encontrados)
    raise ValueError('relação de fonte ausente para '+ident)


def marcas(valor, dados, campo, ativas):
    if not ativas: return valor
    por_campo = dados.get('fontes_por_campo', {})
    K.exigir(isinstance(por_campo, dict), 'fontes_por_campo deve ser mapa')
    refs = por_campo.get(campo, dados.get('fontes', []))
    if isinstance(refs, str): refs = [refs]
    K.exigir(isinstance(refs, list) and all(isinstance(r,str) for r in refs), 'referências de fonte inválidas')
    explicitas = []
    evidencia = dados.get('evidencia')
    candidatos = [dados.get('fonte')]
    if isinstance(evidencia, dict): candidatos.extend([evidencia.get('fonte'), evidencia.get('referencia')])
    elif isinstance(evidencia, str): candidatos.append(evidencia)
    for candidato in candidatos:
        if isinstance(candidato, str) and re.fullmatch(r'(?:F|REC)-\d+', candidato): explicitas.append(candidato)
    refs = list(dict.fromkeys([*refs, *explicitas, *re.findall(r'fonte:\s*((?:F|REC)-\d+)', str(valor))]))
    fontes = set().union(*(fontes_contexto(r) for r in refs)) if refs else set()
    textos = []
    for rh in ativas:
        if fontes.intersection(rh['fontes']):
            limpar = lambda v: str(v).replace('|', '&#124;').replace('\n', ' ')
            textos.append(f"**[{rh['id']} · fonte: {', '.join(sorted(fontes.intersection(rh['fontes'])))} · item negado: {limpar(rh['item'])} · restrição: {limpar(rh['restricao'])} · motivo: {limpar(rh['motivo'])}]**")
    return str(valor) + (' '+ ' '.join(textos) if textos else '')


if __name__ == '__main__': main()
