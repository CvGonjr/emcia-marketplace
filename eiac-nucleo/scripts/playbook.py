"""Carrega e valida o playbook do caso. Nao conhece nenhum metodo em particular."""
import json, pathlib, sys

OBRIGATORIO_ETAPA = {"id", "camada", "modalidade"}
OBRIGATORIO_ENTREGAVEL = {"id", "portao"}


def carregar():
    p = pathlib.Path("registro/playbook.json")
    if not p.exists():
        return None, "registro/playbook.json ausente"
    pb = json.loads(p.read_text(encoding="utf-8"))

    niveis = pb.get("niveis")
    if not niveis:
        return None, "playbook sem lista de niveis"
    if not pb.get("etapas"):
        return None, "playbook sem etapas"

    for e in pb["etapas"]:
        faltando = OBRIGATORIO_ETAPA - set(e)
        if faltando:
            return None, f"etapa {e.get('id','?')} sem {sorted(faltando)}"
        c = e["camada"]
        if not isinstance(c, dict):
            return None, (f"etapa {e['id']}: camada precisa ser um mapa por nivel. "
                          f"A fronteira de delegacao desloca com o nivel (CAT-01 3.6).")
        faltam = [n for n in niveis if n not in c]
        if faltam:
            return None, f"etapa {e['id']}: camada nao declarada para {faltam}"

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


def camada(pb, etapa_id, nivel):
    """Camada de execucao da etapa, resolvida pelo nivel do caso.

    Sem nivel definido, aplica a mais restritiva declarada — nao se assume
    o nivel mais permissivo enquanto a triagem nao apurou.
    """
    e = etapa(pb, etapa_id)
    if not e:
        return None
    c = e["camada"]
    if nivel and nivel in c:
        return c[nivel]
    ordem = ["EX1", "EX2", "EX3", "EX4"]
    return max(c.values(), key=lambda x: ordem.index(x) if x in ordem else 99)


HUMANA = ("EX3", "EX4")


def humana(cam):
    """A camada exige pessoa? A guarda ja aplica esta regra em G1."""
    return cam in HUMANA


def natureza(pb, etapa_id, nivel):
    """Como esta etapa se comporta para este nivel, em uma linha."""
    e = etapa(pb, etapa_id)
    if not e:
        return "?"
    if e.get("delegavel") is False:
        return "nao delegavel"
    return "exige verificacao humana" if humana(camada(pb, etapa_id, nivel)) \
        else "preparacao delegavel"


def proxima_fronteira(pb, etapa_id, nivel):
    """Primeira etapa daqui em diante que exige pessoa. None se nao houver.

    Devolve (id, camada, motivo) da etapa, ou None se a etapa corrente ja
    exigir pessoa — nesse caso nao ha fronteira a anunciar, ela ja chegou.
    """
    ids = [e["id"] for e in pb["etapas"]]
    if etapa_id not in ids:
        return None
    if humana(camada(pb, etapa_id, nivel)) or (etapa(pb, etapa_id) or {}).get("delegavel") is False:
        return None
    for e in pb["etapas"][ids.index(etapa_id) + 1:]:
        cam = camada(pb, e["id"], nivel)
        if e.get("delegavel") is False:
            return e["id"], cam, "nao delegavel"
        if humana(cam):
            return e["id"], cam, "exige verificacao humana"
    return None


if __name__ == "__main__":
    pb, erro = carregar()
    if erro:
        print(erro, file=sys.stderr); sys.exit(1)
    print(f"playbook '{pb.get('nome','?')}' v{pb.get('versao','?')} valido: "
          f"{len(pb['etapas'])} etapas, {len(pb.get('entregaveis', []))} entregaveis, "
          f"{len(pb['inegociaveis'])} itens inegociaveis, "
          f"niveis {pb['niveis']}")
