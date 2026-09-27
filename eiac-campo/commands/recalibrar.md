---
description: Executa a etapa P10 do playbook Engenharia de IA de Campo.
---

**Fluxo A12:** o agente grava apenas preparação. Para validação/decisão,
prepare os argumentos e entregue o comando pronto ao engenheiro. Ele
executa no próprio terminal, fora do Claude Code, no diretório do caso.
Não execute a decisão por Bash, mesmo usando nome humano. Resolva o
caminho do plugin para entregar um comando com caminho absoluto real.

Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P10**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-recalibrar` e siga o procedimento do passo no documento do método, em `metodo/`.

**A decisão de recalibrar, expandir ou descontinuar não é executável por agente.** Se você é um agente, prepare a rotina e o ciclo (detecção, quantificação, recomendação) e pare — não tente gravar o campo `decisao`.

Rotina, referenciando `metricas_ref` (os `MET-*` de P9):

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/calibragem.py" --arquivo registro/calibragem/CAL-NNN.yaml --ator "<nome>"`

Ciclo:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/calibragem.py" --arquivo registro/calibragem/CAL-NNN-C01.yaml --ator "<nome>" --ciclo`

`decisao` exige ator humano nomeado, com `decisor`, `data_decisao` e `justificativa_decisao` preenchidos.

A recorrência também é executada pelo engenheiro no próprio terminal.
Entregue o comando pronto do mecanismo genérico do núcleo: `python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-nucleo/scripts/avancar.py" --registrar-recorrencia P10 --autor "<nome>" --cadencia "<cadência>" --responsavel "<nome>"`

### Definição da rotina (A15)

A rotina com responsável e cadência é decisão humana. O agente prepara
CAL-NNN.yaml e entrega o comando de gravação ao engenheiro para executar
no próprio terminal, fora da sessão. A guarda recusa essa gravação mesmo
com nome humano informado. O agente pode registrar ciclo de drift e
recomendação sem decisão; a decisão do ciclo também pertence ao engenheiro.
Responsável e decisor precisam de nome e sobrenome, sem termos coletivos.
