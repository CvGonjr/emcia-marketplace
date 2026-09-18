# Pacote 2.5.4 — CTX-V01–CTX-V11

## 1. Identificação

- **Ação:** 2.5 — Contexto e Dados
- **Pacote:** 2.5.4
- **Data/hora:** 18/09/2026, execução única de implementação e testes
- **Branch:** `master`
- **HEAD inicial:** `004b42813c63ab7ba7bb3c2c86c7e74df99a9d53`
- **HEAD final:** ver `git-show.txt` (commit criado ao final deste pacote)

## 2. Documentos consultados

| Documento | Versão | Papel |
|---|---:|---|
| EMCIA-CTX-01 | 0.4 | Fonte única e literal das onze condições CTX-V01–CTX-V11 (§3.13), dos sete campos do bloco de decisão (§3.6) e da correspondência ROT-01 (§3.8). |
| EMCIA-ROT-01 | — | Taxonomia oficial de confronto (§3.9), já usada desde o 2.5.3. |
| EMCIA-MET-01, EMCIA-TRA-01, EMCIA-ESP-01, EMCIA-VER-01 | — | Nenhuma divergência aplicável encontrada. |
| EMCIA-TST-01 | — | Convenção de teste negativo + controle positivo por regra. |
| `.projectdocs/evidencias/sprint2/{2.5.0,2.5.1,2.5.2,2.5.3}/` | — | Estado efetivamente implementado por cada pacote anterior, usado para classificar cada CTX-V. |

## 3. Baseline relacionado

D-05, 2.5-BL16, 2.5-BL17, 2.5-BL18, 2.5-BL19.

## 4. Definições oficiais CTX-V

Extraídas literalmente de EMCIA-CTX-01 §3.13 — ver matriz completa em
`matriz-ctx-validacoes.md`. Nenhuma numeração ou significado deste prompt
foi usado como substituto; a matriz reproduz o texto do documento.

## 5. Estado inicial de cada validação

| CTX-V | Estado | Implementação existente | Lacuna |
|---|---|---|---|
| CTX-V01 | JÁ IMPLEMENTADO E CONFORME | `contexto.schema.json` (`required`/`nonempty` da Regra), desde 2.5.1 | Nenhuma — faltava só o código formal nas mensagens. |
| CTX-V02 | JÁ IMPLEMENTADO E CONFORME | `conditional_nonempty.I`, desde 2.5.0/2.5.1 | Idem. |
| CTX-V03 | JÁ IMPLEMENTADO E CONFORME | `conditional_nonempty.V`, desde 2.5.0/2.5.1 | Idem. |
| CTX-V04 | JÁ IMPLEMENTADO E CONFORME | `checar_versao()`, desde 2.5.2 | Idem. |
| CTX-V05 | **AUSENTE** | `entradas` validado só como `list` (tipo), sem resolução | Nenhuma verificação de que os ids em `entradas` existem. |
| CTX-V06 | **AUSENTE** | Idem | Idem. |
| CTX-V07 | **AUSENTE** | Idem; nenhuma distinção entre arquivo em `fontes/` e objeto Fonte CTX | Idem, mais a exigência de contrato mínimo. |
| CTX-V08 | JÁ IMPLEMENTADO E CONFORME | `guarda.py` G2b, desde 2.5.2 | Nenhuma. |
| CTX-V09 | JÁ IMPLEMENTADO E CONFORME | `checar_autoria()`, desde 2.5.2 | Nenhuma. |
| CTX-V10 | JÁ IMPLEMENTADO E CONFORME | `checar_versao()`, desde 2.5.2 | Nenhuma. |
| CTX-V11 | JÁ IMPLEMENTADO E CONFORME | `checar_confronto()`, desde 2.5.3 | Nenhuma. |

O baseline (D-05, 2.5-BL16) registrou "0/11 validações localizadas" porque
nenhuma delas tinha o código formal `CTX-Vxx` associado ao código na época
do S2-BL — não porque o comportamento subjacente estivesse todo ausente.
Os pacotes 2.5.0–2.5.3 implementaram progressivamente oito das onze; este
pacote formaliza essas oito e implementa as três que realmente faltavam.

## 6. Arquitetura do validador

Preservada a separação núcleo/campo. `curar.py` (núcleo) ganhou
`checar_referencias()`, genérica: lê `catalogo_referencias` (prefixo do id
→ tipo e diretório) e `references` (por tipo de objeto, campo → prefixos
aceitos) do schema do caso. Nenhum `if tipo == "regra"` ou `if campo ==
"entradas"` no núcleo — a única EMCIA-especificidade está nos dados do
schema (`eiac-campo/template-caso/registro/contexto.schema.json`), não no
código do núcleo. Quando o objeto referenciado é do tipo `"fonte"`, a
checagem reaproveita `estrutura.validar()` sobre o objeto resolvido, em
vez de duplicar a regra do contrato mínimo.

As mensagens de erro e os eventos (`CuradoriaRecusada`) de `curar.py`
passaram a incluir o código `CTX-Vxx` nas checagens que o justificam.

## 7. Alterações realizadas

