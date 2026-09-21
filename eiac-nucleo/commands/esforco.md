---
description: Registra o esforço observado do engenheiro em uma etapa, com camada lida do playbook.
argument-hint: <etapa> <duração em segundos>
---
Informe a etapa e a duração observada do trabalho do engenheiro. A camada
EX1–EX4 não é digitada: o script a resolve do playbook conforme o nível do caso.

Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/esforco.py" --registrar "<etapa>" --duracao-segundos "<segundos>" --autor "<nome da pessoa>"`

Se o script recusar, apresente o motivo sem contorná-lo.
