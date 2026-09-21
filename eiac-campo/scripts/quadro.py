"""Quadro frequência × consequência compartilhado pelos dois braços.

Este é o único código do cálculo. Núcleo e contraste apenas o encaminham.
"""
import collections
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None
else:
    class _LoaderSemTimestamp(yaml.SafeLoader):
        pass

    _LoaderSemTimestamp.yaml_implicit_resolvers = {
        letra: [
            (tag, regexp) for tag, regexp in resolvedores
            if tag != "tag:yaml.org,2002:timestamp"
        ]
        for letra, resolvedores in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }


def ler_yaml(texto):
    if yaml:
        return yaml.load(texto, Loader=_LoaderSemTimestamp) or {}
    dados = {}
    for linha in texto.splitlines():
        if not linha or linha[0].isspace() or linha.lstrip().startswith("#") or ":" not in linha:
            continue
        chave, _, valor = linha.partition(":")
        valor = valor.strip()
        if valor.startswith("[") and valor.endswith("]"):
            miolo = valor[1:-1].strip()
            dados[chave.strip()] = [x.strip().strip("\"'") for x in miolo.split(",")] if miolo else []
        elif valor and not valor.startswith(("'", '"')) and re.fullmatch(r"-?\d+", valor):
            dados[chave.strip()] = int(valor)
        else:
            dados[chave.strip()] = valor.strip("\"'")
    return dados


CENTRAL = [
    "determinismo", "frequencia", "consequencia_do_erro",
    "decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas", "estabilidade",
]
NAO_EXIGE_CONTEUDO = {"decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas"}
FREQ = ["rotineira", "ocasional", "rara"]
CONS = ["baixa", "media", "alta"]


def main():
    diretorio = pathlib.Path("contexto/regras")
    if not diretorio.exists():
        print("contexto/regras ausente", file=sys.stderr)
        sys.exit(1)
    grade = collections.Counter()
    incompletas = []
    total = 0
    for arquivo in sorted(diretorio.glob("*.yaml")):
        if "modelo" in arquivo.name:
            continue
        regra = ler_yaml(arquivo.read_text(encoding="utf-8"))
        total += 1
        faltando = [
            campo for campo in CENTRAL
            if campo not in regra and campo not in NAO_EXIGE_CONTEUDO
        ]
        if faltando:
            incompletas.append((regra.get("id", arquivo.name), faltando))
        frequencia = regra.get("frequencia")
        consequencia = regra.get("consequencia_do_erro")
        if frequencia in FREQ and consequencia in CONS:
            grade[(frequencia, consequencia)] += 1

    print(f"\n{total} regras\n")
    print(f"{'':<12}" + "".join(f"{c:>10}" for c in CONS))
    for frequencia in FREQ:
        linha = f"{frequencia:<12}"
        for consequencia in CONS:
            numero = grade[(frequencia, consequencia)]
            marca = f"[{numero}]" if (frequencia, consequencia) == ("rara", "alta") else str(numero)
            linha += f"{marca:>10}"
        print(linha)
    critica = grade[("rara", "alta")]
    print(f"\ncelula critica (rara x alta): {critica}")
    if critica == 0 and total > 0:
        print(
            "ATENCAO: celula critica vazia. Ou a organizacao e excepcionalmente\n"
            "regular, ou o levantamento do P3b nao aconteceu. Confronte as duas\n"
            "hipoteses antes de encerrar o passo."
        )
    if incompletas:
        print(f"\n{len(incompletas)} regras com campos centrais ausentes:")
        for identificador, faltando in incompletas:
            print(f"  {identificador}: {faltando}")
        sys.exit(1)


if __name__ == "__main__":
    main()
