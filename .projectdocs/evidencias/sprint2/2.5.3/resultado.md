# Pacote 2.5.3 — Integração CTX ↔ P3d

## 1. Identificação

- **Ação:** 2.5 — Contexto e Dados
- **Pacote:** 2.5.3
- **Data/hora:** 18/09/2026, execução única de implementação e testes
- **Branch:** `master`
- **HEAD inicial:** `c67ea6219c6c78232850e66641ec05349cd83abe`
- **HEAD final:** ver `git-show.txt` (commit criado ao final deste pacote)

## 2. Documentos consultados

| Documento | Versão | Papel |
|---|---:|---|
| EMCIA-CTX-01 | 0.4 | Contrato de `classificacao_confronto`/`referencia_p3d` (§3.5), separação CTX × P3d (§3.11), condição CTX-V11 (§3.13). |
| EMCIA-ROT-01 | — | Única fonte com a taxonomia oficial das classes de confronto (§3.9): `alinhada`, `divergente`, `não documentada`, `órfã`, `escrita-mas-inacessível`. Não há instrumento estruturado de P3d com IDs próprios documentado em lugar nenhum — o §3.9 só descreve o resultado do P3d em prosa, e `hb-confrontar` produz `caso/P3d-divergencias.md` em texto livre. |
| EMCIA-MET-01 | — | Posição do P3d no percurso (dentro do Passo 3). |
| EMCIA-CAT-01 | — | P3d é `EX3`; confirma que o agente prepara e organiza, não confirma o confronto. |
| EMCIA-TRA-01 | — | Nenhuma divergência aplicável encontrada. |
| EMCIA-ESP-01 | — | Separação núcleo/campo preservada. |
| EMCIA-TST-01 | — | Convenção de teste negativo + controle positivo. |
| `eiac-campo/skills/hb-confrontar/SKILL.md`, `eiac-campo/commands/confrontar.md` | — | Confirmam que a saída atual de P3d é `caso/P3d-divergencias.md` (asserção livre), sem estrutura endereçável por ID. |

**Achado que exigiu decisão de implementação (registrado, não resolvido em silêncio):** o CTX-01 pressupõe um "instrumento de P3d" cujos registros `referencia_p3d` resolve — mas nenhum documento oficial nem código define esse instrumento em forma estruturada e endereçável. A saída real do P3d hoje é prosa em `caso/`. Não havia decisão registrada em `decisoes/` sobre esse ponto. Antes de implementar, essa lacuna foi levada ao usuário, que aprovou a introdução de um registro estruturado mínimo (`contexto/divergencias/DIV-*.yaml`, schema próprio) como decisão de implementação deste pacote — não como redesenho do método de confronto. O texto livre de `hb-confrontar`/`caso/P3d-divergencias.md` não foi alterado nem removido; o registro estruturado é o que se grava depois, como resultado curado e endereçável do que já foi decidido na sessão de confronto — mesma relação que já existe entre `caso/` (prosa) e `contexto/regras/` (YAML curado) para P2/P3b.

## 3. Baseline relacionado

D-04, 2.5-BL14, 2.5-BL15.

## 4. Estado inicial

| Requisito | Estado | Evidência | Lacuna |
|---|---|---|---|
| Classificação de confronto P3d (2.5-BL14) | PARCIAL | `classificacao_confronto` já existia no schema desde 2.5.1, com `classe`/`referencia_p3d`, mas sem enum — qualquer string passava. `estatuto`/`divergencia` (contrato antigo apontado pelo baseline) já haviam sido removidos no 2.5.1 (ver `.projectdocs/evidencias/sprint2/2.5.1/resultado.md` §6). | Nenhuma taxonomia verificada; nenhuma instância antiga restante para migrar. |
| Referência para P3d (2.5-BL15) | AUSENTE | `referencia_p3d` existia como campo de string livre, sem verificação de existência nem de resolução. | Uma `referencia_p3d` apontando para nada era aceita silenciosamente. |

## 5. Taxonomia oficial do confronto

| Código/valor | Significado | Fonte documental |
|---|---|---|
| `alinhada` | Regra escrita corresponde à regra praticada. | EMCIA-ROT-01 §3.9 |
| `divergente` | Regra escrita e regra praticada não coincidem. | EMCIA-ROT-01 §3.9 |
| `nao_documentada` | Regra praticada sem correspondente escrito. | EMCIA-ROT-01 §3.9 ("não documentada") |
| `orfa` | Regra escrita sem correspondente prática observável. | EMCIA-ROT-01 §3.9 ("órfã") |
| `escrita_inacessivel` | Regra escrita existe, mas a fonte é inacessível para confronto. | EMCIA-ROT-01 §3.9 ("escrita-mas-inacessível") |

