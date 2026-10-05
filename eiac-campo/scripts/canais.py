"""Planejamento delegável e definição humana dos canais externos do caso.

Nenhuma API é chamada. Coerência local não autentica o conteúdo na origem.
"""
import argparse
import datetime
import fcntl
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import sys
import tempfile

NUCLEO = pathlib.Path(os.environ.get('EIAC_NUCLEO_SCRIPTS',
                    pathlib.Path(__file__).resolve().parents[2]/'eiac-nucleo/scripts'))
sys.path.insert(0, str(NUCLEO))
import estado as E
import playbook as P
import canais_registro as G

IDS = {'tally': ('workspace_id', 'formulario_id'), 'drive': ('drive_id', 'pasta_id'),
       'calendar': ('calendario_id',)}
CONTEINER = {'tally': 'formulario_id', 'drive': 'pasta_id', 'calendar': 'calendario_id'}


def exigir(condicao, motivo):
    if not condicao:
        raise ValueError(motivo)


def texto(valor):
    exigir(isinstance(valor, str) and bool(valor.strip()) and valor == valor.strip(), 'texto vazio ou inválido')
    return valor


def id_externo(valor):
    texto(valor)
    exigir(bool(re.fullmatch(r'[A-Za-z0-9_.@:+-]+', valor)), 'id externo inválido: use id, nunca nome ou caminho')
    return valor


def seguro(caminho, area=None):
    raiz = pathlib.Path.cwd().resolve(); p = pathlib.Path(caminho)
    exigir(p.resolve().is_relative_to(raiz), 'caminho fora do caso')
    exigir(not any(x.is_symlink() for x in [p, *p.parents] if x.absolute().is_relative_to(raiz)), 'caminho contém symlink')
    if area:
        exigir(p.resolve().is_relative_to((raiz/area).resolve()), 'arquivo fora de '+area)
    return p


def contexto(autor=None):
    st = E.ler(); pb, erro = P.carregar()
    exigir(st is not None and not erro, erro or 'caso ausente')
    exigir(E.pessoa_nomeada(st.get('responsavel')), 'responsável precisa ser pessoa nomeada')
    exigir(autor is None or (E.pessoa_nomeada(autor) and autor == st['responsavel']),
           'autor precisa ser o responsável nomeado do caso')
    return st, pb


def escrever(p, dados):
    p = seguro(p); p.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=p.parent, delete=False) as f:
        tmp = pathlib.Path(f.name)
        f.write((json.dumps(dados, ensure_ascii=False, indent=2)+'\n').encode())
        f.flush(); os.fsync(f.fileno())
    try:
        os.replace(tmp, p)
    finally:
        tmp.unlink(missing_ok=True)


