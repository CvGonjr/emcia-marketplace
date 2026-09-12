---
description: Registra uma sessão de campo presencial, liberando as etapas que dependem dela.
argument-hint: <etapa> <participantes>
---
Pergunte ao operador, se não vierem nos argumentos: etapa, participantes e instrumentos aplicados.

Depois execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --registrar-sessao <etapa> --autor "<nome da pessoa>" --participantes "<lista>"`

O autor é sempre pessoa nomeada. Nunca preencha com identificador de agente.
