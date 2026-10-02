"""Guarda de camada. Hook PreToolUse: exit 2 bloqueia a chamada.

Regras, sem ordem fixa exigida entre si:
  G1  habilidade de camada nao delegavel nao carrega
  G2  escrita direta em caso/ e negada; toda assercao passa pelo validador
  G2b escrita direta em contexto/ e negada; todo objeto passa pelo curador
  G3  etapa dependente exige o cumprimento declarado no playbook
  G4  nivel nao apurado apos etapa inicial bloqueia a etapa
  G5  escrita direta em registro/ e negada; apenas os scripts do nucleo
      (avancar.py, curar.py, validar.py, selar.py) gravam ali, via
      estado.gravar()/estado.evento(), nunca por Write/Edit/redirecionamento
      de shell
  G6  escrita, edicao ou remocao em fontes/ por agente e negada; fontes/
      e so leitura, documento novo entra pelo operador, fora da sessao
      do agente
  G7  habilidade de etapa que declara "exige_selo_apos" nao carrega sem
      selo posterior ao encerramento da etapa referenciada
  G8  operações humanas declaradas no playbook não executam pela sessão
"""
import json, os, pathlib, re, shlex, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P
import decisao_humana as H
import caminhos as C
import canais_registro as K
import escopo_externo as S


LEITORES_FONTES = {
    "cat", "file", "grep", "head", "ls", "rg", "sha256sum",
    "stat", "tail", "wc",
}
MARCADOR_CONTRASTE = re.compile(
    r'(?:"execucao"\s*:\s*"contraste"|(?:^|\n)\s*execucao\s*:\s*["\']?contraste["\']?\s*(?:\n|$))'
)


def negar(motivo, **ctx):
    ctx.setdefault("autor", (E.ler() or {}).get("responsavel"))
    E.evento("TentativaNegada", motivo=motivo, **ctx)
    print(motivo, file=sys.stderr)
    sys.exit(2)


def nomes_habilidades(ev, entrada, alvo, comando, caminhos):
    nomes = set()
    if ev.get("tool_name") == "Skill":
        nomes.add(str(entrada.get("skill", "")).split(":")[-1])
    if ev.get("hook_event_name") == "UserPromptExpansion":
        nomes.add(str(ev.get("command_name", "")).lstrip("/").split(":")[-1])
    if alvo:
        nomes.update(caminhos.nomes(alvo))
    if ev.get("tool_name") == "Bash":
        for grupo, cwd in C.comandos(comando, caminhos.cwd):
            for caminho in C.argumentos_caminho(grupo):
                nomes.update(caminhos.nomes(caminho,cwd))
    return nomes


def _bash_fontes(comando, caminhos):
    for grupo, cwd in C.comandos(comando,caminhos.cwd):
        if any(caminhos.em_segmento(p,"fontes",cwd) for p in C.escritas(grupo)):
            return True
        argv,_ = C.redirecionamentos(grupo)
        menciona = any(caminhos.em_segmento(p,"fontes",cwd)
                      for p in C.argumentos_caminho(argv))
        # Código arbitrário que toca uma fonte não é reconhecido como
        # leitor. A inspeção de redirecionamentos não retira essa trava.
        if menciona and argv and pathlib.Path(argv[0]).name not in LEITORES_FONTES | C.ESCRITORES:
            return True
    return False


