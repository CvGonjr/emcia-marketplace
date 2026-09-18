# Pacote 2.5.2 — Curadoria, autoria e versionamento I→V

## 1. Identificação

- **Ação:** 2.5 — Contexto e Dados
- **Pacote:** 2.5.2
- **Data/hora:** 18/09/2026, execução única de implementação e testes
- **Branch:** `master`
- **HEAD inicial:** `61af78ce2886757be2c110ddca8a6a714a272421`
- **HEAD final:** ver `git-show.txt` (commit criado ao final deste pacote)

## 2. Documentos consultados

| Documento | Versão | Papel |
|---|---:|---|
| EMCIA-CTX-01 | 0.4 | Contrato de curadoria (§3.11), autoria (§3.5, §3.8), versionamento e regra de não conversão (§3.12), condições executáveis CTX-V04/V08/V09/V10 (§3.13). |
| EMCIA-ROT-01 | — | Origem das regras levantadas e correspondência de campos com o CTX-01. |
| EMCIA-CAT-01 | — | Fronteira humano/agente; catálogo AG-01–AG-04 (confirma que não há identidade tipada de ator no código, só nomes de papel). |
| EMCIA-MET-01 | — | Papel de P2/P3 na produção do que a curadoria consome. |
| EMCIA-TRA-01 | — | Procedimentos transversais; nenhuma divergência aplicável encontrada. |
| EMCIA-ESP-01 | — | Separação núcleo/campo mantida: proteção de diretório é genérica no núcleo. |
| EMCIA-TST-01 | — | Convenção de teste negativo + controle positivo, já seguida em `negativos.sh`. |
| EMCIA-RTE-01 | 0.3 | Estado registrado dos pacotes 2.5.0 e 2.5.1, baseline S2-BL. |

Nenhuma divergência semântica real entre documentos foi encontrada para este pacote.

## 3. Baseline relacionado

D-03, 2.5-BL07, 2.5-BL08, 2.5-BL09, 2.5-BL10, 2.5-BL11, 2.5-BL12, 2.5-BL13.

## 4. Estado inicial

| Requisito | Estado | Evidência | Lacuna |
|---|---|---|---|
| `autoria_conteudo` × `registrado_por` (2.5-BL07) | PARCIAL | Campos existiam no schema (2.5.1) mas sem verificação de conteúdo humano. | Nenhuma checagem de que os valores eram pessoa, não agente. |
| Evidência obrigatória para V (2.5-BL08) | JÁ IMPLEMENTADO E CONFORME | `contexto.schema.json` `conditional_nonempty.V`. | Nenhuma — herdado do 2.5.1, confirmado pelos testes T04/T05 deste pacote. |
| Premissa obrigatória para I (2.5-BL09) | JÁ IMPLEMENTADO E CONFORME | `contexto.schema.json` `conditional_nonempty.I`. | Nenhuma — confirmado pelos testes T02/T03. |
| Histórico/versionamento da Regra (2.5-BL10) | PARCIAL | Campos `versao`/`historico` existiam no schema, sem lógica comportamental. | Nada impedia sobrescrever `versao: 1` alterando só `procedencia`. |
| I → V sem sobrescrita (2.5-BL11) | AUSENTE | — | Nenhum mecanismo comparava o registro anterior ao candidato. |
| Rascunho × contexto curado (2.5-BL12) | AUSENTE | `guarda.py` protegia só `caso/`. Escrita direta em `contexto/` retornava rc=0 (achado do baseline, reproduzido no início deste pacote). | Sem G2 equivalente para `contexto/`. |
| Agente não pode ser autor de conteúdo curado (2.5-BL13) | PARCIAL/DIVERGENTE | Convenção lexical existia em `selar.py`/`avancar.py`/`validar.py`, mas (a) não cobria os objetos CTX e (b) tinha um defeito: `"AG-01".lower().startswith("ag0")` é `False` por causa do hífen — reproduzido neste pacote com `curar.py --registrado-por AG-01`, que antes da correção retornava rc=0. | Checagem ausente para `autoria_conteudo`/`declarado_por`/`registrado_por` dos objetos CTX; e a convenção existente tinha esse ponto cego lexical. |

## 5. Implementação

**Curadoria.** Novo script `eiac-nucleo/scripts/curar.py`: único caminho de escrita em `contexto/`. Lê o candidato de `rascunho/<nome>`, reaproveita `estrutura.validar()` (schema do 2.5.1) para a checagem estrutural, confere autoria e grava só se tudo passar. Não duplica `validar.py` porque os formatos são diferentes (asserção livre marcada vs. YAML estruturado por campo).

