"""Precondição sintética explícita; nunca chamada pelo encerramento testado.

Fixtures antigas posicionam o estado diretamente em etapas intermediárias.
Para essas fixtures, registra a decisão pelo script real sobre um estado
temporário de F0 e restaura o posicionamento original. Não desativa guardas
nem muda o playbook. Percursos usam seu estado real já apurado.
"""
import json
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]


def preparar(caso):
    caso = pathlib.Path(caso)
    if (caso/'registro/prosseguimento/vigente.yaml').exists(): return
    pb = json.loads((caso/'registro/playbook.json').read_text())
    if not any(a['id'] == 'decidir-prosseguimento' for a in pb['decisoes_humanas']): return
    p = caso/'registro/estado.json'; original = p.read_bytes(); st = json.loads(original)
    # Posicionamento integra apenas a montagem desta fixture isolada.
    temporario = dict(st, etapa_atual='F0', nivel=st.get('nivel') or 'N2',
                      responsavel=st.get('responsavel') or 'Celso do Vale', cumprimentos={})
    pasta = caso/'caso'; pasta.mkdir(exist_ok=True)
    ficha = pasta/'E1-ficha.md'
    if not ficha.exists(): ficha.write_text('- [D · Celso do Vale] Ficha exclusivamente sintética para controle.\n')
    rascunho = caso/'rascunho'; rascunho.mkdir(exist_ok=True)
    entrada = rascunho/'prosseguimento.json'
    entrada.write_text(json.dumps(dict(versao=1,decisor=temporario['responsavel'],data='2026-10-03',
        desfecho='prosseguir',motivo='Decisão exclusivamente sintética de controle',ficha='caso/E1-ficha.md'),ensure_ascii=False))
    try:
        p.write_text(json.dumps(temporario))
        r = subprocess.run([sys.executable,str(RAIZ/'eiac-campo/scripts/prosseguimento.py'),
                            '--entrada','rascunho/prosseguimento.json'],cwd=caso,text=True,capture_output=True)
        if r.returncode: raise RuntimeError(r.stderr or r.stdout)
    finally:
        p.write_bytes(original)
