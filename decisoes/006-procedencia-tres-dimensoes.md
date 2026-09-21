# 006 — Procedência em três dimensões

**Data:** setembro de 2026 · **Estado:** resolvida — procedência é D/I/V, conforme documento controlado

## Contexto

Os documentos acumularam oito rótulos de procedência. Tratados como lista única, se contradizem: `inferido` responde "como foi obtido?" e `antitese` responde "qual execução produziu?". São perguntas diferentes.

## Decisão original (proposta de três dimensões)

| Dimensão | Valores | Aplica-se a |
|---|---|---|
| Contexto | campo · antitese · conversa · livre | toda asserção |
| Origem | verificado · declarado · inferido · externo | toda asserção |
| Apuração | medido · calculado · estimado | asserção numérica |

`simulado` foi retirado — seu produtor deixou de existir quando a antítese substituiu o ensaio contra empresa fictícia.

## Resolução do conflito com CAT-01

**EMCIA-CAT-01 e EMCIA-GLO-01 fixam três marcas: `[D]`, `[I]`, `[V]`.** A dimensão "Contexto" da proposta original se sobrepunha ao papel de `[D][I][V]` sem necessidade — a pergunta "qual execução produziu a asserção" é respondida por um campo de proveniência de execução (`execucao: campo` / `execucao: contraste`, ver decisão [[014-execucao-de-contraste]]), não por mais uma dimensão de procedência.

Procedência fica exclusivamente **D/I/V** (Declarada, Inferida, Verificada), como CAT-01/GLO-01 já fixavam. `apuração` (medido/calculado/estimado) permanece dimensão separada, aplicável a asserção numérica — é a única parte da proposta original que sobreviveu, e já está implementada em `contexto.schema.json` e testada (`testes/ctx_v.py`, `testes/campo_2_6_5.py`).

Confirmação **não converte** a asserção original: cria uma nova `V`, e a anterior permanece no histórico (`CTX-V04`).

**Estado final:** D/I/V é a única marcação de procedência em código, playbook e habilidades — não há campo `contexto` de procedência. Distinguir execução de campo de execução de contraste é resolvido por decisão 014, fora do vocabulário de procedência.
