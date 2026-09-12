---
name: hb-emitir-e3
entregavel: E3-D e E3-E
fase: F2
camada: EX2
description: Emite a decisao da solucao e, quando o portao abrir, a especificacao. Use quando /emitir E3 for invocado ou ao fechar a Fase 2.
---

# E3 — Decisão e especificação da solução

**Modelo:** modelo E3, ação 1.6, em suas duas partes.
**Portão:** P4 e P5 encerradas.

## Duas partes, um portão entre elas

**`E3-D` — decisão. Sempre emitido.** Registra a priorização, a classificação tecnológica e qual tecnologia atende cada caso. Emitido inclusive quando a conclusão é que nenhum caso é de agente.

**`E3-E` — especificação. Condicionado.** Só existe para os casos que P5 classificou como agente. Traz arquétipo, ferramentas, zona de contenção e gatilhos de escalonamento.

> **Emitir `E3-E` quando P5 concluiu que não é agente é erro de método.** Verifique antes de gerar.

## O termo de autonomia não está aqui

Ele é estabelecido no P7 e pertence ao E4. Se o modelo que você tem em mãos ainda o traz anexo ao E3, está desatualizado — não o inclua.

**Saída:** `caso/entregaveis/E3-D.md` e, quando aplicável, `caso/entregaveis/E3-E.md`
