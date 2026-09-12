---
description: Grava um rascunho no repositório do caso, passando pelo validador de procedência.
argument-hint: <arquivo de destino>
---
O conteúdo precisa estar em `rascunho/<nome>` com toda asserção marcada.

Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validar.py" --arquivo <destino> --autor "<nome da pessoa>"`

Se houver recusa, corrija a marcação no rascunho e tente de novo. **Não contorne escrevendo direto em `caso/`** — a guarda bloqueia e a tentativa fica registrada.
