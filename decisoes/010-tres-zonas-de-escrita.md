# 010 — Três zonas de escrita

**Data:** setembro de 2026 · **Estado:** proposta, não implementada

## Contexto

Copilotado significa: o humano conduz, o agente instrumenta em tempo real, e o agente não escreve no repositório. O núcleo hoje tem dois estados — escrita bloqueada ou permitida via validador. Não há "sugere mas não grava".

## Decisão proposta

| Zona | Quem escreve | Custo |
|---|---|---|
| `sugestoes/` | agente, livremente | zero |
| `rascunho/` | operador | move o que aceitar |
| `caso/` | validador | procedência obrigatória |

A sugestão só vira rascunho por ação humana, e o log registra qual sugestão virou o quê.

## Consequência

Dá de graça a métrica que o método precisa: quantas sugestões do agente foram aceitas, alteradas ou descartadas por etapa.

**E resolve uma pendência de nomenclatura:** se copilotado é apenas agente sem ferramenta de escrita, `EX3L` não é camada — é `EX2` com zona restrita a `sugestoes/`. Recomendação: eliminar `EX3L` do inventário de mecanismos e mantê-lo só como nome de arranjo no método.
