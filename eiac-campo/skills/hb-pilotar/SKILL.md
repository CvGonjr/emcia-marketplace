---
name: hb-pilotar
etapa: P8
camada: EX3
modalidade: conforme_nivel
hb: ["HB-15", "HB-16"]
description: Deriva casos de teste com saida esperada das regras da camada de contexto e executa a suite. Use quando /pilotar for invocado, apos P7 encerrada.
---

# Pilote, valide e escale — P8 · EX3

**Procedimento:** EMCIA-CAM-01 3.4, documento do método passo 8.
**Entrada:** P7 encerrado, termo de autonomia decidido, linha de base do passo 3 registrada.

## O que preencher

Conforme EMCIA-CAM-01 Anexo B, cada caso do conjunto registra: identificador (sequencial no conjunto), origem (regra da camada de contexto que o caso exercita), entrada, saída esperada, critério de aprovação, categoria (`comum`, `excecao` ou `celula_critica`), revisor e data da revisão. **O conjunto precisa cobrir a célula crítica** do quadro frequência × consequência — conjunto só com casos comuns não satisfaz o passo.

**A saída esperada é escrita antes de qualquer execução.** Preencha `esperado_definido_em`/`esperado_definido_por` antes de rodar o caso. Depois de observar `saida_obtida`, o campo `resultado` (`aderente`/`divergente`) é calculado pela comparação — nunca escrito por decisão manual, e nunca reescreve a saída esperada para transformar falha em sucesso.

**Não invente campo fora do contrato.** O schema é `registro/piloto.schema.json`.

## O que o agente pode fazer

Derivar casos das regras curadas, priorizando a célula crítica; escrever a saída esperada; executar verificações automatizáveis; comparar esperado × obtido; registrar evidência; estruturar o rascunho do conjunto.

## O que o agente não pode fazer

Inventar o resultado esperado depois de observar a saída real; redefinir critério para transformar falha em sucesso; declarar o conjunto revisado — isso exige quem executa o processo. Escreva `estado: rascunho` — nunca `revisado`.

## Gravação

Escreva o candidato em `rascunho/CT-NNN.yaml` e grave com:

```
python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-campo/scripts/piloto.py" --arquivo registro/piloto/CT-NNN.yaml --ator "<nome>"
```

Para `estado: rascunho`, qualquer ator (inclusive agente) pode gravar. Para `estado: revisado`, o `revisado_por` precisa ser pessoa humana nomeada — o script recusa agente.

**Saída:** `registro/piloto/CT-NNN.yaml`, evidência rastreável para o item inegociável 3 (validação semântica final do portão E5 pertence ao pacote 2.6.5 — não declare E5 emitido aqui).
**Encerramento:** critério do passo 8 no documento do método.
