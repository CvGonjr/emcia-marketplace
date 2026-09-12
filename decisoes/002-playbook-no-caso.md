# 002 — O playbook vive no caso, não no plugin

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

Atualizar o plugin não pode alterar caso em andamento. Se o playbook mudasse ao vivo, um caso parado no P3 poderia acordar com outra camada na etapa corrente, e o entregável emitido depois teria sido produzido sob regras que ninguém registrou.

## Decisão

O `playbook.json` é copiado para `registro/` na abertura do caso. O núcleo lê dali, nunca do plugin.

## Consequência

Correção no núcleo alcança todos os casos imediatamente — é o comportamento certo para um furo de guarda.
Mudança de playbook alcança apenas casos novos.

Migrar caso aberto é ato deliberado: copiar o playbook novo e commitar.

**Não "conserte" isso.** Parece duplicação e não é.
