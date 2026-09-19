---
description: Registra um novo ciclo de uma etapa recorrente, com cadência e responsável.
argument-hint: <etapa> <cadência> <responsável>
---
Só se aplica a etapas que o playbook marca `recorrente: true`, e só depois que a etapa foi encerrada ao menos uma vez.

Pergunte ao operador, se não vierem nos argumentos: etapa, cadência (conforme o nível) e responsável nomeado.

Depois execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --registrar-recorrencia <etapa> --autor "<nome da pessoa>" --cadencia "<cadência>" --responsavel "<nome da pessoa>"`

O responsável precisa ser pessoa nomeada — "equipe" ou "área" não satisfaz `responsavel_obrigatorio`. Se o script recusar, apresente o motivo sem contorná-lo.
