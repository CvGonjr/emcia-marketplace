# Pacote 2.5.5 — Integração P2/P3 → CTX → P4/P5

## 1. Identificação

- **Ação:** 2.5 — Contexto e Dados
- **Pacote:** 2.5.5
- **Data/hora:** 18/09/2026, execução única de implementação e testes
- **Branch:** `master`
- **HEAD inicial:** `2216feef1bece5cee01e3409631945ab1dd1fb93`
- **HEAD final:** ver `git-show.txt` (commit criado ao final deste pacote)

## 2. Documentos consultados

| Documento | Papel |
|---|---|
| EMCIA-MET-01 | Sequência operacional P2–P5; encerramento e corte de cada passo (§3.4.3–3.4.5). |
| EMCIA-CTX-01 | Forma do conhecimento contextual; §3.6 (sete campos centrais); §3.8 (correspondência ROT-01→CTX-01). |
| EMCIA-ROT-01 | Origem das regras não documentadas de P3b. |
| EMCIA-E2, EMCIA-E3 | Confirmação de que geração de entregável não é escopo deste pacote (§21 da instrução). |
| EMCIA-FER-01 | Ferramentas de apoio a P4/P5; nenhuma divergência com o já implementado. |
| EMCIA-ESP-01, EMCIA-TST-01, EMCIA-TRA-01 | Convenções de teste e separação núcleo/campo. |
| `eiac-campo/skills/*`, `eiac-campo/commands/*`, `eiac-campo/agents/*` | Estado real do código antes do pacote (nenhuma referência a `curar.py`/`contexto/`). |

## 3. Baseline relacionado

D-06, 2.5-BL20, 2.5-BL21, 2.5-BL22 (parte relativa ao fluxo; a parte de
proteção de `contexto/` já foi tratada em 2.5.2).

## 4. Estado inicial

Confirmado por inspeção direta do código (`grep` em todas as skills,
comandos e agentes por `curar.py`/`contexto/`): **zero referências**.
Todas as etapas P2–P5 liam e escreviam exclusivamente `caso/*.md` via
`validar.py`. `quadro.py` já existia e já lia `contexto/regras/*.yaml`
estruturado, mas nenhuma skill de P4 instruía usá-lo. `classificador-tecnologico`
(P5) tinha só `Read, Grep`, sem qualquer caminho de consulta estruturada.
Ver `matriz-integracao.md` para o levantamento completo por etapa.

## 5. Matriz de integração

Ver `matriz-integracao.md` — seis etapas (P2, P3a, P3b, P3d, P4, P5),
estado antes/depois de cada seta do fluxo.

## 6. Fluxo P2/P3 → CTX

**P2:** candidata com estrutura suficiente para Termo, Entidade, Regra ou
Fonte agora também é escrita em `rascunho/<id>.yaml` com `procedencia: I`
e premissa citando documento/trecho — além da lista `caso/P2-regras-candidatas.md`
já existente, não em substituição. A candidata só entra em `contexto/`
por curadoria humana explícita (`/eiac-nucleo:curar`); a skill e o agente
dizem isso textualmente.

**P3a:** medição não é objeto CTX — decisão de método registrada, não
lacuna de implementação (CTX-01 não define esse objeto). Quando uma
medição sustenta uma Regra/Fonte `V`, a skill orienta dar um identificador
estável à linha da medição, para que `evidencia.referencia` aponte para
ela sem ambiguidade. Vínculo rastreável, não duplicação nem objeto novo.

**P3b:** o caminho técnico já existia desde 2.5.2 (`curar.py` aceita
Regra com qualquer procedência real da sessão); a skill agora referencia
esse caminho explicitamente, citando CTX-01 §3.8.

**P3d:** já implementado nos pacotes 2.5.3/2.5.4; a skill agora referencia
o comando (`curar.py --tipo divergencia`) e lembra que mudar
`classificacao_confronto` numa Regra já curada é mudança de versão, não
edição — preservando o comportamento do 2.5.2 (testado em T05/T05b).

## 7. Fluxo CTX → P4/P5

**P4:** `hb-priorizar` agora instrui rodar `quadro.py` antes de priorizar
e citar os IDs de Regra (`RN-*`) que sustentam a decisão. `quadro.py` já
lia `frequencia`/`consequencia_do_erro` diretamente do YAML curado (prova
de não reinterpretação, T08) — não foi reescrito, só citado.

