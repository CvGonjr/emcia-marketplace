#!/usr/bin/env bash
# Demonstração sintética da ação 3.8, pela tag v-sprint3-poc.7.
# Executar pelo engenheiro no próprio terminal; inclui decisões humanas
# fictícias de controle. Não é um roteiro para aplicar decisões a clientes.
# Conta invocações diretas: não soma subprocessos internos dos plugins,
# nem as consultas Git internas de resumo-percurso.py.
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo 'uso: percurso-completo.sh <nome>' >&2
  exit 1
fi
raiz_demo="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
base_demo="${EMCIA_DEMO_BASE:-/tmp/emcia-demos}"
python3 - "$raiz_demo" "$base_demo" "$1" <<'PY_DEMO'
import collections, datetime, json, pathlib, shlex, subprocess, sys, tempfile

raiz = pathlib.Path(sys.argv[1])
base = pathlib.Path(sys.argv[2]).expanduser().resolve()
nome = sys.argv[3]
pessoa = 'Celso do Vale'
tag = 'v-sprint3-poc.7'
caso = base / nome
contagens = collections.Counter()

class FalhaComando(Exception):
    def __init__(self, comando, codigo):
        self.comando, self.codigo = comando, codigo


def rodar(comando, cwd=None, categoria='percurso'):
    contagens[categoria] += 1
    numero = sum(contagens.values())
    print(f"[{numero:02d} · {categoria}] $ {shlex.join(str(p) for p in comando)}", flush=True)
    try:
        r = subprocess.run(comando, cwd=cwd or raiz, text=True, capture_output=True)
    except OSError as exc:
        print(str(exc), file=sys.stderr, flush=True)
        raise FalhaComando(comando, 1) from exc
    if r.stdout:
        print(r.stdout.rstrip(), flush=True)
    if r.stderr:
        print(r.stderr.rstrip(), file=sys.stderr, flush=True)
    if r.returncode:
        print('PARADO no primeiro erro; comando: '+shlex.join(str(p) for p in comando),
              file=sys.stderr, flush=True)
        raise FalhaComando(comando, r.returncode)
    return r.stdout.strip()


def candidato(nome_arq, dados):
    # Somente rascunho; todo produto durável passa pelo script de campo.
    (caso/'rascunho').mkdir(exist_ok=True)
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
    (caso/'rascunho'/nome_arq).write_text(yaml(dados)+'\n', encoding='utf-8')


