---
description: Registra um campo declarado no playbook para a etapa corrente.
argument-hint: <etapa> <campo> <valor>
---
Confira `/eiac-nucleo:estado` e a declaração `campos_registraveis` da etapa
em `registro/playbook.json`. Use apenas campos declarados e, quando houver
`valores`, um valor exato dessa taxonomia.

Execute no diretório do caso:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --registrar-campo <etapa> --campo <nome> --valor "<valor>" --autor "<nome da pessoa>"`

A etapa precisa ser a corrente e ainda não encerrada. Autor é pessoa nomeada;
identificador de agente ou coletivo genérico é recusado. Campos internos da
máquina não podem ser declarados por esse mecanismo.

O registro gera `CampoRegistrado`, com etapa, campo, valor, valor anterior e
autor. A recusa preserva o estado e gera `TentativaNegada`. Apresente o motivo
literal da recusa ao operador. Registre o campo antes de encerrar a etapa.
