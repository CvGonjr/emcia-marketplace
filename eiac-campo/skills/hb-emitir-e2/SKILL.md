---
name: hb-emitir-e2
entregavel: E2
fase: F1
camada: EX2
description: Emite o dossie verificado. Use quando /emitir E2 for invocado ou ao fechar a Fase 1.
---

# E2 — Dossiê verificado

**Modelo:** modelo E2, ação 1.6.
**Portão:** P1, P2, P3a, P3b e P3d encerradas.

## Recuse a emissão se

- Houver asserção de `contexto` diferente de `campo`
- A medição inicial tiver `apuracao = estimado` — item inegociável 1
- Houver divergência de P3d sem justificativa
- Não existir `caso/P3b-sessao.md`

**Anexo obrigatório:** lista de procedências e log de divergência.

**Saída:** `caso/entregaveis/E2.md`
