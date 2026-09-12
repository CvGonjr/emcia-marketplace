---
description: Encerra a etapa corrente, se o critério de encerramento estiver cumprido.
argument-hint: <etapa>
---
Antes de executar, releia o critério de encerramento da etapa no documento do método e confirme com o operador que ele foi cumprido.

Depois execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --encerrar <etapa> --autor "<nome da pessoa>"`

Se o script recusar, apresente o motivo sem contorná-lo.
