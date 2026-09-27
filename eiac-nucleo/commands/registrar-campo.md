---
description: Registra um campo declarado no playbook para a etapa corrente.
argument-hint: <etapa> <campo> <valor>
---

**Decisão humana fora da sessão (A12).** O agente prepara os argumentos e
entrega o comando pronto ao engenheiro. Não o execute por Bash na sessão,
mesmo usando nome humano. O engenheiro executa no próprio terminal, fora
do Claude Code, no diretório do caso. Resolva o caminho do plugin antes de
entregar: use o caminho absoluto real, sem variável de sessão no comando.

Confira `/eiac-nucleo:estado` e a declaração `campos_registraveis` da etapa
em `registro/playbook.json`. Use apenas campos declarados e, quando houver
`valores`, um valor exato dessa taxonomia.

Prepare o comando para o engenheiro executar no diretório do caso:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --registrar-campo <etapa> --campo <nome> --valor "<valor>" --autor "<nome da pessoa>"`

A etapa precisa ser a corrente e ainda não encerrada. Autor é pessoa nomeada;
identificador de agente ou coletivo genérico é recusado. Campos internos da
máquina não podem ser declarados por esse mecanismo.

O registro gera `CampoRegistrado`, com etapa, campo, valor, valor anterior e
autor. A recusa preserva o estado e gera `TentativaNegada`. Apresente o motivo
literal da recusa ao operador. Registre o campo antes de encerrar a etapa.
