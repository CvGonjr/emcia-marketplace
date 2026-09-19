# Pacote 2.6.5 — Portões, inegociáveis e entregáveis

## 1. Identificação

Ação: 2.6 — Agentes e Protocolos

Pacote: 2.6.5

Branch: `master`

HEAD inicial: `57700a0d2c421f891de2d48a0ab0f090c45eda63`

HEAD final: `639a8d6`

Data: 19/09/2026

## 2. Documentos consultados

Obrigatórios: EMCIA-MET-01, EMCIA-E1, EMCIA-E2, EMCIA-E3, EMCIA-E4,
EMCIA-E5, EMCIA-ESP-01, EMCIA-TRA-01, EMCIA-CAT-01, EMCIA-TST-01,
EMCIA-VER-01, EMCIA-GLO-01.

Consultados: EMCIA-CTX-01, EMCIA-HAB-01, EMCIA-FER-01, EMCIA-ARQ-01,
EMCIA-IMP-01, EMCIA-CAM-01 (Anexos A–D), evidências 2.6.0–2.6.4.

Pesquisa dedicada (subagente) para localizar o contrato exato do
inegociável 1: confirmou que nenhuma fonte oficial define um objeto/ID
para "linha de base" — só um campo dentro do objeto de métrica (P9,
CAM-01 Anexo C) e a tabela de conteúdo em EMCIA-E2 Parte A.3.

## 3. Baseline relacionado

Portões: 2/6

Inegociáveis semanticamente verificáveis: 0/5

D-12: emissão registrava apenas evento `EntregavelEmitido`, sem
materialização de documento.

## 4. Estado inicial

`avancar.py` já possuía, desde 2.6.1, `--satisfazer-inegociavel`
(gravando `{satisfeito, evidencia, autor, data}`, mas `evidencia` era
texto livre nunca verificado contra artefato real) e `--emitir`
(checando etapas do portão + condição declarativa + presença do
registro estruturado de inegociável, mas produzindo apenas o evento
`EntregavelEmitido`, sem exigir nem gerar documento). Cinco skills
`hb-emitir-e1`–`hb-emitir-e5` já existiam como orientação em prosa
(sem script executável por trás) apontando para `caso/entregaveis/EN.md`
como saída esperada. Nenhum comando `/emitir` existia.

## 5. Arquitetura de validação dos inegociáveis

`eiac-campo/scripts/inegociaveis.py`: cinco funções puras
(`verificar_i1`–`verificar_i5`), cada uma lendo exatamente um artefato
real do domínio correspondente e devolvendo
`{id, satisfeito, evidencia_ref, verificador, motivo, timestamp}`. O
comando `--satisfazer` só é aceito depois que o verificador devolveu
`satisfeito=True`, e então chama `avancar.py --satisfazer-inegociavel`
com a evidência textual carregando o nome do verificador e a referência
do artefato — nunca grava a partir de um valor solto. O núcleo continua
sem saber o que "termo de autonomia" ou "métrica de resultado"
significam.

## 6. Resultado I1

Verificador lê `registro/baseline/BL-*.yaml` (indicador, valor_atual,
apuracao, data, nível). Negativo: sem baseline (T01), apuração
`estimado` fora de N1 recusada em `baseline.py` (T02b, MET-01 §3.4.3).
Positivo: baseline válida (T02). **CONFORME.**

## 7. Resultado I2

Verificador lê `registro/governanca/autonomia/AUT-*.yaml`, exige
`estado: decidido` + `decisor`/`data_decisao`/`justificativa_decisao`.
Negativo: termo apenas proposto (T03). Positivo: termo decidido por
humano nomeado (T04). **CONFORME.**

## 8. Resultado I3

Verificador lê `registro/piloto/CT-*.yaml`, exige `estado: revisado` e
todos os casos com `saida_esperada`/`esperado_definido_em`. Negativo:
conjunto em rascunho, sem saída esperada completa (T05). Positivo:
conjunto revisado com dois casos válidos (T06). **CONFORME.**

## 9. Resultado I4

Verificador lê `registro/metricas/MET-*.yaml`, exige `tipo: resultado`
+ `estado: apurada`. Negativo: só métrica de uso (T07). Positivo:
métrica de resultado apurada (T08). **CONFORME.**

