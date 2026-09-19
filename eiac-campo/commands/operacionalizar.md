---
description: Executa a etapa P6 do playbook Engenharia de IA de Campo.
---
Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P6**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-operacionalizar` e siga o procedimento do passo no documento do método, em `metodo/`.

Escreva o candidato em `rascunho/OP-NNN.yaml` e grave com:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/operacional.py" --arquivo registro/operacional/OP-NNN.yaml --ator "<nome>"`

`estado: proposta` pode ser gravado por qualquer ator. `estado: validado` exige pessoa humana nomeada — o script recusa qualquer tentativa de um agente validar sua própria proposta.
