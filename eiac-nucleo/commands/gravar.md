---
description: Grava um rascunho no repositório do caso, passando pelo validador de procedência.
argument-hint: <arquivo de destino>
---
O conteúdo precisa estar em `rascunho/<nome>` com toda asserção marcada.

Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validar.py" --arquivo <destino>`

A autoria do registro não é escolhida aqui: é sempre o responsável do caso, fixado na abertura por `novo-caso.sh`, fora desta sessão. Se houver recusa, corrija a marcação no rascunho e tente de novo. **Não contorne escrevendo direto em `caso/`** — a guarda bloqueia e a tentativa fica registrada.
