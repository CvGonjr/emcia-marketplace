---
name: hb-emitir-e4
entregavel: E4
fase: F3
camada: EX2
description: Emite o guia operacional e o termo de autonomia. Use quando /emitir E4 for invocado ou ao fechar a Fase 3.
---

# E4 — Guia operacional

**Modelo:** modelo E4, ação 1.6.
**Portão:** P6, P7 encerrados + inegociável 2 (`reference/gates.md`).

## A seção que determina adoção

O que fazer quando a solução erra. **Encaminhamento para uma área equivale a não haver encaminhamento** — exija pessoa nomeada.

## Termo de autonomia

Estabelecido no P7 (`hb-governar`) e emitido aqui, escrito e decidido por pessoa nomeada — nunca por agente. É o item inegociável 2 e bloqueia este entregável. O registro fica em `registro/governanca/autonomia/AUT-*.yaml`, com o estado `decidido` exigindo `decisor`, `data_decisao` e `justificativa_decisao`.

## Desenho operacional

P6 (`hb-operacionalizar`) produz `registro/operacional/OP-*.yaml`, referenciado pelo termo de autonomia (`operacional_ref`). É insumo das seções 1-2 deste entregável (o que muda no processo, passo a passo da nova rotina).

## Estado deste pacote

A materialização final de `caso/entregaveis/E4.md` a partir de P6/P7, a validação semântica completa do inegociável 2 e a ativação definitiva deste portão pertencem ao pacote 2.6.5. Até lá, P6/P7 produzem apenas os insumos rastreáveis — não declare E4 emitido em definitivo com base neles isoladamente.

**Saída:** `caso/entregaveis/E4.md`
