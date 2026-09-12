# 004 — A antítese roda entre P2 e P3a

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

A antítese só é braço de controle se consumir exclusivamente fonte declarada e pública. P3a produz a linha de base sobre amostras — dado de campo. Se a antítese rodasse depois, seria preciso excluir asserções recém-criadas, e exclusão vira filtro em vez de fronteira. Filtros erram em silêncio.

Além disso, a antítese precisa **estimar** a linha de base. É a previsão P4 do pré-registro. Recebendo a medição real, a previsão fica sem objeto.

## Decisão

```
P2 encerrada
  → snapshot fechado (declarado + público, nada de campo)
  → antítese, execução única, F0 a P10
  → selagem, inclusive em caso de falha
  → P3a liberada
  → P3b levantamento presencial
```

Entre o fechamento de P2 e a selagem, o braço de campo fica parado. `P3a` não abre enquanto o selo não existir.

## Consequência

Execução única, sem segunda tentativa — a segunda já saberia o que a primeira produziu. Falha é resultado: antítese que quebrou no meio diz que a camada automatizada não completa o percurso sozinha.

O Quadro de Contraste lê os dois braços e **não escreve em nenhum**.
