---
description: Executa a etapa P10 do playbook Engenharia de IA de Campo.
---
Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P10**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-recalibrar` e siga o procedimento do passo no documento do método, em `metodo/`.

**A decisão de recalibrar, expandir ou descontinuar não é executável por agente.** Se você é um agente, prepare a rotina e o ciclo (detecção, quantificação, recomendação) e pare — não tente gravar o campo `decisao`.

Rotina, referenciando `metricas_ref` (os `MET-*` de P9):

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/calibragem.py" --arquivo registro/calibragem/CAL-NNN.yaml --ator "<nome>"`

Ciclo:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/calibragem.py" --arquivo registro/calibragem/CAL-NNN-C01.yaml --ator "<nome>" --ciclo`

`decisao` exige ator humano nomeado, com `decisor`, `data_decisao` e `justificativa_decisao` preenchidos.

A recorrência (cadência, responsável, histórico) usa o mecanismo genérico do núcleo: `python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-nucleo/scripts/avancar.py" --registrar-recorrencia P10 --autor "<nome>" --cadencia "<cadência>" --responsavel "<nome>"`
