"""Le e escreve o Registro do Caso. Unico caminho de mudanca de etapa."""
import json, pathlib, sys, datetime

CAMINHO = pathlib.Path("registro/estado.json")


def ler():
    if not CAMINHO.exists():
        return None
    return json.loads(CAMINHO.read_text(encoding="utf-8"))


def gravar(e):
    CAMINHO.parent.mkdir(parents=True, exist_ok=True)
    CAMINHO.write_text(json.dumps(e, indent=2, ensure_ascii=False), encoding="utf-8")


def evento(tipo, **campos):
    log = pathlib.Path("registro/eventos.jsonl")
    log.parent.mkdir(parents=True, exist_ok=True)
    reg = {"evento": tipo, "data": datetime.datetime.now().isoformat(timespec="seconds")}
    reg.update(campos)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    e = ler()
    if not e:
        print("Nenhum caso aberto neste diretorio.")
        sys.exit(0)
    if "--resumo" in sys.argv:
        print(f"Caso {e['caso']} | etapa {e['etapa_atual']} "
              f"| camada {e.get('camada_atual','?')} "
              f"| modalidade {e.get('modalidade_atual','?')}")
    else:
        print(json.dumps(e, indent=2, ensure_ascii=False))
