"""Quadro frequencia x consequencia sobre as regras da camada de contexto.

Confere tambem os campos obrigatorios do bloco que o passo 5 interroga.
Nao avalia merito; so ausencia.
"""
import pathlib, sys, collections

try:
    import yaml
except ImportError:
    yaml = None


def ler_yaml(texto):
    """Leitor minimo para os campos escalares e listas simples do modelo CTX-01.
    Usa PyYAML quando disponivel; caso contrario, faz a leitura rasa que o
    quadro precisa. Nao substitui YAML completo."""
    if yaml:
        return yaml.safe_load(texto) or {}
    d = {}
    for linha in texto.splitlines():
        if not linha or linha[0].isspace() or linha.lstrip().startswith("#"):
            continue
        if ":" not in linha:
            continue
        k, _, v = linha.partition(":")
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            miolo = v[1:-1].strip()
            d[k.strip()] = [x.strip().strip('"\'') for x in miolo.split(",")] if miolo else []
        else:
            d[k.strip()] = v.strip('"\'')
    return d

CENTRAL = ["determinismo", "frequencia", "consequencia_do_erro",
           "decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas",
           "estabilidade"]
FREQ = ["rotineira", "ocasional", "rara"]
CONS = ["baixa", "media", "alta"]


def main():
    d = pathlib.Path("contexto/regras")
    if not d.exists():
        print("contexto/regras ausente", file=sys.stderr); sys.exit(1)

    grade = collections.Counter()
    incompletas, total = [], 0

    for f in sorted(d.glob("*.yaml")):
        if "modelo" in f.name:
            continue
        r = ler_yaml(f.read_text(encoding="utf-8"))
        total += 1
        faltando = [c for c in CENTRAL
                    if r.get(c) in (None, "", []) and c != "decisor_quando_nao_cobre"]
        if faltando:
            incompletas.append((r.get("id", f.name), faltando))
        fq, cs = r.get("frequencia"), r.get("consequencia_do_erro")
        if fq in FREQ and cs in CONS:
            grade[(fq, cs)] += 1

    print(f"\n{total} regras\n")
    print(f"{'':<12}" + "".join(f"{c:>10}" for c in CONS))
    for fq in FREQ:
        linha = f"{fq:<12}"
        for cs in CONS:
            n = grade[(fq, cs)]
            marca = f"{n}"
            if (fq, cs) == ("rara", "alta"):
                marca = f"[{n}]"
            linha += f"{marca:>10}"
        print(linha)

    critica = grade[("rara", "alta")]
    print(f"\ncelula critica (rara x alta): {critica}")
    if critica == 0 and total > 0:
        print("ATENCAO: celula critica vazia. Ou a organizacao e excepcionalmente\n"
              "regular, ou o levantamento do P3b nao aconteceu. Confronte as duas\n"
              "hipoteses antes de encerrar o passo.")

    if incompletas:
        print(f"\n{len(incompletas)} regras com campos centrais ausentes:")
        for rid, faltando in incompletas:
            print(f"  {rid}: {faltando}")
        sys.exit(1)


if __name__ == "__main__":
    main()
