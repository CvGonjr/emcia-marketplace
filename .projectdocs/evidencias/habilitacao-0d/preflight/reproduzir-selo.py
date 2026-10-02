"""Diagnóstico sintético: evento de selo não equivale a commit confirmado.
Executar da raiz: python3 .projectdocs/evidencias/habilitacao-0d/preflight/reproduzir-selo.py
Não é teste de aceite da implementação solicitada.
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile

raiz = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(raiz / 'eiac-nucleo/scripts'))
import estado as E
import playbook as P
import selar as S

with tempfile.TemporaryDirectory(prefix='emcia-selo-sintetico-') as tmp:
    os.chdir(tmp)
    def git(*args):
        return subprocess.run(['git', *args], check=True, capture_output=True, text=True).stdout.strip()
    git('init', '-q')
    git('config', 'user.name', 'Pessoa Sintetica')
    git('config', 'user.email', 'sintetico@example.invalid')
    pathlib.Path('registro').mkdir()
    E.evento('CasoAberto', autor='Pessoa Sintetica')
    git('add', '-A')
    git('-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'abertura sintetica')
    hooks = pathlib.Path('hooks-controle').resolve()
    hooks.mkdir()
    hook = hooks / 'pre-commit'
    hook.write_text('#!/bin/sh\nexit 1\n')
    hook.chmod(0o755)
    git('config', 'core.hooksPath', str(hooks))
    git('config', 'commit.gpgsign', 'false')
    E.evento('EtapaEncerrada', etapa='etapa-origem', autor='Pessoa Sintetica')
    erro = S.selar('Pessoa Sintetica', 'selo sintético recusado')
    contrato = {'etapas': [{'id': 'etapa-destino', 'exige_selo_apos': 'etapa-origem'}]}
    aceito, motivo = P.selo_apos_etapa(contrato, 'etapa-destino', E.eventos())
    resultado = {
        'commit_recusado': bool(erro),
        'erro': erro,
        'evento_selo_na_trilha': any(e['evento'] == 'SeloAplicado' for e in E.eventos()),
        'selo_confirmado': E.ultimo_selo(),
        'regra_atual_aceita': aceito,
        'motivo_regra': motivo,
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    assert erro and aceito and resultado['selo_confirmado'] is None