**Autoria.** `checar_autoria()` recusa `autoria_conteudo`, `declarado_por` ou `registrado_por` preenchidos com identificador de agente. `--registrado-por` na linha de comando passa pela mesma checagem — fecha o defeito de `validar.py` em que `--autor` nunca era verificado (2.5-BL13), reproduzido e corrigido também em `validar.py` nesta mesma passagem, já que é o mesmo padrão de defeito.

**`D`.** Aceito sem exigência de evidência de verificação; herda o comportamento já conforme do schema.

**`I`.** Recusado sem `premissa` (herdado do schema; confirmado pelos testes deste pacote).

**`V`.** Recusado sem `evidencia` (idem).

**Histórico e I→V.** `checar_versao()` compara o registro já curado (se existir) com o candidato. Se a `procedencia` muda, exige `versao` estritamente maior e uma entrada de `historico` referenciando a versão imediatamente anterior com `versao`, `data` e responsável (`registrado_por` ou `confirmado_por`). Sem isso, a gravação é recusada com a mensagem explícita "sobrescrita nao e permitida". Se a procedência não muda, apenas impede regressão do número de versão.

**Proteção de `contexto/`.** Nova regra G2b em `guarda.py`, espelhando G2 (que já protegia `caso/`): `Write`/`Edit`/redirecionamento de shell para `contexto/` é negado com evento `TentativaNegada`; leitura continua livre. Caminho positivo: `curar.py`.

**Convenção lexical de agente centralizada.** `autor_e_agente()` em `estado.py` substitui as três cópias (`selar.py`, `avancar.py`, `validar.py`) do mesmo teste `startswith(("ag0","agente","sistema"))`, e corrige o ponto cego do hífen (`AG-01`) normalizando espaço/hífen/underscore antes de comparar. `curar.py` usa a mesma função — não reinventa a regra.

**`rascunho/` não é contexto curado.** Não houve mudança de código para isso — é consequência estrutural do desenho: nada lê `rascunho/` como fonte de verdade fora de `curar.py`/`validar.py`, e ambos exigem passagem explícita pelo respectivo script. Confirmado pelo teste T14 (conteúdo em `rascunho/` não aparece em `contexto/` sem curadoria).

## 6. Alterações por arquivo

| Arquivo | Alteração | Justificativa |
|---|---|---|
| `eiac-nucleo/scripts/curar.py` (novo) | Curador de objetos CTX: valida, confere autoria, impõe versionamento, grava, emite evento. | CTX-V04, V08, V09, V10; §3.11–3.13 do CTX-01. |
| `eiac-nucleo/scripts/guarda.py` | G2b: escrita direta em `contexto/` negada. | CTX-V08; achado 2.5-BL12. |
| `eiac-nucleo/scripts/estado.py` | `autor_e_agente()` centralizada, tolerante a hífen/espaço/underscore. | Corrige defeito do baseline (2.5-BL13) e remove duplicação. |
| `eiac-nucleo/scripts/validar.py` | `--autor` da linha de comando agora passa por `autor_e_agente()`; checagem de autor na asserção usa a função centralizada. | Mesmo defeito do baseline existia aqui; ficaria inconsistente corrigir só em `curar.py`. |
| `eiac-nucleo/scripts/avancar.py`, `eiac-nucleo/scripts/selar.py` | Usam `estado.autor_e_agente()` em vez da checagem local duplicada. | Remove duplicação; nenhuma mudança de comportamento observável (mesma convenção, agora tolerante a hífen). |
| `eiac-nucleo/commands/curar.md` (novo) | Comando `/eiac-nucleo:curar`. | Espelha `gravar.md` para o caminho de curadoria. |
| `eiac-nucleo/README.md` | Documenta `curar.py`, invariantes I-14/I-15, nota sobre `autor_e_agente`. | Rastreabilidade dos invariantes do núcleo. |
| `eiac-campo/template-caso/CLAUDE.md` | Regra "nunca escreva direto em `contexto/`"; `contexto/` na árvore de estrutura. | Mesmo padrão já usado para `caso/`. |
| `eiac-campo/template-caso/contexto/README.md` | Documenta o curador, a exigência de versão nova em mudança de procedência. | Reflete comportamento novo. |
| `eiac-campo/template-caso/contexto/regras/RN-000-modelo.yaml` | Comentário que apontava para "pacote 2.5.2" substituído pela regra real. | O pacote que o comentário anunciava foi concluído. |
| `testes/curadoria.py` (novo) | 17 testes (T01–T16 do mínimo obrigatório + um teste extra do achado específico do baseline). | EMCIA-TST-01; negativa + controle positivo por trava. |
| `testes/README.md` | Documenta a suíte nova; total acumulado 44 → 61. | Rastreabilidade dos testes. |
| `eiac-nucleo/.claude-plugin/plugin.json` | `0.2.7` → `0.2.8`. | Scripts do núcleo mudaram (CLAUDE.md raiz exige bump). |
| `eiac-campo/.claude-plugin/plugin.json` | `0.3.4` → `0.3.5`. | Template do caso mudou (doc e comentário de modelo). |

