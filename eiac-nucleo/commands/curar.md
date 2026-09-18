---
description: Cura um objeto de contexto (termo, entidade, regra, fonte ou divergência de confronto P3d) do rascunho para contexto/, com versionamento.
argument-hint: <tipo> <arquivo de destino em contexto/>
---
O candidato precisa estar em `rascunho/<nome>`, estruturado conforme o schema do caso.

Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curar.py" --tipo <tipo> --arquivo contexto/<tipo>s/<id>.yaml --registrado-por "<nome da pessoa>"`

Para um registro de confronto P3d (`divergencia`), o schema é outro:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curar.py" --tipo divergencia --arquivo contexto/divergencias/DIV-001.yaml --registrado-por "<nome da pessoa>" --schema registro/p3d.schema.json`

Se já existir um registro curado com o mesmo id e a `procedencia` ou a `classificacao_confronto` mudar, o candidato precisa trazer `versao` incrementada e uma entrada de `historico` que preserve a versão anterior — a curadoria recusa sobrescrita.

Quando `classificacao_confronto.classe` for `divergente`, `referencia_p3d` precisa apontar para um `contexto/divergencias/<id>.yaml` já curado — referência ausente ou que não resolve é recusada.

Se houver recusa, corrija o rascunho e tente de novo. **Não contorne escrevendo direto em `contexto/`** — a guarda bloqueia e a tentativa fica registrada.
