# Pacote 2.5.1 — Materialização dos quatro objetos CTX

## 1. Identificação

- **Ação:** 2.5 — Camada de Contexto e Dados
- **Pacote:** 2.5.1
- **Execução:** 18/09/2026, 15:53–16:08 -0300
- **Branch:** `master`
- **HEAD inicial:** `5421c78edaeb074c3d14e61e6686be42431a2c56`
- **Commit de implementação:** `92179256f078880f92fbfe5d395ee4a61dccfbf7`
- **HEAD técnico final:** `92179256f078880f92fbfe5d395ee4a61dccfbf7`
- **eiac-nucleo:** 0.2.6 → 0.2.7
- **eiac-campo:** 0.3.3 → 0.3.4
- **Playbook:** 0.3.1, sem alteração
- **Schema CTX:** 0.1.0

## 2. Documentos consultados

| Documento | Versão | Papel na decisão |
|---|---:|---|
| EMCIA-CTX-01 | 0.4 | Fonte canônica dos quatro objetos e dos sete campos da Regra. |
| EMCIA-MET-01 | 0.1 | Encaixe em P2–P5 e profundidade por nível. |
| EMCIA-ROT-01 | 0.1 | Origem, autoria, gatilho, exceções e procedência das regras. |
| EMCIA-GLO-01 | 0.1 | Terminologia de contexto, entidade, contrato de dados e D/I/V. |
| EMCIA-E2 | 0.1 | Consumo de termos, fontes e regras pelo diagnóstico. |
| EMCIA-E3 | 0.1 | Consumo dos objetos pelas camadas CA4 e CA5. |
| EMCIA-ESP-01 | 0.2 | Contrato executável, separação dos plugins e D/I/V. |
| EMCIA-TST-01 | 0.1 | Testes estruturais, negativas e controles positivos. |

## 3. Baseline relacionado

- D-02 — quatro objetos CTX ainda no schema anterior;
- 2.5-BL03 — Termo implementado, mas divergente;
- 2.5-BL04 — Entidade implementada, mas divergente;
- 2.5-BL05 — Regra implementada, mas divergente;
- 2.5-BL06 — Fonte implementada, mas divergente.

## 4. Estado inicial

| Objeto | Estado | Evidência | Lacuna |
|---|---|---|---|
| Termo | IMPLEMENTADO MAS DIVERGENTE | `T-000-modelo.yaml` | `autor/fonte` não representavam os metadados do CTX-01 v0.4. |
| Entidade | IMPLEMENTADO MAS DIVERGENTE | `E-000-modelo.yaml` | Mesmo desvio de autoria/rastreabilidade do Termo. |
| Regra | IMPLEMENTADO MAS DIVERGENTE | `R-000-modelo.yaml` | Prefixo, gatilho, autoria, origem e confronto divergentes; `estatuto/divergencia` duplicavam o P3d. |
| Fonte | IMPLEMENTADO MAS DIVERGENTE | `F-000-modelo.yaml` | Ausência de `registrado_por` e contrato ainda não verificável estruturalmente. |

Não foram encontradas instâncias reais em `/home/netiv-ai/Projetos`; somente
os quatro templates deste repositório. Nenhum dado de caso foi migrado.

## 5. Matriz schema atual × CTX-01

A extração integral anterior à implementação está em
`matriz-schema-inicial.md`. Síntese das decisões:

| Objeto | Campo atual | Campo alvo | Ação |
|---|---|---|---|
| Termo | `autor`, `fonte` | `declarado_por`, `registrado_por`, premissa/evidência | migrar estrutura |
| Entidade | `autor`, `fonte` | `declarado_por`, `registrado_por`, premissa/evidência | migrar estrutura |
| Regra | `R-*` | `RN-*` | renomear |
| Regra | ausentes | `gatilho`, `autoria_conteudo`, `registrado_por`, `origem_do_conhecimento` | adicionar |
| Regra | `estatuto`, `divergencia` | `classificacao_confronto` | remover duplicação e materializar referência |
| Regra | sete campos centrais | mesmos | preservar e tornar obrigatórios no schema |
| Regra | `historico[].autor` | `historico[].registrado_por` | alinhar vocabulário |
| Fonte | `autor` | `registrado_por` | renomear |
| Fonte | contrato apenas no template | `contrato.estrutura/significado/qualidade` | declarar como estrutura obrigatória |
| Quatro objetos | procedência parcial | `D | I | V` + premissa/evidência condicionais | alinhar |

## 6. Alterações realizadas

