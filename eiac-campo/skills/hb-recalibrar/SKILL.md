---
name: hb-recalibrar
etapa: P10
camada: EX4
modalidade: decisao_humana_registrada
delegavel: false
hb: ["HB-18"]
description: Instala a rotina de recalibragem, monitora desvio e prepara recomendacao. NAO decide recalibragem — isso e sempre humano. Se um agente tentar registrar a decisao, recuse e registre a tentativa.
---

# Aprenda, recalibre e evolua — P10 · EX4 na decisão, EX2 no monitoramento

## ⛔ A decisão de recalibrar, expandir ou descontinuar não é executável por agente

Se você é um agente, pode **detectar** desvio, **quantificar**, **descrever** e **recomendar**, mas **nunca** grave o campo `decisao`. Se tentar, o script recusa e o evento `CicloCalibragemRecusado` fica registrado. A decisão exige pessoa nomeada com autoridade, sempre (CAM-01 3.6, CAT-01 3.4.5).

## Para o agente: a rotina (Anexo D)

**Procedimento:** EMCIA-CAM-01 3.6, documento do método passo 10.
**Entrada:** P9 encerrado, solução em operação ou piloto concluído.

Conforme EMCIA-CAM-01 Anexo D, a rotina registra: responsável (nome, papel, ciência registrada — **pessoa, não área**), cadência (conforme o nível, lançada em calendário), data da primeira revisão, limiares de desvio (definidos antes do piloto — alterar depois exige nova versão justificada), monitoramento (o que é observado e por qual meio), canal de incidente e análise pós-incidente (foco em causa, não em culpa).

A rotina pode referenciar indicadores de P9 via `metricas_ref` (lista de `MET-NNN`).

**Não invente campo fora do contrato.** O schema é `registro/calibragem.schema.json`.

## Para o agente: cada ciclo

Um ciclo sem desvio é caminho positivo legítimo — `drift_detectado: false` não exige recomendação nem decisão, apenas `data_verificacao`. Drift (mudança na distribuição do dado ou na relação que a solução aprendeu) tem limiar fixado antes do piloto; **não ajuste o limiar depois de observar o comportamento**.

Quando `drift_detectado: true`, preencha `drift_descricao`, `drift_quantificacao` e `recomendacao_agente`. Não preencha `decisao`, `decisor`, `data_decisao` nem `justificativa_decisao` — esses quatro campos são exclusivos da decisão humana.

Ciclos anteriores nunca são sobrescritos — cada execução gera um novo identificador (`CAL-NNN-C01`, `CAL-NNN-C02`, ...). Um drift sem decisão humana ainda registrada permanece pendente; não trate como resolvido automaticamente.

## Para o humano: a decisão

Preencha `decisao` (um de `recalibrar`, `expandir`, `descontinuar`), `decisor`, `data_decisao` e `justificativa_decisao`, referida ao limiar definido e ao resultado observado no ciclo.

## Gravação

Rotina:

```
python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-campo/scripts/calibragem.py" --arquivo registro/calibragem/CAL-NNN.yaml --ator "<nome>"
```

Ciclo:

```
python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-campo/scripts/calibragem.py" --arquivo registro/calibragem/CAL-NNN-C01.yaml --ator "<nome>" --ciclo
```

A recorrência (cadência, responsável, histórico de ciclos) também passa por `avancar.py --registrar-recorrencia P10 --autor "<nome>" --cadencia "<cadência>" --responsavel "<nome>"` — mecanismo genérico do núcleo (2.6.1), reaproveitado sem alteração.

**Saída:** `registro/calibragem/CAL-NNN.yaml` e `registro/calibragem/CAL-NNN-CNN.yaml`, evidência rastreável para o item inegociável 5 (validação semântica final do portão E5 pertence ao pacote 2.6.5 — não declare E5 emitido aqui).
**Encerramento:** critério do passo 10 no documento do método.
