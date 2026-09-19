---
description: Executa a etapa P7 do playbook Engenharia de IA de Campo.
---
Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P7**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-governar` e siga o procedimento do passo no documento do método, em `metodo/`.

**A decisão de autonomia não é executável por agente.** Se você é um agente, prepare a minuta (`estado: rascunho`/`proposto`) e pare — não tente gravar `estado: decidido`.

Escreva o candidato em `rascunho/AUT-NNN.yaml`, referenciando `operacional_ref` (o `OP-*` de P6 já validado), e grave com:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/governanca.py" --arquivo registro/governanca/autonomia/AUT-NNN.yaml --ator "<nome>"`

`estado: decidido` exige ator humano nomeado, com `decisor`, `data_decisao` e `justificativa_decisao` preenchidos.