def validar(dados, st, pb):
    exigir(isinstance(dados, dict), 'declaração precisa ser objeto')
    exigir(set(dados) == {'versao', 'caso', 'decidido_por', 'data', 'canais'}, 'campos da declaração inválidos')
    exigir(type(dados['versao']) is int and dados['versao'] > 0, 'versão precisa ser inteiro positivo')
    exigir(dados['caso'] == st['caso'], 'declaração pertence a outro caso')
    exigir(E.pessoa_nomeada(dados['decidido_por']), 'decidido_por precisa ser pessoa nomeada')
    datetime.date.fromisoformat(dados['data'])
    exigir(isinstance(dados['canais'], list) and bool(dados['canais']), 'canais precisa ser lista não vazia')
    previstos = {r['finalidade']: r for r in pb.get('canais_previstos', [])}
    vistos = set()
    for c in dados['canais']:
        exigir(isinstance(c, dict), 'canal precisa ser objeto')
        obrigatorios = {'finalidade', 'ferramenta', 'direcao', 'etapas', 'entregaveis', 'proprietario',
                        'ids', 'acesso_cliente', 'sensivel', 'filtro', 'marcador'}
        exigir(obrigatorios <= set(c) <= obrigatorios | {'origem'}, 'campos de canal inválidos')
        if 'origem' in c:
            o = c['origem']
            exigir(isinstance(o, dict) and set(o) == {'habilitacao', 'expediente_sha256', 'fontes'}, 'vínculo de origem inválido')
            texto(o['habilitacao'])
            exigir(isinstance(o['expediente_sha256'], str) and bool(re.fullmatch('[a-f0-9]{64}', o['expediente_sha256'])), 'hash de expediente inválido')
            exigir(isinstance(o['fontes'], list) and bool(o['fontes']) and all(isinstance(x, str) and x for x in o['fontes']), 'fontes de origem ausentes')
        f = c['finalidade']; ferramenta = c['ferramenta']
        exigir(f in previstos, 'finalidade não prevista no playbook')
        exigir(ferramenta in IDS, 'ferramenta desconhecida')
        for k in ('ferramenta', 'direcao'):
            exigir(c[k] == previstos[f][k], k+' diverge da finalidade declarada')
        for k in ('etapas', 'entregaveis'):
            exigir(isinstance(c[k], list) and all(isinstance(x, str) for x in c[k])
                   and len(set(c[k])) == len(c[k]) and set(c[k]) <= set(previstos[f][k]), k+' fora do contrato')
        exigir(c['proprietario'] in ('emcia', 'cliente'), 'proprietário inválido')
        exigir(c['acesso_cliente'] in ('nenhum', 'leitura', 'escrita'), 'acesso inválido')
        exigir(f != 'trabalho-interno' or c['acesso_cliente'] == 'nenhum', 'trabalho-interno sem acesso do cliente')
        exigir(type(c['sensivel']) is bool, 'sensivel precisa ser booleano')
        exigir(isinstance(c['ids'], dict) and set(c['ids']) == set(IDS[ferramenta]), 'ids específicos ausentes ou desconhecidos')
        for v in c['ids'].values(): id_externo(v)
        chave = (f, tuple(sorted(c['ids'].items())))
        exigir(chave not in vistos, 'canal duplicado'); vistos.add(chave)
        if ferramenta == 'tally':
            exigir(c['filtro'] == {'campo': 'caso', 'valor': st['caso']}, 'filtro precisa identificar o caso')
            exigir(c['marcador'] is None, 'marcador reservado à agenda')
        elif ferramenta == 'calendar':
            exigir(c['filtro'] is None and c['marcador'] == '[{caso}/{etapa}]', 'marcador de agenda inválido')
        else:
            exigir(c['filtro'] is None and c['marcador'] is None, 'filtro/marcador incompatível')
    return dados


def migrar_origens(dados, expediente, hash_expediente):
    """Endereços da habilitação: o workspace faltante vem da decisão humana.

    Nunca inventa ids nem consulta a ferramenta por nome.
    """
    import copy
    resultado = copy.deepcopy(dados)
    bases = [c for c in resultado['canais'] if c['finalidade'] == 'habilitacao']
    exigir(bool(bases), 'defina o workspace de habilitação em canais.py definir antes de importar')
    bases_por_form = {c['ids']['formulario_id']: c for c in bases}
    novos = []
    agrupadas = {}
    for ident, fonte in expediente['fontes'].items():
        agrupadas.setdefault(fonte['formulario'], []).append((ident, fonte))
    for form, fontes in agrupadas.items():
        base = bases_por_form.get(form)
        if base is None:
            exigir(len({c['ids']['workspace_id'] for c in bases}) == 1,
                   'workspace ambíguo: declare cada formulário antes da importação')
            base = bases[0]
        canal = copy.deepcopy(base)
        canal['ids']['formulario_id'] = id_externo(form)
        for _, fonte in fontes:
            if fonte.get('workspace_id'):
                exigir(canal['ids']['workspace_id'] == fonte['workspace_id'], 'workspace diverge do expediente')
        canal['origem'] = dict(habilitacao=expediente['habilitacao'], expediente_sha256=hash_expediente,
                               fontes=[ident for ident, _ in fontes])
        novos.append(canal)
    resultado['canais'] = [c for c in resultado['canais'] if c['finalidade'] != 'habilitacao']+novos
    return resultado