## 10. Resultado I5

Verificador lê `registro/calibragem/CAL-*.yaml`, exige `responsavel`
pessoa nomeada (checagem por token, capturando frases compostas como
"equipe de TI" que escapam da checagem lexical de palavra inteira já
existente em `calibragem.py`) + `cadencia`. Negativo: `responsavel:
equipe` (T09, recusado já em `calibragem.py`) e `responsavel: equipe de
TI` (T09b, recusado no verificador semântico). Positivo: responsável
nominal com demais requisitos (T10). **CONFORME.**

## 11. Total

**5/5 inegociáveis semanticamente conformes.**

## 12. Resultado E1

Portão: F0 encerrada. Negativo: antes de F0 (T13). Positivo: após F0
(T14). **AUTORIZADO no caso positivo.**

## 13. Resultado E2

Portão: P1/P2/P3a/P3b/P3d encerradas + inegociável 1. Negativos: etapa
faltando (T16), etapas completas mas I1 não satisfeito no núcleo (T17).
Positivo: requisitos completos (T18). **AUTORIZADO no caso positivo.**

## 14. Resultado E3-D

Portão: P4/P5 encerradas, sempre avaliado. Negativo: sem P5 (T20).
Positivo: P4/P5 válidas (T21). **AUTORIZADO no caso positivo.**

## 15. Resultado E3-E

Condição declarativa `{campo: classificacao_tecnologica, etapa: P5,
operador: contem, valor: agente}`, avaliada pelo mesmo mecanismo
genérico do 2.6.1 (T25, sem hard-code de "E3-E" no núcleo).

## 16. Cenário não agêntico

`classificacao_tecnologica: "isolado"` → `E3-E` resolve **NÃO
APLICÁVEL** (exit 0, evento `EntregavelNaoAplicavel`), nunca falha
(T22). Materialização de E3 permanece válida, consolidando só a Parte A
(T26).

## 17. Cenário agêntico

`classificacao_tecnologica: "agente"` → `E3-E` resolve **AUTORIZADO**
(T24). Sem P5 encerrada, materialização é recusada por insumo
insuficiente (T23 — não há hoje nenhum artefato/schema de "especificação
completa de agente" no codebase para checar mais além disso, e inventar
esse requisito violaria a mesma regra de não invenção do pacote).
Materialização consolida Parte A + Parte B no mesmo arquivo
`caso/entregaveis/E3.md` (T27).

## 18. Resultado E4

Portão: P6/P7 encerradas + inegociável 2. Negativos: sem P7 (T28),
termo apenas proposto (T29). Positivo: termo decidido válido (T30).
**AUTORIZADO no caso positivo.**

## 19. Resultado E5

Portão: P8/P9/P10 encerradas + inegociáveis 3, 4, 5. Negativos: sem P8
(T32), sem I3 (T33), sem I4 (T34), sem I5 (T35). Positivo: todos
completos (T36). **AUTORIZADO no caso positivo.**

## 20. Total

**6/6 portões conformes** (contrato declarativo reavaliado a cada
chamada de `emitir()`, nunca aberto por flag).

## 21. Arquitetura de materialização

`eiac-campo/scripts/entregaveis.py`: cinco renderizadores
(`render_e1`–`render_e5`), cada um lendo os artefatos reais do domínio
correspondente e escrevendo Markdown estruturado seguindo as seções do
modelo oficial (EMCIA-E1–E5). Levanta `NaoMaterializavel` e recusa
renderizar quando falta evidência rastreável para um campo obrigatório
— nunca preenche com texto genérico. `--emitir` chama, após renderizar,
`avancar.py --emitir --materializar <arquivo>`, que só registra a
emissão se o arquivo existir e não estiver vazio.

## 22. E1 materializado

`caso/entregaveis/E1.md`, seção "4. Nível de complexidade declarado"
com eixos DAD/GOV/CRI e nível apurado (T15, T43).

## 23. E2 materializado

`caso/entregaveis/E2.md`, seção "A.3 Linha de base" com tabela
Marca/Indicador/Valor atual/Como foi obtido/Data reproduzindo
literalmente o artefato de baseline (T19, T44, T49).

