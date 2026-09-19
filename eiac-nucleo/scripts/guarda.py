"""Guarda de camada. Hook PreToolUse: exit 2 bloqueia a chamada.

Regras, sem ordem fixa exigida entre si:
  G1  habilidade de camada nao delegavel nao carrega
  G2  escrita direta em caso/ e negada; toda assercao passa pelo validador
  G2b escrita direta em contexto/ e negada; todo objeto passa pelo curador
  G3  etapa dependente exige o cumprimento declarado no playbook
  G4  nivel nao apurado apos F0 bloqueia a etapa
  G5  escrita direta em registro/ e negada; apenas os scripts do nucleo
      (avancar.py, curar.py, validar.py, selar.py) gravam ali, via
      estado.gravar()/estado.evento(), nunca por Write/Edit/redirecionamento
      de shell
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
    nivel = st.get("nivel")
    etapa = P.etapa(pb, etapa_id) or {}
    camada_corrente = P.camada(pb, etapa_id, nivel)

    # G1 — habilidade de camada humana nao carrega sem sessao valida
    # A camada de uma etapa desloca com o nivel do caso (CAT-01 3.6):
    # a mesma etapa pode ser EX2 em N1 e EX3 em N3. Sessao humana
    # registrada (por avancar.py --registrar-sessao, caminho autorizado)
    # libera o CARREGAMENTO da skill como instrumento de apoio/registro —
    # nao libera decisao, aprovacao ou fechamento da etapa por agente,
    # que continuam bloqueados por outras regras (delegavel:false em
    # avancar.encerrar(), G1 nao muda isso). Sessao de outra etapa, ou
    # ausente, nao libera.
    for e in pb["etapas"]:
        if not e.get("habilidade") or e["habilidade"] not in alvo:
            continue
        cam = P.camada(pb, e["id"], nivel)
        if e.get("delegavel") is False or cam in ("EX3", "EX4"):
            sessao_valida = bool(
                st.get("cumprimentos", {}).get(e["id"], {}).get("sessao")
            )
            if sessao_valida:
                continue
            motivo = ("nao e delegavel a agente" if e.get("delegavel") is False
                      else f"esta em camada humana ({cam}) para o nivel {nivel or 'nao apurado'}")
            negar(
                f"{cam}: a etapa {e['id']} {motivo}. "
                f"Modalidade exigida: {e.get('modalidade','?')}. "
                f"Registre a sessao com /eiac-nucleo:registrar-sessao.",
                etapa=e["id"], camada_exigida=cam, nivel=nivel, ferramenta=ferramenta,
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
            "Toda assercao exige procedencia D, I ou V.",
            etapa=etapa_id, ferramenta=ferramenta, alvo=alvo,
        )

    # G2b — escrita direta na camada de contexto curada
    escrita_ctx = ferramenta in ("Write", "Edit") and alvo.startswith("contexto/")
    escrita_ctx_bash = ferramenta == "Bash" and " contexto/" in comando and any(
        t in comando for t in (">", ">>", "tee ", "mv ", "cp ")
    )
    if escrita_ctx or escrita_ctx_bash:
        negar(
            "Escrita direta em contexto/ nao e permitida. "
            "Grave pelo curador: python3 scripts/curar.py --tipo <tipo> --arquivo <rascunho>. "
            "Toda regra, termo, entidade ou fonte curada exige procedencia, "
            "autoria de pessoa nomeada e passagem pela curadoria (CTX-01 3.11).",
            etapa=etapa_id, ferramenta=ferramenta, alvo=alvo,
        )

    # G4 — nivel nao apurado apos F0
    if etapa_id != "F0" and not nivel:
        negar(
            f"Nivel do caso nao apurado. A camada de {etapa_id} depende dele "
            f"(CAT-01 3.6). Encerre F0 antes de prosseguir.",
            etapa=etapa_id,
        )

    # G5 — escrita direta em registro/ (playbook, estado, eventos, selos)
    # so os scripts do nucleo gravam ali; passar por Write/Edit ou
    # redirecionamento de shell contorna estado, inegociaveis, portoes e
    # eventos (2.6-BL17, D-08).
    escrita_registro = ferramenta in ("Write", "Edit") and alvo.startswith("registro/")
    escrita_registro_bash = ferramenta == "Bash" and " registro/" in comando and any(
        t in comando for t in (">", ">>", "tee ", "mv ", "cp ")
    )
    if escrita_registro or escrita_registro_bash:
        negar(
            "Escrita direta em registro/ nao e permitida. "
            "Etapa, estado e eventos so mudam pelos scripts do nucleo: "
            "avancar.py (etapa/entregavel/inegociavel), curar.py (contexto), "
            "validar.py (asserção) ou selar.py (selo). Escrita direta contorna "
            "portoes e trilha de eventos.",
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