def planejar(st, pb):
    return dict(caso=st['caso'], canais_necessarios=pb.get('canais_previstos', []),
                arvore_proposta=dict(proprietario='emcia', raiz=st['caso'], roteamento='somente ids',
                                    filhos=[dict(nome=n, acesso_cliente='nenhum') for n in
                                            ['00-habilitacao', 'entrada-documentos', 'entrada-amostras',
                                             'entregas', 'trabalho-interno']]))


def definir(dados, st, pb):
    validar(dados, st, pb)
    p = seguro(pb['registro_canais']['arquivo'])
    anterior = G.carregar(pb) if p.exists() else None
    exigir(dados['versao'] == (anterior['versao']+1 if anterior else 1), 'versão deve suceder a vigente')
    if not anterior:
        exigir(not any(e.get('evento') == pb['registro_canais']['evento'] for e in E.eventos()),
               'definição anterior sem registro vigente')
    if anterior:
        historico = seguro(f"registro/canais/versao-{anterior['versao']:04d}.json")
        exigir(not historico.exists(), 'versão histórica já existe')
        escrever(historico, anterior)
    backup = p.read_bytes() if p.exists() else None
    try:
        escrever(p, dados)
        E.evento(pb['registro_canais']['evento'], autor=st['responsavel'], decidido_por=dados['decidido_por'], versao=dados['versao'],
                 sha256=hashlib.sha256(p.read_bytes()).hexdigest(), caso=st['caso'])
    except Exception:
        if backup is None: p.unlink(missing_ok=True)
        else: p.write_bytes(backup)
        if anterior: historico.unlink(missing_ok=True)
        raise
    return dados


def resolver(pb, alvo, direcao):
    erro = G.conferir(pb, alvo, entregavel=any(e['id'] == alvo for e in pb.get('entregaveis', [])))
    exigir(not erro, erro)
    canais = G.selecionar(pb, alvo, direcao)
    # Uma etapa pode ter canais históricos administrativos; os requisitos
    # do percurso selecionam a finalidade quando houver.
    chave = 'canais_por_etapa' if P.etapa(pb, alvo) else 'canais_por_entregavel'
    finalidades = [r['finalidade'] for r in pb.get(chave, {}).get(alvo, []) if r['direcao'] == direcao]
    if finalidades: canais = [c for c in canais if c['finalidade'] in finalidades]
    exigir(len(canais) == 1, 'canal ausente ou ambíguo; execute '+pb['registro_canais']['comando_definicao'])
    return canais[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('operacao', choices=['planejar', 'definir', 'resolver'])
    ap.add_argument('alvo', nargs='?'); ap.add_argument('direcao', nargs='?', choices=['entrada', 'saida', 'agenda'])
    ap.add_argument('--entrada'); ap.add_argument('--autor')
    ap.add_argument('--aprovacao', help='testemunho conferido pela guarda da sessão')
    a = ap.parse_args()
    try:
        st, pb = contexto(a.autor)
        if a.operacao == 'planejar': resultado = planejar(st, pb)
        elif a.operacao == 'resolver': resultado = resolver(pb, a.alvo, a.direcao)
        else:
            exigir(a.entrada is not None, 'definir exige --entrada')
            lock = seguro('registro/.canais.lock')
            with lock.open('a') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                resultado = definir(json.loads(pathlib.Path(a.entrada).read_text()), st, pb)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        E.evento('TentativaNegada', autor=(E.ler() or {}).get('responsavel'), operacao='canais-'+a.operacao, motivo=str(exc))
        ap.exit(1, 'Recusado: '+str(exc)+'\n')


if __name__ == '__main__': main()
