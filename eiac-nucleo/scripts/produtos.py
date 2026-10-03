"""Produtos de encerramento declarados pelo caso; sem vocabulário de método."""
import hashlib
import json
import pathlib
import estrutura as X
import estado as E


def validar(et):
    regras = et.get('produtos_encerramento', [])
    if not isinstance(regras, list):
        return f"etapa {et['id']}: produtos_encerramento precisa ser lista"
    for r in regras:
        if not isinstance(r, dict) or not isinstance(r.get('descricao'), str) or not r['descricao'].strip():
            return f"etapa {et['id']}: produto sem descricao"
        if r.get('tipo') == 'estado':
            if set(r) != {'tipo', 'campo', 'descricao'} or r.get('campo') not in et.get('campos_registraveis', {}):
                return f"etapa {et['id']}: produto de estado exige campo registravel"
        elif r.get('tipo') == 'arquivo':
            if set(r) - {'tipo', 'padrao', 'iguais', 'preenchidos', 'descricao', 'pessoas'} or not {'tipo', 'padrao', 'iguais', 'preenchidos', 'descricao'} <= set(r):
                return f"etapa {et['id']}: contrato de produto de arquivo invalido"
            if not isinstance(r.get('pessoas', []), list) or any(not isinstance(c, str) or not c.strip() for c in r.get('pessoas', [])):
                return f"etapa {et['id']}: campos de pessoa invalidos no produto"
            p = r['padrao']
            if not isinstance(p, str) or not p.strip() or pathlib.Path(p).is_absolute() or '..' in pathlib.Path(p).parts:
                return f"etapa {et['id']}: padrao de produto deve ficar dentro do caso"
            if (not isinstance(r['iguais'], dict) or not isinstance(r['preenchidos'], list)
                    or any(not isinstance(c, str) or not c.strip() for c in [*r['iguais'], *r['preenchidos']])):
                return f"etapa {et['id']}: campos do produto invalidos"
        elif r.get('tipo') == 'cobertura':
            try:
                if set(r) != {'tipo', 'descricao', 'origem', 'destino', 'estados', 'campo_estado', 'eventos', 'eventos_origem'}:
                    raise ValueError('campos de cobertura inválidos')
                for nome in ('origem', 'destino'):
                    d = r[nome]
                    if set(d) != {'arquivo', 'campo', 'chave'} or any(not isinstance(v, str) or not v.strip() for v in d.values()):
                        raise ValueError('coleção inválida')
                    p = pathlib.Path(d['arquivo'])
                    if p.is_absolute() or '..' in p.parts: raise ValueError('coleção fora do caso')
                if not isinstance(r['campo_estado'], str) or not r['campo_estado'].strip(): raise ValueError('campo_estado inválido')
                for chave in ('eventos','eventos_origem'):
                    if not isinstance(r[chave], list) or not r[chave] or any(not isinstance(v,str) or not v for v in r[chave]): raise ValueError('eventos inválidos')
                if not isinstance(r['estados'], dict) or not r['estados']: raise ValueError('estados inválidos')
                for campos in r['estados'].values():
                    if set(campos) != {'preenchidos', 'pessoas'} or any(not isinstance(v,list) or any(not isinstance(c,str) or not c for c in v) for v in campos.values()):
                        raise ValueError('campos do estado inválidos')
            except (ValueError, KeyError, TypeError, AttributeError) as exc:
                return f"etapa {et['id']}: contrato de cobertura inválido: {exc}"
        else:
            return f"etapa {et['id']}: tipo de produto desconhecido"


def faltas(et, st):
    ausentes = []
    raiz = pathlib.Path.cwd().resolve()
    for regra in et.get('produtos_encerramento', []):
        if regra['tipo'] == 'estado':
            valor = st.get('cumprimentos', {}).get(et['id'], {}).get(regra['campo'])
            permitido = et['campos_registraveis'][regra['campo']].get('valores')
            ok = bool(str(valor or '').strip()) and (permitido is None or valor in permitido)
            detalhe = regra['campo']
        elif regra['tipo'] == 'cobertura':
            erros = _cobertura(regra)
            ausentes.extend(f"{regra['descricao']} ({erro})" for erro in erros)
            continue
        else:
            ok = False
            detalhe = f"{regra['padrao']} | iguais={regra['iguais']} | preenchidos={regra['preenchidos']} | pessoas={regra.get('pessoas', [])}"
            for arquivo in raiz.glob(regra['padrao']):
                try:
                    if not arquivo.is_file() or not arquivo.resolve().is_relative_to(raiz):
                        continue
                    dados = X.carregar_yaml(arquivo.read_text(encoding='utf-8'))
                    if not isinstance(dados, dict):
                        continue
                    if (all(dados.get(c) == v for c, v in regra['iguais'].items())
                            and all(str(dados.get(c) or '').strip() for c in regra['preenchidos'])
                            and all(E.pessoa_nomeada(dados.get(c)) for c in regra.get('pessoas', []))):
                        ok = True
                        break
                except (OSError, UnicodeError, ValueError, X.yaml.YAMLError if X.yaml else X.ErroYaml):
                    continue
        if not ok:
            ausentes.append(f"{regra['descricao']} ({detalhe})")
    return ausentes


def _campo(dados, nome):
    for parte in nome.split('.'):
        dados = dados[parte]
    return dados


def _colecao(contrato):
    raiz = pathlib.Path.cwd().resolve()
    p = raiz/contrato['arquivo']
    if not p.resolve().is_relative_to(raiz) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(raiz)):
        raise ValueError('coleção fora do caso ou com link')
    dados = json.loads(p.read_text())
    itens = _campo(dados, contrato['campo'])
    if not isinstance(itens, list) or any(not isinstance(i, dict) for i in itens):
        raise ValueError('coleção precisa ser lista de objetos')
    ids = [i[contrato['chave']] for i in itens]
    if any(not isinstance(i,str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('identificador inválido ou duplicado na coleção')
    return itens, p


def _cobertura(regra):
    """Cada id de uma coleção deve ter registro com estado declarado válido."""
    try:
        origem, fonte = _colecao(regra['origem'])
        eventos_origem = [e for e in E.eventos() if e.get('evento') in regra['eventos_origem']]
        if not eventos_origem or eventos_origem[-1].get('registro_sha256') != hashlib.sha256(fonte.read_bytes()).hexdigest():
            raise ValueError('integridade da coleção de origem sem evento correspondente')
        if not origem: return []  # Cobertura vazia sem arquivo de destino.
        destino, arquivo = _colecao(regra['destino'])
        eventos = [e for e in E.eventos() if e.get('evento') in regra['eventos']]
        if not eventos or eventos[-1].get('registro_sha256') != hashlib.sha256(arquivo.read_bytes()).hexdigest():
            raise ValueError('integridade da coleção sem evento correspondente')
        erros = []
        for item in origem:
            ident = item[regra['origem']['chave']]
            registro = next((d for d in destino if d[regra['destino']['chave']] == ident), None)
            campos = regra['estados'].get((registro or {}).get(regra['campo_estado']))
            if registro is None or campos is None or not all(_campo(registro, c) for c in campos['preenchidos']) or not all(E.pessoa_nomeada(_campo(registro,c)) for c in campos['pessoas']):
                erros.append('item pendente: '+ident)
        return erros
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError) as exc:
        # Expõe os ids de origem para tornar a pendência rastreável.
        ids = ', '.join(str(i.get(regra['origem']['chave'])) for i in locals().get('origem', []))
        return [f'cobertura ausente ou inválida {ids}: {exc}']