## 7. Testes

| ID | Cenário | Esperado | Obtido | Resultado | Evidência |
|---|---|---|---|---|---|
| 2.5.2-T01 | D com autoria humana válida | PASS | curado, rc=0 | PASS | `teste-2.5.2-T01.txt` |
| 2.5.2-T02 | I sem premissa | RECUSA | rc≠0, msg "premissa" | PASS | `teste-2.5.2-T02.txt` |
| 2.5.2-T03 | I com premissa | PASS | curado, rc=0 | PASS | `teste-2.5.2-T03.txt` |
| 2.5.2-T04 | V sem evidência | RECUSA | rc≠0, msg "evidencia" | PASS | `teste-2.5.2-T04.txt` |
| 2.5.2-T05 | V com evidência | PASS | curado, rc=0 | PASS | `teste-2.5.2-T05.txt` |
| 2.5.2-T06 | agente como `autoria_conteudo` | RECUSA | rc≠0, msg específica | PASS | `teste-2.5.2-T06.txt` |
| 2.5.2-T07 | pessoa como `autoria_conteudo` | PASS | curado, rc=0 | PASS | `teste-2.5.2-T07.txt` |
| 2.5.2-T08 | `registrado_por` ≠ `autoria_conteudo` | PASS | papéis distintos preservados no arquivo gravado | PASS | `teste-2.5.2-T08.txt` |
| 2.5.2-T09 | sobrescrever I por V sem versão nova | RECUSA | v1 curada; sobrescrita para V recusada com "sobrescrita nao e permitida" | PASS | `teste-2.5.2-T09.txt` |
| 2.5.2-T10 | I → V com nova versão | PASS | v1 (I) e v2 (V, com histórico) curadas | PASS | `teste-2.5.2-T10.txt` |
| 2.5.2-T11 | histórico preservado | PASS | v1 (I) legível dentro do arquivo v2 | PASS | `teste-2.5.2-T11.txt` |
| 2.5.2-T12 | escrita direta em `contexto/` | RECUSA | guarda bloqueia, rc=2 | PASS | `teste-2.5.2-T12.txt` |
| 2.5.2-T13 | escrita autorizada em `contexto/` | PASS | curadoria grava, rc=0 | PASS | `teste-2.5.2-T13.txt` |
| 2.5.2-T14 | rascunho não é contexto curado | PASS | conteúdo em `rascunho/` não aparece em `contexto/` | PASS | `teste-2.5.2-T14.txt` |
| 2.5.2-T15 | recusa gera evento | RECUSA + evento | `CuradoriaRecusada` em `eventos.jsonl` | PASS | `teste-2.5.2-T15.txt` |
| 2.5.2-T16 | operação válida gera trilha | PASS + evento | `ObjetoContextoCurado` em `eventos.jsonl` | PASS | `teste-2.5.2-T16.txt` |
| 2.5.2-T-extra | `--registrado-por AG-01` (achado específico do baseline, §27) | RECUSA | rc≠0, msg "pessoa nomeada" | PASS | `teste-2.5.2-T-extra-baseline.txt` |
| 2.5.2-T17 | regressão completa (61 verificações) | sem regressão | 61/61 PASS | PASS | `teste-regressao-final.txt` |

## 8. Controles positivos

| Negativo | Positivo correspondente |
|---|---|
| Agente como `autoria_conteudo` (T06) | Pessoa como `autoria_conteudo` (T07) |
| I sem premissa (T02) | I com premissa (T03) |
| V sem evidência (T04) | V com evidência (T05) |
| Sobrescrever I por V sem histórico (T09) | Criar nova versão V com histórico (T10) |
| Escrita direta em `contexto/` (T12) | Gravação pelo curador (T13) |
| `--registrado-por AG-01` (T-extra) | `--registrado-por` com pessoa nomeada (T01, T05, T10, T13 etc.) |

