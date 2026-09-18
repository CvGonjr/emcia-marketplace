---
description: Cura um objeto de contexto (termo, entidade, regra ou fonte) do rascunho para contexto/, com versionamento.
argument-hint: <tipo> <arquivo de destino em contexto/>
---
O candidato precisa estar em `rascunho/<nome>`, estruturado conforme o schema do caso.

Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curar.py" --tipo <tipo> --arquivo contexto/<tipo>s/<id>.yaml --registrado-por "<nome da pessoa>"`

Se já existir um registro curado com o mesmo id e a procedência mudar (por exemplo I → V), o candidato precisa trazer `versao` incrementada e uma entrada de `historico` que preserve a versão anterior — a curadoria recusa sobrescrita.

Se houver recusa, corrija o rascunho e tente de novo. **Não contorne escrevendo direto em `contexto/`** — a guarda bloqueia e a tentativa fica registrada.
