# 003 — Chat não tem autoridade de escrita

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

Se Chat e Worker tiverem o mesmo acesso, o Chat vira porta dos fundos: o que a guarda nega no percurso, o operador pergunta fora dele e cola. Todas as travas morrem em um Ctrl+C.

## Decisão

Relação inversa entre liberdade e autoridade:

| | Chat | Worker |
|---|---|---|
| Vinculado a caso | não | sim |
| Conhecimento | amplo — método, casos anteriores, divergências | estreito — só o caso |
| Escreve no caso | **nunca** | sim, pelo validador |
| Procedência da saída | `conversa` — rejeitada | conforme a etapa |

O estreitamento do Worker não é limitação técnica: é a mesma prevenção de ancoragem que o braço de controle exige.

## Consequência

Assistentes e tarefas agendadas cabem sem exceção, porque caem inteiros do lado sem autoridade. Personalização é segura porque o poder já foi retirado.

A única passagem é o gesto **levar para um caso**, e o conteúdo entra como proposta marcada, não como conteúdo.

Não impede Ctrl+C. Impede que a colagem seja invisível.