Nenhuma trava deste pacote recusa sem que exista o caminho positivo correspondente comprovado por teste.

## 9. Regressão

- **Antes:** 44 total / 44 PASS / 0 FAIL / 0 SKIP (33 de `negativos.sh` + 11 de `contexto.py`). Ver `teste-regressao-inicial.txt`.
- **Depois:** 61 total / 61 PASS / 0 FAIL / 0 SKIP (33 + 11 + 17 de `curadoria.py`). Ver `teste-regressao-final.txt`.
- **Novos testes do pacote:** 17 total / 17 PASS / 0 FAIL.

## 10. Defeitos encontrados

- **Reprodução do achado do baseline (§27 do pacote):** `validar.py --autor AG-01` nunca verificava o valor de `--autor` contra a convenção de nome de agente — só era usado para o evento. `rc=0` mesmo com autor identificado como agente.
- **Defeito adicional descoberto durante a implementação (não estava no baseline nem era esperado):** a convenção lexical `startswith(("ag0","agente","sistema"))`, já usada em `selar.py`/`avancar.py`/`validar.py` desde pacotes anteriores, não cobria `"AG-01"` com hífen — `"ag-01".startswith("ag0")` é `False`. Os testes anteriores (`testes/negativos.sh` #6, #15, #18) só usavam `AG05` (sem hífen), por isso o ponto cego nunca apareceu antes. Reproduzido em `curar.py --registrado-por AG-01` e em `autoria_conteudo: AG-01` durante o desenvolvimento deste pacote.

## 11. Correções realizadas

- `curar.py --registrado-por` e o conteúdo de `autoria_conteudo`/`declarado_por`/`registrado_por` passam por `autor_e_agente()`.
- `validar.py --autor` passa a ser verificado (fecha o achado original do baseline).
- `autor_e_agente()` centralizada em `estado.py`, tolerante a hífen/espaço/underscore no separador entre "ag" e o número — fecha o defeito adicional.
- `selar.py`, `avancar.py` e `validar.py` passaram a usar a função centralizada em vez de três cópias divergentes da mesma regra.

## 12. Retestes

Após as duas correções, os testes T06, T08, T15 e T-extra (e os testes 6/15/18 já existentes de `negativos.sh`) foram reexecutados com `AG05` e `AG-01` como entrada — ambos recusados. Suíte completa reexecutada com 61/61 PASS (`teste-regressao-final.txt`).

## 13. Eventos

`eventos.jsonl` desta evidência contém, em ordem: `ObjetoContextoCurado` (criação v1, `I`), `CuradoriaRecusada` (agente como autor), `ObjetoContextoCurado` (transição para v2, `V`, com `versao_anterior: 1`), `TentativaNegada` (bypass de escrita direta em `contexto/`).

## 14. Itens adiados

- **2.5.3:** semântica completa de `classificacao_confronto` e obrigatoriedade de `referencia_p3d`.
- **2.5.4:** CTX-V01–V11 como bateria formal completa; validação referencial entre objetos (Termo, Entidade, Fonte referenciados por Regra).
- **2.5.5:** integração executável P2/P3 → CTX → P4/P5.
- **2.5.6:** verificação consolidada da camada.
- **Ação 2.6:** agentes e protocolos, P6–P10, 18 HB, 4 AG, portões E4/E5, geração de entregáveis.

Nenhum desses itens foi antecipado. `curar.py` verifica apenas estrutura, autoria e versionamento — não resolve referências entre Regra e Termo/Entidade/Fonte, nem interpreta `classificacao_confronto` além de sua presença estrutural (herdada do 2.5.1).

## 15. Commit

Ver `git-show.txt` e `diff.patch` neste diretório.

## 16. Estado final

**CONFORME.**

Todos os 18 critérios de pronto do pacote (§39 da instrução) foram atendidos:
autoria dupla com semântica distinta, agente recusado como autor de conteúdo
curado, D/I/V com caminhos positivo e negativo comprovados, I→V só por versão
nova, histórico recuperável, escrita direta em `contexto/` bloqueada com
caminho positivo real, `rascunho/` não tratado como curado, recusas com
trilha auditável, suíte anterior sem regressão, evidências persistidas,
RTE-01 atualizado, e nenhum item de 2.5.3 em diante antecipado.
