# Pacote 2.6.0 — Contrato executável F0–P10

## 1. Identificação

**Ação:** 2.6 — Agentes e Protocolos
**Pacote:** 2.6.0
**Data/hora:** 2026-09-18 23:00 -0300
**Branch:** master
**HEAD inicial:** `667c0212e81721b67b3dcf866b3eb3333a7d60d4`
**HEAD final:** registrado em `git-show.txt` após o commit deste pacote.

## 2. Documentos consultados

Leitura obrigatória: EMCIA-MET-01 (documento do método, fases e dez
passos), EMCIA-CAT-01 (fronteira de delegação, EX1–EX4, catálogo AG/HB),
EMCIA-ESP-01 v0.2 (especificação executável — contrato de playbook,
portões, inegociáveis como condição de máquina, guardas mínimas G1–G6),
EMCIA-CAM-01 v0.1 (protocolo de campo P6–P10: entrada, atividade, saída,
encerramento, fronteira e condições executáveis M1–M10).

Consultado: EMCIA-E1 a EMCIA-E5 (cabeçalhos de fase/passos, confirmam
E4=Passos 6/7, E5=Passos 8/9/10), EMCIA-ROT-01 (referência de P3d, já
tratada na Ação 2.5), `decisoes/002`, `decisoes/006`, `decisoes/009`,
`decisoes/012`.

## 3. Baseline relacionado

`2.6-BL01` (8/13 etapas), `2.6-BL02` (etapas existentes F0–P5),
`2.6-BL03` (P3b não delegável — já conforme), `2.6-BL04` (P7 não
delegável — ausente), `2.6-BL05` (P10 recorrente — ausente), `2.6-BL18`
(2/6 portões estritamente conformes), `2.6-BL19` (E4 com
`portao_pendente`), `2.6-BL20` (E5 divergente: P9/P10 sem P8 e sem
inegociável 3), `2.6-BL21`–`BL25` (cinco inegociáveis declarados parcial
ou totalmente, sem validação semântica completa).

`D-07` — apenas 8 das 13 etapas do método estavam declaradas.

## 4. Estado inicial do playbook

`eiac-campo/template-caso/registro/playbook.json` v0.3.1: 8 etapas (F0,
P1, P2, P3a, P3b, P3d, P4, P5); `E4`/`E5` com `portao_pendente: true`;
`E5` com portão `["P9","P10"]` (sem P8) e inegociável `[4,5]` (sem 3);
`E3-E` com `condicao` como string livre não interpretável; inegociável 1
com texto "apuracao diferente de estimado" (mais restritivo que MET-01
§3.4.3, que admite estimativa em N1); pendências registrando a mesma
divergência de correspondência já descrita em `decisoes/012`.

Ver `playbook-antes.json` nesta pasta (cópia literal, congelada como
evidência, pré-edição).

## 5. Matriz F0–P10

Ver `matriz-contrato-f0-p10.md` nesta pasta — matriz completa
playbook-atual → método-oficial → diferenças, matriz de etapas e matriz
de emissões.

Resumo das 13 etapas finais:

| Etapa | Fase | Delegável | Recorrente | Depende de |
|---|---|---|---|---|
| F0 | F0 | sim | não | — |
| P1 | F1 | sim | não | — |
| P2 | F1 | sim | não | — |
| P3a | F1 | sim | não | — |
| P3b | F1 | **não** | não | — |
| P3d | F1 | sim | não | P3b |
| P4 | F2 | sim | não | — |
| P5 | F2 | sim | não | — |
| P6 | F3 | sim (preparação) | não | P5 |
| P7 | F3 | **não** | não | P6 |
| P8 | F4 | sim (geração híbrida; revisão humana) | não | P7 |
| P9 | F4 | sim (apuração determinística; interpretação humana) | não | P8 |
| P10 | F4 | **não** (decisão) | **sim** | P9 |

## 6. Camadas e fronteiras

EX1–EX4 preservadas conforme CAT-01 §3.3. Nenhum agente autorizado a
operar em EX3/EX4 — as novas etapas P6 (EX3), P7 (EX4), P8 (EX3), P9
(EX3) e P10 (EX4 na decisão, `camada_monitoramento` EX2 apenas para o
monitoramento de desvio por HB-18, que é preparatório e não decide
recalibrar) seguem essa regra. Nenhuma etapa inteira foi automaticamente
classificada como delegável apenas por conter uma atividade preparatória
EX2 — a camada declarada é a que governa o fechamento da etapa (decisão
humana), conforme o item 11 do pacote.

## 7. P3b

Preservada sem alteração: `delegavel: false`, EX4 nos três níveis,
modalidade presencial. `2.6.0-T05` confirma.

## 8. P7

Adicionada: `delegavel: false`, EX4 nos três níveis, `depende_de: "P6"`,
habilidade apontada (`hb-governar`, ainda não implementada — HB-14 é a
minuta, decisão humana continua sendo o fechamento). Fronteira humana
declarada; nenhum comando de agente para concluir P7 foi criado.
`2.6.0-T06`/`T07` confirmam.

