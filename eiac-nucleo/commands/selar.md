---
description: Sela o caso — commita o estado corrente no histórico, com o autor nomeado.
argument-hint: <nota do selo>
---
O selo é a terceira trava: o histórico do repositório do caso. Sele depois de encerrar uma etapa ou emitir um entregável — enquanto não selar, a trilha existe só no disco.

Antes de executar, confirme com o operador que o que está no caso é o que ele quer assinar. **Selar é ato dele, não seu.**

Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/selar.py" --autor "<nome da pessoa>" --nota "<o que está sendo selado>"`

O commit sai com o autor nomeado, o mesmo que a trilha registra — não a identidade da máquina. Se o script recusar, apresente o motivo sem contorná-lo.
