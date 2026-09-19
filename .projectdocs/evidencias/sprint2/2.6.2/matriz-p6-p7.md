# Matriz P6/P7 — pacote 2.6.2

**HEAD inicial:** `3f7fb2a1926619a27ba009e0fc07637ecaf18b74`

Fontes: EMCIA-CAM-01 §3.2/§3.3, EMCIA-MET-01 §3.4.6/§3.4.7, EMCIA-CAT-01
§3.4.4/§3.5.1, EMCIA-ESP-01 §3.5, EMCIA-E3 B1 (fronteira de delegação,
matriz de autonomia), EMCIA-E4 (guia operacional, seções 1-5).

## 1. Matriz P6/P7

| Elemento | P6 | P7 |
|---|---|---|
| Entrada | E3-E emitido (ou candidato), P5 encerrada, contexto CTX registrado | P6 encerrado; especificação operacional (`OP-*`) em `estado: validado`; arquétipo e zona de contenção de P4 |
| Saída | `registro/operacional/OP-NNN.yaml` — ponto de inserção nominado, entrada, saída, ator humano, sistema, exceção, fallback, responsável operacional | `registro/governanca/autonomia/AUT-NNN.yaml` — três listas (faz_sozinha/exige_aprovacao/nunca_faz), gatilhos de escalonamento, decisão registrada |
| Automação permitida | Ler E3/CTX, organizar fluxo, identificar interfaces, estruturar mapa técnico, gerar rascunho (`estado: proposta`), apontar inconsistências | Recuperar arquétipo, pesquisar/comparar/organizar referências regulatórias, preencher minuta (`estado: rascunho`/`proposto`) |
| Decisão humana | Validar (`estado: validado`) o desenho operacional — pessoa nomeada, nunca agente | Decidir (`estado: decidido`) a autonomia — pessoa nomeada, nunca agente; preencher `decisor`/`data_decisao`/`justificativa_decisao` |
| Camada EX | EX3 (N1/N2/N3) | EX4 (N1/N2/N3), `delegavel: false` |
| Dependências | `depende_de: P5` (playbook) | `depende_de: P6` (playbook); `operacional_ref` resolvendo para `OP-*` em `estado: validado` (checagem de campo, script `governanca.py`) |
| Evidência produzida | `OP-NNN.yaml` versionado, eventos `EspecificacaoOperacionalRegistrada`/`EspecificacaoOperacionalValidada`/`EspecificacaoOperacionalRecusada` | `AUT-NNN.yaml` versionado, eventos `TermoAutonomiaRegistrado`/`AutonomiaDecidida`/`TermoAutonomiaRecusado` |
| Relação com E4 | Insumo para EMCIA-E4 §1-2 ("o que muda no processo", "passo a passo da nova rotina") | Insumo para EMCIA-E4 §3-5 ("quando a solução erra", "o que a solução nunca faz", "papéis, acessos e registro") e para o inegociável 2 |

## 2. Matriz de autonomia (fonte: EMCIA-E3 B1.3/B1.4, CAT-01 §3.1)

| Tipo de ação | Agente pode preparar? | Agente pode decidir? | Humano requerido? |
|---|---|---|---|
| Estruturar desenho operacional (P6, `estado: proposta`) | Sim | Não | Sim, para `estado: validado` |
| Minutar termo de autonomia (P7, `estado: rascunho`/`proposto`) | Sim | Não | Sim, para `estado: decidido` |
| Classificar atividade como automatizada/híbrida/humana (E3 B1.3) | Sim (proposta, com justificativa) | Não | Sim, confirmação por quem executa o processo |
| Decidir o que a solução "faz sozinha" | Não | Não | Sim — regra absoluta (CAT-01 §3.5.1: "agente que propõe a própria autonomia" é antipadrão recusado) |
| Decidir o que "exige aprovação" e o aprovador nomeado | Não | Não | Sim |
| Decidir o que "nunca faz" (zona de contenção) | Não (pode listar candidatos a partir de P4) | Não | Sim |
| Pesquisar norma/política aplicável | Sim (localizar, resumir, comparar, organizar) | Não (aplicação ao caso é decisão humana) | Sim |
| Registrar decisão final de autonomia (`decisor`, `data_decisao`, `justificativa_decisao`) | Não | **Nunca** — bloqueado estruturalmente por `governanca.py` | Sim, pessoa nomeada |

## 3. Achado: G1 (guarda.py) e sessão humana

**Achado, não previsto no escopo original do pacote:** ao implementar
`hb-operacionalizar` (P6, EX3) e `hb-governar` (P7, EX4/`delegavel:false`),
foi identificado que `guarda.py` G1 bloqueava o **carregamento** do
próprio arquivo `SKILL.md` de qualquer etapa EX3/EX4, independentemente
de sessão humana registrada — comportamento pré-existente desde antes do
2.6.2 (já afetava `hb-confrontar`, `hb-priorizar`, `hb-classificar`).

Corrigido por decisão explícita: G1 passa a liberar o carregamento da
skill quando existe sessão humana válida registrada **para a mesma
etapa corrente** (`cumprimentos[etapa]["sessao"]`, gravado só por
`avancar.py --registrar-sessao`, que já recusa autor agente). Sessão de
outra etapa, ou ausente, continua bloqueando. A liberação é só de
**carregamento como instrumento de apoio/registro** — não delega decisão,
aprovação ou fechamento de etapa: `avancar.encerrar()` continua exigindo
sessão própria para `delegavel: false`, e `governanca.py`/`operacional.py`
continuam recusando agente em `estado: decidido`/`validado`
independentemente de G1.

Commit separado: `fix(nucleo): allow human-layer skills with valid session`.

## 4. Verificação de hard-code EMCIA

Busca `grep -rniE` por P6, P7, autonomia, governança/governanca, E4 em
`eiac-nucleo/`: ver `resultado.md` §15 para a lista completa e
classificação de cada ocorrência.
