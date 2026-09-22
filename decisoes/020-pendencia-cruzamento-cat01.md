# 020 — Pendência única de correspondência entre CAT-01, catálogo e playbook

**Data:** 22/09/2026 · **Estado:** pendente de decisão de método

## Contexto

O cruzamento integral das treze etapas, registrado em
`docs/cruzamento-cat01.md`, encontrou três classes relacionadas de
desalinhamento: atividades automatizadas ou híbridas sem HB no Anexo A, HBs
existentes que não são referenciadas pela habilidade da etapa no playbook e
camadas de etapa que agregam ou contradizem as naturezas/camadas do CAT-01.

O problema é sistemático. O CAT-01 v0.2 classifica atividades por passo e
mantém um catálogo de dezoito HB, mas não declara a correspondência completa
entre as duas tabelas. O playbook v0.4.1 introduz treze etapas, divide o passo 3
em P3a/P3b/P3d e incorpora P6–P10 executáveis sem que essa correspondência tenha
sido revisada no CAT-01.

## Decisão provisória de implementação

O conjunto fica registrado como **uma única pendência de método**, remetendo ao
cruzamento. CAT-01, `reference/habilidades.json` e o playbook não serão
alterados até decisão humana sobre a revisão do método.

Para não inventar autoridade na execução de contraste, quando a habilidade da
etapa não resolver um `ag_autorizado` por `skill_ref`, a autoria estrutural será
o próprio identificador da habilidade (`hb-*`) e o registro guardará
`camada_substituida` igual à camada da etapa resolvida para o nível. P3b
permanece `nao_realizado`. Essa regra se aplica uniformemente a toda etapa sem
AG identificada pelo cruzamento, hoje P3a, P3b, P3d e P6.

## Consequência

- Nenhum código AG é inferido ou inventado.
- A execução de contraste pode prosseguir com autoria rastreável enquanto a
  lacuna documental permanece visível.
- A revisão futura precisa tratar o conjunto completo do cruzamento, não casos
  isolados por etapa.
- Resolver a pendência exigirá nova decisão que atualize os documentos
  controlados e superseda explicitamente esta regra provisória.
