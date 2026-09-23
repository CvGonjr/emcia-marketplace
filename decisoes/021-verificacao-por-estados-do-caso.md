# 021 — Retirada da execução de contraste e verificação por estados do caso

**Data:** 23/09/2026 · **Estado:** firme · **Substitui:** [[004-janela-da-antitese]], [[014-execucao-de-contraste]], [[015-isolamento-esforco-calculo-compartilhado]], [[016-identidade-runtime-do-contraste]], [[017-pacote-controlado-e-pendencias-no-contraste]], [[018-isolamento-por-carimbo-no-selo]], [[019-autoria-atribuida-pelo-responsavel]] (só a parte específica de execução de contraste — a regra geral de autoria por responsável, aplicável a todo o núcleo, permanece válida e não é revertida por esta decisão), [[020-pendencia-cruzamento-cat01]] (só na parte que menciona a execução de contraste; a pendência de cruzamento CAT-01 em si continua aberta)

## Contexto

A execução de contraste (`emcia-contraste`/`eiac-contraste`, decisões 014–020) foi uma execução completa e independente do mesmo playbook em repositório e plugin próprios, comparável à execução de campo, com um aparato de isolamento (marcador `execucao: contraste`, carimbo `componente.variante` no selo) construído especificamente para impedir que as duas execuções se misturassem no mesmo caso.

Essa arquitetura foi retirada do projeto por decisão metodológica: a comparação entre o que a organização declara e o que o levantamento presencial confirma não precisa de uma segunda execução autônoma do método. Ela pode ser interna ao próprio caso de campo, comparando dois **estados** do mesmo caso — o estado declarado, fechado (selado) ao fim de P2, e o estado verificado, que P3b/P3d produzem depois do levantamento presencial.

## Decisão

A verificação por estados do caso substitui a execução de contraste:

- **Não há segunda execução.** Um único caso de campo, um único playbook, um único núcleo. Não há repositório irmão, não há plugin alternativo, não há colisão de identidade a resolver no selo.
- **P2 fecha o estado declarado.** O selo aplicado depois do encerramento de P2 (`SeloAplicado`, via `/eiac-nucleo:selar`) é o ponto de corte: tudo que o caso sabe sobre o processo até ali é declarado, ainda não confrontado com o levantamento presencial.
- **P3b abre o estado verificado.** P3b (levantamento de regras não documentadas, presencial, não delegável) e P3d (confronto declarado × observado) produzem o segundo estado. A trava de código é única: **P3b não abre, nem encerra, sem um selo posterior ao encerramento de P2.**
- **A trava é declarativa, não hard-coded.** O playbook marca `{"exige_selo_apos": "P2"}` em P3b. O núcleo não sabe o que "P2" ou "P3b" significam — `eiac-nucleo/scripts/playbook.py::selo_apos_etapa()` só compara a posição de eventos `EtapaEncerrada`/`SeloAplicado` na trilha (`estado.eventos()`) contra o campo declarativo, do mesmo jeito que a checagem de condições de emissão (`avancar._avaliar_condicao()`, 2.6.0) já compara campo/etapa/valor sem interpretar seu significado. Aplicada em dois pontos: `guarda.py` (G7, bloqueia a abertura — carregamento da skill) e `avancar.py::encerrar()` (bloqueia o fechamento).
- **"Posterior" é definido por ordem de evento, não por timestamp.** Dois eventos podem cair no mesmo segundo (`estado.evento()` usa precisão de segundo); comparar por `data` produziria falso negativo em qualquer percurso rápido. A posição na lista de eventos é o único ordenador confiável.
- **O Quadro de Confronto lê os dois estados e não escreve em nenhum** — mesma regra de leitura-sem-escrita que já valia para o Quadro de Contraste em 004/014.

O aparato de isolamento núcleo × contraste em `guarda.py` (busca por marcador `execucao: contraste`) e `selar.py` (carimbo `componente.variante`/`componente.commit` em todo evento, recusa de selo sobre trilha com variante diferente de `campo`) **não foi removido nesta decisão**. Ele permanece funcional — não conflita com a nova trava de selo, que opera sobre um par de tipos de evento diferente (`EtapaEncerrada`/`SeloAplicado`) — mas passou a proteger contra uma execução que não é mais parte do fluxo declarado do projeto. Fica registrado como candidato explícito a remoção em decisão futura; até lá, manter é mais seguro do que apagar sob incerteza sobre dependências residuais.

## Consequência

- Não existe mais repositório irmão, plugin de contraste, nem identidade de execução a distinguir. A garantia de que o estado declarado não se confunde com o estado verificado vive inteiramente dentro do caso de campo, como propriedade do próprio percurso F0–P10.
- Toda suíte de teste que constrói um percurso F0→P3b (ou além) precisa selar o caso depois de encerrar P2 — os módulos `testes/nucleo_2_6_1.py`, `testes/campo_2_6_3.py`, `testes/campo_2_6_5.py` e `testes/campo_2_6_6.py` foram ajustados nesta mesma frente para refletir isso; nenhum resultado que eles verificam mudou de sentido, só a sequência de comandos que os produz.
- `README.md`, `INSTALACAO.md`, `eiac-campo/reference/gates.md`, `CTX-01-instrumento-camada-contexto.md` (as duas cópias) e `.projectdocs/map.md` deixam de mencionar antítese/contraste como parte do método executável — a terminologia "Quadro de Contraste" vira "Quadro de Confronto (declarado × verificado)".
- Esta decisão não resolve a pendência 020 (cruzamento CAT-01 Anexo A × catálogo × playbook), que permanece aberta por seu próprio mérito.