## 24. E3 materializado

`caso/entregaveis/E3.md`, sempre com "A2. Classificação tecnológica";
"Parte B — Blueprint do agente" só presente quando agêntico (T26, T27,
T45).

## 25. E4 materializado

`caso/entregaveis/E4.md`, seções "1. O que muda no processo", "3.
Quando a solução erra" e "Termo de autonomia" (decisor, data,
justificativa) (T31, T46).

## 26. E5 materializado

`caso/entregaveis/E5.md`, seções "1. O que foi testado", "2. Resultado
contra a linha de base" (linha de base × resultado apurado) e "6. Plano
de medição e calibragem" (responsável, cadência) (T37, T47).

## 27. Total

**5/5 entregáveis materializáveis.**

## 28. Relação arquivo ↔ evento

Todo `EntregavelEmitido` bem-sucedido carrega `arquivo` e `versao`
apontando para o documento real (T38, T39, T51, T52). Tentativa de
emitir apontando para arquivo inexistente é recusada antes de qualquer
evento de sucesso (T40). Reemissão incrementa `versao` em
`estado.entregaveis_emitidos[ID]`, nunca sobrescreve silenciosamente
(T41, T42).

## 29. Teste de não invenção

Campo obrigatório sem evidência → materialização recusada, nunca
preenchida com texto genérico (T48). Dados presentes são reproduzidos
literalmente das fontes do caso, não resumidos nem reescritos por
geração livre (T49).

## 30. Caso de controle

`.projectdocs/evidencias/sprint2/2.6.5/caso-controle.md` — percurso
F0→E5 completo, cenário agêntico (E3-E autorizado), P6–P10 válidos, os
cinco inegociáveis satisfeitos a partir de artefato real, os seis
portões avaliados, os cinco entregáveis materializados, tentativa de
agente regravar termo já decidido recusada com evento
`TermoAutonomiaRecusado`.

## 31. Arquivos alterados

`eiac-nucleo/scripts/avancar.py` (emitir com NAO_APLICAVEL +
materializar), `eiac-nucleo/.claude-plugin/plugin.json` (versão);
`eiac-campo/scripts/baseline.py` (novo), `eiac-campo/scripts/
inegociaveis.py` (novo), `eiac-campo/scripts/entregaveis.py` (novo),
`eiac-campo/scripts/metrica.py` (baseline_ref), `eiac-campo/
template-caso/registro/baseline.schema.json` (novo), `eiac-campo/
template-caso/registro/metricas.schema.json` (baseline_ref),
`eiac-campo/skills/hb-medir/SKILL.md`, `eiac-campo/commands/medir.md`,
`eiac-campo/commands/emitir.md` (novo), `eiac-campo/reference/
gates.md`, `eiac-campo/.claude-plugin/plugin.json` (versão);
`testes/campo_2_6_5.py` (novo), `testes/nucleo_2_6_1.py` (T27b
corrigido para o contrato NAO_APLICAVEL).

## 32. Testes T01–T60

62 verificações (`2.6.5-T01`–`T60`, mais `T02b`/`T09b`), 0 falhas. Ver
`teste-2.6.5-T01.txt`–`teste-2.6.5-T60.txt` e
`teste-2.6.5-saida-completa.txt`.

## 33. Pares negativo/positivo

Todos os 10 pares obrigatórios da seção 60 do pacote cobertos: I1
(T01/T02), I2 (T03/T04), I3 (T05/T06), I4 (T07/T08), I5 (T09-T09b/T10),
E1 (T13/T14), E2 (T17/T18), E3-E (T22/T24), E4 (T29/T30), E5
(T35/T36), emissão (T40/T38-T39).

## 34. Eventos

`NivelApurado`, `EtapaEncerrada`, `SessaoDeCampoRegistrada`,
`LinhaDeBaseRegistrada`/`LinhaDeBaseRecusada`, `InegociavelSatisfeito`,
`EntregavelEmitido` (com `arquivo`/`versao`), `EntregavelNaoAplicavel`,
`RecusaEmissao`, `TermoAutonomiaRecusado` (fronteira agente/humano após
decisão) — ver `eventos.jsonl` desta pasta (caso de controle).

