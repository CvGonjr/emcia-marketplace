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
import datetime, json, pathlib, subprocess, sys, tempfile
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

# Expediente e PDFs exclusivamente sintéticos; importação/validação/selo reais.
sys.path.insert(0, str(raiz / 'testes'))
from apoio.habilitacao_0d import criar as criar_expediente
with tempfile.TemporaryDirectory(prefix='emcia-habilitacao-demo-') as tmp_hab:
    exp = criar_expediente(pathlib.Path(tmp_hab)/'expediente', nome, pessoa)
    rodar([sys.executable, str(raiz/'eiac-campo/scripts/importar_habilitacao.py'), '--expediente', str(exp)], caso)
    rodar([sys.executable, str(raiz/'eiac-nucleo/scripts/validar.py'), '--arquivo', 'caso/00-habilitacao.md'], caso)
    rodar([sys.executable, str(raiz/'eiac-nucleo/scripts/selar.py'), '--nota', 'habilitação sintética importada e conferida'], caso)

def avancar(*args):
    return rodar([sys.executable, str(raiz / 'eiac-nucleo/scripts/avancar.py'), *args, '--autor', pessoa], caso)

def candidato(nome_arq, dados):
    # YAML simples também funciona sem PyYAML. Grava apenas rascunho;
    # registros passam pelos scripts de campo.
    (caso / 'rascunho').mkdir(exist_ok=True)
    def yaml(dado, indent=0):
        pad = ' '*indent
        if isinstance(dado, dict):
            linhas=[]
            for chave, valor in dado.items():
                if isinstance(valor, (dict, list)):
                    linhas.append(pad+chave+':')
                    linhas.append(yaml(valor, indent+2))
                else:
                    linhas.append(pad+chave+': '+json.dumps(valor, ensure_ascii=False))
            return '\n'.join(linhas)
        if isinstance(dado, list):
            return '\n'.join(pad+'-\n'+yaml(v,indent+2) if isinstance(v,dict)
                             else pad+'- '+json.dumps(v,ensure_ascii=False) for v in dado)
    (caso / 'rascunho' / nome_arq).write_text(yaml(dados)+'\n')

def campo(script, destino):
    rodar([sys.executable, str(raiz / 'eiac-campo/scripts' / script), '--arquivo', destino, '--ator', pessoa], caso)

