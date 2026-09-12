"""Carrega e valida o playbook do caso. Nao conhece nenhum metodo em particular."""
import json, pathlib, sys

OBRIGATORIO_ETAPA = {"id", "camada", "modalidade"}
OBRIGATORIO_ENTREGAVEL = {"id", "portao"}


def raiz() -> pathlib.Path:
    return pathlib.Path.cwd()


def carregar():
    p = raiz() / "registro" / "playbook.json"
    if not p.exists():
        return None, "registro/playbook.json ausente"
    pb = json.loads(p.read_text(encoding="utf-8"))

    if not pb.get("etapas"):
        return None, "playbook sem etapas"
    for e in pb["etapas"]:
        faltando = OBRIGATORIO_ETAPA - set(e)
        if faltando:
            return None, f"etapa {e.get('id','?')} sem {sorted(faltando)}"
    for d in pb.get("entregaveis", []):
        faltando = OBRIGATORIO_ENTREGAVEL - set(d)
        if faltando:
            return None, f"entregavel {d.get('id','?')} sem {sorted(faltando)}"
    if not pb.get("inegociaveis"):
        return None, "playbook sem itens inegociaveis"
    if not pb.get("procedencia", {}).get("origem"):
        return None, "playbook sem rotulos de origem"
    return pb, None


def etapa(pb, etapa_id):
    for e in pb["etapas"]:
        if e["id"] == etapa_id:
            return e
    return None


if __name__ == "__main__":
    pb, erro = carregar()
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"playbook '{pb.get('nome','?')}' valido: "
          f"{len(pb['etapas'])} etapas, "
          f"{len(pb.get('entregaveis', []))} entregaveis, "
          f"{len(pb['inegociaveis'])} itens inegociaveis")
