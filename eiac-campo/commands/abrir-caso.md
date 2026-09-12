---
description: Cria o repositório de um caso novo a partir do template do playbook.
argument-hint: <nome-do-caso>
---
Execute, substituindo `<nome>`:

```bash
cp -r "${CLAUDE_PLUGIN_ROOT}/template-caso" ./<nome>
cd <nome> && git init -q && git add -A && git commit -qm "abertura do caso"
```

Depois edite `registro/estado.json` trocando `ALTERE-ME` pelo nome do caso, e copie os documentos do método para `metodo/`.

**Não altere `registro/playbook.json`.** Ele é o método como arquivo, e mudá-lo durante o caso invalida o percurso.

Ao final, confirme com `/eiac-nucleo:estado`.