## 35. Resultado de hard-code

Busca por `E1`/`E2`/`E3-D`/`E3-E`/`E4`/`E5`/`baseline`/`autonomia`/
`saida_esperada`/`metrica de resultado`/`recalibragem` em
`eiac-nucleo/scripts/*.py`: todas as ocorrências são docstring de uso
(exemplo `--emitir E2`) ou comentário explicando o que o mecanismo
genérico não conhece. **0 ocorrências comportamentais** (T54).

## 36. Regressão antes/depois

342 → 404 verificações, 0 falhas em ambos os extremos. Ver
`teste-regressao-inicial.txt` e `teste-regressao-final.txt`.

## 37. Defeitos encontrados

Nenhum defeito de produção pré-existente. Um erro de nome de campo
introduzido neste próprio pacote (`entregaveis.py::render_e5` lia
`criterio_aprovacao` em vez de `criterio_aprovacao_escala`) foi
encontrado ao inspecionar o E5 materializado no caso de controle, antes
do commit.

## 38. Correções e retestes

Campo corrigido em `render_e5`; suíte completa (`campo_2_6_5.py`) e
caso de controle reexecutados, ambos limpos após a correção.

## 39. Situação D-12

**RESOLVIDO.** E1–E5 geram artefatos reais, o evento aponta para o
artefato e a versão, a versão é rastreável e incrementada sem
sobrescrita silenciosa, e emissão negada nunca produz documento válido
(recusa ocorre na renderização, antes de qualquer tentativa de
emissão).

## 40. Item adiado

2.6.6 — verificação integral F0–P10 (caso de controle único cobrindo
todas as camadas juntas, incluindo o cenário não agêntico dentro do
mesmo percurso, e fechamento final da Ação 2.6/Sprint 2).

## 41. Caminhos das evidências

`.projectdocs/evidencias/sprint2/2.6.5/`: `resultado.md`,
`matriz-portoes.md`, `matriz-inegociaveis.md`, `matriz-entregaveis.md`,
`caso-controle.md`, `caso-controle-driver.py`, `caso-controle-*.yaml`,
`caso-controle-E1..E5.md`, `caso-controle-estado-final.json`,
`caso-controle-log-comandos.txt`, `eventos.jsonl`,
`teste-regressao-inicial.txt`, `teste-regressao-final.txt`,
`teste-2.6.5-T01.txt`–`T60.txt`, `teste-2.6.5-saida-completa.txt`,
`diff.patch`, `git-show.txt`.

## 42. Entrada adicionada ao RTE-01

`§3.10.13 Pacote 2.6.5`, linha da tabela de pacotes atualizada para
"Concluído", D-12 marcado RESOLVIDO em `§3.11`, linha de revisão 0.14.

## 43. Versões antes/depois

| Componente | Antes | Depois | Motivo |
|---|---|---|---|
| `eiac-nucleo` | 0.2.15 | 0.2.16 | `avancar.py::emitir` genérico (NAO_APLICAVEL, `--materializar`) |
| `eiac-campo` | 0.6.0 | 0.7.0 | novos scripts (baseline, inegociáveis, entregáveis), novo domínio `registro/baseline/`, comando `/emitir` |

## 44. git diff --stat

Ver `diff.patch` (15 arquivos de implementação, 1855 inserções, 22
remoções, `eiac-nucleo/`+`eiac-campo/`+`testes/`).

## 45. git show --stat

Ver `git-show.txt` (commit `639a8d6`).

## 46. Hash do commit

`639a8d6` — `feat(field+nucleo): enforce deliverable gates and materialize E1-E5`

## 47. git status final

Limpo após o commit de implementação; evidência commitada em seguida
(`docs(evidence): register package 2.6.5 execution`).

## 48. Estado final

**CONFORME** quanto ao escopo executável do pacote (5/5 inegociáveis
semanticamente conformes, 6/6 portões conformes, 5/5 entregáveis
materializáveis, D-12 resolvido). Ação 2.6 e Sprint 2 permanecem em
aberto — fechamento final pertence a 2.6.6.
