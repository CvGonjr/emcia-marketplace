# 016 — O contraste substitui a identidade de runtime do núcleo

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

A decisão 014 exige que `eiac-campo` seja compartilhado sem alteração de suas
habilidades. Essas habilidades chamam comandos no namespace
`/eiac-nucleo:*`, e o Claude Code deriva esse namespace do nome do plugin.

## Decisão

O repositório `emcia-contraste` fornece uma implementação alternativa da porta
de runtime `eiac-nucleo`. Campo e contraste usam a mesma identidade de comando,
mas nunca na mesma sessão:

- campo: `eiac-campo` + implementação original de `eiac-nucleo`;
- contraste: `eiac-campo` + implementação de `emcia-contraste`, cujo manifesto
  também declara `eiac-nucleo`.

## Consequência

A colisão nominal é uma trava de isolamento, não um modo sem guardas no núcleo.
As habilidades fazem exatamente as mesmas chamadas nos dois braços. A origem da
implementação, `execucao: contraste` e os commits selados preservam a distinção
de auditoria.
