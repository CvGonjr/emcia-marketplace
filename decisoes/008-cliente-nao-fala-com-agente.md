# 008 — O cliente nunca fala com um agente

**Data:** setembro de 2026 · **Estado:** firme
**Referência:** EMCIA-CAT-01 seção 2

## Contexto

> *os agentes aqui catalogados operam para o engenheiro, não para a organização cliente: o interlocutor de um agente é sempre quem conduz o método.*

F0 ser quase inteiramente delegável não contradiz isso. Significa que o agente **processa o que o cliente declarou**, para o consultor.

## Decisão

Os pontos de contato com o cliente são artefatos assíncronos mediados pelo consultor: formulário de triagem, material recebido, sessão presencial, entregáveis, aceite assinado.

Sem portal, sem chat para o cliente, sem login. Seis contatos em três meses não justificam infraestrutura.

## Consequência

Fecha-se a cadeia de procedência na fronteira com `receber.py`, `entregar.py` e `aceitar.py` — o que hoje é memória do consultor vira registro datado com hash.

**Limite declarado:** o aceite é `EX4` do lado do cliente. O sistema registra que o consultor registrou que o cliente decidiu. Testemunho, não assinatura. Nenhuma trava muda isso.

## Tensão a resolver

A `EX1` se chama **conversacional** e inclui *coleta declarativa*. Conversa com quem? Ou o nome muda, ou a seção 2 do CAT-01 ganha uma frase.
