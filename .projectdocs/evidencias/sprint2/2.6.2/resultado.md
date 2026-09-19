# Pacote 2.6.2 — P6 e P7

## 1. Identificação

**Ação:** 2.6 — Agentes e Protocolos
**Pacote:** 2.6.2
**Branch:** master
**HEAD inicial:** `3f7fb2a1926619a27ba009e0fc07637ecaf18b74`
**HEAD final:** registrado em `git-show.txt` após o commit deste pacote.
**Data/hora:** 2026-09-19 00:23 -0300

## 2. Documentos consultados

Leitura obrigatória: EMCIA-MET-01 §3.4.6/§3.4.7, EMCIA-CAT-01 §3.4.4/
§3.5.1, EMCIA-ESP-01 §3.5, EMCIA-TRA-01 (marcação de procedência,
consultado), EMCIA-E3 (Blueprint — Parte B1, fronteira de delegação,
matriz de autonomia B1.3/B1.4), EMCIA-E4 (Guia operacional, §1-5),
EMCIA-GLO-01, EMCIA-TST-01, EMCIA-ARQ-01. Consultado: EMCIA-CTX-01,
EMCIA-VER-01, evidências de 2.6.0 e 2.6.1.

## 3. Baseline relacionado

`D-10` (P7/P10 ausentes) — este pacote trata a parte de P7; P10
permanece para 2.6.3. Achados do S2-BL: P6 AUSENTE, P7 AUSENTE, P7 não
delegável AUSENTE operacionalmente, E4 declarado para P6/P7 mas
bloqueado pela ausência das etapas, inegociável 2 ainda não
semanticamente verificável.

## 4. Estado inicial

Playbook (2.6.0) já declarava P6/P7 com `delegavel`/`camada`/
`depende_de` corretos, mas nenhuma skill, script ou objeto de domínio
existia para eles — `eiac-campo/skills/` não tinha `hb-operacionalizar`
nem `hb-governar`; não havia schema nem script para especificação
operacional ou termo de autonomia. `reference/gates.md` e
`hb-emitir-e4/SKILL.md` ainda citavam a pendência de correspondência
entregável×passo já resolvida em 2.6.0 (`decisoes/013`).

Achado adicional durante a implementação (não estava no escopo original
do pacote): `guarda.py` G1 bloqueava o carregamento do próprio
`SKILL.md` para qualquer etapa EX3/EX4, independentemente de sessão
humana registrada — comportamento pré-existente desde antes do 2.6.2,
que já afetava `hb-confrontar`, `hb-priorizar`, `hb-classificar` e
passaria a afetar `hb-operacionalizar`/`hb-governar` do mesmo jeito.
Tratado como correção de defeito pré-existente, não como escopo novo.

## 5. Contrato de P6

EMCIA-CAM-01 §3.2: entrada (E3-E/P5 encerrada, contexto registrado),
saída (ponto de inserção nominado, entrada, saída, ator humano, sistema,
exceção, fallback, responsável operacional). EMCIA-MET-01 §3.4.6 confirma
o mesmo critério de encerramento. P6 produz **especificação**, nunca
deployment — não constrói, não integra, não implanta.

## 6. Implementação de P6

Terceiro domínio de registro, distinto de `contexto/` (CTX-01) e de
`registro/governanca/` (P7): `registro/operacional/OP-NNN.yaml`, schema
`registro/operacional.schema.json`. Script `eiac-campo/scripts/
operacional.py` reaproveita `estrutura.validar()`, `estado.evento()` e
`estado.autor_e_agente()` do núcleo sem alterá-los. Dois estados apenas
— `proposta`→`validado` (não copia os três estados do termo de
autonomia, que são semântica própria de P7, por decisão explícita).
Agente pode gravar `proposta`; só humano nomeado pode gravar `validado`.
`operacional_ref` (`OP-NNN`) é a referência estável que P7 consome.

## 7. Contrato de P7

