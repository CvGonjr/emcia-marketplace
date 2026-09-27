---
description: Executa a etapa P6 do playbook Engenharia de IA de Campo.
---

**Fluxo A12:** o agente grava apenas preparação. Para validação/decisão,
prepare os argumentos e entregue o comando pronto ao engenheiro. Ele
executa no próprio terminal, fora do Claude Code, no diretório do caso.
Não execute a decisão por Bash, mesmo usando nome humano. Resolva o
caminho do plugin para entregar um comando com caminho absoluto real.

Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P6**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-operacionalizar` e siga o procedimento do passo no documento do método, em `metodo/`.

Escreva o candidato em `rascunho/OP-NNN.yaml` e grave com:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/operacional.py" --arquivo registro/operacional/OP-NNN.yaml --ator "<nome>"`

`estado: proposta` continua permitido à sessão. Com `estado: validado`,
a guarda recusa a chamada mesmo com nome humano: entregue o comando ao
engenheiro para execução no próprio terminal.