**P5:** novo `eiac-nucleo/scripts/consultar.py`, leitura genérica e
somente-leitura por id, reaproveitando o mesmo `catalogo_referencias`
declarativo que `curar.py` já usa para resolver `entradas`/`onde_vive`
(nenhum hard-code de tipo no núcleo). A saída expõe `procedencia` e os
sete campos centrais como dado estruturado. `hb-classificar` e o agente
`classificador-tecnologico` passam a consultar por esse caminho, e a
preservar o estatuto documental: `D`/`I`/`V` não são intercambiáveis, mas
a exigência de `V` só se aplica quando a decisão específica depende de
conhecimento verificado — não há exigência global de `V` em P5 (ajuste
explícito pedido antes da implementação).

## 8. Alterações realizadas

| Arquivo | Alteração | Justificativa |
|---|---|---|
| `eiac-nucleo/scripts/consultar.py` (novo) | Leitor genérico e somente-leitura de objeto CTX por id. | Fecha o gap real de consumo estruturado em P5. |
| `eiac-nucleo/scripts/quadro.py` | Corrige defeito real: `entradas: []`/`excecoes_conhecidas: []` eram tratados como "campo ausente"; agora seguem a mesma semântica de presença do schema (`required` sem `nonempty`), como `decisor_quando_nao_cobre` já recebia. | Reprodução e correção de defeito encontrado ao testar o fluxo P4 real. |
| `eiac-campo/template-caso/registro/contexto.schema.json` | `catalogo_referencias` ganha `RN`→regra e `DIV`→divergencia (antes só T/E/F, escopo da resolução de referências do 2.5.4). | `consultar.py` precisa resolver qualquer tipo de objeto por id, não só os referenciáveis por `entradas`/`onde_vive`. |
| `eiac-campo/template-caso/registro/p3d.schema.json` | Ganha seu próprio `catalogo_referencias` (`DIV`→divergencia). | Consistência: cada schema declara o catálogo dos tipos que define. |
| `eiac-campo/skills/hb-extrair-regras/SKILL.md`, `eiac-campo/agents/extrator-documental.md` | P2 ganha orientação de escrever candidata estruturada em `rascunho/`, sem curar automaticamente. | Fecha D-06/2.5-BL20 para P2. |
| `eiac-campo/skills/hb-medir/SKILL.md` | P3a ganha orientação de vínculo rastreável via `evidencia.referencia`, sem objeto CTX novo. | Ajuste pedido: não deixar P3a fora da camada quando aplicável. |
| `eiac-campo/skills/hb-levantar-regras/SKILL.md`, `eiac-campo/skills/hb-confrontar/SKILL.md` | P3b/P3d referenciam o caminho de curadoria já existente (2.5.2/2.5.3). | Formalização, sem mudança de comportamento. |
| `eiac-campo/skills/hb-priorizar/SKILL.md` | P4 instruída a rodar `quadro.py` e citar IDs de Regra. | Fecha 2.5-BL21 para P4. |
| `eiac-campo/skills/hb-classificar/SKILL.md`, `eiac-campo/agents/classificador-tecnologico.md` | P5 instruída a consultar via `consultar.py`; distinção D/I/V sem exigência global de V. | Fecha D-06/2.5-BL21 para P5. |
| `eiac-nucleo/commands/consultar.md` (novo) | Comando `/eiac-nucleo:consultar`. | Espelha `curar.md`/`quadro.md`. |
| `eiac-nucleo/README.md` | Documenta `consultar.py`. | Rastreabilidade. |
| `testes/integracao.py` (novo) | 17 testes (T01–T16 + T05b). | EMCIA-TST-01. |
| `testes/README.md` | Documenta a suíte nova; total acumulado 96 → 113. | Rastreabilidade dos testes. |
| `eiac-nucleo/.claude-plugin/plugin.json` | `0.2.10` → `0.2.11`. | `consultar.py` novo, `quadro.py` corrigido. |
| `eiac-campo/.claude-plugin/plugin.json` | `0.3.7` → `0.3.8`. | Schemas e seis skills/agentes mudaram. |

## 9. Testes

