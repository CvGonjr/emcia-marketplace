---
name: hb-operacionalizar
etapa: P6
camada: EX3
modalidade: presencial_ou_remoto
description: Estrutura a especificacao operacional a partir de E3-E/P5 e do contexto curado. Use quando /operacionalizar for invocado, apos P5 encerrada.
---

# Operacionalize a solução — P6 · EX3

**Procedimento:** EMCIA-CAM-01 3.2, documento do método passo 6.
**Entrada:** E3-E emitido (ou o candidato correspondente), caso classificado como agente em P5, camada de contexto registrada — não reexecute P4/P5.

**Este passo produz especificação, não deployment.** O Estúdio não implanta sistema, não integra com o ambiente do cliente, não constrói o agente real. Ele documenta onde a solução entraria no fluxo.

## O que preencher

Conforme EMCIA-CAM-01 3.2 e EMCIA-MET-01 3.4.6, a especificação registra: ponto de inserção nominado (quem, em que momento, em que sistema — não a área), entrada, saída, ator humano que recebe, sistema/interface tocado, exceção prevista, fallback quando a exceção ocorre, e responsável operacional nomeado.

**Não invente campo fora do contrato.** O schema é `registro/operacional.schema.json`.

## O que o agente pode fazer

Ler E3/E3-E, ler o contexto curado (`consultar.py --id RN-XXX`), organizar o fluxo, identificar interfaces, estruturar o mapa técnico, gerar rascunho, apontar inconsistências.

## O que o agente não pode fazer

Decidir política organizacional, assumir aprovação humana, implantar sistema, executar mudança real no processo do cliente. **Proposta não é aprovação.** Escreva `estado: proposta` — nunca `validado`.

## Gravação

Escreva o candidato em `rascunho/OP-NNN.yaml` e grave com:

```
python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-campo/scripts/operacional.py" --arquivo registro/operacional/OP-NNN.yaml --ator "<nome>"
```

Para `estado: proposta`, qualquer ator (inclusive agente) pode gravar. Para `estado: validado`, o ator precisa ser pessoa humana nomeada — o script recusa qualquer tentativa de um agente validar sua própria proposta.

**Saída:** `registro/operacional/OP-NNN.yaml`, referenciável por `operacional_ref` em P7.
**Encerramento:** critério do passo 6 no documento do método.
