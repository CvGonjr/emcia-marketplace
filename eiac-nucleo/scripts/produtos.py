"""Produtos de encerramento declarados pelo caso; sem vocabulário de método."""
import pathlib
import estrutura as X


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
            if set(r) != {'tipo', 'padrao', 'iguais', 'preenchidos', 'descricao'}:
                return f"etapa {et['id']}: contrato de produto de arquivo invalido"
            p = r['padrao']
            if not isinstance(p, str) or not p.strip() or pathlib.Path(p).is_absolute() or '..' in pathlib.Path(p).parts:
                return f"etapa {et['id']}: padrao de produto deve ficar dentro do caso"
            if (not isinstance(r['iguais'], dict) or not isinstance(r['preenchidos'], list)
                    or any(not isinstance(c, str) or not c.strip() for c in [*r['iguais'], *r['preenchidos']])):
                return f"etapa {et['id']}: campos do produto invalidos"
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
        else:
            ok = False
            detalhe = f"{regra['padrao']} | iguais={regra['iguais']} | preenchidos={regra['preenchidos']}"
            for arquivo in raiz.glob(regra['padrao']):
                try:
                    if not arquivo.is_file() or not arquivo.resolve().is_relative_to(raiz):
                        continue
                    dados = X.carregar_yaml(arquivo.read_text(encoding='utf-8'))
                    if not isinstance(dados, dict):
                        continue
                    if (all(dados.get(c) == v for c, v in regra['iguais'].items())
                            and all(str(dados.get(c) or '').strip() for c in regra['preenchidos'])):
                        ok = True
                        break
                except (OSError, UnicodeError, ValueError, X.yaml.YAMLError if X.yaml else X.ErroYaml):
                    continue
        if not ok:
            ausentes.append(f"{regra['descricao']} ({detalhe})")
    return ausentes
