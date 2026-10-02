"""Le e escreve o Registro do Caso. Unico caminho de mudanca de etapa."""
import json, pathlib, re, subprocess, sys, datetime

CAMINHO = pathlib.Path("registro/estado.json")
RAIZ_COMPONENTE = pathlib.Path(__file__).resolve().parents[2]
_MANIFESTO = pathlib.Path(__file__).resolve().parents[1] / ".claude-plugin" / "plugin.json"


def _commit_componente():
    """SHA do commit do repositorio deste componente (eiac-nucleo/campo),
    lido em tempo de execucao -- nunca digitado. 'desconhecido' fora de um
    repositorio git (ex.: plugin copiado sem historico); isso ainda carimba
    a variante, so nao a rastreabilidade de commit."""
    try:
        r = subprocess.run(
            ["git", "-C", str(RAIZ_COMPONENTE), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else "desconhecido"
    except (OSError, subprocess.SubprocessError):
        return "desconhecido"


def _variante_componente():
    try:
        return json.loads(_MANIFESTO.read_text(encoding="utf-8")).get("variante", "desconhecida")
    except (OSError, json.JSONDecodeError):
        return "desconhecida"


def _componente():
    return {"variante": _variante_componente(), "commit": _commit_componente()}


def ler():
    if not CAMINHO.exists():
        return None
    return json.loads(CAMINHO.read_text(encoding="utf-8"))


def eventos():
    """Le a trilha completa (registro/eventos.jsonl), na ordem em que foi
    gravada. Linha ilegivel e pulada (nao interrompe a leitura) -- quem
    precisar de trilha integra sabe onde procurar a falha; um leitor de
    trava nao deve quebrar por uma linha antiga corrompida."""
    log = pathlib.Path("registro/eventos.jsonl")
    if not log.exists():
        return []
    lidos = []
    for linha in log.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha:
            continue
        try:
            lidos.append(json.loads(linha))
        except json.JSONDecodeError:
            continue
    return lidos


def selos_confirmados():
    """Deriva selos e snapshots pela primeira introdução no histórico Git.

    Retorna (lista, erro). Eventos fora de commit não comprovam aplicação.
    A introdução precisa ter autoria e nota correspondentes ao evento.
    """
    def git(*args):
        return subprocess.run(["git", *args], capture_output=True, text=True, timeout=5)

    try:
        raiz = git("rev-parse", "--show-toplevel")
        if raiz.returncode or pathlib.Path(raiz.stdout.strip()).resolve() != pathlib.Path.cwd().resolve():
            return [], "histórico Git inacessível ou fora da raiz do caso"
        historico = git("log", "--reverse", "--format=%H", "--", "registro/eventos.jsonl")
        if historico.returncode:
            return [], "histórico Git inacessível: " + historico.stderr.strip()
        vistos, selos = set(), []
        for sha in historico.stdout.splitlines():
            snapshot = git("show", sha+":registro/eventos.jsonl")
            if snapshot.returncode:
                return [], "snapshot da trilha inacessível no histórico Git"
            novos, eventos_snapshot = [], []
            for pos, linha in enumerate(snapshot.stdout.splitlines()):
                try:
                    ev = json.loads(linha)
                except json.JSONDecodeError:
                    eventos_snapshot.append(None)
                    continue
                eventos_snapshot.append(ev)
                chave = (pos, json.dumps(ev, sort_keys=True, ensure_ascii=False))
                if ev.get("evento") == "SeloAplicado" and chave not in vistos:
                    novos.append((pos,ev))
                vistos.add(chave)
            if not novos:
                continue
            meta = git("show", "-s", "--format=%an%x00%B", sha)
            if meta.returncode:
                return [], "metadados do commit inacessíveis no histórico Git"
            autor, nota = meta.stdout.split("\0", 1)
            for pos,ev in novos:
                if ev.get("autor") == autor and ev.get("nota", "").strip() == nota.strip():
                    selos.append({"hash":sha,"data":ev.get("data"),"nota":ev.get("nota"),
                                  "posicao":pos,"eventos":eventos_snapshot,"linhas":snapshot.stdout.splitlines()})
        return selos, None
    except (OSError, subprocess.SubprocessError, ValueError, AttributeError, TypeError) as exc:
        return [], "histórico Git inacessível: " + str(exc)


def ultimo_selo():
    """Apresentação somente leitura: último selo comprovado no histórico."""
    selos, erro = selos_confirmados()
    if erro or not selos:
        return None
    return {k:selos[-1][k] for k in ("hash","data","nota")}


def gravar(e):
    CAMINHO.parent.mkdir(parents=True, exist_ok=True)
    CAMINHO.write_text(json.dumps(e, indent=2, ensure_ascii=False), encoding="utf-8")


def evento(tipo, **campos):
    log = pathlib.Path("registro/eventos.jsonl")
    log.parent.mkdir(parents=True, exist_ok=True)
    reg = {
        "evento": tipo,
        "data": datetime.datetime.now().isoformat(timespec="seconds"),
        "componente": _componente(),
    }
    reg.update(campos)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")


def autor_e_agente(nome):
    """Convencao lexical: nomes de agente/sistema nao sao autor humano.

    O nucleo ainda nao tem identidade tipada de ator; esta e a forma minima
    consistente com o que ja e verificado em selar.py, validar.py e
    avancar.py. O separador entre "ag" e o numero (hifen, espaco ou nada)
    e ignorado, para nao deixar passar "papel-01" so porque nao e "AG01".
    Limitacao: um nome humano que comece por essas silabas seria recusado;
    nenhum caso assim foi observado no metodo ate aqui.
    """
    chave = re.sub(r"[\s\-_]", "", (nome or "").strip().lower())
    return chave.startswith(("ag0", "agente", "sistema"))


def pessoa_nomeada(nome, regra=None):
    import pessoa
    if regra is None:
        try:
            regra = json.loads(pathlib.Path('registro/playbook.json').read_text(encoding='utf-8')).get('pessoa_nomeada')
        except (OSError, ValueError):
            return False
    return not autor_e_agente(nome) and pessoa.aceita(nome, regra)


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
    e["selo"] = ultimo_selo()
    if "--resumo" in sys.argv:
        cam = e.get("camada_atual")
        pb = None
        try:
            import playbook as P
            pb, _ = P.carregar()
        except Exception:
            P = None
        if not cam and pb:
            cam = P.camada(pb, e["etapa_atual"], e.get("nivel"))
        nivel = e.get("nivel") or "nao apurado"
        # a camada sozinha so informa quem decorou EX1-EX4; diga o que ela exige
        sentido = ""
        if pb:
            sentido = " · " + P.natureza(pb, e["etapa_atual"], e.get("nivel"))
        print(f"Caso {e['caso']} | nivel {nivel} | etapa {e['etapa_atual']} "
              f"| camada {cam or '?'}{sentido} | modalidade {e.get('modalidade_atual','?')}")
        selo = e["selo"]
        print(f"Selo: {selo['hash']} | {selo['data']} | {selo['nota']}" if selo else "Selo: nenhum")
        if pb:
            prox = P.proxima_fronteira(pb, e["etapa_atual"], e.get("nivel"))
            if prox:
                pid, pcam, motivo = prox
                ids = [x["id"] for x in pb["etapas"]]
                i = ids.index(e["etapa_atual"])
                imediata = i + 1 < len(ids) and ids[i + 1] == pid
                if imediata:
                    print(f"Ultima etapa delegavel do caso. A seguinte, {pid} "
                          f"({pcam}), {motivo}.")
                else:
                    print(f"Proxima fronteira: {pid} ({pcam}) {motivo}.")
        if not e.get("nivel") and pb and e["etapa_atual"] != pb["etapas"][0]["id"]:
            print("ATENCAO: nivel nao apurado. A camada das etapas depende dele.")
    else:
        print(json.dumps(e, indent=2, ensure_ascii=False))
