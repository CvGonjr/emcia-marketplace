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


def validar_valor(valor, schema, caminho):
    tipos = {'string': str, 'boolean': bool, 'integer': int, 'object': dict, 'array': list}
    tipo = schema.get('type')
    if tipo not in tipos or type(valor) is not tipos[tipo]:
        raise ValueError('tipo externo inválido: '+caminho)
    if 'enum' in schema and valor not in schema['enum']:
        raise ValueError('valor externo fora dos permitidos: '+caminho)
    if tipo == 'integer' and (valor < schema.get('minimum',valor) or valor > schema.get('maximum',valor)):
        raise ValueError('valor externo fora dos limites: '+caminho)
    if tipo == 'array':
        for i,v in enumerate(valor): validar_valor(v,schema.get('items',{}),f'{caminho}.{i}')
    if tipo == 'object':
        conferir_parametros(valor,schema.get('properties',{}),schema.get('required',[]),caminho+'.')


def conferir_parametros(entrada, parametros, obrigatorios, prefixo=''):
    if not isinstance(entrada,dict): raise ValueError('argumentos externos precisam ser objeto')
    extras=set(entrada)-set(parametros)
    if extras: raise ValueError('parâmetro extra não previsto no perfil: '+prefixo+', '.join(sorted(extras)))
    if not set(obrigatorios)<=set(entrada): raise ValueError('parâmetro externo obrigatório ausente')
    for campo,valor in entrada.items(): validar_valor(valor,parametros[campo],prefixo+campo)


def regra_aplicavel(dados, ferramenta, entrada):
    regras=[r for r in dados['regras'] if re.fullmatch(r['padrao'],ferramenta)]
    if len(regras)!=1: raise ValueError('ferramenta externa não declarada ou ambígua')
    regra=regras[0]
    if regra.get('recusa'): raise ValueError(regra['recusa'])
    if 'parametros' in regra: conferir_parametros(entrada,regra['parametros'],regra.get('obrigatorios',[]))
    alternativas=regra.get('alternativas')
    if alternativas is not None:
        candidatas=[]
        for alt in alternativas:
            c=alt['quando'];valor=argumento(entrada,c['campo'])
            if ('igual' in c and valor==c['igual']) or ('diferente' in c and valor!=c['diferente']): candidatas.append(alt)
        if len(candidatas)!=1: raise ValueError('variante externa ausente ou ambígua')
        regra=dict(regra,**candidatas[0])
    if any(c in entrada for c in regra.get('ausentes',[])): raise ValueError('variante externa contém parâmetro proibido')
    campos=regra.get('exige_um_de')
    if campos and sum(c in entrada for c in campos)!=1: raise ValueError('variante externa exige um conteúdo exclusivo')
    return regra


def conferir_eventos(dados, regra, ferramenta, entrada, eventos, autor, contexto):
    if regra.get('exige_aprovacao'):
        nome=dados.get('evento_aprovacao','AprovacaoExternaRegistrada')
        if not any(e.get('evento')==nome and e.get('ferramenta')==ferramenta
                   and e.get('argumentos')==entrada and e.get('autor')==autor
                   and e.get('contexto')==contexto and e.get('testemunho') for e in eventos):
            raise ValueError('efeito externo sem aprovação registrada para ferramenta, parâmetros e contexto')
    c=regra.get('precondicao_registrada')
    if c:
        candidatos=[e for e in eventos if e.get('evento')==c['evento']
                    and e.get(c['campo_evento'])==argumento(entrada,c['argumento'])
                    and e.get('autor')==autor and e.get('contexto')==contexto]
        if c.get('ultimo'): candidatos=candidatos[-1:]
        if not any(all(e.get(k)==v for k,v in c.get('valores',{}).items()) for e in candidatos):
            motivos=candidatos[-1].get(c.get('campo_motivo'),[]) if candidatos else []
            raise ValueError('pré-condição externa não registrada: '+str(c.get('valores',{}))+'; '+str(motivos))


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
        regra = regra_aplicavel(dados, ferramenta, entrada)
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
        st=E.ler() or {}
        conferir_eventos(dados,regra,ferramenta,entrada,E.eventos(),st.get('responsavel'),st.get('caso'))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, re.error) as exc:
        return str(exc)
    return None
