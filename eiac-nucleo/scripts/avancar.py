"""Maquina de etapas. Unico caminho de avanco.

Uso:
  python3 avancar.py --apurar-nivel N2 --autor "Nome" --eixos "DAD 4, GOV 5, CRI 7"
  python3 avancar.py --encerrar P2 --autor "Nome"
  python3 avancar.py --registrar-sessao P3b --autor "Nome" --participantes "A, B"
  python3 avancar.py --emitir E2 --autor "Nome"
"""
import argparse, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P


def apurar_nivel(st, pb, nivel, autor, eixos):
    if nivel not in pb["niveis"]:
        return f"nivel '{nivel}' nao existe no playbook: {pb['niveis']}"
    anterior = st.get("nivel")
    st["nivel"] = nivel
    st["camada_atual"] = P.camada(pb, st["etapa_atual"], nivel)
    if eixos:
        st["cumprimentos"].setdefault("F0", {})["eixos"] = eixos
    E.evento("NivelApurado", nivel=nivel, anterior=anterior, autor=autor, eixos=eixos)
    return None


def encerrar(st, pb, etapa_id, autor):
    et = P.etapa(pb, etapa_id)
    if not et:
        return f"etapa {etapa_id} nao existe no playbook"
    if etapa_id == "F0" and not st.get("nivel"):
        return ("F0 nao encerra sem o nivel apurado. A camada das etapas seguintes "
                "depende dele (CAT-01 3.6). Grave o nivel em registro/estado.json.")
    if st.get("nivel") and st["nivel"] not in pb["niveis"]:
        return f"nivel '{st['nivel']}' nao existe no playbook: {pb['niveis']}"
    if et.get("delegavel") is False and not st["cumprimentos"].get(etapa_id, {}).get("sessao"):
        return (f"{etapa_id} e {et['modalidade']} e nao delegavel. "
                f"Registre a sessao antes de encerrar.")
    dep = et.get("depende_de")
    if dep and not st["cumprimentos"].get(dep, {}).get("cumprido"):
        return f"{etapa_id} depende de {dep}, ainda nao cumprida"
    st["cumprimentos"].setdefault(etapa_id, {})
    st["cumprimentos"][etapa_id].update({"cumprido": True, "autor": autor})
    idx = [e["id"] for e in pb["etapas"]].index(etapa_id)
    if idx + 1 < len(pb["etapas"]):
        prox = pb["etapas"][idx + 1]
        st["etapa_atual"] = prox["id"]
        st["camada_atual"] = P.camada(pb, prox["id"], st.get("nivel"))
        st["modalidade_atual"] = prox["modalidade"]
    E.evento("EtapaEncerrada", etapa=etapa_id, autor=autor)
    return None


def registrar_sessao(st, etapa_id, autor, participantes):
    st["cumprimentos"].setdefault(etapa_id, {})
    st["cumprimentos"][etapa_id]["sessao"] = {
        "autor": autor, "participantes": participantes
    }
    E.evento("SessaoDeCampoRegistrada", etapa=etapa_id, autor=autor,
             participantes=participantes)
    return None


def emitir(st, pb, ent_id, autor):
    ent = next((d for d in pb.get("entregaveis", []) if d["id"] == ent_id), None)
    if not ent:
        return f"entregavel {ent_id} nao existe no playbook"
    if ent.get("portao_pendente"):
        return (f"{ent_id} tem portao pendente de decisao no playbook. "
                f"Nao emita ate a pendencia ser resolvida.")
    faltando = [e for e in ent["portao"]
                if not st["cumprimentos"].get(e, {}).get("cumprido")]
    if faltando:
        return f"{ent_id} exige as etapas {faltando} encerradas"
    for n in ent.get("inegociavel", []):
        item = next(i for i in pb["inegociaveis"] if i["n"] == n)
        if not st.get("inegociaveis", {}).get(str(n)):
            return f"{ent_id} bloqueado pelo item inegociavel {n}: {item['item']}"
    E.evento("EntregavelEmitido", entregavel=ent_id, autor=autor)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apurar-nivel")
    ap.add_argument("--encerrar"); ap.add_argument("--registrar-sessao")
    ap.add_argument("--emitir"); ap.add_argument("--autor", required=True)
    ap.add_argument("--participantes", default="")
    ap.add_argument("--eixos", default="")
    a = ap.parse_args()

    st = E.ler()
    pb, erro = P.carregar()
    if not st or erro:
        print(erro or "nenhum caso aberto", file=sys.stderr); sys.exit(1)
    if a.autor.lower().startswith(("ag0", "agente", "sistema")):
        print("autor precisa ser pessoa nomeada", file=sys.stderr); sys.exit(1)

    if a.apurar_nivel:
        err = apurar_nivel(st, pb, a.apurar_nivel, a.autor, a.eixos)
    elif a.registrar_sessao:
        err = registrar_sessao(st, a.registrar_sessao, a.autor, a.participantes)
    elif a.encerrar:
        err = encerrar(st, pb, a.encerrar, a.autor)
    elif a.emitir:
        err = emitir(st, pb, a.emitir, a.autor)
    else:
        print("nada a fazer", file=sys.stderr); sys.exit(1)

    if err:
        print(err, file=sys.stderr); sys.exit(1)
    E.gravar(st)
    print(f"ok | etapa atual: {st['etapa_atual']} | camada: {st.get('camada_atual')}")


if __name__ == "__main__":
    main()