Os slugs (`nao_documentada`, `orfa`, `escrita_inacessivel`) são normalização ortográfica/técnica dos termos em prosa do ROT-01 — nenhum documento define códigos formais; a normalização segue o mesmo padrão já usado para os demais enums do schema (`snake_case`, sem acento). Não foram inventadas classes adicionais nem removida nenhuma das cinco.

## 6. Contrato CTX × P3d

**Fica no CTX (Regra):** `classificacao_confronto.classe` (uma das cinco classes oficiais) e `classificacao_confronto.referencia_p3d` (obrigatória e resolvível somente quando `classe: divergente` — a única classe para a qual o CTX-01 §3.5 descreve o conteúdo mínimo exigido do registro referenciado).

**Fica no P3d (`contexto/divergencias/DIV-*.yaml`, novo):** `regra_confrontada`, `classe`, `documento_diz`, `observado`, `justificativa`, `autor`, `data` — o detalhamento completo do confronto.

**O que deixou de ser duplicado:** nada foi duplicado nesta implementação — o schema de Regra nunca chegou a ganhar `documento_diz`/`observado`/`justificativa` (verificado e confirmado pelo teste 2.5.3-T07). A duplicação anterior (`estatuto`/`divergencia`) já havia sido removida no 2.5.1.

## 7. Mapeamento do schema antigo

| Campo antigo | Destino | Ação |
|---|---|---|
| `estatuto` (Regra, pré-2.5.1) | — | REMOVER — já executado no 2.5.1; confirmado neste pacote (T08) que não existe no schema atual. |
| `divergencia` (Regra, pré-2.5.1) | `classificacao_confronto` | SUBSTITUIR POR REFERÊNCIA — já executado no 2.5.1; este pacote adicionou a resolução real da referência. |
| `registrada_em` (achado do baseline) | — | Não encontrado em nenhum arquivo do repositório atual (templates, testes, evidências). Nada a migrar; achado já historicamente superado antes deste pacote. |
| `classificacao_confronto.classe` (string livre, 2.5.1) | `classificacao_confronto.classe` (enum de 5 valores) | MIGRAR — adicionado enum no schema; nenhuma instância real existia para conversão. |
| `classificacao_confronto.referencia_p3d` (string livre, sem resolução) | `classificacao_confronto.referencia_p3d` (resolve contra `contexto/divergencias/`) | ADIAR PARCIAL → RESOLVER — a exigência de existência foi implementada; validação genérica para todos os objetos CTX (bateria CTX-V01–V11) fica para 2.5.4. |

Não havia instâncias de caso real com nenhum desses campos — só templates e testes, confirmado por busca em todo o repositório (§19 da instrução do pacote).

## 8. Alterações realizadas

