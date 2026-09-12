"""Guarda de camada. Hook PreToolUse: exit 2 bloqueia a chamada.

Tres regras, nesta ordem:
  G1  habilidade de camada nao delegavel nao carrega
  G2  escrita direta em caso/ e negada; toda assercao passa pelo validador
  G3  etapa dependente exige o cumprimento declarado no playbook
"""
import json, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P


def negar(motivo, **ctx):
    E.evento("TentativaNegada", motivo=motivo, **ctx)
    print(motivo, file=sys.stderr)
    sys.exit(2)


def main():
    try:
        ev = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    st = E.ler()
    if not st:
        sys.exit(0)          # fora de caso, o nucleo nao opina

    pb, erro = P.carregar()
    if erro:
        negar(f"Playbook invalido: {erro}. O caso nao opera sem playbook valido.")

    ferramenta = ev.get("tool_name", "")
    entrada = ev.get("tool_input", {}) or {}
    alvo = str(entrada.get("file_path") or entrada.get("path") or "")
    comando = str(entrada.get("command") or "")
    etapa_id = st["etapa_atual"]
    etapa = P.etapa(pb, etapa_id) or {}

    # G1 — habilidade de etapa nao delegavel
    for e in pb["etapas"]:
        if e.get("delegavel") is False and e.get("habilidade") and e["habilidade"] in alvo:
            negar(
                f"{e['camada']}: a etapa {e['id']} nao e delegavel a agente. "
                f"Modalidade exigida: {e.get('modalidade','?')}. "
                f"Registre a sessao com /eiac-nucleo:registrar-sessao.",
                etapa=e["id"], camada_exigida=e["camada"], ferramenta=ferramenta,
            )

    # G2 — escrita direta no repositorio do caso
    escrita = ferramenta in ("Write", "Edit") and alvo.startswith("caso/")
    escrita_bash = ferramenta == "Bash" and " caso/" in comando and any(
        t in comando for t in (">", ">>", "tee ", "mv ", "cp ")
    )
    if escrita or escrita_bash:
        negar(
            "Escrita direta em caso/ nao e permitida. "
            "Grave pelo validador: python3 scripts/validar.py --arquivo <caminho>. "
            "Toda assercao exige contexto e origem.",
            etapa=etapa_id, ferramenta=ferramenta, alvo=alvo,
        )

    # G3 — dependencia entre etapas
    dep = etapa.get("depende_de")
    if dep and not st.get("cumprimentos", {}).get(dep, {}).get("cumprido"):
        negar(
            f"A etapa {etapa_id} depende de {dep}, que nao foi cumprida. "
            f"Modalidade de {dep}: {(P.etapa(pb, dep) or {}).get('modalidade','?')}.",
            etapa=etapa_id, depende_de=dep,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
