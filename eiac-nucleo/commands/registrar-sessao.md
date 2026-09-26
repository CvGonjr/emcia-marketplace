---
description: Registra a sessão humana da etapa corrente, na modalidade declarada no caso.
argument-hint: <etapa> <participantes>
---
Pergunte ao operador, se não vierem nos argumentos: etapa, participantes e instrumentos aplicados.

Confirme com `/eiac-nucleo:estado` que a etapa é a corrente e ainda não
foi encerrada. Não registre sessão antecipada para uma etapa futura nem
retroativa para etapa já encerrada. A recusa fica na trilha como
`TentativaNegada`. A sessão só satisfaz a exigência da própria etapa.

Depois execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --registrar-sessao <etapa> --autor "<nome da pessoa>" --participantes "<lista>"`

O autor é sempre pessoa nomeada. Nunca preencha com identificador de agente.