hoje = datetime.date.today().isoformat()
op = dict(id='OP-001', estado='proposta', ponto_insercao='Fila sintética de pedidos', momento='Após recepção', sistema='Sistema de controle sintético', entrada='Pedido fictício', saida='Sugestão de encaminhamento', ator_humano=pessoa, excecao='Pedido sem referência', fallback='Revisão manual', responsavel_operacional=pessoa, procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
aut = dict(id='AUT-001', estado='rascunho', operacional_ref='OP-001', escopo='Controle sintético da demonstração', faz_sozinha=['Preparar sugestão'], exige_aprovacao=['Aplicar sugestão'], nunca_faz=['Alterar dados de cliente'], gatilhos_escalonamento=['Referência ausente'], procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
# Produtos e rascunhos de decisão são dados sintéticos da demonstração.
comum = dict(procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
bl = dict(comum, id='BL-001', indicador='Tempo de controle', valor_atual='10 minutos', apuracao='medido', nivel='N2')
ct = dict(comum, id='CT-001', estado='rascunho', modo='assistido', duracao='1 semana', plano_reversao='Retorno manual', criterio_aprovacao_escala='100% no caso de controle', criterio_aprovacao_escala_definido_em=hoje, casos=[dict(identificador='CT-001-01', origem='Controle sintético', entrada='Pedido fictício', saida_esperada='Encaminhar', criterio_aprovacao='Igual à saída esperada', categoria='celula_critica', revisor=pessoa, data_revisao=hoje, esperado_definido_em=hoje, esperado_definido_por=pessoa)])
met = dict(comum, id='MET-001', estado='planejada', piloto_ref='CT-001', baseline_ref='BL-001', metrica='Tempo de controle', tipo='resultado', linha_base='10 minutos', linha_base_data=hoje, linha_base_procedencia='D', metodo_apuracao='Diferença de horários', fonte_dado='Controle sintético', periodicidade='mensal', responsavel_apuracao=pessoa)
cal = dict(comum, id='CAL-001', metricas_ref=['MET-001'], responsavel='Marina Prado', responsavel_ciente=True, cadencia='mensal', data_primeira_revisao=(datetime.date.today()+datetime.timedelta(days=30)).isoformat(), limiares_desvio='Aumento de 15%', limiares_desvio_definidos_em=hoje, monitoramento='Controle sintético', canal_incidente='Terminal do engenheiro', analise_pos_incidente='Revisar causa com responsável')
prontos = []
def decisao_pronta(nome_arq, dados):
    dados.update(decisor=pessoa, data_decisao=hoje, justificativa_decisao='Revisão sintética para demonstração')
    candidato(nome_arq, dados)
    prontos.append(nome_arq)

avancar('--apurar-nivel', 'N2', '--eixos', 'DAD 5, GOV 3, CRI 6')
for et in pb['etapas']:
    eid = et['id']
    if eid == 'P3a':
        candidato('BL-001.yaml', bl)
        campo('baseline.py', 'registro/baseline/BL-001.yaml')
    if eid == 'P5':
        avancar('--registrar-campo', eid, '--campo', 'classificacao_tecnologica', '--valor', 'agente')
    if eid == 'P6':
        candidato('OP-001.yaml', op)
        campo('operacional.py', 'registro/operacional/OP-001.yaml')
        op.update(versao=2, validado_por=pessoa, data_validacao=hoje)
        decisao_pronta('OP-001.yaml', op)
        if ate != eid:
            op.update(estado='validado')
            candidato('OP-001.yaml', op)
            campo('operacional.py', 'registro/operacional/OP-001.yaml')
    if eid == 'P7':
        candidato('AUT-001.yaml', aut)
        campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
        aut.update(estado='proposto', versao=2)
        candidato('AUT-001.yaml', aut)
        campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
        aut.update(versao=3)
        decisao_pronta('AUT-001.yaml', aut)
        if ate != eid:
            aut.update(estado='decidido')
            candidato('AUT-001.yaml', aut)
            campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
    if eid == 'P8':
        candidato('CT-001.yaml', ct)
        campo('piloto.py', 'registro/piloto/CT-001.yaml')
        ct.update(versao=2, revisado_por=pessoa, data_revisao=hoje)
        decisao_pronta('CT-001.yaml', ct)
        if ate != eid:
            ct.update(estado='revisado')
            candidato('CT-001.yaml', ct)
            campo('piloto.py', 'registro/piloto/CT-001.yaml')
    if eid == 'P9':
        candidato('MET-001.yaml', met)
        campo('metrica.py', 'registro/metricas/MET-001.yaml')
        met.update(estado='apurada', versao=2, resultado_apurado='8 minutos', resultado_apurado_data=hoje, resultado_apurado_procedencia='D', fatores_externos_declarados='Nenhum: controle sintético')
        candidato('MET-001.yaml', met)
        campo('metrica.py', 'registro/metricas/MET-001.yaml')
    if eid == 'P10':
        candidato('CAL-001.yaml', cal)
        campo('calibragem.py', 'registro/calibragem/CAL-001.yaml')
        ciclo = dict(comum, id='CAL-001-C01', calibragem_ref='CAL-001', ciclo=1, data_verificacao=hoje, drift_detectado=True, drift_descricao='Aumento sintético de tempo', drift_quantificacao='20%', recomendacao_agente='Recalibrar o controle', declarado_por='AG-04', registrado_por='AG-04')
        candidato('CAL-001-C01.yaml', ciclo)
        rodar([sys.executable, str(raiz / 'eiac-campo/scripts/calibragem.py'), '--arquivo', 'registro/calibragem/CAL-001-C01.yaml', '--ciclo', '--ator', 'AG-04'], caso)
        ciclo.update(versao=2)
        decisao_pronta('CAL-001-C01.yaml', ciclo)
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
print('Rascunhos de decisão (anteriores já decididos no percurso pelo engenheiro):')
for nome_arq in prontos:
    print('  '+str(caso/'rascunho'/nome_arq))
if ate == 'P10':
    print('Ciclo sem decisão: preencher apenas decisao (recalibrar/expandir/descontinuar).')
else:
    print('Na etapa corrente, mudar apenas estado para validado/decidido/revisado conforme o rascunho.')
PY
