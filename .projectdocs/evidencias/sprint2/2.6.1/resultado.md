# Pacote 2.6.1 — Núcleo genérico de protocolos

## 1. Identificação

**Ação:** 2.6 — Agentes e Protocolos
**Pacote:** 2.6.1
**Branch:** master
**HEAD inicial:** `70d1d9bf793ab53b0218b1a5663915c4baa1c9ae`
**HEAD final:** registrado em `git-show.txt` após o commit deste pacote.
**Data/hora:** 2026-09-18 23:30 -0300

## 2. Documentos consultados

Leitura obrigatória: EMCIA-ARQ-01 v0.2 (arquitetura do Estúdio,
separação núcleo/campo, cinco camadas de referência), EMCIA-ESP-01 v0.2
(invariantes de carga, guardas mínimas G1–G6, eventos mínimos),
EMCIA-MET-01, EMCIA-CAT-01, EMCIA-TRA-01 (procedimentos transversais —
consultado; TRA-V01–V10 fora de escopo deste pacote, já cobertos por P3d
na Ação 2.5), EMCIA-TST-01, EMCIA-GLO-01, EMCIA-IMP-01. Consultado:
EMCIA-VER-01, EMCIA-CTX-01, EMCIA-E1–E5, evidências de 2.6.0
(`resultado.md`, `matriz-contrato-f0-p10.md`).

## 3. Baseline relacionado

`2.6-BL12` (máquina de estados PARCIAL — `avancar.py` encerrava etapa por
argumento sem checar etapa corrente), `2.6-BL13` (dependências PARCIAL),
`2.6-BL14` (guardas de camada PARCIAL), `2.6-BL15` (eventos de recusa
PARCIAL — guarda/validador geravam evento, máquina de etapas e emissão
não), `2.6-BL16` (proteção de `caso/` PARCIAL), `2.6-BL17` (proteção de
`registro/` AUSENTE — escrita direta retornava rc=0), `2.6-BL26`
(caminho positivo dos inegociáveis AUSENTE — flag manual sem trilha).

`D-08` (`registro/` sem proteção), `D-09` (recusas da máquina sem
evento).

## 4. Estado inicial

Reproduzido e confirmado antes de qualquer edição: com o caso em `P1`,
`avancar.py --encerrar P5 --autor "Celso"` retornava `exit 0` e movia
`etapa_atual` diretamente para `P6`, pulando `P2, P3a, P3b, P3d, P4, P5`
sem checar dependências nem sessões dessas etapas intermediárias — bug
exato de `2.6-BL12`. `guarda.py` não possuía nenhuma regra sobre
`registro/`: `Write`/`Edit`/redirecionamento de shell nesse caminho
passavam sem recusa. `avancar.py` retornava mensagens de erro em `stderr`
em todo caminho de recusa, mas só emitia evento explicitamente em dois
pontos (`apurar_nivel`, `encerrar` com sucesso); todo `return "mensagem"`
de erro em `encerrar()`/`emitir()` saía sem `E.evento()`.
`st["inegociaveis"][n]` era um booleano simples, gravável apenas por
edição direta do JSON (nenhum comando o produzia).

## 5. Arquitetura do núcleo após o pacote

Nenhum vocabulário EMCIA foi introduzido em `eiac-nucleo/`. Busca
`grep -rniE` por P6–P10, E4, E5, autonomia, recalibragem, piloto, métrica
de resultado em `eiac-nucleo/scripts/`, `eiac-nucleo/commands/`,
`eiac-nucleo/hooks/` após as edições: 2 ocorrências, ambas não
comportamentais (exemplo de CLI no docstring de `avancar.py` e comentário
explicando o que o núcleo não decide). `HARD-CODE EMCIA NO NÚCLEO: 0`
comportamental. Ver `matriz-regras-nucleo.md` §"Hard-code EMCIA no
núcleo".

## 6. Máquina de estados

`avancar.encerrar()` agora recusa qualquer `etapa_id != st["etapa_atual"]`
antes de qualquer outra checagem. Corrige `2.6-BL12` sem introduzir
vocabulário de etapa: a comparação é puramente estrutural. `2.6.1-T01`
reproduz o cenário exato do baseline (`P1` corrente, tentativa de
encerrar `P5`) e confirma a recusa; `2.6.1-T02` confirma que a etapa
corrente correta continua encerrando normalmente.

## 7. Dependências

Comportamento pré-existente (`depende_de`) preservado e revalidado —
`2.6.1-T03`/`T03b` isolam a checagem de dependência (G3 em `guarda.py` e
a checagem equivalente em `avancar.encerrar()`) de outras causas de
recusa (delegabilidade), usando uma etapa delegável (`P3d`, EX3) em vez
de uma etapa humana. `2.6.1-T04` confirma que dependência satisfeita
libera o avanço.

## 8. Delegabilidade e camadas

