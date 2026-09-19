---
description: Executa a etapa P3a do playbook Engenharia de IA de Campo.
---
Confirme com `/eiac-nucleo:estado` que a etapa corrente é **P3a**. Se não for, pare e diga qual é.

Carregue a habilidade `hb-medir` e siga o procedimento do passo no documento do método, em `metodo/`.

A narrativa vai para `rascunho/`, com toda asserção marcada. Grave com `/eiac-nucleo:gravar`.

A evidência estruturada da linha de base (item inegociável 1) vai em `rascunho/BL-NNN.yaml`, gravada com:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/baseline.py" --arquivo registro/baseline/BL-NNN.yaml --ator "<nome>"`
