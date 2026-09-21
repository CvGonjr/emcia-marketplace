"""Encaminha a consulta ao componente de controle selecionado pela execução."""
import os
import pathlib
import runpy

controle = pathlib.Path(
    os.environ.get(
        "EIAC_NUCLEO_SCRIPTS",
        pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts",
    )
)
runpy.run_path(str(controle / "consultar.py"), run_name="__main__")
