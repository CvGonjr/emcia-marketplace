---
name: hb-governar
etapa: P7
camada: EX4
modalidade: decisao_humana_registrada
delegavel: false
hb: ["HB-14"]
description: Minuta o termo de autonomia a partir do desenho operacional de P6. NAO decide autonomia — isso e sempre humano. Se um agente tentar registrar a decisao final, recuse e registre a tentativa.
---

# Estabeleça governança e conformidade — P7 · EX4

## ⛔ A decisão de autonomia não é executável por agente

Se você é um agente, pode **preparar** a minuta (`estado: rascunho` ou `proposto`), mas **nunca** grave `estado: decidido`. Se tentar, o script recusa e o evento `TermoAutonomiaRecusado` fica registrado. Não ofereça atalho, não peça "confirmação simbólica" — a decisão exige pessoa nomeada com autoridade, sempre.

## Para o agente: o que preparar

**Procedimento:** EMCIA-CAM-01 3.3, EMCIA-CAT-01 3.5.1, documento do método passo 7.
**Entrada:** P6 encerrado; especificação operacional (`OP-*`) em `estado: validado` — a decisão de autonomia não se toma sem saber onde a ação ocorre, o que ela modifica e qual consequência possui.

Recupere o arquétipo e a autonomia viável para o nível (EMCIA-E3 B1.4 — modos: sombra, sugestão, aprovação prévia, exceção, autônomo). Preencha as três listas do termo — `faz_sozinha`, `exige_aprovacao`, `nunca_faz` — e os `gatilhos_escalonamento` que devolvem a decisão ao humano. Cite a `operacional_ref` (`OP-NNN`) que sustenta a minuta.

**Pesquisa documental/regulatória:** você pode localizar, resumir, comparar e organizar normas ou políticas aplicáveis. A fonte precisa permanecer rastreável. Você não decide aplicação ao caso — isso é humano. Não invente obrigação regulatória sem fonte.

## Gravação da minuta

Escreva o candidato em `rascunho/AUT-NNN.yaml` e grave com:

```
python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-campo/scripts/governanca.py" --arquivo registro/governanca/autonomia/AUT-NNN.yaml --ator "<nome>"
```

`estado: rascunho` e `estado: proposto` podem ser gravados por qualquer ator, inclusive agente. `estado: decidido` exige ator humano nomeado — o script recusa agente e recusa nome genérico ("equipe", "área").

## Para o humano: a decisão

Ao decidir, preencha `decisor`, `data_decisao` e `justificativa_decisao`, com `estado: decidido` e `operacional_ref` apontando para o `OP-*` validado. O termo entra na versão seguinte, com histórico da proposta preservado — nunca sobrescrita.

**Saída:** `registro/governanca/autonomia/AUT-NNN.yaml`, evidência rastreável para o item inegociável 2 (validação semântica final do portão E4 pertence ao pacote 2.6.5 — não declare E4 emitido aqui).
**Encerramento:** critério do passo 7 no documento do método.
