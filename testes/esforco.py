#!/usr/bin/env python3
"""Contrato do esforço de campo: camada derivada e autoria humana."""
import json
import pathlib
import shutil
import subprocess
import tempfile


RAIZ = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / "eiac-nucleo" / "scripts" / "esforco.py"
TEMPLATE = RAIZ / "eiac-campo" / "template-caso" / "registro"


def executar(*args, cwd):
    return subprocess.run(
        ["python3", str(SCRIPT), *args], cwd=cwd, text=True,
        capture_output=True, check=False,
    )


def main():
    with tempfile.TemporaryDirectory() as temporario:
        caso = pathlib.Path(temporario)
        (caso / "registro").mkdir()
        shutil.copy(TEMPLATE / "playbook.json", caso / "registro" / "playbook.json")
        (caso / "registro" / "estado.json").write_text(
            json.dumps({"caso": "esforco", "etapa_atual": "P1", "nivel": "N1"}),
            encoding="utf-8",
        )

        negativo = executar(
            "--registrar", "P1", "--duracao-segundos", "30",
            "--autor", "agente-01", cwd=caso,
        )
        assert negativo.returncode != 0 and "pessoa nomeada" in negativo.stderr
        eventos = (caso / "registro" / "eventos.jsonl").read_text(encoding="utf-8")
        assert "EsforcoRecusado" in eventos

        positivo = executar(
            "--registrar", "P1", "--duracao-segundos", "30.5",
            "--autor", "Maria Silva", cwd=caso,
        )
        assert positivo.returncode == 0, positivo.stderr
        registro = json.loads(
            (caso / "registro" / "esforco.jsonl").read_text(encoding="utf-8").splitlines()[-1]
        )
        assert registro["camada"] == "EX2"
        assert registro["duracao_segundos"] == 30.5
        assert registro["execucao"] == "campo"
        assert set(registro) == {
            "evento", "etapa", "camada", "nivel", "autor", "inicio", "fim",
            "duracao_segundos", "execucao",
        }
        print("esforço de campo: recusa + caminho positivo + contrato comparável")


if __name__ == "__main__":
    main()
