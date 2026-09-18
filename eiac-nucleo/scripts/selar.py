"""Selo do caso. Unico caminho de commit no repositorio do caso.

Uso:  python3 selar.py --autor "Nome" --nota "F0 encerrada, E1 emitido"

O selo e a terceira trava: o historico do repositorio do caso. O commit sai
com o autor nomeado, o mesmo que a trilha registra — nao a identidade da
maquina. Selar continua sendo ato deliberado; este script so tira do
operador a necessidade de saber git.
"""
import argparse, pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def selar(autor, nota):
    if not pathlib.Path(".git").is_dir():
        return "aqui nao e um repositorio git. O selo depende do historico do caso."

    pendente = git("status", "--porcelain").stdout.strip()
    if not pendente:
        return "nada a selar: o caso ja esta limpo."

    arquivos = len(pendente.splitlines())
    # O evento entra antes do commit: o selo precisa conter o proprio registro
    # de que foi aplicado, senao a trilha fica sempre fora do que ela sela.
    E.evento("SeloAplicado", arquivos=arquivos, autor=autor, nota=nota)

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
