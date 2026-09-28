"""Coerência com fonte vigente declarada no playbook do caso."""
import fnmatch, pathlib
import estrutura as X
import estado as E

CHAVE = 'coerencia_responsavel_recorrencia'
CAMPOS = {'padrao', 'excluir_padrao', 'campo', 'campo_versao', 'selecao', 'orientacao_troca'}


def validar(et):
    if CHAVE not in et:
        return None
    r = et[CHAVE]
    if not isinstance(r, dict) or set(r) != CAMPOS:
        return f"etapa {et['id']}: contrato de {CHAVE} invalido"
    if any(not isinstance(v, str) or not v.strip() for v in r.values()):
        return f"etapa {et['id']}: {CHAVE} exige campos preenchidos"
    if not et.get('recorrente') or not et.get('responsavel_obrigatorio'):
        return f"etapa {et['id']}: {CHAVE} exige etapa recorrente com responsavel obrigatorio"
    for campo in ('padrao', 'excluir_padrao'):
        p = pathlib.Path(r[campo])
        if p.is_absolute() or '..' in p.parts:
            return f"etapa {et['id']}: {campo} precisa ficar dentro do caso"
    if r['selecao'] != 'maior_versao':
        return f"etapa {et['id']}: selecao de fonte desconhecida: {r['selecao']}"
    return None


def conferir(et, responsavel):
    """Retorna erro e fonte; não altera estado nem grava evento."""
    r = et.get(CHAVE)
    if r is None:
        return None, None
    raiz = pathlib.Path.cwd().resolve()
    fontes = []
    orientacao = r['orientacao_troca']
    for p in sorted(raiz.glob(r['padrao'])):
        relativo = p.relative_to(raiz).as_posix()
        if fnmatch.fnmatchcase(relativo, r['excluir_padrao']):
            continue
        if not p.resolve().is_relative_to(raiz):
            return f"fonte {relativo} fora do caso; {orientacao}", None
        try:
            d = X.carregar_yaml(p.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, ValueError, X.yaml.YAMLError if X.yaml else X.ErroYaml):
            return f"fonte {relativo} ilegivel; {orientacao}", None
        if not isinstance(d, dict):
            return f"fonte {relativo} precisa ser objeto; {orientacao}", None
        v = d.get(r['campo_versao'])
        if (type(v) is not int or v < 1):
            return f"fonte {relativo}: {r['campo_versao']} exige inteiro positivo; {orientacao}", None
        pessoa = d.get(r['campo'])
        if not E.pessoa_nomeada(pessoa):
            return f"fonte {relativo}: {r['campo']} exige pessoa nomeada; {orientacao}", None
        fontes.append(dict(arquivo=relativo, versao=v, campo=r['campo'], valor=pessoa))
    if not fontes:
        return f"fonte vigente ausente: {r['padrao']} (exclui {r['excluir_padrao']}); {orientacao}", None
    maior = max(f['versao'] for f in fontes)
    vigentes = [f for f in fontes if f['versao'] == maior]
    if len({f['valor'] for f in vigentes}) != 1:
        nomes = '; '.join(f"{f['arquivo']}: {f['valor']}" for f in vigentes)
        return f"fonte vigente ambigua na versao {maior}: {nomes}; {orientacao}", None
    fonte = vigentes[0]
    if responsavel != fonte['valor']:
        return (f"responsavel da recorrencia '{responsavel}' diverge do responsavel "
                f"da fonte vigente '{fonte['valor']}' ({fonte['arquivo']}, versao {maior}); {orientacao}"), None
    return None, fonte
