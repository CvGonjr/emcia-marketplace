---
description: Executa a etapa P8 do playbook Engenharia de IA de Campo.
---
Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P8**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-pilotar` e siga o procedimento do passo no documento do método, em `metodo/`.

Escreva o candidato em `rascunho/CT-NNN.yaml` e grave com:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/piloto.py" --arquivo registro/piloto/CT-NNN.yaml --ator "<nome>"`

`estado: rascunho` pode ser gravado por qualquer ator. `estado: revisado` exige `revisado_por` humano nomeado — o script recusa a autorrevisão de um agente.
