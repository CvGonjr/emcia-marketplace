---
name: hb-governar
etapa: P7
camada: EX4
modalidade: decisao_humana_registrada
delegavel: false
hb: ["HB-13", "HB-14"]
description: Minuta o termo de autonomia a partir do desenho operacional de P6. NAO decide autonomia — isso e sempre humano. Se um agente tentar registrar a decisao final, recuse e registre a tentativa.
---

# Estabeleça governança e conformidade — P7 · EX4

## ⛔ A decisão de autonomia não é executável por agente

Se você é um agente, pode **preparar** a minuta (`estado: rascunho` ou `proposto`), mas **nunca** grave `estado: decidido`. Se a chamada de decisão vier da sessão, a guarda recusa e registra `TentativaNegada`, mesmo com nome humano. Não ofereça atalho, não peça "confirmação simbólica" — a decisão exige pessoa nomeada com autoridade, sempre.

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

## Execução das decisões humanas (A12)

O agente prepara a proposta e os comandos; o engenheiro executa as decisões
no próprio terminal, fora da sessão do Claude Code, no diretório do caso.
Nome humano informado não autoriza o agente. Resolva o caminho do plugin e
entregue comandos com caminho absoluto real e argumentos confirmados.

Apuração de nível, sessão, campos de decisão, recorrência e satisfação de
inegociáveis são operações humanas declaradas no playbook. A verificação de
inegociável sem `--satisfazer` continua permitida; com `--satisfazer`, entregue
o comando ao engenheiro. Encerramento em EX3/EX4 também é feito por ele.
O agente pode ler, gravar preparação pelos scripts, validar asserções, curar
contexto e materializar/emitir entregáveis. A recusa da guarda registra
`TentativaNegada` com operação e comando exato.