| ID | Cenário | Esperado | Obtido | Resultado | Evidência |
|---|---|---|---|---|---|
| 2.5.5-T01 | P2 produz candidato CTX em `rascunho/` | PASS | candidato existe, `contexto/` não tem o objeto | PASS | `teste-2.5.5-T01.txt` |
| 2.5.5-T02 | Candidato sem curadoria não é consumido | RECUSA | `consultar.py` recusa | PASS | `teste-2.5.5-T02.txt` |
| 2.5.5-T03 | Candidato curado entra no CTX | PASS | curado, rc=0 | PASS | `teste-2.5.5-T03.txt` |
| 2.5.5-T04 | P3b gera Regra rastreável | PASS | RN-001 (I) curada referenciando T-001 | PASS | `teste-2.5.5-T04.txt` |
| 2.5.5-T05 | P3d atualiza confronto sem sobrescrever | PASS/RECUSA | DIV curada; mudança sem histórico recusada | PASS | `teste-2.5.5-T05.txt` |
| 2.5.5-T05b | Mesmo cenário com histórico correto | PASS | v2 curada com histórico | PASS | `teste-2.5.5-T05b.txt` |
| 2.5.5-T06 | P4 consome contexto válido | PASS | `quadro.py` exit 0 | PASS | `teste-2.5.5-T06.txt` |
| 2.5.5-T07 | P4 com `contexto/regras/` vazio | PASS c/ alerta | roda, 0 regras, célula crítica vazia sinalizada | PASS | `teste-2.5.5-T07.txt` |
| 2.5.5-T08 | P4 não reinfere valor curado | PASS | `quadro.py` lê `r.get(...)` do YAML, sem chamada a LLM | PASS | `teste-2.5.5-T08.txt` |
| 2.5.5-T09 | P5 consome os sete campos centrais | PASS | `consultar.py --campo` retorna exatamente os sete | PASS | `teste-2.5.5-T09.txt` |
| 2.5.5-T10 | P5 com Regra incompleta | RECUSA | nunca cura, nunca é consultável | PASS | `teste-2.5.5-T10.txt` |
| 2.5.5-T11 | P5 distingue I de V | PASS | `procedencia: I` exposta, não mascarada | PASS | `teste-2.5.5-T11.txt` |
| 2.5.5-T12 | P5 com V válida | PASS | `procedencia: V` consultável | PASS | `teste-2.5.5-T12.txt` |
| 2.5.5-T13 | CTX inválido não é consumido | RECUSA | referência quebrada bloqueia curadoria e consulta | PASS | `teste-2.5.5-T13.txt` |
| 2.5.5-T14 | Evento de falha de consumo | RECUSA + evento | `CuradoriaRecusada` registrado | PASS | `teste-2.5.5-T14.txt` |
| 2.5.5-T15 | Fluxo mínimo P2 → CTX → P4 | PASS | T-001 (P2) → RN-001 (P3b) → `quadro.py` (P4), exit 0 | PASS | `teste-2.5.5-T15.txt` |
| 2.5.5-T16 | Fluxo mínimo P3 → CTX → P5 | PASS | RN-001 (P3d, V, divergente) → `consultar.py` (P5), exit 0 | PASS | `teste-2.5.5-T16.txt` |
| 2.5.5-T17 | Regressão completa (113 verificações) | sem regressão | 113/113 PASS | PASS | `teste-regressao-final.txt` |

## 10. Controles positivos

| Negativo | Positivo correspondente |
|---|---|
| Candidato não curado (T02) | Candidato curado (T03) |
| P4 sem contexto útil (T07, alerta) | P4 com contexto válido (T06) |
| P5 com Regra incompleta (T10) | P5 com Regra completa (T09) |
| I quando decisão exige V — nunca mascarada (T11) | V válida consultável (T12) |
| Objeto CTX inválido (T13) | Objeto CTX válido em todo o resto da suíte |
| Mudança de confronto sem histórico (T05) | Mudança de confronto com histórico (T05b) |

## 11. Prova de não reinterpretação

`quadro.py` (consumido por P4) lê `r.get("frequencia")` e
`r.get("consequencia_do_erro")` diretamente do dicionário resultante do
parse do YAML curado — não há chamada a modelo de linguagem no arquivo
(confirmado por inspeção do próprio código-fonte no teste T08, não por
alegação). O mesmo vale para `consultar.py`: a saída de
`--campo frequencia` é o valor literal do campo no arquivo YAML, não uma
súmula gerada.

## 12. Fluxo mínimo ponta a ponta

