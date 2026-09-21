"""Registro comparável de esforço da execução de campo.

O engenheiro informa etapa e duração observada. A camada nunca é recebida por
argumento: é resolvida do playbook com o nível corrente do caso.
"""
import argparse
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P

ARQUIVO = pathlib.Path("registro/esforco.jsonl")


def registrar(etapa_id, duracao_segundos, autor, pb, nivel):
    if E.autor_e_agente(autor):
        return "autor do esforço precisa ser pessoa nomeada, não agente", None
    if not autor.strip():
        return "autor do esforço é obrigatório", None
    if duracao_segundos < 0:
        return "duração do esforço não pode ser negativa", None
    if not P.etapa(pb, etapa_id):
        return f"etapa {etapa_id} não existe no playbook", None

    agora = datetime.datetime.now().isoformat(timespec="seconds")
    registro = {
        "evento": "FimPasso",
        "etapa": etapa_id,
        "camada": P.camada(pb, etapa_id, nivel),
        "nivel": nivel,
        "autor": autor,
        "inicio": None,
        "fim": agora,
        "duracao_segundos": duracao_segundos,
        "execucao": "campo",
    }
    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with ARQUIVO.open("a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
    E.evento(
        "EsforcoConcluido",
        etapa=etapa_id,
        camada=registro["camada"],
        autor=autor,
        duracao_segundos=duracao_segundos,
        execucao="campo",
    )
    return None, registro


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registrar", required=True, metavar="ETAPA")
    parser.add_argument("--duracao-segundos", required=True, type=float)
    parser.add_argument("--autor", required=True)
    args = parser.parse_args()

    estado = E.ler()
    playbook, erro = P.carregar()
    if not estado or erro:
        print(erro or "nenhum caso aberto", file=sys.stderr)
        sys.exit(1)
    erro, registro = registrar(
        args.registrar, args.duracao_segundos, args.autor, playbook, estado.get("nivel")
    )
    if erro:
        E.evento("EsforcoRecusado", motivo=erro, etapa=args.registrar, autor=args.autor)
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(
        f"esforco {registro['evento']} | etapa {registro['etapa']} | "
        f"camada {registro['camada']}"
    )


if __name__ == "__main__":
    main()