def _bash_em(comando, caminhos, area):
    return any(caminhos.em(p,area,cwd) for grupo,cwd in C.comandos(comando,caminhos.cwd)
               for p in C.escritas(grupo))


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

    raiz = C.raiz_caso(ev)
    if raiz is None:
        sys.exit(0)
    caminhos = C.Contexto(raiz, ev.get("cwd") or os.getcwd())
    os.chdir(raiz)
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
    erro_escopo = S.conferir(pb, ferramenta, entrada)
    if erro_escopo:
        negar(erro_escopo, ferramenta=ferramenta, operacao='escopo-externo')
    alvo = str(entrada.get("file_path") or entrada.get("path") or entrada.get("notebook_path") or "")
    comando = str(entrada.get("command") or "")
    etapa_id = st["etapa_atual"]
    nivel = st.get("nivel")
    etapa = P.etapa(pb, etapa_id) or {}
    camada_corrente = P.camada(pb, etapa_id, nivel)

    # Toda chamada recebida neste hook vem da sessão do agente. A
    # identidade digitada não muda essa origem; condições vêm do caso.
    if ferramenta == "Bash":
        decisao = H.avaliar(pb, st, comando)
        if decisao:
            operacao, motivo = decisao
            negar(
                f"{motivo} A decisao humana e executada pelo engenheiro no "
                f"proprio terminal, fora da sessao do Claude Code. "
                f"Comando exato: {comando}",
                operacao=operacao, acao_tentada=operacao, comando=comando,
                autor=st.get("responsavel"), etapa=etapa_id, ferramenta=ferramenta,
            )

    # A habilidade é identificada pelo nome declarado, em todas as rotas
    # de carregamento. O namespace e a localização da instalação não
    # fazem parte da regra do método.
    nomes = nomes_habilidades(ev, entrada, alvo, comando, caminhos)
    habilidades = [e for e in pb["etapas"] if e.get("habilidade") in nomes]
    # G7 continua independente da autorização de carregamento.
    for e in habilidades:
        confirmado,motivo=P.selo_confirmado_apos_evento(pb,e['id'],E.eventos())
        if not confirmado:
            negar(motivo,etapa=e['id'],ferramenta=ferramenta)
        erro_canal = K.conferir(pb, e['id'])
        if erro_canal:
            negar(erro_canal, etapa=e['id'], ferramenta=ferramenta)
        selo_ok, motivo_selo = P.selo_apos_etapa(pb, e["id"], E.eventos())
        if not selo_ok:
            negar(motivo_selo, etapa=e["id"], ferramenta=ferramenta)

    # G1: sessão registrada não delega uma etapa explicitamente humana.
    # Nas etapas delegáveis de camada humana, mantém-se o uso instrumental
    # após a sessão da própria etapa, sem delegar a decisão.
    for e in habilidades:
        cam = P.camada(pb, e["id"], nivel)
        sessao = st.get("cumprimentos", {}).get(e["id"], {}).get("sessao")
        if e.get("delegavel") is False or (P.humana(cam) and not sessao):
            motivo = ("nao e delegavel a agente" if e.get("delegavel") is False
                      else f"esta em camada humana ({cam}) para o nivel {nivel or 'nao apurado'}")
            negar(
                f"{cam}: a etapa {e['id']} {motivo}. "
                f"Modalidade exigida: {e.get('modalidade','?')}. "
                "A sessao registrada nao delega uma etapa humana."
                if e.get("delegavel") is False else
                f"{cam}: a etapa {e['id']} {motivo}. Registre a sessao com /eiac-nucleo:registrar-sessao.",
                etapa=e["id"], camada_exigida=cam, nivel=nivel, ferramenta=ferramenta,
                habilidade=e["habilidade"], hook_event_name=ev.get("hook_event_name"),
            )

    # G2 — escrita direta no repositorio do caso
    escrita = ferramenta in ("Write", "Edit", "NotebookEdit") and caminhos.em(alvo,"caso")
    escrita_bash = ferramenta == "Bash" and _bash_em(comando,caminhos,"caso")
    if escrita or escrita_bash:
        negar(
            "Escrita direta em caso/ nao e permitida. "
            "Grave pelo validador: python3 scripts/validar.py --arquivo <caminho>. "
            "Toda assercao exige procedencia D, I ou V.",
            etapa=etapa_id, ferramenta=ferramenta, alvo=alvo,
        )

    # G2b — escrita direta na camada de contexto curada
    escrita_ctx = ferramenta in ("Write", "Edit", "NotebookEdit") and caminhos.em(alvo,"contexto")
    escrita_ctx_bash = ferramenta == "Bash" and _bash_em(comando,caminhos,"contexto")
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
    escrita_fontes = ferramenta in ("Write", "Edit", "NotebookEdit") and caminhos.em_segmento(alvo,"fontes")
    escrita_fontes_bash = ferramenta == "Bash" and _bash_fontes(comando,caminhos)
    if escrita_fontes or escrita_fontes_bash:
        negar(
            "Escrita, edicao ou remocao em fontes/ nao e permitida a agente. "
            "fontes/ e somente leitura (fontes/README.md): documento novo "
            "entra pelo operador, fora da sessao do agente.",
            etapa=etapa_id, ferramenta=ferramenta, alvo=alvo,
        )

    # G4 — nivel nao apurado apos etapa inicial
    if etapa_id != pb["etapas"][0]["id"] and not nivel:
        negar(
            f"Nivel do caso nao apurado. A camada de {etapa_id} depende dele "
            f"Encerre {pb['etapas'][0]['id']} antes de prosseguir.",
            etapa=etapa_id,
        )

    # G5 — escrita direta em registro/ (playbook, estado, eventos, selos)
    # so os scripts do nucleo gravam ali; passar por Write/Edit ou
    # redirecionamento de shell contorna estado, inegociaveis, portoes e
    # eventos (2.6-BL17, D-08).
    escrita_registro = ferramenta in ("Write", "Edit", "NotebookEdit") and caminhos.em(alvo,"registro")
    escrita_registro_bash = ferramenta == "Bash" and _bash_em(comando,caminhos,"registro")
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
    try:
        main()
    except (C.CaminhoInvalido, ValueError) as exc:
        negar(f"Entrada de caminho/comando invalida: {exc}")