**T15 (P2 → CTX → P4):** `T-001` curado (P2, `I`) → `RN-001` curado (P3b,
referenciando `T-001` em `entradas`) → `quadro.py` roda sobre
`contexto/regras/`, exit 0. IDs rastreáveis: `T-001`, `RN-001`.

**T16 (P3 → CTX → P5):** `RN-001` atualizado para `V` com
`classificacao_confronto.classe: divergente` e `referencia_p3d: DIV-001`
(P3d), versão 2 com histórico da versão 1 preservado → `consultar.py --id RN-001`
(P5), exit 0, retorna `procedencia: V`. IDs rastreáveis: `RN-001`, `DIV-001`.

## 13. Eventos

`eventos.jsonl` desta evidência: `ObjetoContextoCurado` (Termo T-001, P2),
`ObjetoContextoCurado` (Regra RN-001, P3b, referenciando T-001),
`CuradoriaRecusada` (Regra RN-002 com referência quebrada — o cenário que
bloquearia consumo por P4/P5).

## 14. Regressão

- **Antes:** 96 total / 96 PASS / 0 FAIL / 0 SKIP. Ver `teste-regressao-inicial.txt`.
- **2.5.5:** 17 total / 17 PASS / 0 FAIL.
- **Depois:** 113 total / 113 PASS / 0 FAIL / 0 SKIP. Ver `teste-regressao-final.txt`.

## 15. Defeitos encontrados

**Defeito real em `quadro.py` (pré-existente, não introduzido por este
pacote):** o script tratava `entradas: []` e `excecoes_conhecidas: []`
como "campo central ausente", quando o schema já os considera válidos
sem conteúdo (`required` sem `nonempty`) — o mesmo tratamento que
`decisor_quando_nao_cobre` já recebia dentro do próprio `quadro.py`.
Descoberto ao montar o fluxo mínimo P2→CTX→P4 (T06/T15): uma Regra
recém-curada e estruturalmente válida era sinalizada como "incompleta"
pelo quadro, o que teria bloqueado P4 desnecessariamente.

## 16. Correções e retestes

`CENTRAL`/`NAO_EXIGE_CONTEUDO` em `quadro.py`: a checagem de campo
"ausente" passou de `r.get(c) in (None, "", [])` para `c not in r`,
exceto para os três campos que o próprio CTX-01 3.6 não exige terem
conteúdo não-trivial (`decisor_quando_nao_cobre`, `entradas`,
`excecoes_conhecidas`). Retestado com Regra genuinamente incompleta
(`estabilidade` removida do arquivo curado) — `quadro.py` continua
recusando corretamente (rc=1).

## 17. Itens adiados

- **2.5.6:** verificação consolidada da camada.
- **Ação 2.6:** contrato executável F0–P10, P6–P10, 18 HB, 4 AG, portões E4/E5, geração de entregáveis.

Este pacote não implementou dependência de etapa nova em
`avancar.py`/`playbook.json` (isso é o contrato F0–P10 da ação 2.6), nem
criou objeto CTX para medição de P3a, nem exigiu `V` globalmente em P5.

## 18. Commit

Ver `git-show.txt` e `diff.patch` neste diretório.

## 19. Estado final

**CONFORME.**

**Indicadores da camada:**
- P2/P3 → CTX: **IMPLEMENTADO**
- CTX → P4: **IMPLEMENTADO**
- CTX → P5: **IMPLEMENTADO**
- Recusas de contexto auditáveis: **SIM**

Todos os 16 critérios de pronto do pacote (§41 da instrução) foram
atendidos: P2 e P3 com caminho demonstrável de alimentação/atualização do
contexto; conteúdo candidato nunca curado automaticamente; contexto
válido passa pelas CTX-V já formalizadas (2.5.4); P4 consome dado
estruturado (`quadro.py`); P5 consome os sete campos centrais
(`consultar.py`); P5 distingue D/I/V sem tratar I como V; contexto
incompleto produz recusa explícita (curadoria ou consulta); contexto
completo tem caminho positivo; prova de não reinterpretação demonstrada
por inspeção de código, não por alegação; percurso mínimo P2/P3→CTX→P4/P5
demonstrado com IDs rastreáveis; recusas auditáveis via `eventos.jsonl`;
suíte anterior sem regressão; evidências persistidas; RTE-01 atualizado;
máquina F0–P10 não antecipada.
