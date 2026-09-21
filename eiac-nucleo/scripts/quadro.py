"""Adaptador para o cálculo único mantido no eiac-campo compartilhado."""
import importlib.util
import os
import pathlib
import sys

campo = pathlib.Path(
    os.environ.get(
        "EIAC_CAMPO_RAIZ",
        pathlib.Path(__file__).resolve().parents[2] / "eiac-campo",
    )
)
caminho = campo / "scripts" / "quadro.py"
spec = importlib.util.spec_from_file_location("eiac_campo_quadro", caminho)
if not spec or not spec.loader:
    raise RuntimeError(f"cálculo compartilhado não encontrado: {caminho}")
_compartilhado = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_compartilhado)

# API Python preservada para consumidores existentes.
ler_yaml = _compartilhado.ler_yaml
main = _compartilhado.main

# Contrato auditável de não reinterpretação: a implementação compartilhada
# lê diretamente r.get("frequencia") e r.get("consequencia_do_erro").

if __name__ == "__main__":
    main()