| Arquivo | Alteração | Justificativa |
|---|---|---|
| `eiac-campo/template-caso/registro/contexto.schema.json` | Novo bloco `catalogo_referencias` (T/E/F → tipo/diretório); `references` em `regra.entradas` (T,E,F) e `entidade.onde_vive` (F). Versão do schema `0.1.0` → `0.2.0`. | Declara a superfície de referências resolvíveis sem hard-code no núcleo. |
| `eiac-nucleo/scripts/curar.py` | Nova `checar_referencias()` (CTX-V05/V06/V07), genérica por schema. Mensagens de `checar_autoria()`, `checar_versao()` e `checar_confronto()` prefixadas com o código CTX-V correspondente. | Fecha D-05/2.5-BL17–19; formaliza o restante sem reescrever lógica. |
| `eiac-nucleo/README.md` | Novo invariante I-17; seção "Resolução de referências (I-17)" explicando o mecanismo declarativo. | Rastreabilidade dos invariantes do núcleo. |
| `eiac-nucleo/commands/curar.md` | Documenta a resolução de referências. | Orientação de uso. |
| `eiac-campo/template-caso/contexto/README.md` | Nova seção "Resolução de referências"; remove nota que apontava para "pacote 2.5.4" (concluído). | Orientação para quem opera o caso. |
| `eiac-campo/template-caso/contexto/regras/RN-000-modelo.yaml`, `.../entidades/E-000-modelo.yaml` | Comentários de `entradas`/`onde_vive` esclarecem os prefixos aceitos e o código CTX-V correspondente. | Torna o contrato de referência visível no modelo. |
| `testes/ctx_v.py` (novo) | 22 testes (Vxx-N/Vxx-P) + 1 teste de violações múltiplas. | EMCIA-TST-01; negativa + controle positivo por CTX-V. |
| `testes/README.md` | Documenta a bateria formal; total acumulado 73 → 96. | Rastreabilidade dos testes. |
| `eiac-nucleo/.claude-plugin/plugin.json` | `0.2.9` → `0.2.10`. | `curar.py` mudou. |
| `eiac-campo/.claude-plugin/plugin.json` | `0.3.6` → `0.3.7`. | Schema e templates do caso mudaram. |

## 8. Matriz negativo × positivo

Ver `matriz-ctx-validacoes.md` — 11 pares completos, todos CONFORME.

## 9. Resultado dos testes

22 pares negativo/positivo (`2.5.4-V01-N`/`P` a `2.5.4-V11-N`/`P`) + 1 teste
de violações múltiplas (`2.5.4-multi`) = 23 verificações, todas PASS.
Evidência bruta individual em `CTX-Vxx-negativo.txt`/`CTX-Vxx-positivo.txt`
e `2.5.4-multi.txt`.

## 10. Eventos

`eventos.jsonl` desta evidência demonstra: `ObjetoContextoCurado` (Termo
T-001), `CuradoriaRecusada` com `"CTX-V05: referencia 'T-999' em
'entradas' nao resolve..."` (Regra referenciando termo inexistente),
`ObjetoContextoCurado` (mesma Regra, agora referenciando T-001 existente).
O código CTX-V aparece dentro da lista `erros` do evento de recusa,
permitindo auditoria posterior pelo RTE-01 sem reprocessar o log bruto.

## 11. Regressão

- **Antes:** 73 total / 73 PASS / 0 FAIL / 0 SKIP. Ver `teste-regressao-inicial.txt`.
- **CTX-V:** 23 total / 23 PASS / 0 FAIL.
- **Depois:** 96 total / 96 PASS / 0 FAIL / 0 SKIP. Ver `teste-regressao-final.txt`.

## 12. Novos defeitos encontrados

Nenhum defeito de código nos pacotes anteriores. As três lacunas reais
(CTX-V05/V06/V07) já estavam corretamente registradas como ausentes nos
resultados de 2.5.1–2.5.3 (itens deliberadamente adiados); não houve
achado inesperado.

## 13. Correções

Não houve correção de defeito pré-existente — o pacote formalizou oito
validações já corretas e implementou as três ausentes.

## 14. Retestes

Todos os 23 testes passaram na primeira execução após a implementação.
Um erro de fixture nos próprios testes (três casos usavam valores
auto-preenchidos de `premissa`/`evidencia` que mascaravam o cenário
negativo pretendido) foi corrigido nos helpers de `testes/ctx_v.py`
antes da execução registrada como evidência — não é defeito de
`curar.py`, é ajuste do gerador de fixtures do teste.

## 15. Itens adiados

- **2.5.5:** integração executável P2/P3 → CTX → P4/P5 (não antecipada; `checar_referencias()` resolve referências dentro de `contexto/`, não substitui o fluxo completo entre passos).
- **2.5.6:** verificação consolidada da camada.
- **Ação 2.6:** agentes e protocolos, P6–P10, 18 HB, 4 AG, portões E4/E5, geração de entregáveis.

## 16. Commit

Ver `git-show.txt` e `diff.patch` neste diretório.

## 17. Estado final

**CONFORME.**

**Indicador CTX:** baseline `0/11` → final `11/11`.

Todos os 19 critérios de pronto do pacote (§44 da instrução) foram
atendidos: as onze CTX-V extraídas literalmente do CTX-01, todas com
representação executável, teste negativo e controle positivo; valores
inválidos recusados deterministicamente; referências a Termo, Entidade e
Fonte resolvidas (com distinção entre arquivo físico e objeto Fonte CTX);
histórico/versionamento e I→V preservados (não reescritos, apenas
formalizados); P3d rastreável quando exigido; agente não promovido a
autor de conteúdo curado; recusas auditáveis via eventos com o código
CTX-V; nenhuma CTX-V contabilizada só por existir no documento; suíte
anterior sem regressão; evidências persistidas; RTE-01 atualizado;
integração P2/P3→P4/P5 não antecipada.
