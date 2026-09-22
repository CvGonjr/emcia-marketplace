# 015 — Isolamento, esforço comparável e cálculo compartilhado

**Data:** setembro de 2026 · **Estado:** parcialmente superada por [[018-isolamento-por-carimbo-no-selo]] — a checagem de isolamento por "eiac-contraste habilitado nas configurações efetivas" não podia funcionar (a decisão 016 faz o manifesto do contraste colidir de propósito com `eiac-nucleo`, então essa chave nunca aparece); substituída por carimbo de componente verificado no selo. Esforço comparável e cálculo compartilhado desta decisão continuam firmes, sem mudança.

## Contexto

A decisão 014 separou campo e contraste, mas a separação precisava existir em
código. A pesquisa também exige esforço comparável e o mesmo cálculo
determinístico nos dois braços.

## Decisão

O núcleo recusa qualquer ferramenta dentro de um caso quando encontra
`eiac-contraste` habilitado nas configurações efetivas ou um marcador durável
`execucao: contraste` em `registro/`. Toda recusa produz evento.

O esforço de campo é lançado pelo engenheiro com etapa e duração; a camada
EX1–EX4 é sempre resolvida do playbook. O registro final usa o mesmo conjunto de
campos do contraste e distingue a origem por `execucao: campo`.

O quadro frequência × consequência passa a ter uma única implementação em
`eiac-campo/scripts/quadro.py`. Núcleo e contraste são apenas adaptadores para
esse cálculo, evitando duas versões do mesmo algoritmo.

## Consequência

Um braço não pode operar sobre o repositório do outro, o custo pode ser somado
pelas mesmas chaves e diferenças do quadro não podem ser atribuídas a versões
distintas do cálculo.