## 9. P10

Adicionada: `delegavel: false`, `recorrente: true`,
`cadencia_obrigatoria: true`, `responsavel_obrigatorio: true`. Mecanismo
de recorrência (scheduler, atualização de última verificação) **não**
implementado — isso é 2.6.1/2.6.3. `2.6.0-T08`/`T09`/`T10` confirmam a
declaração; `2.6.0-N03` confirma que o carregador recusa `recorrente`
sem os dois campos de suporte.

## 10. Cinco inegociáveis

Todos os cinco já estavam declarados com `passo` associado; a correção
deste pacote foi textual (inegociável 1) e estrutural (portões E4/E5).
Mapeamento verificado: 1→P3a, 2→P7, 3→P8, 4→P9, 5→P10 (`2.6.0-T12`). Não
foi declarado que os cinco são semanticamente verificáveis — isso
permanece pendente para os pacotes seguintes.

### 10.1 Ajuste do inegociável 1

Texto anterior: "Linha de base registrada, apuracao diferente de
estimado" — mais restritivo que o método vigente. MET-01 §3.4.3: "A
linha de base é obrigatória nos três níveis. Estimada em N1, medida em
N2 e N3, mas sempre registrada antes do piloto." Corrigido para: "Linha
de base registrada antes do piloto, apuracao proporcional ao nivel
(estimada em N1, medida em N2 e N3)".

## 11. Seis autorizações

E1, E2, E3-D, E3-E, E4, E5 — todas presentes (`2.6.0-T13`). Nenhuma
emitida neste pacote; apenas o contrato declarativo foi corrigido.

## 12. E3-E

Condição textual livre ("P5 concluiu que a solucao e um agente")
substituída por estrutura declarativa:
`{"descricao": ..., "campo": "classificacao_tecnologica", "etapa": "P5", "operador": "contem", "valor": "agente"}`.
O núcleo não interpreta essa condição — nenhum `if entregavel == "E3-E"`
foi adicionado a `avancar.py`. A interpretação semântica é 2.6.1/2.6.5.
`2.6.0-T17` confirma a forma; `pendencias` do playbook registra
explicitamente que o motor ainda não a interpreta.

## 13. E4

`portao: ["P6","P7"]`, `inegociavel: [2]`, `portao_pendente` removido.
Remover o campo não afirma que E4 é emitível hoje — P6/P7 ainda não têm
skill implementada. `2.6.0-T18`/`T22` confirmam.

## 14. E5

`portao: ["P8","P9","P10"]` (P8 adicionado), `inegociavel: [3,4,5]`
(inegociável 3 adicionado), `portao_pendente` removido. `2.6.0-T19`/`T22`
confirmam.

## 15. Pendências removidas

- "Correspondência entregável x passos diverge entre o relatório do PFC e
  os documentos internos. Bloqueia E4 e E5." — resolvida por precedência
  documental (EMCIA-CAM-01, EMCIA-ESP-01 v0.2, ambos de 17/09/2026).
  Registrada como `decisoes/013`, que marca a seção "Pendência" de
  `decisoes/012` como superada.

## 16. Pendências ainda reais

- "P6 a P10 sem habilidade: instrumentos ausentes" — persiste, agora
  detalhada por nome de skill (`hb-operacionalizar`, `hb-governar`,
  `hb-pilotar`, `hb-medir-valor`, `hb-recalibrar`), tratamento em
  2.6.2/2.6.3.
- Motor do núcleo ainda não interpreta semanticamente a condição de
  E3-E, a recorrência de P10 (scheduler/cadência) nem os cinco
  inegociáveis — capacidade declarativa pronta, validador em 2.6.1.
- `registro/` ainda permite escrita direta fora do que `guarda.py` já
  cobre para `caso/`/`contexto/` (D-08, 2.6.1).
- Recusas de `avancar.py` não emitem evento (D-09, 2.6.1).
- `decisoes/006` permanece em conflito com documento controlado —
  decisão humana pendente, fora do escopo deste pacote.

## 17. Arquivos alterados

- `eiac-campo/template-caso/registro/playbook.json` — v0.3.1 → v0.4.0;
  13 etapas, portões E4/E5 corrigidos, E3-E declarativo, inegociável 1
  ajustado, pendências atualizadas.
- `eiac-nucleo/scripts/playbook.py` — checagens estruturais genéricas
  novas: ID de etapa duplicado, camada fora de EX1–EX4, `depende_de`
  órfão, portão/inegociável órfão, recorrência exige cadência e
  responsável. Nenhum vocabulário do método adicionado.
- `eiac-nucleo/.claude-plugin/plugin.json` — 0.2.11 → 0.2.12 (script do
  núcleo alterado).
