---
description: Registra a sessão humana da etapa corrente, na modalidade declarada no caso.
argument-hint: <etapa> <participantes>
---

**Decisão humana fora da sessão (A12).** O agente prepara os argumentos e
entrega o comando pronto ao engenheiro. Não o execute por Bash na sessão,
mesmo usando nome humano. O engenheiro executa no próprio terminal, fora
do Claude Code, no diretório do caso. Resolva o caminho do plugin antes de
entregar: use o caminho absoluto real, sem variável de sessão no comando.

Pergunte ao operador, se não vierem nos argumentos: etapa, participantes e instrumentos aplicados.

Confirme com `/eiac-nucleo:estado` que a etapa é a corrente e ainda não
foi encerrada. Não registre sessão antecipada para uma etapa futura nem
retroativa para etapa já encerrada. A recusa fica na trilha como
`TentativaNegada`. A sessão só satisfaz a exigência da própria etapa.

Prepare e entregue ao engenheiro este comando:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --registrar-sessao <etapa> --autor "<nome da pessoa>" --participantes "<lista>"`

O autor é sempre pessoa nomeada. Nunca preencha com identificador de agente.

Se houver referência externa, acrescente `--referencia-externa <id>` junto
com `--canal-externo <id>` e `--marcador "[<caso>/<etapa>]"`. Os três valores
precisam corresponder ao canal declarado; um id isolado não satisfaz a regra.
Se o playbook exigir referência para a camada resolvida, sua ausência recusa.