| Arquivo/grupo | Mudança | Justificativa |
|---|---|---|
| Quatro modelos em `contexto/` | Materialização dos campos do CTX-01 v0.4; Regra renomeada para `RN-000-modelo.yaml`. | CTX-01 §§3.3–3.8. |
| `registro/contexto.schema.json` | Contrato declarativo de campos, tipos, IDs e D/I/V. | Estrutura reutilizável e congelada no caso. |
| `eiac-nucleo/scripts/estrutura.py` | Validador genérico orientado pelo schema do caso. | Mantém o núcleo sem vocabulário específico do EMCIA. |
| `testes/contexto.py` | T01–T11 com geração contemporânea de evidência. | TST-01: negativa + controle positivo. |
| Documentação diretamente afetada | Exemplos, instruções, inventário e contagem de testes alinhados. | Evita consumo do schema antigo. |
| Manifests | Núcleo 0.2.7 e Campo 0.3.4. | Scripts do núcleo e contrato do campo mudaram. |

## 7. Testes

| ID | Cenário | Esperado | Obtido | Resultado | Evidência |
|---|---|---|---|---|---|
| 2.5.1-T01 | Termo válido | aceite | aceite | PASS | `teste-2.5.1-T01.txt` |
| 2.5.1-T02 | Entidade válida | aceite | aceite | PASS | `teste-2.5.1-T02.txt` |
| 2.5.1-T03 | Regra válida | aceite | aceite | PASS | `teste-2.5.1-T03.txt` |
| 2.5.1-T04 | Fonte válida | aceite | aceite | PASS | `teste-2.5.1-T04.txt` |
| 2.5.1-T05 | Termo sem significado | recusa | recusa | PASS | `teste-2.5.1-T05.txt` |
| 2.5.1-T06 | Entidade sem nome | recusa | recusa | PASS | `teste-2.5.1-T06.txt` |
| 2.5.1-T07 | Regra sem estabilidade | recusa | recusa | PASS | `teste-2.5.1-T07.txt` |
| 2.5.1-T08 | Fonte sem contrato.significado | recusa | recusa | PASS | `teste-2.5.1-T08.txt` |
| 2.5.1-T09 | D/I/V nos quatro objetos | 12 aceites | 12 aceites | PASS | `teste-2.5.1-T09.txt` |
| 2.5.1-T10 | Taxonomias obsoletas | 8 recusas | 8 recusas | PASS | `teste-2.5.1-T10.txt` |
| 2.5.1-T11 | Sete campos centrais | presentes | presentes | PASS | `teste-2.5.1-T11.txt` |
| 2.5.1-T12 | Regressão acumulada | sem regressão | 44 aprovações | PASS | `teste-regressao-final.txt` |

## 8. Regressão

- **Antes:** 33 total / 33 PASS / 0 FAIL / 0 SKIP.
- **Depois:** 44 total / 44 PASS / 0 FAIL / 0 SKIP.

A contagem aumentou em 11 pelos testes estruturais T01–T11. T12 é a execução
acumulada, não uma décima segunda verificação adicional.

## 9. Defeitos encontrados

Nenhum novo defeito funcional demonstrável. O pacote tratou D-02 e os achados
2.5-BL03 a 2.5-BL06 já registrados no baseline.

## 10. Correções realizadas

- alinhamento de Termo, Entidade, Regra e Fonte ao CTX-01 v0.4;
- remoção estrutural de `estatuto` e da divergência duplicada na Regra;
- prefixo estável `RN-*`;
- sete campos centrais obrigatórios no schema;
- contrato D/I/V aplicável aos quatro objetos;
- contrato mínimo de Fonte estruturalmente verificável;
- validador genérico e testes positivos/negativos correspondentes.

## 11. Itens deliberadamente adiados

- **2.5.2:** curadoria, restrição de autoria, proteção de escrita e
  versionamento comportamental I→V;
- **2.5.3:** semântica de `classificacao_confronto` e obrigatoriedade de
  `referencia_p3d`;
- **2.5.4:** CTX-V01–V11 completos e resolução de referências entre objetos;
- **2.5.5:** integração P2/P3 → CTX → P4/P5;
- **2.5.6:** verificação consolidada da camada.

## 12. Eventos

Nenhum evento é aplicável. O validador deste pacote é estrutural, somente
leitura e não grava estado. Eventos de recusa e curadoria pertencem aos
pacotes comportamentais posteriores.

## 13. Commit

- **Implementação:** `92179256f078880f92fbfe5d395ee4a61dccfbf7` —
  `feat(context): materialize CTX core objects`.
- **Diff anterior ao commit:** `diff.patch`.
- **Commit materializado:** `git-show.txt`.
- **Atualização do RTE-01 oficial:** `rte-01.diff`.
- **Logs brutos:** `teste-2.5.1-T01.txt` a `teste-2.5.1-T11.txt`,
  `teste-regressao-inicial.txt` e `teste-regressao-final.txt`.
- **Matriz anterior:** `matriz-schema-inicial.md`.

## 14. Estado final

**CONFORME.** Os critérios técnicos e de teste estão atendidos, o commit está
registrado e o EMCIA-RTE-01 oficial foi atualizado para a versão 0.3.
