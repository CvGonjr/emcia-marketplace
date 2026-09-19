---
description: Executa a etapa P9 do playbook Engenharia de IA de Campo.
---
Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P9**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-medir-valor` e siga o procedimento do passo no documento do método, em `metodo/`.

Escreva o candidato em `rascunho/MET-NNN.yaml`, referenciando `piloto_ref` (o `CT-*` de P8 já revisado), e grave com:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/metrica.py" --arquivo registro/metricas/MET-NNN.yaml --ator "<nome>"`

Ao menos uma métrica do plano precisa ter `tipo: resultado` — métrica de uso não satisfaz sozinha o item inegociável 4.
