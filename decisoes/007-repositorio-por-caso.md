# 007 — Um repositório Git por caso

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

O caso contém dado de cliente: regras de negócio, volumes, nomes, divergências entre declarado e praticado. Repositório único com todos os casos torna o histórico de um cliente legível a partir de qualquer outro — o que a política de anonimização proíbe.

## Decisão

Um repositório por caso, fora do repositório do marketplace e fora de qualquer outro caso. O `novo-caso.sh` recusa destino dentro de repositório existente.

**GitHub não serve para casos.** Plataforma de código não é onde dado de cliente mora, nem em repositório privado.

## Consequência

Sem espelho na nuvem enquanto não houver servidor Git próprio. Para o PoC: uma máquina, backup criptografado local, limitação declarada.

## Em aberto

Separar **trilha** de **conteúdo**. `registro/eventos.jsonl` não contém dado de negócio — contém etapas, camadas, autores, datas e recusas. Sensibilidade diferente pode significar destino diferente. Precisa ser decidido antes do primeiro caso real; depois, é migração.