| Arquivo | Alteração | Justificativa |
|---|---|---|
| `eiac-campo/template-caso/registro/p3d.schema.json` (novo) | Schema declarativo do objeto `divergencia`: `id`, `regra_confrontada`, `classe` (enum das 5 classes oficiais), `documento_diz`, `observado`, `justificativa`, `autor`, `data`. | Registro estruturado mínimo do confronto P3d, decisão de implementação aprovada (§2). |
| `eiac-campo/template-caso/contexto/divergencias/DIV-000-modelo.yaml` (novo) | Modelo do registro de confronto. | Mesmo padrão dos outros quatro `*-000-modelo.yaml`. |
| `eiac-campo/template-caso/registro/contexto.schema.json` | Adicionado `classificacao_confronto.classe` ao bloco `enums` da Regra, com as 5 classes oficiais. | Fecha 2.5-BL14: taxonomia agora verificada, não string livre. |
| `eiac-nucleo/scripts/curar.py` | `checar_confronto()`: quando `classe == "divergente"`, exige `referencia_p3d` preenchida e resolvível contra `contexto/divergencias/<id>.yaml`. `checar_versao()` generalizado: mudança em `classificacao_confronto` (não só em `procedencia`) agora também exige versão nova com histórico. `checar_autoria()` passa a considerar também o campo `autor` (do registro P3d). `--schema` tornou-se parametrizável na CLI para permitir curar contra `p3d.schema.json`. | Fecha 2.5-BL15 (CTX-V11 mínimo); preserva o regime de versionamento do 2.5.2 estendendo-o à mudança de confronto, conforme CTX-01 §3.12 ("toda alteração cria uma nova versão"). |
| `eiac-nucleo/commands/curar.md` | Documenta `--schema` e o caminho de curadoria de `divergencia`. | Rastreabilidade do comando. |
| `eiac-nucleo/README.md` | Invariantes I-15 (generalizado) e I-16 (novo). | Rastreabilidade dos invariantes do núcleo. |
| `eiac-campo/template-caso/CLAUDE.md`, `eiac-campo/template-caso/contexto/README.md` | Documentam `contexto/divergencias/`, a taxonomia oficial e a regra de resolução de referência. | Orientação para quem opera o caso. |
| `eiac-campo/template-caso/contexto/regras/RN-000-modelo.yaml` | Comentário do bloco `classificacao_confronto` corrigido (`inacessivel` → `escrita_inacessivel`) e atualizado para apontar ao CTX-01 em vez de "pertence ao pacote 2.5.3". | O pacote que o comentário anunciava foi concluído. |
| `testes/p3d.py` (novo) | 12 testes (T01–T12 do mínimo obrigatório). | EMCIA-TST-01; negativa + controle positivo por trava. |
| `testes/README.md` | Documenta a suíte nova; total acumulado 61 → 73. | Rastreabilidade dos testes. |
| `eiac-nucleo/.claude-plugin/plugin.json` | `0.2.8` → `0.2.9`. | `curar.py` mudou. |
| `eiac-campo/.claude-plugin/plugin.json` | `0.3.5` → `0.3.6`. | Template do caso ganhou schema, diretório e modelo novos. |

## 9. Testes

| ID | Cenário | Esperado | Obtido | Resultado | Evidência |
|---|---|---|---|---|---|
| 2.5.3-T01 | Classificação oficial válida (`alinhada`) | PASS | curado, rc=0 | PASS | `teste-2.5.3-T01.txt` |
| 2.5.3-T02 | Classificação fora da taxonomia | RECUSA | rc≠0, msg "classificacao_confronto.classe" | PASS | `teste-2.5.3-T02.txt` |
| 2.5.3-T03 | `divergente` sem `referencia_p3d` | RECUSA | rc≠0, msg "exige referencia_p3d preenchida" | PASS | `teste-2.5.3-T03.txt` |
| 2.5.3-T04 | `divergente` com `referencia_p3d` inexistente | RECUSA | rc≠0, msg "nao resolve para registro existente" | PASS | `teste-2.5.3-T04.txt` |
| 2.5.3-T05 | `divergente` com `referencia_p3d` válida | PASS | DIV curada, RN curada, rc=0 | PASS | `teste-2.5.3-T05.txt` |
| 2.5.3-T06 | Referência resolve para o registro correto | PASS | conteúdo do DIV recuperado contém `regra_confrontada` e detalhe esperados | PASS | `teste-2.5.3-T06.txt` |
| 2.5.3-T07 | CTX não duplica detalhe da divergência | PASS | Regra curada sem `documento_diz`/`observado`/`justificativa` | PASS | `teste-2.5.3-T07.txt` |
| 2.5.3-T08 | Estrutura antiga (`estatuto`/`divergencia`) não existe mais | PASS | ausentes do schema desde 2.5.1; Regra atual cura normalmente | PASS | `teste-2.5.3-T08.txt` |
| 2.5.3-T09 | Classificação que não exige `referencia_p3d` (`nao_documentada`) | PASS | curada sem referência | PASS | `teste-2.5.3-T09.txt` |
| 2.5.3-T10 | Atualização do confronto preserva histórico | RECUSA sem histórico; PASS com | v1 sem confronto curada; mudança de `classificacao_confronto` sem versão nova recusada ("sobrescrita"); com versão nova e histórico, aceita | PASS | `teste-2.5.3-T10.txt` |
| 2.5.3-T11 | Agente não confirma confronto humano | RECUSA | rc≠0, `autor` agente recusado | PASS | `teste-2.5.3-T11.txt` |
| 2.5.3-T12 | Controle humano válido | PASS | registro de confronto curado por pessoa nomeada | PASS | `teste-2.5.3-T12.txt` |
| 2.5.3-T13 | Regressão completa (73 verificações) | sem regressão | 73/73 PASS | PASS | `teste-regressao-final.txt` |

