"""Trava genérica de argumentos externos conforme contrato local do caso."""
import hashlib
import json
import pathlib
import re
import canais_registro as K
import estado as E


def contrato(pb):
    valor = pb.get('escopo_ferramentas_externas')
    if not valor: return None
    p = pathlib.Path(valor['arquivo'])
    if p.is_absolute() or '..' in p.parts or not p.resolve().is_relative_to(pathlib.Path.cwd().resolve()):
        raise ValueError('contrato externo fora do caso')
    if any(x.is_symlink() for x in [p, *p.parents]):
        raise ValueError('contrato externo contém link')
    dados = json.loads(p.read_text())
    if not isinstance(dados.get('regras'), list) or not dados['regras']:
        raise ValueError('contrato externo sem regras')
    return dados


def argumento(dados, campo):
    valor = dados
    for parte in campo.split('.'):
        if not isinstance(valor, dict) or parte not in valor:
            raise ValueError('argumento externo ausente: '+campo)
        valor = valor[parte]
    return valor


def ids(pb, regra):
    canais = K.carregar(pb)['canais']
    return [c['ids'][regra['campo_id']] for c in canais if regra['campo_id'] in c['ids']
            and (not regra.get('finalidade') or c['finalidade'] == regra['finalidade'])
            and (not regra.get('direcao') or c['direcao'] == regra['direcao'])]


def ids_listados(pb):
    declaracao = pb['escopo_ferramentas_externas']
    p = pathlib.Path(declaracao['listagens'])
    if p.is_absolute() or '..' in p.parts or not p.resolve().is_relative_to(pathlib.Path.cwd().resolve()):
        raise ValueError('manifesto externo fora do caso')
    if any(x.is_symlink() for x in [p, *p.parents]):
        raise ValueError('manifesto externo contém link')
    conteudo = p.read_bytes(); reg = json.loads(conteudo)
    evs = [e for e in E.eventos() if e.get('evento') == declaracao['evento_listagem']]
    if not evs or evs[-1].get('sha256') != hashlib.sha256(conteudo).hexdigest():
        raise ValueError('manifesto externo sem integridade na trilha')
    declarados = {v for c in K.carregar(pb)['canais'] for v in c['ids'].values()}
    encontrados = []
    for r in reg['listagens']:
        if r['conteiner_id'] in declarados:
            encontrados.extend(r['objetos'])
    return encontrados


def conferir(pb, ferramenta, entrada):
    try:
        declaracao = pb.get('escopo_ferramentas_externas')
        if not declaracao:
            return None
        if not re.fullmatch(declaracao['padrao'], ferramenta):
            return None
        dados = contrato(pb)
        regras = [r for r in dados['regras'] if re.fullmatch(r['padrao'], ferramenta)]
        if len(regras) != 1:
            raise ValueError('ferramenta externa não declarada ou ambígua')
        regra = regras[0]
        if not isinstance(regra.get('argumentos'), list) or not regra['argumentos']:
            raise ValueError('regra externa sem argumentos de escopo')
        for a in regra['argumentos']:
            valor = argumento(entrada, a['campo'])
            tipo = a['tipo']
            if tipo == 'constante':
                if valor != a['valor']: raise ValueError('argumento externo diverge da constante declarada')
                continue
            valores = ids_listados(pb) if tipo == 'id_listado' else ids(pb, a)
            if tipo in ('id_de_canal', 'id_listado'):
                if not isinstance(valor, str) or valor not in valores:
                    raise ValueError('id externo fora do escopo declarado/listado')
            elif tipo == 'expressao':
                if not isinstance(valor, str) or not any(re.fullmatch(a['expressao'].replace('{id}', re.escape(v)), valor) for v in valores):
                    raise ValueError('expressão externa sem restrição declarada')
            else:
                raise ValueError('tipo de argumento externo desconhecido')
    except (OSError, ValueError, KeyError, TypeError, AttributeError, re.error) as exc:
        return str(exc)
    return None
