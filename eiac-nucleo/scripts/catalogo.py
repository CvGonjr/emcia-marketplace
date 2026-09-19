"""Resolucao generica de catalogo de capacidades e papeis.

Uso:
  python3 catalogo.py --capacidades <arquivo.json> --papeis <arquivo.json>
  python3 catalogo.py --capacidades <arquivo.json> --papeis <arquivo.json> \
      --resolver-papel-capacidade AG-01 HB-03
  python3 catalogo.py --capacidades <arquivo.json> --playbook <playbook.json>

Este script nao sabe o que e HB, AG, "habilidade" ou "agente" -- conhece
apenas dois tipos de objeto genericos:

  capacidade: {id, camada, automatizado, criterio_de_verificacao, ...}
  papel:      {id, camada, capacidades_autorizadas: [id, ...], ...}

e duas relacoes:

  papel -> capacidade   (um papel so pode ser autorizado a usar uma
                          capacidade se o id aparecer em
                          'capacidades_autorizadas')
  referencia -> capacidade (uma lista externa de ids, tipicamente vinda
                          do playbook, precisa resolver contra ids
                          existentes no catalogo de capacidades)

Reaproveita playbook.capacidade_valida() (2.6.1/ESP-01 G6): toda
capacidade automatizada precisa de criterio_de_verificacao nao vazio
para ser valida.

O vocabulario EMCIA (HB-01..HB-18, AG-01..AG-04, "habilidade", "agente")
vive inteiramente em eiac-campo/reference/*.json -- este script so le o
campo "id" de cada objeto.
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import playbook as P


def carregar_json(caminho):
    try:
        return json.loads(pathlib.Path(caminho).read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as erro:
        return None, f"{caminho}: {erro}"


def validar_capacidades(dados, chave_lista="capacidades", chave_capacidades_autorizadas=None):
    """Verifica integridade estrutural de uma lista de capacidades:
    ids unicos e, para cada uma marcada automatizada, criterio de
    verificacao presente (via playbook.capacidade_valida, generico).

    'dados' e o JSON completo do catalogo; 'chave_lista' e o campo que
    contem a lista de objetos capacidade (o eiac-campo usa
    "habilidades", mas o nucleo nao precisa saber disso -- quem chama
    passa o nome do campo).
    """
    itens = dados.get(chave_lista)
    if not isinstance(itens, list) or not itens:
        return [f"catalogo sem lista de capacidades em '{chave_lista}'"]

    erros = []
    ids = []
    for item in itens:
        if not isinstance(item, dict) or not item.get("id"):
            erros.append(f"item de capacidade sem 'id': {item}")
            continue
        ids.append(item["id"])
        candidato = {
            "automatizado": item.get("automatizada"),
            "criterio_de_verificacao": item.get("criterio_de_verificacao"),
        }
        ok, motivo = P.capacidade_valida(candidato)
        if not ok:
            erros.append(f"{item['id']}: {motivo}")

    if len(ids) != len(set(ids)):
        duplicados = sorted({i for i in ids if ids.count(i) > 1})
        erros.append(f"ids de capacidade duplicados: {duplicados}")

    return erros


def validar_papeis(dados_papeis, ids_capacidades_validas, chave_lista="papeis",
                    chave_autorizadas="capacidades_autorizadas"):
    """Verifica que cada papel referencia apenas capacidades existentes
    no catalogo (ids_capacidades_validas), e que os ids de papel sao
    unicos.
    """
    itens = dados_papeis.get(chave_lista)
    if not isinstance(itens, list) or not itens:
        return [f"catalogo sem lista de papeis em '{chave_lista}'"]

    erros = []
    ids = []
    for item in itens:
        if not isinstance(item, dict) or not item.get("id"):
            erros.append(f"item de papel sem 'id': {item}")
            continue
        ids.append(item["id"])
        autorizadas = item.get(chave_autorizadas) or []
        for cap_id in autorizadas:
            if cap_id not in ids_capacidades_validas:
                erros.append(
                    f"{item['id']}: referencia capacidade inexistente "
                    f"'{cap_id}' em '{chave_autorizadas}'"
                )

    if len(ids) != len(set(ids)):
        duplicados = sorted({i for i in ids if ids.count(i) > 1})
        erros.append(f"ids de papel duplicados: {duplicados}")

    return erros


def resolver_papel_capacidade(dados_papeis, papel_id, capacidade_id,
                               chave_lista="papeis", chave_autorizadas="capacidades_autorizadas"):
    """Um papel esta autorizado a executar uma capacidade? Retorna
    (True, None) ou (False, motivo). Nao decide nada alem de
    pertencimento de conjunto -- a semantica de "o que e uma HB" ou
    "o que e um AG" nunca entra aqui.
    """
    papel = next((p for p in dados_papeis.get(chave_lista, [])
                  if p.get("id") == papel_id), None)
    if not papel:
        return False, f"papel '{papel_id}' nao existe no catalogo"
    autorizadas = papel.get(chave_autorizadas) or []
    if capacidade_id not in autorizadas:
        return False, (f"papel '{papel_id}' nao esta autorizado a executar "
                       f"'{capacidade_id}'")
    return True, None


def resolver_referencias_playbook(dados_capacidades, pb, chave_lista="capacidades",
                                   campo_referencia="hb"):
    """Toda referencia (campo declarado em cada etapa do playbook, por
    exemplo "hb": ["HB-01"]) precisa resolver contra um id existente no
    catalogo de capacidades. Retorna lista de erros (vazia se tudo
    resolve).
    """
    ids_validos = {c.get("id") for c in dados_capacidades.get(chave_lista, [])
                   if isinstance(c, dict)}
    erros = []
    for etapa in pb.get("etapas", []):
        for ref in (etapa.get(campo_referencia) or []):
            if ref not in ids_validos:
                erros.append(
                    f"etapa {etapa.get('id','?')} referencia '{ref}' "
                    f"({campo_referencia}), que nao existe no catalogo"
                )
    return erros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capacidades", required=True)
    ap.add_argument("--papeis")
    ap.add_argument("--playbook")
    ap.add_argument("--chave-capacidades", default="capacidades")
    ap.add_argument("--chave-papeis", default="papeis")
    ap.add_argument("--chave-autorizadas", default="capacidades_autorizadas")
    ap.add_argument("--campo-referencia", default="hb")
    ap.add_argument("--resolver-papel-capacidade", nargs=2, metavar=("PAPEL", "CAPACIDADE"))
    a = ap.parse_args()

    dados_cap, erro = carregar_json(a.capacidades)
    if erro:
        print(erro, file=sys.stderr); sys.exit(1)

    erros = validar_capacidades(dados_cap, chave_lista=a.chave_capacidades)
    if erros:
        for e in erros:
            print(e, file=sys.stderr)
        sys.exit(1)

    ids_validos = {c["id"] for c in dados_cap[a.chave_capacidades]}

    if a.papeis:
        dados_papeis, erro = carregar_json(a.papeis)
        if erro:
            print(erro, file=sys.stderr); sys.exit(1)
        erros = validar_papeis(dados_papeis, ids_validos, chave_lista=a.chave_papeis,
                                chave_autorizadas=a.chave_autorizadas)
        if erros:
            for e in erros:
                print(e, file=sys.stderr)
            sys.exit(1)

        if a.resolver_papel_capacidade:
            papel_id, capacidade_id = a.resolver_papel_capacidade
            ok, motivo = resolver_papel_capacidade(
                dados_papeis, papel_id, capacidade_id,
                chave_lista=a.chave_papeis, chave_autorizadas=a.chave_autorizadas)
            if not ok:
                print(motivo, file=sys.stderr); sys.exit(1)
            print(f"ok | {papel_id} autorizado para {capacidade_id}")
            return

    if a.playbook:
        pb = json.loads(pathlib.Path(a.playbook).read_text(encoding="utf-8"))
        erros = resolver_referencias_playbook(dados_cap, pb, chave_lista=a.chave_capacidades,
                                               campo_referencia=a.campo_referencia)
        if erros:
            for e in erros:
                print(e, file=sys.stderr)
            sys.exit(1)
        print(f"ok | todas as referencias '{a.campo_referencia}' do playbook resolvem")
        return

    print(f"ok | catalogo valido: {len(ids_validos)} capacidades")


if __name__ == "__main__":
    main()
