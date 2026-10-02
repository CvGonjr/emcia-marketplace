"""Declarações exclusivamente sintéticas, gravadas pelo comando humano real."""
import datetime
import json
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = RAIZ/'eiac-campo/scripts/canais.py'


def dados(caso):
    st = json.loads((pathlib.Path(caso)/'registro/estado.json').read_text())
    pb = json.loads((pathlib.Path(caso)/'registro/playbook.json').read_text())
    canais = []
    for req in pb.get('canais_previstos', []):
        ferramenta = req['ferramenta']
        campos = {'tally': ['workspace_id', 'formulario_id'],
                  'drive': ['drive_id', 'pasta_id'], 'calendar': ['calendario_id']}[ferramenta]
        canal = dict(req, proprietario='emcia', acesso_cliente='nenhum', sensivel=True,
                     ids={k: 'SINTETICO-'+req['finalidade']+'-'+k for k in campos},
                     filtro={'campo': 'caso', 'valor': st['caso']} if ferramenta == 'tally' else None,
                     marcador='[{caso}/{etapa}]' if ferramenta == 'calendar' else None)
        canais.append(canal)
    return dict(versao=1, caso=st['caso'], decidido_por=st['responsavel'],
                data=datetime.date.today().isoformat(), canais=canais)


def definir(caso):
    caso = pathlib.Path(caso)
    if (caso/'registro/canais.json').exists():
        return
    p = caso/'rascunho/canais-sinteticos.json'
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(dados(caso), ensure_ascii=False))
    r = subprocess.run([sys.executable, str(SCRIPT), 'definir', '--entrada', str(p)],
                       cwd=caso, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr)

