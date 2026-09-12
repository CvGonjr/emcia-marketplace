---
name: hb-classificar
etapa: P5
camada: EX2
modalidade: video
description: Aplica a matriz problema-tecnologia na passada de especificacao e decide qual tecnologia atende cada caso priorizado. Use quando /classificar for invocado.
---

# Classificação tecnológica — P5 · EX2

**Procedimento:** documento do método, passo 5.
**Instrumento:** Matriz Problema→Tecnologia, passada de especificação.

## A regra que define o passo

> **Este passo tem autoridade para concluir que o caso não é de agente.**

Cinco de nove casos da simulação não eram, incluindo os dois de maior prioridade. Saída que classifica tudo como agente está errada antes de ser lida.

**"Não é agente" é resultado, não descarte.** Registre qual tecnologia atende, para que o caso siga.

## Efeito no entregável

A conclusão deste passo abre ou fecha o portão de `E3-E`. Ver `reference/gates.md`.

**Saída:** `caso/P5-classificacao.md`, marcada `inferido` até o operador confirmar.
**Encerramento:** critério do passo 5 no documento do método.
