"""Consulta somente-leitura de um objeto CTX curado, por id.

Uso:  python3 consultar.py --id RN-014
      python3 consultar.py --id RN-014 --schema registro/contexto.schema.json

Le o `catalogo_referencias` do schema do caso para descobrir tipo e
diretorio a partir do prefixo do id (o mesmo mecanismo que curar.py usa
para resolver `entradas`/`onde_vive`), valida o objeto contra o proprio
schema e imprime seus campos em JSON.

Nao decide merito nem grava nada. Existe para que P4/P5 leiam o contexto
ja curado como dado estruturado, em vez de reinterpretar prosa ou abrir
arquivos por caminho fixo espalhado pelas skills.
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estrutura as X


def resolver(id_objeto, schema_caminho="registro/contexto.schema.json"):
    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as erro:
        return None, f"schema invalido: {erro}"

    catalogo = schema.get("catalogo_referencias", {})
    prefixo = id_objeto.split("-", 1)[0] if "-" in id_objeto else id_objeto
    entrada = catalogo.get(prefixo)
    if not entrada:
        return None, f"prefixo '{prefixo}' nao consta em catalogo_referencias do schema"

    alvo = pathlib.Path(entrada["diretorio"]) / f"{id_objeto}.yaml"
    if not alvo.exists():
        return None, f"{alvo} nao existe — objeto nao curado"

    try:
        dados = X.carregar_yaml(alvo.read_text(encoding="utf-8"))
    except (X.ErroYaml, ValueError) as erro:
        return None, f"{alvo} esta ilegivel: {erro}"

    erros = X.validar(dados, schema, entrada["tipo"])
    if erros:
        return None, f"{alvo} nao passa na validacao estrutural: {erros}"

    return dados, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--schema", default="registro/contexto.schema.json")
    ap.add_argument("--campo", action="append", default=None,
                     help="restringe a saida a este campo (repetivel); "
                          "sem uso, imprime o objeto inteiro")
    a = ap.parse_args()

    dados, erro = resolver(a.id, a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)

    if a.campo:
        saida = {c: dados.get(c) for c in a.campo}
    else:
        saida = dados
    print(json.dumps(saida, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
