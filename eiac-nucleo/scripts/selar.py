"""Selo do caso. Unico caminho de commit no repositorio do caso.

Uso:  python3 selar.py --autor "Nome" --nota "F0 encerrada, E1 emitido"

O selo e a terceira trava: o historico do repositorio do caso. O commit sai
com o autor nomeado, o mesmo que a trilha registra — nao a identidade da
maquina. Selar continua sendo ato deliberado; este script so tira do
operador a necessidade de saber git.
"""
import argparse, json, pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def checar_identidade_trilha():
    """O selo e o ponto de verificacao de identidade de execucao (nao a
    guarda, nao o nome de plugin -- eiac-nucleo e eiac-contraste colidem de
    proposito no manifesto para preservar as mesmas chamadas de habilidade;
    ver decisao 008 do emcia-contraste). Um caso de campo so sela se
    toda linha de registro/eventos.jsonl: (a) tiver o carimbo `componente`,
    e (b) esse carimbo declarar variante 'campo'. Ausencia de carimbo e
    tratada como falha, nao como evento antigo tolerado -- selar sobre
    trilha nao rastreavel esconderia exatamente o risco que este selo
    existe para prevenir.
    """
    log = pathlib.Path("registro/eventos.jsonl")
    if not log.exists():
        return None
    for numero, linha in enumerate(log.read_text(encoding="utf-8").splitlines(), 1):
        linha = linha.strip()
        if not linha:
            continue
        try:
            reg = json.loads(linha)
        except json.JSONDecodeError:
            return f"evento ilegivel na linha {numero} de registro/eventos.jsonl"
        if reg.get("execucao") == "contraste":
            return (f"evento na linha {numero} marcado execucao: contraste "
                    f"-- caso de campo nao sela registro de execucao de "
                    f"contraste (decisao 014).")
        componente = reg.get("componente")
        if not isinstance(componente, dict) or not componente.get("variante"):
            return (f"evento na linha {numero} sem carimbo de componente "
                    f"(variante). Todo evento precisa declarar de qual "
                    f"componente (campo/contraste) e commit ele veio -- "
                    f"sem isso, a identidade da execucao nao e verificavel.")
        if componente["variante"] != "campo":
            return (f"evento na linha {numero} veio de componente variante "
                    f"'{componente['variante']}', nao 'campo'. Caso de "
                    f"campo nao sela evento de outra variante.")
    return None


def commits_componente_na_trilha():
    """Lista, sem duplicar, os commits de componente que aparecem na
    trilha -- vai no manifesto do selo (evento SeloAplicado), para que o
    selo registre exatamente qual codigo de eiac-nucleo produziu o caso."""
    log = pathlib.Path("registro/eventos.jsonl")
    if not log.exists():
        return []
    vistos, commits = set(), []
    for linha in log.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha:
            continue
        try:
            reg = json.loads(linha)
        except json.JSONDecodeError:
            continue
        componente = reg.get("componente")
        if isinstance(componente, dict) and componente.get("commit"):
            chave = (componente.get("variante"), componente["commit"])
            if chave not in vistos:
                vistos.add(chave)
                commits.append({"variante": componente.get("variante"), "commit": componente["commit"]})
    return commits


def selar(autor, nota):
    if not pathlib.Path(".git").is_dir():
        return "aqui nao e um repositorio git. O selo depende do historico do caso."

    erro_identidade = checar_identidade_trilha()
    if erro_identidade:
        return f"identidade de execucao invalida: {erro_identidade}"

    pendente = git("status", "--porcelain").stdout.strip()
    if not pendente:
        return "nada a selar: o caso ja esta limpo."

    arquivos = len(pendente.splitlines())
    # O evento entra antes do commit: o selo precisa conter o proprio registro
    # de que foi aplicado, senao a trilha fica sempre fora do que ela sela.
    E.evento("SeloAplicado", arquivos=arquivos, autor=autor, nota=nota,
             manifesto_componentes=commits_componente_na_trilha())

    git("add", "-A")
    r = git("commit", "-m", nota, "--author", f"{autor} <>")
    if r.returncode != 0:
        return f"git recusou o commit: {r.stderr.strip() or r.stdout.strip()}"

    sha = git("rev-parse", "--short", "HEAD").stdout.strip()
    print(f"selado {sha} | {arquivos} arquivo(s) | autor {autor}")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autor", required=True)
    ap.add_argument("--nota", required=True)
    a = ap.parse_args()

    if E.autor_e_agente(a.autor):
        print("autor precisa ser pessoa nomeada", file=sys.stderr); sys.exit(1)
    if not E.ler():
        print("nenhum caso aberto neste diretorio", file=sys.stderr); sys.exit(1)

    err = selar(a.autor, a.nota)
    if err:
        print(err, file=sys.stderr); sys.exit(1)


if __name__ == "__main__":
    main()
