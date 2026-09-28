"""Produtos sintéticos para a preparação dos testes anteriores ao A14.

Chamado explicitamente apenas nos percursos/precondições; nunca no wrapper
que executa o encerramento testado. Estado é alterado somente por comando.
"""
import json, pathlib, subprocess
RAIZ=pathlib.Path(__file__).resolve().parents[2]
PESSOA='Celso do Vale'

def produto(caso, etapa, responsavel=None):
    caso=pathlib.Path(caso)
    st=json.loads((caso/'registro/estado.json').read_text())
    if etapa=='P5':
        if st.get('cumprimentos',{}).get(etapa,{}).get('classificacao_tecnologica'): return
        r=subprocess.run(['python3',str(RAIZ/'eiac-nucleo/scripts/avancar.py'),'--registrar-campo',etapa,'--campo','classificacao_tecnologica','--valor','agente','--autor',PESSOA],cwd=caso,text=True,capture_output=True)
        if r.returncode: raise RuntimeError(r.stderr)
        return
    dados={
      'P3a':('registro/baseline/BL-999.yaml',dict(id='BL-999',indicador='tempo de controle',valor_atual='10 minutos',apuracao='medido',nivel=st.get('nivel') or 'N2',data='2026-08-01')),
      'P6':('registro/operacional/OP-999.yaml',dict(id='OP-999',estado='validado',ponto_insercao='controle',momento='entrada',sistema='controle',entrada='pedido',saida='sugestao',ator_humano=PESSOA,excecao='erro',fallback='manual',responsavel_operacional=PESSOA,validado_por=PESSOA,data_validacao='2026-09-19',data='2026-09-19')),
      'P7':('registro/governanca/autonomia/AUT-999.yaml',dict(id='AUT-999',estado='decidido',operacional_ref='OP-999',escopo='controle',faz_sozinha=['preparar'],exige_aprovacao=['aplicar'],nunca_faz=['alterar'],gatilhos_escalonamento=['erro'],decisor=PESSOA,data_decisao='2026-09-19',justificativa_decisao='controle sintetico',data='2026-09-19')),
      'P8':('registro/piloto/CT-999.yaml',dict(id='CT-999',estado='revisado',modo='assistido',duracao='1 semana',plano_reversao='manual',criterio_aprovacao_escala='100%',criterio_aprovacao_escala_definido_em='2026-09-01',revisado_por=PESSOA,data_revisao='2026-09-19',casos=[dict(identificador='CT-999-01',origem='controle',entrada='pedido',saida_esperada='ok',criterio_aprovacao='igual',categoria='celula_critica',revisor=PESSOA,data_revisao='2026-09-19',esperado_definido_em='2026-09-01',esperado_definido_por=PESSOA)],data='2026-09-19')),
      'P9':('registro/metricas/MET-999.yaml',dict(id='MET-999',estado='apurada',tipo='resultado',piloto_ref='CT-999',metrica='tempo',linha_base='10',linha_base_data='2026-08-01',linha_base_procedencia='D',metodo_apuracao='calculo',fonte_dado='controle',periodicidade='mensal',responsavel_apuracao=PESSOA,resultado_apurado='8',resultado_apurado_data='2026-09-20',resultado_apurado_procedencia='D',fatores_externos_declarados='nenhum',data='2026-09-20')),
      'P10':('registro/calibragem/CAL-999.yaml',dict(id='CAL-999',metricas_ref=['MET-999'],responsavel=PESSOA,responsavel_ciente=True,cadencia='mensal',data_primeira_revisao='2026-10-19',limiares_desvio='15%',monitoramento='controle',canal_incidente='controle',analise_pos_incidente='revisao',data='2026-09-19')),
    }
    if etapa not in dados: return
    destino,d=dados[etapa]; p=caso/destino; p.parent.mkdir(parents=True,exist_ok=True)
    if etapa == 'P10' and responsavel is not None:
        d['responsavel'] = responsavel
    d.update(procedencia='D',declarado_por=PESSOA,registrado_por=PESSOA,versao=1)
    p.write_text('\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in d.items())+'\n')
