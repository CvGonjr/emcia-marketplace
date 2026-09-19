---
name: hb-medir-valor
etapa: P9
camada: EX3
modalidade: conforme_nivel
hb: ["HB-17"]
description: Apura metricas contra a linha de base do passo 3 e diferencia resultado de uso. Use quando /medir-valor for invocado, apos P8 encerrada.
---

# Meça o valor gerado — P9 · EX3

**Procedimento:** EMCIA-CAM-01 3.5, documento do método passo 9.
**Entrada:** P8 encerrado, piloto executado, linha de base do passo 3 disponível — não reexecute P8.

## O que preencher

Conforme EMCIA-CAM-01 Anexo C, cada métrica registra: nome e o que mede, tipo (`resultado`, `uso` ou `qualidade`), linha de base (valor, data, procedência), método de apuração (determinístico, documentado), fonte do dado, periodicidade, responsável pela apuração (pessoa nomeada) e resultado apurado (valor, data, procedência).

**Medir adoção não é medir valor.** Ao menos uma métrica do plano precisa ter `tipo: resultado` — métricas de uso podem compor o plano, mas não satisfazem sozinhas o item inegociável 4.

**A linha de base não pode ser inventada depois do piloto.** `linha_base_data` precisa preceder `resultado_apurado_data`. Cite a `piloto_ref` (`CT-NNN`) revisada que sustenta a medição — P9 não mede sobre piloto que não existe.

**Não declare causa sem evidência.** Ao apurar, preencha `fatores_externos_declarados` — mesmo que seja "nenhum identificado". "Houve redução" não vira "a solução causou a redução" sem separar o efeito de sazonalidade ou de esforço paralelo (CAT-01 3.4.5: atribuição de causa não está nos dados). Isso é julgamento humano.

**Não invente campo fora do contrato.** O schema é `registro/metricas.schema.json`.

## O que o agente pode fazer

Calcular, comparar, normalizar, estruturar indicadores, produzir tabelas, detectar ausência de baseline, sinalizar inconsistências.

## O que o agente não pode fazer

Inventar baseline; alterar fórmula de apuração depois do resultado; definir sozinho que o impacto é suficiente para escalar; interpretar por que a métrica se moveu e apresentar ao patrocinador — isso é humano (CAT-01 3.4.5).

## Gravação

Escreva o candidato em `rascunho/MET-NNN.yaml` e grave com:

```
python3 "${CLAUDE_PLUGIN_ROOT}/../eiac-campo/scripts/metrica.py" --arquivo registro/metricas/MET-NNN.yaml --ator "<nome>"
```

**Saída:** `registro/metricas/MET-NNN.yaml`, evidência rastreável para o item inegociável 4 (validação semântica final do portão E5 pertence ao pacote 2.6.5 — não declare E5 emitido aqui).
**Encerramento:** critério do passo 9 no documento do método.
