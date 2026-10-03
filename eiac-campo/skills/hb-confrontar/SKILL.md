---
name: hb-confrontar
etapa: P3d
camada: EX3
modalidade: remoto
description: Confronta regra declarada contra regra observada, item a item, e produz o log de divergencia. Use quando /confrontar for invocado, apos a sessao de campo registrada.
hb: ["HB-09", "HB-20"]
---

# Confronto declarado × observado — P3d · EX3

**Pré-requisito:** `caso/P3b-sessao.md` existe. Sem ele, pare — o confronto não tem contra o que confrontar.

**Procedimento:** documento do método, passo 3, parte de confronto.
**Mapa de valor — HB-09:** prepare a varredura conforme EMCIA-MET-01 §3.4.3,
sobre o estado declarado preservado pelo selo confirmado posterior a P2.
Leia esse estado pelo commit do selo; não o redesenhe com base no observado.
Registre candidatos rastreáveis ao fluxo em `caso/P3d-mapa-valor.md`, com
procedência D ou I e referência ao commit de entrada, para uso em P4.
**Preparação do confronto — HB-20:** EMCIA-CAT-01 Anexo A.
O confronto e a decisão de cada item continuam humanos, em EX3.
**Instrumentos:** placar regra escrita × praticada, registro de divergência.

**Um item por vez.** Cada correção exige justificativa escrita e autor nomeado. Correção sem justificativa não é correção, é reescrita.

**Você prepara o confronto; o operador decide cada item.** A transição para `V` cria asserção nova — a original permanece com seu estado.

**Saída:** `caso/E2-dossie.md` e `caso/P3d-divergencias.md`

**Do confronto para o contexto:** quando um item classificado exigir vínculo formal (`classe: divergente`), escreva o registro em `rascunho/DIV-*.yaml` e cure com `/eiac-nucleo:curar --tipo divergencia --schema registro/p3d.schema.json`. Depois, a Regra correspondente em `contexto/regras/` referencia esse registro por `classificacao_confronto.referencia_p3d` — a Regra não duplica `documento_diz`/`observado`/`justificativa`, só aponta para onde estão. Alterar a classificação de uma Regra já curada é mudança de versão, não edição (CTX-01 3.12) — preserva o histórico.

**Encerramento:** critério do passo 3 no documento do método.