`delegavel: false` continua bloqueado genericamente em `guarda.py` (G1) e
em `avancar.encerrar()` (exige sessão registrada). Nenhum nome de etapa
aparece nesse código — a regra lê `e.get("delegavel")` e `cam in ("EX3",
"EX4")`. `2.6.1-T05`/`T06`/`T07` confirmam positivo/negativo/positivo
pós-sessão. `playbook.carregar()` (já implementado em 2.6.0) continua
recusando camada fora de `EX1`–`EX4`; `2.6.1-T08` revalida com fixture.

## 9. Critério de verificação

Implementado como mecanismo **isolado**: `playbook.capacidade_valida()`
recebe um dict `{automatizado, criterio_de_verificacao}` sintético e
aplica a regra "capacidade automatizada sem critério não é válida para
carregamento/execução" — sem tocar no playbook oficial, sem estruturar
`hb: [...]` em objetos, sem conhecer HB-01 ou AG-01. Testado
isoladamente por `2.6.1-T09`/`T10`/`T10b`. Decisão explícita registrada
com o usuário antes da implementação: a integração com as 18 HB e 4 AG
reais pertence a 2.6.4; este pacote só constrói e testa o mecanismo
genérico.

## 10. Recorrência, cadência e responsável

Novo comando `avancar.py --registrar-recorrencia <etapa> --cadencia
<...> --responsavel <...>`. Exige que a etapa já tenha sido encerrada ao
menos uma vez, e que `cadencia`/`responsavel` estejam presentes quando o
playbook marcar `cadencia_obrigatoria`/`responsavel_obrigatorio`.
`_ator_valido()` recusa nome vazio, agente, ou termo genérico de coletivo
("equipe", "área", "time", "setor", "departamento", "a definir") — o
núcleo não sabe o que é "responsável pela recalibragem", só que um
coletivo não é uma pessoa nomeada. Cada registro atualiza
`cumprimentos[etapa]["estado_recorrente"]` com `ciclo`,
`ultima_verificacao` (nome de campo já usado por EMCIA-CAM-01 Anexo D) e
`historico` — sem apagar ciclos anteriores. `2.6.1-T11`–`T14` cobrem
ausência/presença de responsável e cadência; `2.6.1-T15`/`T16` revalidam
a checagem estrutural já existente desde 2.6.0 (recorrente exige os dois
campos de suporte no contrato).

## 11. Inegociáveis

Novo comando `avancar.py --satisfazer-inegociavel <n> --evidencia <...>`
— único caminho autorizado. Grava um registro estruturado
`{satisfeito, evidencia, autor, data}` em vez de um booleano solto, e
`emitir()` passou a validar essa estrutura (`registro.get("satisfeito")`
e `evidencia`/`autor` não vazios), não apenas um valor truthy.
`2.6.1-T18` confirma que a escrita direta do booleano mágico é bloqueada
pela G5 nova (protege `registro/`, que inclui `estado.json`); `T19`
confirma que o caminho autorizado exige evidência; `T20`/`T20b`/`T20c`
confirmam satisfação válida, evento `InegociavelSatisfeito`, e liberação
da emissão. O núcleo não julga a semântica da evidência — isso permanece
decisão humana/metodológica dos pacotes seguintes.

## 12. Proteção de registro/

Nova regra G5 em `guarda.py`, espelhando G2/G2b: bloqueia
`Write`/`Edit`/`Bash`-redirecionamento para `registro/`. Permite que
`Bash` invoque `avancar.py`/`curar.py`/`validar.py`/`selar.py`
normalmente, porque esses scripts escrevem via `estado.gravar()` (I/O
Python direto), nunca via redirecionamento de shell — a mesma
distinção que já protegia `caso/` e `contexto/` sem bloquear o próprio
Estúdio. `2.6.1-T21`/`T22` confirmam negativo/positivo.

## 13. Regressão de contexto/

Nenhuma mudança em G2b. `2.6.1-T23`/`T24` revalidam: escrita direta
continua recusada, curadoria via `curar.py` continua funcional
(fixture de Termo ajustada para incluir os campos `nao_e` e
`sinonimos_em_uso` exigidos pelo schema — erro do teste, não do
produto).

## 14. Portões e condições

`playbook.carregar()` (2.6.0) já recusava portão/inegociável órfão;
revalidado por `2.6.1-T25`/`T26`. Neste pacote, `carregar()` passou a
validar a **estrutura** de `condicao` declarativa (campos obrigatórios
`campo`/`etapa`/`operador`, etapa referenciada existente, operador
dentro de `CONDICAO_OPERADORES = {"contem", "igual", "diferente"}`).
`avancar._avaliar_condicao()` faz a **avaliação** em tempo de emissão,
lendo `cumprimentos[etapa][campo]` sem conhecer o significado do campo —
`2.6.1-T27`/`T27b` demonstram a condição de E3-E (já declarada em 2.6.0)
sendo satisfeita e não satisfeita conforme um valor gravado por uma
etapa anterior. `2.6.1-T28` confirma que operador desconhecido é
recusado explicitamente no carregamento, não ignorado.

