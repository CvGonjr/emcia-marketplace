# Matriz de regras genéricas — núcleo (pacote 2.6.1)

**HEAD inicial:** `70d1d9bf793ab53b0218b1a5663915c4baa1c9ae`

Nenhuma regra abaixo conhece semântica EMCIA (P6–P10, E4/E5, autonomia,
recalibragem, piloto, métrica de resultado). Todas leem campos genéricos
do playbook (`delegavel`, `depende_de`, `camada`, `recorrente`,
`cadencia_obrigatoria`, `responsavel_obrigatorio`, `inegociavel`,
`portao`, `condicao`) ou do estado (`etapa_atual`, `cumprimentos`,
`inegociaveis`).

| Regra genérica | Campo no playbook/estado | Mecanismo | Negativo | Positivo | Estado |
|---|---|---|---|---|---|
| Etapa corrente | `st["etapa_atual"]` | `avancar.encerrar()` compara `etapa_id != st["etapa_atual"]` antes de qualquer outra checagem | T01 | T02 | CONFORME |
| Dependência | `depende_de` | `avancar.encerrar()` e `guarda.py` G3 checam `cumprimentos[dep]["cumprido"]` | T03, T03b | T04 | CONFORME |
| Delegabilidade | `delegavel: false` | `guarda.py` G1 (por habilidade em carregamento) e `avancar.encerrar()` (por sessão exigida) | T06 | T05, T07 | CONFORME |
| Camadas EX1–EX4 | `camada.<nível>` | `playbook.carregar()` rejeita valor fora do conjunto fixo | T08 | (regressão: playbook oficial válido) | CONFORME |
| Critério de verificação | `automatizado` / `criterio_de_verificacao` | `playbook.capacidade_valida()` — mecanismo isolado, sem integração ao playbook oficial | T09 | T10, T10b | MECANISMO CONFORME; integração a HB/AG real PENDENTE 2.6.4 |
| Responsável nominal | `responsavel_obrigatorio` | `avancar.registrar_recorrencia()` + `_ator_valido()` (nome não vazio, não agente, não genérico) | T11, T12b | T12 | CONFORME |
| Cadência obrigatória | `cadencia_obrigatoria` | `avancar.registrar_recorrencia()` exige `cadencia` não vazia | T13 | T14 | CONFORME |
| Recorrência (contrato) | `recorrente` + `cadencia_obrigatoria` + `responsavel_obrigatorio` | `playbook.carregar()` recusa `recorrente: true` sem os dois campos de suporte | T15 | T16 | CONFORME |
| Recorrência (execução) | `estado_recorrente` em `cumprimentos[etapa]` | `avancar.registrar_recorrencia()` grava ciclo/`ultima_verificacao`/histórico sem apagar ciclos anteriores | — (T15 cobre o contrato) | T11–T14 (fluxo completo) | CONFORME |
| Inegociável — caminho positivo | `st["inegociaveis"][n]` como registro `{satisfeito, evidencia, autor, data}` | `avancar.satisfazer_inegociavel()` — único caminho autorizado | T18, T19 | T20, T20b, T20c | CONFORME |
| Inegociável — booleano mágico | idem | `emitir()` valida `registro.get("satisfeito")` e `evidencia`/`autor` não vazios, não apenas truthy | T18 (bloqueado por G5 antes mesmo de chegar ao inegociável) | T20c | CONFORME |
| Proteção de `registro/` | caminho `registro/` | `guarda.py` G5 — bloqueia `Write`/`Edit`/`Bash`-redirect; permite invocação de `avancar.py`/`curar.py`/`validar.py`/`selar.py` via `Bash` | T21 | T22 | CONFORME |
| Proteção de `caso/` (revalidação) | caminho `caso/` | `guarda.py` G2 — inalterado neste pacote | T31 (mesmo teste cobre negativo e positivo já coberto em `negativos.sh`) | `negativos.sh` #2 | CONFORME (revalidado, sem regressão) |
| Proteção de `contexto/` (revalidação) | caminho `contexto/` | `guarda.py` G2b — inalterado neste pacote | T23 | T24 | CONFORME (revalidado, sem regressão) |
| Integridade de portão | `entregaveis[].portao` | `playbook.carregar()` recusa referência a etapa inexistente | T25 | (regressão: playbook oficial válido) | CONFORME |
| Integridade de inegociável em portão | `entregaveis[].inegociavel` | `playbook.carregar()` recusa referência a inegociável inexistente | T26 | (regressão: playbook oficial válido) | CONFORME |
| Condição declarativa — avaliação | `entregaveis[].condicao` `{campo, etapa, operador, valor}` | `avancar._avaliar_condicao()` lê `cumprimentos[etapa][campo]` e compara pelo operador | T27b | T27 | CONFORME |
| Condição declarativa — integridade | idem | `playbook.carregar()` recusa `condicao` incompleta ou com operador fora de `CONDICAO_OPERADORES` | T28 | (regressão: E3-E do playbook oficial válido) | CONFORME |
| Eventos de recusa da máquina | — | `avancar.main()` emite `RecusaMaquina`/`RecusaEmissao` em todo caminho de erro antes de sair | T29 | T01b (mesmo mecanismo) | CONFORME |
| Eventos de recusa de emissão | — | idem, `tipo_evento = "RecusaEmissao"` quando `acao == "emitir"` | T30 | T20c (emissão bem-sucedida também gera `EntregavelEmitido`) | CONFORME |
| Selo Git | — | `selar.py` — inalterado neste pacote | (coberto por `negativos.sh` #18/#19/#21) | T32, `negativos.sh` #20 | CONFORME (revalidado, sem regressão) |

## Hard-code EMCIA no núcleo

Busca (`grep -rniE` por P6–P10, E4, E5, autonomia, recalibragem, piloto,
métrica de resultado em `eiac-nucleo/scripts/`, `eiac-nucleo/commands/`,
`eiac-nucleo/hooks/`) após as edições: **2 ocorrências, ambas não
comportamentais** —

1. `avancar.py` linha 7: exemplo de uso no docstring do CLI
   (`--registrar-recorrencia P10 ...`), ilustrando a sintaxe com um valor
   plausível — não é uma decisão de código.
2. `avancar.py` linha ~147: comentário explicando o que o núcleo **não**
   decide ("baseline, termo de autonomia etc.").

Nenhuma ocorrência é um `if etapa == "P7"` ou equivalente. `HARD-CODE
EMCIA NO NÚCLEO: 0` (comportamental).
