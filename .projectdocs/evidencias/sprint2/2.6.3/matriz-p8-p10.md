# Matriz P8/P9/P10 — pacote 2.6.3

Fonte primária: EMCIA-CAM-01 (Protocolo de Campo por Passo) §3.4/3.5/3.6 e
Anexos B/C/D; EMCIA-MET-01 §3.4.8-3.4.10; EMCIA-CAT-01 §3.4.5. Onde CAT-01
e CAM-01 divergem em granularidade (CAT-01 atribui natureza por
atividade; CAM-01 atribui uma camada EX única por passo), ambas as
fontes são citadas — não houve reconciliação silenciosa.

| Elemento | P8 | P9 | P10 |
|---|---|---|---|
| Objetivo | Estruturar o piloto e verificar a solução por casos de teste com saída esperada | Medir o valor gerado, comparado à linha de base | Instalar rotina recorrente de calibragem, monitorar desvio, decidir evolução |
| Entrada | P7 encerrado; termo de autonomia decidido; linha de base do passo 3 registrada | P8 encerrado; piloto executado; linha de base disponível | P9 encerrado; solução em operação ou piloto concluído |
| Saída | Conjunto de casos de teste com saída esperada (Anexo B), modo/duração acordados, plano de reversão escrito | Plano de medição preenchido (Anexo C), ao menos uma métrica de resultado apurada | Rotina de recalibragem instalada (Anexo D), responsável nomeado, cadência em calendário |
| Automação permitida | Derivar casos das regras curadas; executar suíte de avaliação; consolidar falhas (CAT-01 3.4.5: "Automatizado") | Coletar métricas e comparar com a linha de base (CAT-01 3.4.5: "Automatizado") | Monitorar desvio de desempenho e degradação de saída (CAT-01 3.4.5: "Automatizado") |
| Julgamento humano | Julgar se falha é aceitável ou impeditiva; aprovar passagem de sombra→assistido e a escala (CAT-01 3.4.5: "Humano") | Interpretar por que a métrica se moveu; apresentar ao patrocinador (CAT-01 3.4.5: "Humano" — "Atribuição de causa não está nos dados") | Diagnosticar causa da degradação; decidir recalibrar, expandir ou descontinuar (CAT-01 3.4.5 / CAM-01 3.6: "A decisão... é humana") |
| Camada EX | EX3 (CAM-01 3.4, header) | EX3 (CAM-01 3.5, header) | EX4 na decisão, EX2 no monitoramento (CAM-01 3.6, header — citação textual) |
| Dependências | `depende_de: P7` (playbook.json) | `depende_de: P8` (playbook.json) | `depende_de: P9`; `recorrente: true`, `cadencia_obrigatoria: true`, `responsavel_obrigatorio: true`, `delegavel: false` (playbook.json) |
| Evidência produzida | `registro/piloto/CT-NNN.yaml` (conjunto de casos, Anexo B) | `registro/metricas/MET-NNN.yaml` (plano de medição, Anexo C) | `registro/calibragem/CAL-NNN.yaml` (rotina, Anexo D) + `registro/calibragem/CAL-NNN-CNN.yaml` (ciclos) |
| Inegociável | 3 — "Conjunto de casos de teste com saída esperada" (MET-01 §3.6) | 4 — "Ao menos uma métrica de resultado, e não apenas de uso" (MET-01 §3.6) | 5 — "Um responsável nomeado pela recalibragem" (MET-01 §3.6) |
| Relação com E5 | Insumo estrutural — não valida semanticamente o inegociável 3 neste pacote (2.6.5) | Insumo estrutural — não valida semanticamente o inegociável 4 neste pacote (2.6.5) | Insumo estrutural — não valida semanticamente o inegociável 5 neste pacote (2.6.5) |

## Nota sobre granularidade EX (divergência registrada, não reconciliada)

CAT-01 §3.4.5 atribui natureza (Automatizado/Híbrido/Humano) por
atividade individual dentro de cada passo, nunca uma única camada EX por
passo. CAM-01 §3.2-3.6 atribui uma única camada EX no cabeçalho de cada
passo (ex.: P10 = "EX4 na decisão, EX2 no monitoramento"). São
compatíveis — o rótulo único de CAM-01 resume a tabela por atividade de
CAT-01 — mas são duas fontes com granularidade diferente. O playbook e
as skills deste pacote seguem CAM-01 (fonte executável), citando CAT-01
para a justificativa da fronteira agente×humano.

## Matriz agente × humano

| Operação | Agente pode executar? | Humano requerido? |
|---|---|---|
| Criar caso de teste (Anexo B) | Sim — derivar da regra curada, escrever saída esperada, estruturar rascunho | Sim, para `estado: revisado` — revisão de quem executa o processo é condição de validade (CAM-01 3.4), não etapa opcional |
| Definir saída esperada | Sim — mas antes de qualquer execução (`esperado_definido_em`/`esperado_definido_por`, congelamento contra viés retrospectivo) | Não obrigatoriamente, mas a revisão do conjunto (acima) é |
| Comparar saída esperada × obtida | Sim — comparação determinística, calculada, nunca escrita por decisão manual (`piloto.py::checar_casos`) | Não — mas humano pode revisar o conjunto revisado |
| Calcular métrica | Sim — apuração determinística, documentada (CAT-01 3.4.5: "Automatizado") | Não |
| Interpretar por que a métrica se moveu / declarar causa | Não | Sim — CAT-01 3.4.5: "Atribuição de causa não está nos dados" |
| Detectar drift | Sim — descrever, quantificar, recomendar (`calibragem.py::checar_drift`) | Não, para detecção |
| Decidir recalibragem (recalibrar/expandir/descontinuar) | **Não — bloqueado estruturalmente** (`calibragem.py::checar_decisao`, evento `CicloCalibragemRecusado`) | Sim, sempre — CAM-01 3.6: "A decisão de recalibrar, expandir ou descontinuar é humana" |
| Decidir expansão | Não | Sim (mesma decisão de recalibragem — não há decisão de expansão separada nos documentos) |

Nota sobre vocabulário de decisão: os documentos nomeiam exatamente três
opções — `recalibrar`, `expandir`, `descontinuar` (CAT-01 3.4.5, CAM-01
3.6, ESP-01 3.5, texto idêntico nas três fontes). Não existe `manter`,
`restringir` ou `suspender` como opção nomeada; um ciclo sem drift é o
caminho positivo que corresponde a "manter" implicitamente (T27), e o
schema recusa qualquer valor de `decisao` fora do enum de três opções
(T32), para não inventar uma quarta opção não documentada.
