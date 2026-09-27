#!/usr/bin/env bash
# Caso sintético para demonstração; executar pelo engenheiro no terminal.
# "até etapa" significa deixá-la corrente, ainda aberta.
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo 'uso: preparar-caso.sh <nome> <ate-etapa>' >&2
  exit 1
fi
raiz_demo="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
base_demo="${EMCIA_DEMO_BASE:-/tmp/emcia-demos}"
python3 - "$raiz_demo" "$base_demo" "$1" "$2" <<'PY'
import datetime, json, pathlib, subprocess, sys
raiz, base, nome, ate = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).expanduser().resolve(), sys.argv[3], sys.argv[4]
pb = json.loads((raiz / 'eiac-campo/template-caso/registro/playbook.json').read_text())
if ate not in [e['id'] for e in pb['etapas']]:
    sys.exit('etapa não declarada: '+ate)
caso = base / nome
pessoa = 'Celso do Vale'

def rodar(comando, cwd=None):
    r = subprocess.run(comando, cwd=cwd, text=True, capture_output=True)
    if r.returncode:
        sys.exit(r.stderr.strip() or r.stdout.strip())
    return r.stdout

rodar(['bash', str(raiz / 'novo-caso.sh'), nome, '--responsavel', pessoa, str(base)])
for chave, valor in [('user.name', pessoa), ('user.email', 'controle@exemplo.com')]:
    rodar(['git', 'config', chave, valor], caso)

def avancar(*args):
    return rodar([sys.executable, str(raiz / 'eiac-nucleo/scripts/avancar.py'), *args, '--autor', pessoa], caso)

def candidato(nome_arq, dados):
    # YAML simples também funciona sem PyYAML. Grava apenas rascunho;
    # registros passam pelos scripts de campo.
    (caso / 'rascunho').mkdir(exist_ok=True)
    (caso / 'rascunho' / nome_arq).write_text('\n'.join(
        chave+': '+json.dumps(valor, ensure_ascii=False) for chave, valor in dados.items())+'\n')

def campo(script, destino):
    rodar([sys.executable, str(raiz / 'eiac-campo/scripts' / script), '--arquivo', destino, '--ator', pessoa], caso)

hoje = datetime.date.today().isoformat()
op = dict(id='OP-001', estado='proposta', ponto_insercao='Fila sintética de pedidos', momento='Após recepção', sistema='Sistema de controle sintético', entrada='Pedido fictício', saida='Sugestão de encaminhamento', ator_humano=pessoa, excecao='Pedido sem referência', fallback='Revisão manual', responsavel_operacional=pessoa, procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
aut = dict(id='AUT-001', estado='rascunho', operacional_ref='OP-001', escopo='Controle sintético da demonstração', faz_sozinha=['Preparar sugestão'], exige_aprovacao=['Aplicar sugestão'], nunca_faz=['Alterar dados de cliente'], gatilhos_escalonamento=['Referência ausente'], procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
avancar('--apurar-nivel', 'N2', '--eixos', 'DAD 5, GOV 3, CRI 6')
for et in pb['etapas']:
    eid = et['id']
    if eid == 'P5':
        avancar('--registrar-campo', eid, '--campo', 'classificacao_tecnologica', '--valor', 'agente')
    if eid == 'P6':
        candidato('OP-001.yaml', op)
        campo('operacional.py', 'registro/operacional/OP-001.yaml')
        if ate != eid:
            op.update(estado='validado', versao=2, validado_por=pessoa, data_validacao=hoje)
            candidato('OP-001.yaml', op)
            campo('operacional.py', 'registro/operacional/OP-001.yaml')
    if eid == 'P7':
        candidato('AUT-001.yaml', aut)
        campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
        aut.update(estado='proposto', versao=2)
        candidato('AUT-001.yaml', aut)
        campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
    if pb['encerramento_por_camada'][et['camada']['N2']] or et.get('delegavel') is False:
        avancar('--registrar-sessao', eid, '--participantes', pessoa+', Pessoa Cliente (controle sintético)')
    if eid == ate:
        break
    avancar('--encerrar', eid)
    if any(e.get('exige_selo_apos') == eid for e in pb['etapas']):
        rodar([sys.executable, str(raiz / 'eiac-nucleo/scripts/selar.py'), '--autor', pessoa, '--nota', 'controle sintético: selo de '+eid], caso)
st = json.loads((caso / 'registro/estado.json').read_text())
print('Caso de controle: '+str(caso))
print('Etapa final: '+st['etapa_atual']+' | nível: '+st['nivel'])
PY
