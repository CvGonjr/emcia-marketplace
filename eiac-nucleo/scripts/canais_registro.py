"""Conferência genérica de canais declarados e de seu evento de definição."""
import hashlib
import json
import pathlib
import re

import estado as E


def carregar(pb):
    contrato = pb.get('registro_canais')
    if not isinstance(contrato, dict):
        raise ValueError('registro de canais não declarado no playbook')
    p = pathlib.Path(contrato['arquivo'])
    if p.is_absolute() or '..' in p.parts or not p.resolve().is_relative_to(pathlib.Path.cwd().resolve()):
        raise ValueError('registro de canais fora do caso')
    if any(x.is_symlink() for x in [p, *p.parents]):
        raise ValueError('registro de canais contém link')
    conteudo = p.read_bytes()
    dados = json.loads(conteudo)
    if dados.get('caso') != (E.ler() or {}).get('caso'):
        raise ValueError('registro de canais pertence a outro caso')
    eventos = [e for e in E.eventos() if e.get('evento') == contrato['evento']]
    if not eventos or eventos[-1].get('sha256') != hashlib.sha256(conteudo).hexdigest():
        raise ValueError('registro de canais sem definição íntegra na trilha')
    if (eventos[-1].get('versao') != dados.get('versao')
            or eventos[-1].get('decidido_por') != dados.get('decidido_por')
            or eventos[-1].get('autor') != (E.ler() or {}).get('responsavel')):
        raise ValueError('versão/autoria de canais diverge do evento')
    if not E.pessoa_nomeada(dados.get('decidido_por')) or not isinstance(dados.get('canais'), list):
        raise ValueError('registro de canais inválido')
    return dados


def selecionar(pb, alvo, direcao, finalidade=None):
    dados = carregar(pb)
    chave = 'etapas' if any(e['id'] == alvo for e in pb['etapas']) else 'entregaveis'
    return [c for c in dados['canais'] if alvo in c.get(chave, [])
            and c.get('direcao') == direcao
            and (finalidade is None or c.get('finalidade') == finalidade)]


def conferir(pb, alvo, entregavel=False):
    requisitos = pb.get('canais_por_entregavel' if entregavel else 'canais_por_etapa', {}).get(alvo, [])
    etapa = next((e for e in pb['etapas'] if e['id'] == alvo), {})
    if not requisitos and not etapa.get('exige_registro_canais'):
        return None
    comando = pb.get('registro_canais', {}).get('comando_definicao', 'definir os canais no terminal humano')
    try:
        carregar(pb)
        for r in requisitos:
            candidatos = selecionar(pb, alvo, r['direcao'], r['finalidade'])
            if not candidatos:
                raise ValueError(f"{alvo}: canal {r['finalidade']}/{r['direcao']} ausente")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return f'{exc}. Execute {comando}.'
    return None


def validar_contrato(pb):
    for chave, universo in [('canais_por_etapa', {e['id'] for e in pb['etapas']}),
                             ('canais_por_entregavel', {e['id'] for e in pb.get('entregaveis', [])})]:
        mapa = pb.get(chave, {})
        if not isinstance(mapa, dict):
            return f'{chave} precisa ser objeto'
        for alvo, requisitos in mapa.items():
            if alvo not in universo or not isinstance(requisitos, list) or not requisitos:
                return f'{chave}: alvo/requisitos inválidos'
            for r in requisitos:
                if (not isinstance(r, dict) or not isinstance(r.get('finalidade'), str)
                        or not r['finalidade'].strip() or r.get('direcao') not in ('entrada', 'saida', 'agenda')):
                    return f'{chave}: requisito inválido'
    if (pb.get('canais_por_etapa') or pb.get('canais_por_entregavel')
            or any(e.get('exige_registro_canais') for e in pb['etapas'])):
        contrato = pb.get('registro_canais')
        if not isinstance(contrato, dict) or any(not isinstance(contrato.get(k), str) or not contrato[k].strip()
                                              for k in ('arquivo', 'evento', 'comando_definicao')):
            return 'registro_canais precisa declarar arquivo, evento e comando_definicao'
    camadas = pb.get('exige_referencia_externa_por_camada', [])
    if not isinstance(camadas, list) or any(c not in ('EX1', 'EX2', 'EX3', 'EX4') for c in camadas):
        return 'exige_referencia_externa_por_camada inválida'
    contrato = pb.get('referencia_externa_sessao')
    if camadas or contrato is not None:
        if (not isinstance(contrato, dict) or any(not isinstance(contrato.get(k), str) or not contrato[k].strip()
                                                for k in ('finalidade', 'direcao', 'campo_id'))
                or contrato['direcao'] not in ('entrada', 'saida', 'agenda')):
            return 'referencia_externa_sessao inválida'
    for chave, campos in [('registro_fontes', ('arquivo', 'campo', 'id', 'caminho', 'hash', 'evento')),
                           ('escopo_ferramentas_externas', ('arquivo', 'padrao', 'listagens', 'evento_listagem'))]:
        contrato = pb.get(chave)
        if contrato is None: continue
        if not isinstance(contrato, dict) or any(not isinstance(contrato.get(k), str) or not contrato[k].strip() for k in campos):
            return chave+' inválido'
        for campo in ('arquivo', 'listagens'):
            if campo in contrato:
                p = pathlib.Path(contrato[campo])
                if p.is_absolute() or '..' in p.parts: return chave+': caminho fora do caso'
        if 'padrao' in contrato:
            try: re.compile(contrato['padrao'])
            except re.error: return chave+': padrão inválido'
    return None


def conferir_referencia(pb, etapa, camada, referencia):
    contrato = pb.get('referencia_externa_sessao', {})
    obrigatoria = camada in pb.get('exige_referencia_externa_por_camada', [])
    if not referencia:
        return 'referência externa exigida para a camada' if obrigatoria else None
    try:
        if not isinstance(referencia, dict) or set(referencia) != {'id', 'canal_id', 'marcador'}:
            raise ValueError('referência externa inválida')
        if not all(isinstance(v, str) and v.strip() for v in referencia.values()):
            raise ValueError('referência externa incompleta')
        canais = selecionar(pb, etapa, contrato['direcao'], contrato['finalidade'])
        candidatos = [c for c in canais if c['ids'].get(contrato['campo_id']) == referencia['canal_id']]
        if len(candidatos) != 1:
            raise ValueError('referência externa fora do canal declarado')
        esperado = candidatos[0]['marcador'].format(caso=(E.ler() or {})['caso'], etapa=etapa)
        if referencia['marcador'] != esperado:
            raise ValueError('marcador externo diverge do caso/etapa')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return str(exc)
    return None
