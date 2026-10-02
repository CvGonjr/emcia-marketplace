---
description: Mostra o estado do caso corrente — etapa, camada, modalidade e cumprimentos.
---
Execute `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/estado.py"` e apresente o resultado.
O campo `selo` é derivado do histórico Git confirmado da trilha: hash, data e nota.
Não interprete além dos dados apresentados. Se não houver caso aberto, diga isso e pare.

Apresente também `integridade_referencia`: compara somente leitura os arquivos com o manifesto declarado no playbook do caso. Divergências são diagnóstico; não autorizam nem recusam operações.
