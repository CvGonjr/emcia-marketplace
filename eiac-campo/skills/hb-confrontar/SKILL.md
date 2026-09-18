---
name: hb-confrontar
etapa: P3d
camada: EX3
modalidade: remoto
description: Confronta regra declarada contra regra observada, item a item, e produz o log de divergencia. Use quando /confrontar for invocado, apos a sessao de campo registrada.
---

# Confronto declarado × observado — P3d · EX3

**Pré-requisito:** `caso/P3b-sessao.md` existe. Sem ele, pare — o confronto não tem contra o que confrontar.

**Procedimento:** documento do método, passo 3, parte de confronto.
**Instrumentos:** placar regra escrita × praticada, registro de divergência.

**Um item por vez.** Cada correção exige justificativa escrita e autor nomeado. Correção sem justificativa não é correção, é reescrita.

**Você prepara o confronto; o operador decide cada item.** A transição para `V` cria asserção nova — a original permanece com seu estado.

**Saída:** `caso/E2-dossie.md` e `caso/P3d-divergencias.md`

**Do confronto para o contexto:** quando um item classificado exigir vínculo formal (`classe: divergente`), escreva o registro em `rascunho/DIV-*.yaml` e cure com `/eiac-nucleo:curar --tipo divergencia --schema registro/p3d.schema.json`. Depois, a Regra correspondente em `contexto/regras/` referencia esse registro por `classificacao_confronto.referencia_p3d` — a Regra não duplica `documento_diz`/`observado`/`justificativa`, só aponta para onde estão. Alterar a classificação de uma Regra já curada é mudança de versão, não edição (CTX-01 3.12) — preserva o histórico.

**Encerramento:** critério do passo 3 no documento do método.
