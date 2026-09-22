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
  G6  escrita, edicao ou remocao em fontes/ por agente e negada; fontes/
      e so leitura, documento novo entra pelo operador, fora da sessao
      do agente
"""
import json, os, pathlib, re, shlex, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P


META_SHELL = re.compile(r"(?:\n|\r|&&|\|\||[;|<>`]|\$\()")
LEITORES_FONTES = {
    "cat", "file", "grep", "head", "ls", "rg", "sha256sum",
    "stat", "tail", "wc",
}
MARCADOR_CONTRASTE = re.compile(
    r'(?:"execucao"\s*:\s*"contraste"|(?:^|\n)\s*execucao\s*:\s*["\']?contraste["\']?\s*(?:\n|$))'
)


def negar(motivo, **ctx):
    E.evento("TentativaNegada", motivo=motivo, **ctx)
    print(motivo, file=sys.stderr)
    sys.exit(2)


def _em_fontes(alvo):
    if not alvo:
        return False
    if "fontes" in pathlib.PurePath(alvo).parts:
        return True
    caminho = pathlib.Path(alvo)
    resolvido = caminho.resolve() if caminho.is_absolute() else (pathlib.Path.cwd() / caminho).resolve()
    return "fontes" in resolvido.parts


def _bash_menciona_fontes(comando):
    if "fontes/" in comando or "/fontes/" in comando:
        return True
    try:
        partes = shlex.split(comando)
    except ValueError:
        partes = comando.split()
    return any(
        parte == "fontes" or parte.startswith("fontes/") or "/fontes/" in parte
        for parte in partes
    )


def _bash_leitura_fontes(comando):
    """Reconhece somente comandos simples e explicitamente de leitura."""
    if not comando.strip() or META_SHELL.search(comando):
        return False
    try:
        partes = shlex.split(comando)
    except ValueError:
        return False
    return bool(partes) and pathlib.Path(partes[0]).name in LEITORES_FONTES


def _registro_contraste():
    """Localiza marcador duravel de contraste sem interpretar o metodo."""
    raiz = pathlib.Path("registro")
    if not raiz.is_dir():
        return None
    for caminho in raiz.rglob("*"):
        if not caminho.is_file() or caminho.stat().st_size > 5_000_000:
            continue
        try:
            texto = caminho.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if MARCADOR_CONTRASTE.search(texto):
            return str(caminho)
    return None


def main():
    try:
        ev = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    st = E.ler()
    if not st:
        sys.exit(0)          # fora de caso, o nucleo nao opina

    registro_contraste = _registro_contraste()
    if registro_contraste:
        negar(
            "Isolamento de execuções: eiac-nucleo não opera em caso com "
            "registro marcado como execucao: contraste. A identidade de "
            "plugin não distingue campo de contraste (colisão deliberada, "
            "ver decisão 008 do emcia-contraste) — a verificação de "
            "identidade completa (variante + commit por evento) é feita "
            "no selo, não aqui.",
            registro_contraste=registro_contraste,
        )

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

    # G6 — fontes/ e so leitura (fontes/README.md ja declara isso; sem
    # esta regra, nada impedia a escrita antes da guarda existir — so o
    # SHA-256 gravado por validar.py detectava alteracao depois da
    # citacao, nunca antes dela). Cobre qualquer segmento "fontes/" na
    # arvore do caso (raiz e contexto/fontes/, esta ultima ja coberta
    # tambem por G2b). Entrada de documento novo e feita pelo operador,
    # fora da sessao do agente.
    escrita_fontes = ferramenta in ("Write", "Edit") and _em_fontes(alvo)
    escrita_fontes_bash = (
        ferramenta == "Bash"
        and _bash_menciona_fontes(comando)
        and not _bash_leitura_fontes(comando)
    )
    if escrita_fontes or escrita_fontes_bash:
        negar(
            "Escrita, edicao ou remocao em fontes/ nao e permitida a agente. "
            "fontes/ e somente leitura (fontes/README.md): documento novo "
            "entra pelo operador, fora da sessao do agente.",
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