EMCIA-CAM-01 §3.3, EMCIA-CAT-01 §3.5.1 ("nenhum agente define a própria
autonomia... regra absoluta, sem exceção por nível ou prazo"),
EMCIA-E3 B1.3/B1.4 (classificação de atividades, cinco modos de
delegação). P7 produz o termo de autonomia: três listas (`faz_sozinha`,
`exige_aprovacao`, `nunca_faz`), gatilhos de escalonamento, decisão
registrada com decisor nominal.

## 8. Fronteira agente × humano

Implementada estruturalmente em ambos os scripts, não apenas
documentada: `operacional.py` recusa agente gravando `estado: validado`;
`governanca.py` recusa agente gravando `estado: decidido`, e recusa
também nome genérico de coletivo ("equipe", "área" etc.) como decisor —
mesma convenção `_ator_valido()` já usada por `avancar.registrar_recorrencia()`
(2.6.1). Nenhuma das duas checagens está no núcleo: ambas vivem nos
scripts de campo, que importam `estado.autor_e_agente()` genérico.

## 9. Termo de autonomia

`registro/governanca/autonomia/AUT-NNN.yaml`, schema `registro/
autonomia.schema.json`. Estados `rascunho`→`proposto`→`decidido`.
`operacional_ref` obrigatório e resolvido (`checar_operacional_ref()`):
o termo não pode ser preparado, muito menos decidido, sem referenciar
uma especificação operacional já `validada` — relação P7→P6 aplicada
por checagem de campo em `eiac-campo`, não por `depende_de` no núcleo
(que já cobre a dependência entre *etapas*, separadamente). Estado
`decidido` exige `decisor`, `data_decisao`, `justificativa_decisao`
preenchidos, além de decisor não-agente.

## 10. Arquitetura núcleo × campo

Nenhuma linha de `eiac-nucleo/scripts/avancar.py` foi alterada para
conhecer P6/P7 (a única mudança de núcleo neste pacote é a correção de
G1 em `guarda.py`, genérica). `operacional.py` e `governanca.py` vivem
inteiramente em `eiac-campo/scripts/`, importando apenas as primitivas
genéricas já existentes. Verificação de hard-code (§15) confirma:
nenhuma ocorrência comportamental de P6, P7, autonomia, governança ou E4
em `eiac-nucleo/`.

## 11. Caso de controle

`PP-TEST-2.6.2-001` — ver `caso-controle.md`. Percurso completo F0→P7:
P6 proposto por agente (`AG-02`), validado por humano (`Rafael
Nogueira`); P7 preparado por agente (`AG-03`, rascunho→proposto),
tentativa de decisão por agente **recusada** com evento
`TermoAutonomiaRecusado`, decisão final por humano nomeado (`Marina
Prado`) com evento `AutonomiaDecidida`. Evidência do inegociável 2
registrada via `avancar.py --satisfazer-inegociavel 2`. Nota honesta:
`avancar.py --emitir E4` retornou `exit 0` neste caso (portão estrutural
satisfeito pelo mecanismo genérico de 2.6.1) — isso não substitui a
validação semântica do inegociável 2 nem a materialização do documento,
ambas do pacote 2.6.5.

## 12. Testes

38 verificações (`2.6.2-T01`–`T33` + `G1a`/`G1b`/`G1c`), todas PASS. Ver
`teste-2.6.2-T01.txt` a `teste-2.6.2-T33.txt`.

## 13. Pares negativo/positivo

Todos os sete pares exigidos pelo §41 do pacote estão cobertos: P6
sem/com dependência (T02/T01), P7 sem/com P6 (T08/T07), agente
decide/prepara (T10/T09), agente confirma/humano confirma minuta
(T10/T11), sem/com responsável nominal (T12/T13), escrita direta/
caminho autorizado em `registro/` (T18/T19), booleano/termo rastreável
do inegociável (T27/T26).

## 14. Eventos

Novos tipos, todos emitidos por scripts de `eiac-campo/scripts/`:
`EspecificacaoOperacionalRegistrada`, `EspecificacaoOperacionalValidada`,
`EspecificacaoOperacionalRecusada` (P6); `TermoAutonomiaRegistrado`,
`AutonomiaDecidida`, `TermoAutonomiaRecusado` (P7). Reaproveitam
`estado.evento()` do núcleo sem modificá-lo. Evidência completa em
`eventos.jsonl` desta pasta.

## 15. Hard-code

Busca `grep -rniE` por P6, P7, autonomia, governança/governanca, E4 em
`eiac-nucleo/scripts/`, `eiac-nucleo/commands/`, `eiac-nucleo/hooks/`
após as edições deste pacote: **1 ocorrência**, não comportamental —
`avancar.py` linha ~147, comentário pré-existente (desde 2.6.1)
explicando o que o núcleo não decide ("baseline, termo de autonomia
etc."). Nenhum `if etapa == "P6"`/`if etapa == "P7"` ou equivalente.
`HARD-CODE EMCIA NO NÚCLEO: 0` comportamental.

## 16. Regressão

**Antes:** 197 verificações (158 da Ação 2.5+2.6.0 + 39 de 2.6.1), 197
PASS, 0 FAIL, 0 SKIP. Ver `teste-regressao-inicial.txt` (executado sobre
o estado imediatamente anterior a este pacote, via `git stash`
temporário, restaurado em seguida sem perda).

**Pacote 2.6.2:** 38 verificações, 38 PASS, 0 FAIL.

**Depois:** 235 verificações, 235 PASS, 0 FAIL, 0 SKIP. Ver
`teste-regressao-final.txt`.

Comparação histórica: S2-BL 26 → Ação 2.5 129 → 2.6.0 158 → 2.6.1 197 →
2.6.2 235. Crescimento rastreável aos requisitos deste pacote.

## 17. Defeitos encontrados

Um defeito de produção real, pré-existente (não introduzido pelos
pacotes 2.6.0/2.6.1), descoberto ao implementar `hb-operacionalizar`/
`hb-governar`: G1 em `guarda.py` bloqueava o carregamento de qualquer
skill EX3/EX4 mesmo com sessão humana registrada para a etapa. Corrigido
por decisão explícita do usuário, com testes negativo/positivo/negativo
(G1a/G1b/G1c) e regressão completa das suítes anteriores.

## 18. Correções e retestes

G1 corrigida em `eiac-nucleo/scripts/guarda.py`: passa a checar
`cumprimentos[etapa]["sessao"]` (gravado só por `avancar.py
--registrar-sessao`, que já recusa agente) antes de bloquear
carregamento — sessão de outra etapa, ou ausente, continua bloqueando.
`avancar.encerrar()` continua exigindo sessão própria para
`delegavel:false`; `operacional.py`/`governanca.py` continuam recusando
agente em `estado: validado`/`decidido` independentemente de G1. Suíte
completa (235 verificações) reexecutada após a correção, 0 falhas.

Documentação stale corrigida: `reference/gates.md` e `hb-emitir-e4/
SKILL.md` citavam a pendência de correspondência entregável×passo já
resolvida em 2.6.0 (`decisoes/013`) — atualizados para refletir E4=P6/P7,
E5=P8/P9/P10.

## 19. Evidência produzida para E4

`registro/operacional/OP-*.yaml` (insumo das seções 1-2 de EMCIA-E4) e
`registro/governanca/autonomia/AUT-*.yaml` (insumo das seções 3-5,
inegociável 2). Ambos versionados, com autoria e eventos rastreáveis.
**Não** materializados como `caso/entregaveis/E4.md` — isso é 2.6.5.
**Não** declarada validação semântica final do inegociável 2 — o núcleo
confirma apenas que a evidência é uma string não vazia associada a
autor humano e ao item real do playbook, não que o conteúdo do termo
satisfaz o método.

## 20. Itens adiados

- **2.6.3** — P8, P9 e P10 operacionais; recorrência operacional
  completa de P10.
- **2.6.4** — 18 HB e 4 AG mapeados formalmente; critérios de
  verificação reais conectados ao mecanismo isolado de 2.6.1.
- **2.6.5** — validação semântica completa dos cinco inegociáveis
  (incluindo o conteúdo do termo de autonomia e da especificação
  operacional), portões finais, materialização de E4/E5.
- **2.6.6** — percurso F0–P10 end-to-end e suíte integral.

## 21. Commit

Ver `git-show.txt` nesta pasta. Dois commits: correção de G1
(`fix(nucleo): allow human-layer skills with valid session`) e
implementação de P6/P7 (`feat(field): implement P6-P7 operational
governance flow`).

## 22. Estado final

**CONFORME.**

P6 e P7 estão operacionalmente executáveis, preservando a decisão
humana sobre a fronteira de autonomia em ambos. Nenhuma decisão de
autonomia foi ou pode ser tomada por agente — cada tentativa é recusada
estruturalmente, com evento. P6/P7 produzem os insumos rastreáveis
necessários para E4; **não se afirma que E4 está emitido em definitivo**
— essa validação pertence ao 2.6.5.