hoje = datetime.date.today().isoformat()
op = dict(id='OP-001', estado='proposta', ponto_insercao='Fila sintética de pedidos', momento='Após recepção', sistema='Sistema de controle sintético', entrada='Pedido fictício', saida='Sugestão de encaminhamento', ator_humano=pessoa, excecao='Pedido sem referência', fallback='Revisão manual', responsavel_operacional=pessoa, procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
aut = dict(id='AUT-001', estado='rascunho', operacional_ref='OP-001', escopo='Controle sintético da demonstração', faz_sozinha=['Preparar sugestão'], exige_aprovacao=['Aplicar sugestão'], nunca_faz=['Alterar dados de cliente'], gatilhos_escalonamento=['Referência ausente'], procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
# Produtos e rascunhos de decisão são dados sintéticos da demonstração.
comum = dict(procedencia='D', declarado_por=pessoa, registrado_por=pessoa, data=hoje, versao=1)
bl = dict(comum, id='BL-001', indicador='Tempo de controle', valor_atual='10 minutos', apuracao='medido', nivel='N2')
ct = dict(comum, id='CT-001', estado='rascunho', modo='assistido', duracao='1 semana', plano_reversao='Retorno manual', criterio_aprovacao_escala='100% no caso de controle', criterio_aprovacao_escala_definido_em=hoje, casos=[dict(identificador='CT-001-01', origem='Controle sintético', entrada='Pedido fictício', saida_esperada='Encaminhar', criterio_aprovacao='Igual à saída esperada', categoria='celula_critica', revisor=pessoa, data_revisao=hoje, esperado_definido_em=hoje, esperado_definido_por=pessoa)])
met = dict(comum, id='MET-001', estado='planejada', piloto_ref='CT-001', baseline_ref='BL-001', metrica='Tempo de controle', tipo='resultado', linha_base='10 minutos', linha_base_data=hoje, linha_base_procedencia='D', metodo_apuracao='Diferença de horários', fonte_dado='Controle sintético', periodicidade='mensal', responsavel_apuracao=pessoa)
cal = dict(comum, id='CAL-001', metricas_ref=['MET-001'], responsavel='Marina Prado', responsavel_ciente=True, cadencia='mensal', data_primeira_revisao=(datetime.date.today()+datetime.timedelta(days=30)).isoformat(), limiares_desvio='Aumento de 15%', limiares_desvio_definidos_em=hoje, monitoramento='Controle sintético', canal_incidente='Terminal do engenheiro', analise_pos_incidente='Revisar causa com responsável')

def executar(fonte):
    nucleo = fonte/'eiac-nucleo/scripts'
    campo_scripts = fonte/'eiac-campo/scripts'
    # Cada processo usa os componentes congelados, inclusive os filhos de
    # entregaveis.py/inegociaveis.py. Nenhuma flag desliga uma guarda.
    import os
    os.environ['EIAC_NUCLEO_SCRIPTS'] = str(nucleo)
    rodar(['bash', str(fonte/'novo-caso.sh'), nome, '--responsavel', pessoa, str(base)])
    for chave, valor in [('user.name', pessoa), ('user.email', 'controle@exemplo.com')]:
        rodar(['git', 'config', chave, valor], caso)
    pb = json.loads((caso/'registro/playbook.json').read_text())

    def avancar(*args):
        rodar([sys.executable, str(nucleo/'avancar.py'), *args, '--autor', pessoa], caso)
    def campo(script, destino, *args, ator=pessoa):
        rodar([sys.executable, str(campo_scripts/script), '--arquivo', destino,
               '--ator', ator, *args], caso)
    def satisfazer(n, artefato):
        rodar([sys.executable, str(campo_scripts/'inegociaveis.py'), '--verificar', str(n),
               '--arquivo', artefato, '--satisfazer', '--autor', pessoa], caso)
    def emitir(entregavel):
        rodar([sys.executable, str(campo_scripts/'entregaveis.py'), '--renderizar', entregavel,
               '--emitir', '--autor', pessoa], caso)
    def selar(nota):
        rodar([sys.executable, str(nucleo/'selar.py'), '--autor', pessoa, '--nota', nota], caso)
    def decisao(dados):
        dados.update(decisor=pessoa, data_decisao=hoje,
                     justificativa_decisao='Revisão sintética para demonstração')

    avancar('--apurar-nivel', 'N2', '--eixos', 'DAD 5, GOV 3, CRI 6')
    fases = {'F0': ('F0','E1'), 'P3d': ('F1','E2'), 'P5': ('F2','E3'),
             'P7': ('F3','E4'), 'P10': ('F4','E5')}
    for etapa in pb['etapas']:
        eid = etapa['id']
        if eid == 'P3a':
            candidato('BL-001.yaml', bl)
            campo('baseline.py', 'registro/baseline/BL-001.yaml')
            satisfazer(1, 'registro/baseline/BL-001.yaml')
        elif eid == 'P5':
            avancar('--registrar-campo', eid, '--campo', 'classificacao_tecnologica', '--valor', 'agente')
        elif eid == 'P6':
            candidato('OP-001.yaml', op)
            campo('operacional.py', 'registro/operacional/OP-001.yaml')
            op.update(estado='validado', versao=2, validado_por=pessoa, data_validacao=hoje)
            decisao(op)
            candidato('OP-001.yaml', op)
            campo('operacional.py', 'registro/operacional/OP-001.yaml')
        elif eid == 'P7':
            candidato('AUT-001.yaml', aut)
            campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
            aut.update(estado='proposto', versao=2)
            candidato('AUT-001.yaml', aut)
            campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
            aut.update(estado='decidido', versao=3)
            decisao(aut)
            candidato('AUT-001.yaml', aut)
            campo('governanca.py', 'registro/governanca/autonomia/AUT-001.yaml')
            satisfazer(2, 'registro/governanca/autonomia/AUT-001.yaml')
        elif eid == 'P8':
            candidato('CT-001.yaml', ct)
            campo('piloto.py', 'registro/piloto/CT-001.yaml')
            ct.update(estado='revisado', versao=2, revisado_por=pessoa, data_revisao=hoje)
            decisao(ct)
            candidato('CT-001.yaml', ct)
            campo('piloto.py', 'registro/piloto/CT-001.yaml')
            satisfazer(3, 'registro/piloto/CT-001.yaml')
        elif eid == 'P9':
            candidato('MET-001.yaml', met)
            campo('metrica.py', 'registro/metricas/MET-001.yaml')
            met.update(estado='apurada', versao=2, resultado_apurado='8 minutos',
                       resultado_apurado_data=hoje, resultado_apurado_procedencia='D',
                       fatores_externos_declarados='Nenhum: controle sintético')
            candidato('MET-001.yaml', met)
            campo('metrica.py', 'registro/metricas/MET-001.yaml')
            satisfazer(4, 'registro/metricas/MET-001.yaml')
        elif eid == 'P10':
            candidato('CAL-001.yaml', cal)
            campo('calibragem.py', 'registro/calibragem/CAL-001.yaml')
            ciclo = dict(comum, id='CAL-001-C01', calibragem_ref='CAL-001', ciclo=1,
                         data_verificacao=hoje, drift_detectado=True,
                         drift_descricao='Aumento sintético de tempo', drift_quantificacao='20%',
                         recomendacao_agente='Recalibrar o controle',
                         declarado_por='AG-04', registrado_por='AG-04')
            candidato('CAL-001-C01.yaml', ciclo)
            campo('calibragem.py', 'registro/calibragem/CAL-001-C01.yaml', '--ciclo', ator='AG-04')
            ciclo.update(versao=2, decisao='recalibrar')
            decisao(ciclo)
            candidato('CAL-001-C01.yaml', ciclo)
            campo('calibragem.py', 'registro/calibragem/CAL-001-C01.yaml', '--ciclo')
            satisfazer(5, 'registro/calibragem/CAL-001.yaml')
        if pb['encerramento_por_camada'][etapa['camada']['N2']] or etapa.get('delegavel') is False:
            avancar('--registrar-sessao', eid, '--participantes', pessoa+', Pessoa Cliente (controle sintético)')
        avancar('--encerrar', eid)
        if any(e.get('exige_selo_apos') == eid for e in pb['etapas']):
            selar('estado declarado depois de '+eid)
        if eid == 'P10':
            avancar('--registrar-recorrencia', eid, '--responsavel', 'Marina Prado', '--cadencia', 'mensal')
        if eid in fases:
            fase, entregavel = fases[eid]
            emitir(entregavel)
            selar('fim da fase '+fase)
    rodar([sys.executable, str(raiz/'.projectdocs/demos/resumo-percurso.py'), str(caso)],
           categoria='resumo')


def main():
    if not nome or '/' in nome or nome.startswith('.'):
        sys.exit('nome inválido: use apenas o nome do caso, sem barras')
    if caso.exists() or caso.is_symlink():
        sys.exit('o destino já existe: '+str(caso))
    codigo = 0
    # Cópia de trabalho separada: o estado local do repositório não muda.
    with tempfile.TemporaryDirectory(prefix='emcia-percurso-v7-') as temporario:
        fonte = pathlib.Path(temporario)/'fonte'
        criada = False
        try:
            commit = rodar(['git','rev-parse','--verify',tag+'^{commit}'], categoria='infraestrutura')
            print('Versão congelada: '+tag+' / '+commit, flush=True)
            rodar(['git','worktree','add','--detach',str(fonte),tag], categoria='infraestrutura')
            criada = True
            executar(fonte)
        except FalhaComando as exc:
            codigo = exc.codigo
        finally:
            # Após uma falha, só remove a fonte temporária criada aqui;
            # não repete comandos nem continua qualquer etapa do caso.
            if criada:
                try:
                    rodar(['git','worktree','remove',str(fonte)], categoria='infraestrutura')
                except FalhaComando as exc:
                    if not codigo:
                        codigo = exc.codigo
            print(f"Comandos do percurso: {contagens['percurso']}; "
                  f"infraestrutura: {contagens['infraestrutura']}; resumo: {contagens['resumo']}; "
                  f"total de invocações diretas: {sum(contagens.values())}", flush=True)
            print('Contagem inclui a tentativa que falhou, se houver; não inclui subprocessos internos.', flush=True)
    return codigo

sys.exit(main())
PY_DEMO