- `eiac-campo/.claude-plugin/plugin.json` — 0.3.8 → 0.3.9 (descrição
  atualizada para F0–P10; template-caso alterado).
- `testes/playbook_2_6_0.py` — nova suíte, 29 verificações.
- `testes/README.md` — nova seção do pacote 2.6.0, total atualizado
  129 → 158.
- `decisoes/012-e3-dividido.md` — nota de superação da seção Pendência.
- `decisoes/013-e4-e5-correspondencia-fixada.md` — nova decisão.
- `decisoes/README.md` — índice atualizado.

Nenhum arquivo de `eiac-nucleo/scripts/estado.py`, `avancar.py` ou
`guarda.py` foi alterado — todos já liam os campos genéricos necessários
(`delegavel`, `depende_de`, `portao`, `inegociavel`, `camada`)
corretamente, sem exigir mudança de comportamento para aceitar as 13
etapas.

## 18. Testes estruturais

24 verificações positivas (`2.6.0-T01`–`T24`), todas PASS. Ver
`teste-2.6.0-T01.txt` a `teste-2.6.0-T24.txt` e `matriz-contrato-f0-p10.md`.

## 19. Testes negativos

5 verificações (`2.6.0-N01`–`N05`), todas PASS quanto ao comportamento
esperado do carregador. `2.6.0-N02` (E5 só com P9/P10) é reportado como
**CAPACIDADE DECLARATIVA OK / VALIDADOR DO NÚCLEO PENDENTE PARA 2.6.1**:
`playbook.py` confirma que as etapas referenciadas existem, mas não
valida semanticamente se o *conjunto* de um portão corresponde à
composição exigida pelo método (isso é regra de método, não checagem
estrutural genérica) — a estrutura oficial já está corrigida (`T19`),
apenas o validador genérico dessa classe de regra fica para 2.6.1.

## 20. Capacidades ainda pendentes do núcleo

- Interpretação semântica da condição declarativa de E3-E.
- Scheduler/mecanismo de cadência de P10.
- Verificação semântica dos cinco inegociáveis (hoje, `avancar.py`
  confia em `st["inegociaveis"]` gravado externamente).
- Validação de composição semântica de portão (ex.: "E5 deve ser
  exatamente P8+P9+P10", não apenas "as etapas referenciadas existem").
- Proteção de `registro/` (D-08) e eventos de recusa de `avancar.py`
  (D-09).

## 21. Regressão

**Antes:** 129 verificações (33 `negativos.sh` + 11 `contexto.py` + 17
`curadoria.py` + 12 `p3d.py` + 23 `ctx_v.py` + 17 `integracao.py` + 16
`consolidado.py`), 129 PASS, 0 FAIL, 0 SKIP. Ver
`teste-regressao-inicial.txt` (executado sobre o estado imediatamente
anterior a este pacote, via `git stash` temporário, restaurado em
seguida sem perda).

**Pacote 2.6.0:** 29 verificações, 29 PASS, 0 FAIL.

**Depois:** 158 verificações, 158 PASS, 0 FAIL, 0 SKIP. Ver
`teste-regressao-final.txt`.

Comparação com S2-BL (26 PASS) e final da Ação 2.5 (129 PASS): a
quantidade cresceu de forma rastreável ao requisito coberto (13 etapas,
seis autorizações, cinco inegociáveis, cinco negativas estruturais), não
como meta numérica.

## 22. Defeitos encontrados

Nenhum defeito de produção novo. O que existia (`D-07`, e os
sub-itens de `2.6-BL18`–`BL20`) já estava catalogado no baseline. A
divergência textual do inegociável 1 e a pendência de correspondência
E4/E5 são tratadas como lacunas de contrato do baseline, não como
defeitos novos descobertos durante o pacote.

## 23. Correções

Ver seções 9–14 acima e `matriz-contrato-f0-p10.md`.

## 24. Itens adiados

- **2.6.1** — núcleo genérico de protocolos: proteção de `registro/`,
  eventos para toda recusa de `avancar.py`, validação semântica de
  composição de portão, interpretação da condição de E3-E, mecanismo de
  cadência de P10.
- **2.6.2** — P6 e P7 operacionais (`hb-operacionalizar`, `hb-governar`).
- **2.6.3** — P8, P9 e P10 operacionais e recorrência (`hb-pilotar`,
  `hb-medir-valor`, `hb-recalibrar`).
- **2.6.4** — 18 HB completas, 4 AG mapeados, critérios de verificação.
- **2.6.5** — seis autorizações ativas, inegociáveis semanticamente
  verificados, geração material de E4/E5.
- **2.6.6** — caso de controle F0–P10 e suíte end-to-end.

## 25. Commit

Ver `git-show.txt` nesta pasta.

## 26. Estado final

**CONFORME.**

O playbook representa integralmente o método F0–P10 como contrato
declarativo. Não se afirma que o Estúdio executa integralmente F0–P10 —
essa afirmação só é legítima após 2.6.1–2.6.6.