## 15. Eventos

`avancar.main()` agora emite `RecusaMaquina` (para `apurar-nivel`,
`encerrar`, `registrar-sessao`, `registrar-recorrencia`,
`satisfazer-inegociavel`) ou `RecusaEmissao` (para `emitir`) em **todo**
caminho de erro, com `acao_tentada`, `alvo`, `motivo`, `autor` e
`etapa_corrente`. `2.6.1-T29`/`T30` confirmam. Evidência consolidada em
`eventos.jsonl` desta pasta, com um `RecusaMaquina`, um
`TentativaNegada` (G5), um `RecusaEmissao` e um `InegociavelSatisfeito`
no mesmo percurso.

## 16. Testes

39 verificações (`2.6.1-T01`–`T32`, com sub-itens `T01b`, `T03b`,
`T10b`, `T12b`, `T20b`, `T20c`, `T27b`), todas PASS. Ver
`teste-2.6.1-T01.txt` a `teste-2.6.1-T32.txt` e
`matriz-regras-nucleo.md`.

## 17. Pares negativo/positivo

Todas as travas críticas listadas em §36 do pacote têm par
negativo+positivo: etapa corrente (T01/T02), dependência (T03/T04),
delegabilidade (T06/T05,T07), cadência (T13/T14), responsável
(T11/T12), inegociável (T18,T19/T20), `registro/` (T21/T22), condição de
portão (T27b/T27).

## 18. Regressão

**Antes:** 158 verificações (129 da Ação 2.5 + 29 de 2.6.0), 158 PASS, 0
FAIL, 0 SKIP. Ver `teste-regressao-inicial.txt`.

**Pacote 2.6.1:** 39 verificações, 39 PASS, 0 FAIL.

**Depois:** 197 verificações, 197 PASS, 0 FAIL, 0 SKIP. Ver
`teste-regressao-final.txt`.

Comparação histórica: S2-BL 26 PASS → final Ação 2.5 129 PASS → final
2.6.0 158 PASS → final 2.6.1 197 PASS. Crescimento rastreável aos
requisitos deste pacote (etapa corrente, dependências, delegabilidade,
critério de verificação, recorrência, cadência, responsável,
inegociáveis, `registro/`, portões/condições, eventos), não meta
numérica.

## 19. Defeitos encontrados

Um defeito de produção real, já catalogado no baseline (`2.6-BL12`),
reproduzido e corrigido: `avancar.py --encerrar <etapa>` não verificava
se a etapa informada era a etapa corrente do caso. Seis bugs de fixture
de teste (não de produto), todos no próprio `testes/nucleo_2_6_1.py`
durante sua construção: (1) alvo de teste que casava com G1 antes de G3
(T03b); (2) sequência de setup que não registrava sessão para `P7`
antes de tentar encerrá-lo (T11–T14, afetando também P10 pois P10
também é não delegável); (3) fixture de Termo em T24 sem os campos
`nao_e`/`sinonimos_em_uso` exigidos pelo schema do caso. Todos
corrigidos antes da execução registrada como evidência.

## 20. Correções e retestes

Ver seções 6–15 acima. Todos os testes envolvidos foram reexecutados
após cada correção; evidência final em `teste-2.6.1-*.txt` reflete a
versão corrigida.

## 21. Itens adiados

- **2.6.2** — P6 e P7 operacionais (decisão humana de autonomia).
- **2.6.3** — P8, P9 e P10 operacionais; mecanismo de scheduler real
  para recorrência (este pacote só representa o estado, não agenda).
- **2.6.4** — 18 HB e 4 AG estruturados; integração do mecanismo de
  `criterio_de_verificacao` com capacidades reais do playbook.
- **2.6.5** — seis autorizações ativas com semântica completa,
  inegociáveis semanticamente verificados (este pacote garante só o
  registro rastreável, não a validação de conteúdo), geração material
  de E4/E5.
- **2.6.6** — caso de controle F0–P10 e suíte end-to-end.

## 22. Commit

Ver `git-show.txt` nesta pasta.

## 23. Estado final

**CONFORME.**

O núcleo agora impõe genericamente etapa corrente, dependências,
delegabilidade, camadas, recorrência/cadência/responsável, inegociáveis
por caminho autorizado, proteção de `registro/`, integridade de
portão/condição e eventos de recusa — tudo sem conhecer a semântica
específica de P6–P10, E4, E5, autonomia, recalibragem, piloto ou métrica
de resultado. Não se afirma que P6–P10 estão operacionalmente
implementados — isso permanece para os pacotes seguintes.
