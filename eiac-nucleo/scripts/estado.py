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
        # aviso util: caso existente em subdiretorio significa sessao no lugar errado
        vizinhos = [d.parent.parent.name for d in pathlib.Path(".").glob("*/registro/estado.json")]
        if vizinhos:
            print("Nenhum caso aberto AQUI, mas existe caso em: " + ", ".join(vizinhos))
            print("A guarda so protege dentro do diretorio do caso. "
                  "Abra a sessao la dentro.")
        else:
            print("Nenhum caso aberto neste diretorio.")
        sys.exit(0)
    if "--resumo" in sys.argv:
        cam = e.get("camada_atual")
        if not cam:
            try:
                import playbook as P
                pb, erro = P.carregar()
                if pb:
                    cam = P.camada(pb, e["etapa_atual"], e.get("nivel"))
            except Exception:
                pass
        nivel = e.get("nivel") or "nao apurado"
        print(f"Caso {e['caso']} | nivel {nivel} | etapa {e['etapa_atual']} "
              f"| camada {cam or '?'} | modalidade {e.get('modalidade_atual','?')}")
        if not e.get("nivel") and e["etapa_atual"] != "F0":
            print("ATENCAO: nivel nao apurado. A camada das etapas depende dele.")
    else:
        print(json.dumps(e, indent=2, ensure_ascii=False))
