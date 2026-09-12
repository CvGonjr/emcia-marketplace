---
name: hb-emitir-e5
entregavel: E5
fase: F4
camada: EX2
description: Emite o relatorio de piloto, o plano de medicao e a calibragem. Use quando /emitir E5 for invocado ou ao fechar a Fase 4.
---

# E5 — Relatório de piloto e calibragem

**Modelo:** modelo E5, ação 1.6.
**Portão:** ver pendência em `reference/gates.md`.

## Recuse a emissão se

- Não houver comparação contra a linha de base registrada na F1
- Todas as métricas forem de uso, nenhuma de resultado — item inegociável 4
- O responsável pela recalibragem for uma área e não uma pessoa — item inegociável 5
- O critério de aprovação não registrar a data em que foi definido, anterior ao início do piloto

**Cadência da recalibragem:** conforme o nível do caso, definida no documento do método.

**Saída:** `caso/entregaveis/E5.md`
