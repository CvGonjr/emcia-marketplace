---
description: Registra um novo ciclo de uma etapa recorrente, com cadência e responsável.
argument-hint: <etapa> <cadência> <responsável>
---

**Decisão humana fora da sessão (A12).** O agente prepara os argumentos e
entrega o comando pronto ao engenheiro. Não o execute por Bash na sessão,
mesmo usando nome humano. O engenheiro executa no próprio terminal, fora
do Claude Code, no diretório do caso. Resolva o caminho do plugin antes de
entregar: use o caminho absoluto real, sem variável de sessão no comando.

Só se aplica a etapas que o playbook marca `recorrente: true`, e só depois que a etapa foi encerrada ao menos uma vez.

Pergunte ao operador, se não vierem nos argumentos: etapa, cadência (conforme o nível) e responsável nomeado.

Prepare e entregue ao engenheiro este comando:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --registrar-recorrencia <etapa> --autor "<nome da pessoa>" --cadencia "<cadência>" --responsavel "<nome da pessoa>"`

O responsável precisa ser pessoa nomeada — "equipe" ou "área" não satisfaz `responsavel_obrigatorio`. Se o script recusar, apresente o motivo sem contorná-lo.

Quando a etapa declara `coerencia_responsavel_recorrencia`, o responsável
informado precisa coincidir com o da fonte vigente, selecionada pela maior
versão. A recusa mostra os dois nomes e a orientação de troca do playbook.
Para trocar o responsável, siga a orientação declarada no playbook:
o engenheiro grava uma nova versão da fonte no próprio terminal antes de
registrar a recorrência. Não tente repetir com outro nome para
contornar a recusa.
