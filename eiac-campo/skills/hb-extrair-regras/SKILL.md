---
name: hb-extrair-regras
etapa: P2
camada: EX2
modalidade: assincrono
description: Extrai regras candidatas dos documentos entregues e lista o que eles nao respondem. Use quando /mapear-fontes for invocado ou quando houver documento do caso nao varrido.
---

# Fontes e regras candidatas — P2 · EX2

**Procedimento:** documento do método, passo 2.

**Toda candidata nasce `I`,** mesmo quando o documento parece inequívoco. Documento diz o que foi escrito, não o que é praticado.

**Não sintetize.** Cada candidata exige documento, página e trecho literal. Sem trecho, não grave.

**A lista de lacunas vale mais que a de regras** — é o insumo do roteiro de campo.

**Saída:** `caso/P2-regras-candidatas.md` e `caso/P2-lacunas.md`

**Candidata que já nasce endereçável ao contexto:** quando o documento sustenta um Termo, Entidade, Regra ou Fonte com estrutura suficiente para o schema de `contexto/`, escreva-a também em `rascunho/<id>.yaml`, sempre com `procedencia: I` e `premissa` citando o documento e o trecho. Isso não substitui `caso/P2-regras-candidatas.md`; é o mesmo candidato, em forma curável. **Você não cura.** O operador decide com `/eiac-nucleo:curar` — a candidata em `rascunho/` não é contexto até isso acontecer (CTX-01 3.11).

**Encerramento:** critério do passo 2 no documento do método.
