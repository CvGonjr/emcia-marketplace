# 017 — O campo empacota o método; o contraste registra ambiguidades como pendências

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

As habilidades remetem ao documento do método em `metodo/`, sem reproduzi-lo.
Isso preserva a decisão 009, mas a execução de contraste só pode ler `insumo/` e
o `eiac-campo` pela trava T2. O template de campo também não serve como instrução
de uma execução sem contato humano: ele exige pessoa nomeada, permite V e usa
`fontes/`.

Os documentos controlados fixam ainda que informação I exige premissa, permanece
fora de decisão conclusiva até confirmação e que ausência ou ambiguidade nunca
resolve para o modo mais permissivo (EMCIA-MET-01 3.7 e EMCIA-ESP-01 3.8).

## Decisão

`eiac-campo/reference/metodo/` passa a conter o pacote operacional versionado dos
16 documentos controlados usados na execução, com manifesto SHA-256. O campo
continua sendo a única fonte de método consumida pelos dois controles; nenhum
documento é copiado para `emcia-contraste`.

O inicializador do contraste cria, no repositório da execução, um vínculo
`metodo/` para esse pacote. A resolução real do vínculo permanece dentro de
`eiac-campo`, portanto T2 continua fechada.

Quando uma habilidade pedir confirmação que o insumo não permite obter, o
contraste registra uma pendência com procedência I, premissa, pergunta,
alternativas e decisão provisória. O registro permanece
`pendente_confirmacao`; quando o percurso exigir uma alternativa provisória,
aplica-se a regra documental de nunca escolher a alternativa mais permissiva.
Isso não transforma a inferência em V nem simula contato humano.

## Consequência

Uma sessão real pode ler o mesmo procedimento do campo sem abrir acesso externo,
e a ausência da camada humana se torna dado comparável, não resposta inventada.
O template de campo e as habilidades permanecem sem alteração de texto.
