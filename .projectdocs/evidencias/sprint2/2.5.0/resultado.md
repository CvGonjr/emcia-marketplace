# Pacote 2.5.0 — Registro de execução

## Identificação

- **Pacote:** 2.5.0 — Normalização do contrato de procedência D/I/V
- **Data recuperável:** 18/09/2026 15:28:33 -0300, data do commit de implementação
- **Data/hora da execução original dos testes:** NÃO PRESERVADA NA EXECUÇÃO ORIGINAL
- **Baseline:** `9a54017411c20cf54ab3a28fa488678c945a34b1` — S2-BL
- **Commit inicial do pacote:** `acf35f963bff718cfaa25981c4c84753f661c367`
- **Commit final do pacote:** `acf35f963bff718cfaa25981c4c84753f661c367`
- **Branch:** `master`

## Requisitos tratados

- D-01 — Procedência multidimensional antiga.
- 2.5-BL01 — Contrato D/I/V implementado, mas divergente.
- 2.5-BL02 — Taxonomias concorrentes implementadas como procedência.

## Estado inicial

**IMPLEMENTADO MAS DIVERGENTE.** O playbook representava procedência por
`contexto`, `origem` e `apuracao`, com valores concorrentes ao contrato
documental D/I/V.

## Alterações realizadas

Mudanças demonstráveis pelo diff entre o baseline e o commit final:

- substituição do contrato declarativo por `D`, `I` e `V`, com os rótulos
  Declarada, Inferida e Verificada;
- separação de `apuracao` e `tipo_fonte` da procedência documental;
- validação de uma única procedência por asserção;
- exigência de `premissa:` para I e evidência rastreável para V;
- recusa de `X`, `campo` e `externo` como procedência;
- atualização dos consumidores executáveis, exemplos e modelos mínimos;
- adição de T01-T07 e adequação lexical dos testes antigos ao contrato novo;
- versões alteradas: `eiac-nucleo` 0.2.5→0.2.6,
  `eiac-campo` 0.3.2→0.3.3 e playbook 0.3.0→0.3.1.

O commit modifica 28 arquivos, com 265 inserções e 144 remoções. A relação
integral está em `git-show.txt` e o patch está em `diff.patch`.

## Testes

O commit contém os testes T01-T07 e define T08 como a regressão acumulada da
suíte. O log bruto da execução original não foi armazenado no repositório.
Cada caso é, portanto, classificado como executado sem log original preservado;
o resultado abaixo é corroborado pelo reteste reconstruído no mesmo commit.

| ID | Cenário | Status de execução | Resultado | Tipo de evidência | Referência |
|---|---|---|---|---|---|
| 2.5.0-T01 | D válido aceito | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |
| 2.5.0-T02 | I sem premissa recusado | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |
| 2.5.0-T03 | I com premissa aceito | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |
| 2.5.0-T04 | V sem evidência recusado | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |
| 2.5.0-T05 | V com evidência aceito | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |
| 2.5.0-T06 | X, campo e externo recusados como procedência | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |
| 2.5.0-T07 | V e `apuracao: medido` coexistem em campos distintos | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |
| 2.5.0-T08 | Regressão dos 26 cenários anteriores | EXECUTADO SEM LOG PRESERVADO | PASS no reteste reconstruído | Commit contemporâneo + reteste reconstruído | `teste-regressao-final.txt` |

## Regressão

- **Baseline S2-BL:** 26 PASS / 0 FAIL / 0 SKIP, conforme registro controlado
  do baseline. O stdout bruto correspondente não está preservado neste
  diretório.
- **Execução original após 2.5.0:** stdout/stderr bruto NÃO PRESERVADO NA
  EXECUÇÃO ORIGINAL.
- **Reteste reconstruído em 18/09/2026 15:41:28 -0300:** 33 verificações
  aprovadas, 0 falhas, exit code 0, no commit final do pacote.

A contagem passou de 26 para 33 pela adição de T01-T07. T08 é a regressão dos
26 cenários anteriores, não uma oitava linha adicional na suíte.

## Defeitos encontrados

Nenhum defeito novo demonstrável foi identificado. O pacote tratou os achados
já controlados D-01, 2.5-BL01 e 2.5-BL02.

## Correções

Somente as correções presentes no commit foram atribuídas ao pacote:

- contrato canônico D/I/V;
- premissa obrigatória para I;
- evidência obrigatória para V;
- D aceito sem exigência própria de V;
- taxonomias não documentais separadas ou removidas da procedência;
- validação genérica do contrato declarativo pelo `eiac-nucleo`;
- cobertura negativa e positiva para o contrato.

## Evidências

- `resultado.md` — consolidação reconstruída após a execução original;
- `git-show.txt` — reconstrução fiel de `git show` do commit de implementação;
- `diff.patch` — reconstrução fiel do diff baseline→commit final;
- `teste-regressao-final.txt` — reteste real executado posteriormente no
  commit final;
- `rte-01.diff` — diff reconstruído com `git diff --no-index`, pois o
  diretório do documento oficial não possui repositório Git;
- `testes/negativos.sh` no commit — definição contemporânea dos testes;
- commit `acf35f963bff718cfaa25981c4c84753f661c367` — evidência contemporânea
  da implementação.

Não foram encontrados logs brutos nem eventos preservados da execução original.

## Estado final

**CONFORME.** O diff demonstra a normalização para D/I/V, os testes estão
versionados no commit e o reteste reconstruído no mesmo estado executável
obteve 33 aprovações e exit code 0.

## Observação de proveniência da evidência

### EVIDÊNCIA CONTEMPORÂNEA

- commit `acf35f963bff718cfaa25981c4c84753f661c367`;
- código, documentação e testes contidos nesse commit;
- data, autoria, mensagem e estatística preservadas pelo Git.

### EVIDÊNCIA RECONSTRUÍDA

- `resultado.md`, criado após a execução;
- `git-show.txt`, extraído posteriormente do objeto Git preservado;
- `diff.patch`, extraído posteriormente entre baseline e commit final;
- `teste-regressao-final.txt`, produzido por reexecução posterior da suíte;
- `rte-01.diff`, produzido posteriormente contra uma cópia reconstruída do
  estado anterior do RTE-01.

O stdout/stderr bruto da execução original e os eventos temporários dos testes
não foram preservados. Nenhum desses registros foi reconstruído de forma
fictícia.