Nenhum teste ficou NÃO APLICÁVEL: a taxonomia oficial tem exatamente uma classe (`divergente`) que exige vínculo, o que deu conteúdo real a T03/T04/T05 e a T09 (classe que não exige).

## 10. Controles positivos

| Negativo | Positivo correspondente |
|---|---|
| Divergência sem referência (T03) | Divergência com referência válida (T05) |
| Referência inexistente (T04) | Referência resolvível (T05, T06) |
| Classificação inválida (T02) | Classificação oficial (T01) |
| Agente substituindo confirmação humana (T11) | Registro humano autorizado (T12) |
| Mudar confronto sem versão nova (dentro de T10) | Mudar confronto com versão nova e histórico (dentro de T10) |

Nenhuma trava deste pacote recusa sem que exista o caminho positivo correspondente comprovado por teste.

## 11. Regressão

- **Antes:** 61 total / 61 PASS / 0 FAIL / 0 SKIP (33 + 11 + 17). Ver `teste-regressao-inicial.txt`.
- **Depois:** 73 total / 73 PASS / 0 FAIL / 0 SKIP (33 + 11 + 17 + 12 de `p3d.py`). Ver `teste-regressao-final.txt`.
- **Testes 2.5.3:** 12 total / 12 PASS / 0 FAIL.

## 12. Eventos

`eventos.jsonl` desta evidência contém, em ordem: `ObjetoContextoCurado` (registro `divergencia` DIV-001), `ObjetoContextoCurado` (Regra RN-001 com `classe: divergente` e `referencia_p3d: DIV-001` resolvida), `CuradoriaRecusada` (referência inexistente DIV-999) e `CuradoriaRecusada` (classe fora da taxonomia).

## 13. Defeitos encontrados

Nenhum defeito de código foi encontrado nos pacotes anteriores. O único achado deste pacote foi documental: a ausência de um instrumento estruturado de P3d pressuposto pelo CTX-01 mas nunca definido em nenhum documento oficial — tratado como decisão de implementação (§2), não como defeito de código a corrigir.

## 14. Correções e retestes

Não houve correção de defeito de código pré-existente — o pacote implementou requisitos previamente ausentes ou parciais (D-04, 2.5-BL14, 2.5-BL15). Todos os 12 testes passaram na primeira execução após a implementação; nenhum reteste de correção foi necessário.

## 15. Migração de registros antigos

Não aplicável. Nenhuma instância real de caso com `estatuto`, `divergencia`, `registrada_em` ou `classificacao_confronto` foi encontrada no repositório (só templates e testes, já cobertos no mapeamento §7). A migração estrutural do formato antigo já havia sido concluída no pacote 2.5.1.

## 16. Itens adiados

- **2.5.4:** bateria formal CTX-V01–V11 completa; resolvedor genérico para Termo, Entidade e Fonte referenciados por Regra (`entradas`); generalização da verificação de referência além de `referencia_p3d`.
- **2.5.5:** integração executável P2/P3 → CTX → P4/P5.
- **2.5.6:** verificação consolidada da camada.
- **Ação 2.6:** agentes e protocolos, P6–P10, 18 HB, 4 AG, portões E4/E5, geração de entregáveis.

Este pacote não redefiniu o método de confronto nem transformou P3d em etapa automatizada: `hb-confrontar`, `confrontar.md` e a fronteira EX3 do P3d permanecem inalterados. O registro estruturado em `contexto/divergencias/` é curado pelo mesmo caminho humano (`curar.py`, autoria de pessoa nomeada) já em vigor desde o 2.5.2.

## 17. Commit

Ver `git-show.txt` e `diff.patch` neste diretório.

## 18. Estado final

**CONFORME.**

Todos os 15 critérios de pronto do pacote (§36 da instrução) foram atendidos:
taxonomia oficial extraída de EMCIA-ROT-01 §3.9 (não inventada), Regra CTX
registra classificação, `referencia_p3d` disponível e resolúvel, divergência
sem referência obrigatória recusada, referência inexistente recusada,
referência válida com caminho positivo comprovado, detalhamento permanece
no registro P3d sem duplicação na Regra, histórico/curadoria do 2.5.2
preservados e estendidos (não contornados), fronteira humana do P3d
inalterada, testes negativos e positivos executados, sem regressões,
evidências persistidas, RTE-01 atualizado, e CTX-V01–V11 completas não
declaradas como concluídas (apenas o comportamento mínimo de CTX-V11 para
a classe `divergente`).
