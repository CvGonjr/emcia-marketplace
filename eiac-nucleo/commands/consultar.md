---
description: Consulta um objeto de contexto curado por id, como dado estruturado.
argument-hint: <id do objeto, ex. RN-014>
---
Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/consultar.py" --id <id>`

Para restringir a campos específicos: `--campo procedencia --campo frequencia` (repetível).

Para objetos que vivem em outro schema (por exemplo `divergencia`, do confronto P3d): `--schema registro/p3d.schema.json`.

Não reinterprete o que a saída já traz estruturado — `procedencia`, `frequencia`, `consequencia_do_erro` e os demais campos centrais vêm prontos. Se o id não existir ou o objeto não passar na validação estrutural, a consulta recusa; isso significa que o contexto necessário ainda não está curado, não que o campo deva ser inventado.
