# Resumo final da Ação 2.6 — Camada de Agentes e Protocolos

Sprint 2 · Ação 2.6

Síntese consolidada dos pacotes 2.6.0–2.6.6, construída exclusivamente a
partir do baseline S2-BL, do EMCIA-RTE-01 oficial, das evidências
persistidas e dos commits reais do repositório `emcia-marketplace`.

HEAD inicial: `667c0212e81721b67b3dcf866b3eb3333a7d60d4`
HEAD final: `6f4bb2f`
17 commits
Data: 19/09/2026

---

## 1. Identificação

**HEAD**

| Campo | Valor |
|---|---|
| Inicial (início 2.6.0) | `667c0212e81721b67b3dcf866b3eb3333a7d60d4` |
| Final (fim 2.6.6) | `6f4bb2f` |

**Versões**

| Componente | Inicial | Final |
|---|---|---|
| eiac-nucleo | `0.2.11` | `0.2.16` |
| eiac-campo | `0.3.8` | `0.7.1` |
| playbook | `0.3.1` | `0.4.0` |

---

## 2–3. Estado inicial (S2-BL) → estado final (após 2.6.6)

| Indicador | S2-BL | Final Ação 2.6 |
|---|---|---|
| Etapas declaradas | 8/13 | **13/13** |
| Etapas operacionalmente executáveis | 8/13 (F0–P5) | **13/13** |
| Percurso F0–P10 | ausente | **PASS** |
| P7 | ausente | **operacional, decisão humana protegida** |
| P10 | ausente | **recorrente, 2 ciclos demonstrados** |
| Máquina de estados / dependências | parcial | **CONFORME** |
| Guardas EX / proteção `registro/` | desprotegido | **SIM** |
| Eventos de recusa | sem trilha completa | **CONFORME** |
| HB referenciadas / código estável / critério | 9/18 · 0/18 · — | **18/18 · 14/18 · 13/13** |
| AG físicos / formalmente mapeados | 2 · 0/4 | **2 · 4/4** |
| Inegociáveis semanticamente verificáveis | 0/5 | **5/5** |
| Portões conformes | 2/6 | **6/6** |
| E4 | não operacional | **autorizado e materializado** |
| E5 | divergente | **autorizado e materializado** |
| Materialização E1–E5 | ausente | **5/5** |
| P10 recorrente | — | **SIM** |
| AG com autoridade EX3/EX4 indevida | — | **0** |

---

## 4. Caso de controle final (2.6.6)

ID: `caso-controle-2.6.6` — caso novo, template padrão, nível **N2**,
cenário **agêntico** (decisão registrada em P5, não forçada). Nenhum
estado reaproveitado de casos anteriores.

| Etapa | Ator predominante | Camada EX | Principal saída | Resultado |
|---|---|---|---|---|
| F0 | Celso do Vale (humano) | EX1→EX2 | Nível N2 apurado, E1 emitido e materializado | PASS |
| P1 | Celso do Vale | EX2 | Setor/processo-alvo levantado, etapa encerrada | PASS |
| P2 | Celso do Vale (via `curar.py`) | EX2 | RN-101 curada em `contexto/regras/` | PASS |
| P3a | Marina Prado (declarante) | EX3 | Linha de base BL-101 (medido, N2, 3 dias úteis) | PASS |
| P3b | Celso do Vale (não delegável, sessão obrigatória) | EX4 | Sessão registrada, etapa encerrada | PASS |
| P3d | Celso do Vale | EX3 | RN-101 confrontada, sem divergência aberta | PASS |
| P4 | Celso do Vale (consulta via `consultar.py`) | EX2 | RN-101 consumida sem reinferência | PASS |
| P5 | Celso do Vale | EX2/EX3 | `classificacao_tecnologica: agente` — abre E3-E | PASS |
| P6 | AG-02 propõe / Rafael Nogueira valida | EX2 → EX3 | OP-101 validado (agente tentando validar a própria proposta, recusado) | PASS |
| P7 | AG-03 prepara minuta / Marina Prado decide | EX2 → EX4 | AUT-101 decidido (agente tentando decidir, recusado) | PASS |
| P8 | Celso do Vale / Marina Prado revisa | EX2/EX3 | CT-101: 1 caso aderente + 1 divergente (falha funcional honesta, calculada) | PASS |
| P9 | Marina Prado | EX2 | MET-101 (resultado, contra BL-101: 3d→1d) + MET-102 (uso) | PASS |
| P10 | AG-04 (ciclos) / Marina Prado (decisão) | EX2 → EX4 | CAL-101 + 2 ciclos | PASS |

**Registros de ponto crítico**

- **Validação humana de P6:** AG-02 recusado ao tentar validar a própria proposta; Rafael Nogueira valida.
- **Decisão humana de autonomia (P7):** AG-03 recusado ao tentar decidir; Marina Prado decide (AUT-101 decidido).
- **P8 — saída esperada:** 2 casos, ambos com saída esperada declarada antes da execução; 1 aderente, 1 divergente.
- **P9 — métrica de resultado:** MET-101 (tipo `resultado`), distinta de MET-102 (tipo `uso`), `baseline_ref: BL-101`.
- **P10 — dois ciclos:** ciclo 1 sem drift (persistido, sem decisão exigida); ciclo 2 com drift detectado e quantificado por AG-04, recomendação "recalibrar", decisão humana final.
- **Drift / recomendação / decisão:** drift "+150% sobre o resultado apurado em P9"; recomendação do agente: recalibrar limiares; decisão humana (Marina Prado): recalibrar.

---

## 5. Fronteira humano × agente

| Etapa | Agente | Humano |
|---|---|---|
| P3b | AG-01 tenta encerrar sem sessão → **recusado** | Celso do Vale registra sessão e encerra → **PASS** |
| P6 (validação) | AG-02 tenta validar a própria proposta → **recusado** | Rafael Nogueira valida → **PASS** |
| P7 (decisão) | AG-03 tenta decidir autonomia → **recusado** | Marina Prado decide → **PASS** |
| P10 (recalibragem) | AG-04 tenta gravar `decisao: recalibrar` → **recusado** | Marina Prado decide → **PASS** |

**AG assumindo EX3/EX4:** nenhuma ocorrência — os 4 agentes lógicos
estão declarados em EX1/EX2 no catálogo
(`eiac-campo/reference/agentes.json`); a proteção decorre de checagens
determinísticas em `operacional.py`, `governanca.py` e `calibragem.py`,
não de convenção.

---

## 6. HB e AG

- HB formalizadas: **18/18**
- HB resolvíveis: **18/18**
- HB automatizadas com critério: **13/13**
- AG mapeados: **4/4**

**HB utilizadas no caso final (14/18):** HB-01, HB-02, HB-03, HB-07,
HB-08, HB-09, HB-10, HB-11, HB-12, HB-14, HB-15, HB-16, HB-17, HB-18.

| AG | Nome | HB autorizadas | Participou do caso final? |
|---|---|---|---|
| AG-01 | Agente de enquadramento | HB-01–05 | Não (verificado só pela fronteira formal) |
| AG-02 | Agente de análise documental | HB-06/07/08/09/10/13 | Sim — P6 |
| AG-03 | Agente de especificação | HB-11/12/14 | Sim — P7 |
| AG-04 | Agente de avaliação | HB-15/16/17/18 | Sim — P10 |

**Agentes físicos finais:** 2
(`eiac-campo/agents/classificador-tecnologico.md` → AG-03/HB-11;
`eiac-campo/agents/extrator-documental.md` → AG-02/HB-07).
**Relação agentes físicos × AG lógicos:** parcial — 2 dos 4 AG lógicos
têm subagente físico dedicado; os demais (AG-01, AG-04) e as demais HB
de AG-02/AG-03 são carregados por skill sem subagent próprio.

---

## 7. Cinco inegociáveis

| ID | Descrição | Evidência | Resultado |
|---|---|---|---|
| I1 | Linha de base antes do piloto | `BL-101.yaml` — medido, N2, 3 dias úteis, 2026-09-01 | PASS |
| I2 | Termo de autonomia escrito | `AUT-101.yaml` — decidido, decisor Marina Prado, justificativa registrada | PASS |
| I3 | Casos com saída esperada | `CT-101.yaml` — revisado, 2 casos, ambos com `saida_esperada` | PASS |
| I4 | Métrica de resultado | `MET-101.yaml` — tipo `resultado`, apurada, "1 dia útil" | PASS |
| I5 | Responsável nominal pela calibragem | `CAL-101.yaml` — responsável Marina Prado (pessoa nomeada) | PASS |

**Resultado: 5/5** — todos verificados a partir de artefato real via
`eiac-campo/scripts/inegociaveis.py`, nenhuma flag manual usada como
prova.

---

## 8. Seis autorizações

| Portão | Requisitos | Resultado |
|---|---|---|
| E1 | F0 encerrada | AUTORIZADO |
| E2 | P1–P3d + I1 satisfeito | AUTORIZADO |
| E3-D | P4, P5 encerradas | AUTORIZADO |
| E3-E | Aplicável (classificação P5 = agente) | AUTORIZADO |
| E4 | P6, P7 + I2 satisfeito | AUTORIZADO |
| E5 | P8, P9, P10 + I3/I4/I5 satisfeitos | AUTORIZADO |

**Resultado: 6/6** aplicáveis/conformes (cenário agêntico — E3-E
avaliado, não NÃO APLICÁVEL).

---

## 9. Cinco entregáveis

| Entregável | Arquivo real | Versão |
|---|---|---|
| E1 — Ficha de Enquadramento | `caso/entregaveis/E1.md` | 1 |
| E2 — Diagnóstico e Oportunidade | `caso/entregaveis/E2.md` | 1 |
| E3 — Blueprint da Solução | `caso/entregaveis/E3.md` | 1 |
| E4 — Guia Operacional | `caso/entregaveis/E4.md` | 1 |
| E5 — Relatório de Piloto | `caso/entregaveis/E5.md` | 1 |

Todos existem fisicamente e não vazios · todos possuem versão
rastreável em `estado.entregaveis_emitidos` · todo evento
`EntregavelEmitido` aponta para arquivo + versão · **E3 permaneceu um
único entregável** ao cliente apesar de consolidar as duas autorizações
internas E3-D e E3-E (Parte A sempre presente, Parte B presente porque
E3-E autorizou).

---

## 10. Testes

| Marco | Total | Pass | Fail | Skip |
|---|---|---|---|---|
| Suíte no S2-BL | 26 | 26 | 0 | 0 |
| Suíte final da Ação 2.5 | 129 | 129 | 0 | 0 |
| Suíte no início de 2.6.6 | 404 | 404 | 0 | 0 |
| Testes consolidados 2.6.6 (C01–C43) | 43 | 43 | 0 | — |
| Suíte final após 2.6.6 | 447 | 447 | 0 | 0 |

**Resultado do caso integral F0–P10:** PASS — 13/13 etapas, 0 falhas
inesperadas fora dos negativos planejados.

---

## 11. Defeitos D-07 a D-13

| ID | Estado inicial | Pacote que tratou | Correção | Estado final |
|---|---|---|---|---|
| D-07 | Só 8/13 etapas declaradas | 2.6.0 | Playbook v0.3.1→v0.4.0, 13/13 etapas + fronteiras | RESOLVIDO |
| D-08 | `registro/` permite escrita direta | 2.6.1 | Guarda G5 (`guarda.py`) | RESOLVIDO |
| D-09 | Recusas da máquina sem evento | 2.6.1 | `RecusaMaquina`/`TentativaNegada` em toda recusa | RESOLVIDO |
| D-10 | P7 e P10 ausentes | 2.6.2 / 2.6.3 | Fluxo de governança (P7) e calibragem recorrente (P10) | RESOLVIDO |
| D-11 | HB/AG sem códigos e relações estáveis | 2.6.4 | Catálogo 18/18 formal e resolvível; 4/18 HB sem skill física | PARCIAL |
| D-12 | Emissão autoriza, não materializa | 2.6.5 | `--materializar` + `entregaveis.py` | RESOLVIDO |
| D-13 | Sem percurso positivo F0–P10 | 2.6.6 | Caso de controle novo, 13/13 etapas, 43 verificações | RESOLVIDO |

**D-2.6.6-01** (defeito adicional, descoberto durante 2.6.6):
`calibragem.py::checar_autoria()` bloqueava indevidamente autoria de
agente também em `ciclo_calibragem`, contrariando o próprio contrato
documentado do módulo. Corrigido com `checar_autoria_ciclo()` dedicada
(commit `31ffff2`), sem alterar a vedação de decisão a agente.

---

## 12. Principais componentes implementados

**eiac-nucleo**
- `avancar.py` — máquina de etapas, condições declarativas, inegociáveis, emissão com `NAO_APLICAVEL` e `--materializar`
- `guarda.py` — G1–G5 (camada, escrita em `caso/`, `contexto/`, dependência, `registro/`)
- `catalogo.py` — resolução genérica papel×capacidade
- `playbook.py` — checagens estruturais do contrato

**eiac-campo**
- `operacional.py`, `governanca.py` — P6/P7
- `piloto.py`, `metrica.py`, `calibragem.py` — P8/P9/P10
- `baseline.py`, `inegociaveis.py` — I1–I5
- `entregaveis.py` — materialização E1–E5

**catálogos**
- `reference/habilidades.json` — 18 HB
- `reference/agentes.json` — 4 AG
- `agents/classificador-tecnologico.md`, `agents/extrator-documental.md`

**artefatos operacionais / templates**
- `registro/baseline.schema.json`, `operacional.schema.json`, `autonomia.schema.json`, `piloto.schema.json`, `metricas.schema.json`, `calibragem.schema.json`
- `skills/hb-emitir-e1..e5`, `commands/emitir.md`

---

## 13. Commits 2.6.0–2.6.6

| Hash | Pacote | Título |
|---|---|---|
| `f3ae15e` | 2.6.0 | refactor(playbook): freeze full F0-P10 execution contract |
| `70d1d9b` | 2.6.0 | docs(evidence): close package 2.6.0 |
| `2105f6c` | 2.6.1 | feat(nucleo): enforce generic F0-P10 protocol contracts |
| `3f7fb2a` | 2.6.1 | docs(evidence): close package 2.6.1 |
| `f1f1a4c` | 2.6.2 | fix(nucleo): allow human-layer skills with valid session |
| `25905ac` | 2.6.2 | feat(field): implement P6-P7 operational governance flow |
| `144b7c6` | 2.6.2 | docs(evidence): register package 2.6.2 execution |
| `3431e6f` | 2.6.2 | docs(evidence): close package 2.6.2 |
| `e210266` | 2.6.3 | feat(field): implement P8-P10 pilot measurement calibration flow |
| `418a916` | 2.6.3 | docs(evidence): register package 2.6.3 execution |
| `dff5a08` | 2.6.4 | feat(field): formalize HB and AG capability catalogs |
| `57700a0` | 2.6.4 | docs(evidence): register package 2.6.4 execution |
| `639a8d6` | 2.6.5 | feat(field+nucleo): enforce deliverable gates and materialize E1-E5 |
| `bcc85a6` | 2.6.5 | docs(evidence): register package 2.6.5 execution |
| `31ffff2` | 2.6.6 | fix(field): allow agent authorship of calibration cycle records |
| `1599e51` | 2.6.6 | test(workflow): verify full F0-P10 execution path |
| `6f4bb2f` | 2.6.6 | docs(evidence): register package 2.6.6 execution |

---

## 14. Comparação baseline → final

Ver tabela completa na seção 2–3 acima (mesmo conteúdo, formato exigido
pela seção 14 da instrução original).

---

## 15. Resultado final oficial

**Ação 2.6 — Camada de Agentes e Protocolos: CONFORME**

Escopo executável de referência: 13/13 etapas, 6/6 portões, 5/5
inegociáveis, 5/5 entregáveis, proteção de `registro/`/`contexto/`
confirmada, fronteira humana preservada, percurso F0–P10 demonstrado.
Ressalva não bloqueante: D-11 PARCIAL.

**Sprint 2 (Ação 2.5 + Ação 2.6): CONFORME**

Implementação de referência do Estúdio de Trabalho concluída para as
duas camadas, dentro do escopo acadêmico definido.

---

## 16. Limitações remanescentes

- **Dívida técnica** — D-11 PARCIAL: 4/18 HB (HB-04, HB-05, HB-06,
  HB-13) sem implementação física própria; nenhuma é exigida pelo
  contrato F0–P10 congelado, mas o catálogo formal não corresponde 1:1
  a skills executáveis.
- **Limitação técnica** — P5 sem script executável dedicado: não existe
  `eiac-campo/scripts/classificar.py` equivalente a
  `baseline.py`/`operacional.py`; a skill `hb-classificar` produz
  apenas texto livre. Registrado em 2.6.5 e reafirmado em 2.6.6, não
  corrigido por não ser capacidade já especificada a implementar neste
  ciclo.
- **Fora do escopo acadêmico** — nenhuma integração real com sistemas
  externos de cliente; nenhuma infraestrutura de produção; nenhum ROI
  empresarial comprovado; P10 não roda automaticamente em produção —
  todo o percurso foi demonstrado sob controle, com atores simulados.
- **Fora do escopo acadêmico** — o objeto de verificação é o método
  (EMCIA), materializado como implementação de referência executável —
  não uma solução empresarial implantada no cliente.

---

## 17. Prints reais recomendados para o relatório

**FIGURA A — Playbook F0–P10**
Objetivo: mostrar o contrato declarativo completo.
Comando: `cat eiac-campo/template-caso/registro/playbook.json | python3 -m json.tool | less`
Tela: array `etapas` com as 13 entradas F0→P10, campo `depende_de` visível.
Por quê: resolve D-07 na origem — prova visual do contrato completo.

**FIGURA B — Catálogo HB → AG → critério**
Objetivo: Etapa → HB → AG → `criterio_de_verificacao`.
Comando: `cat eiac-campo/reference/habilidades.json | python3 -m json.tool | less`
Tela: um item HB completo (ex. HB-11) com `etapas`, `ag_autorizado`, `criterio_de_verificacao`.
Por quê: prova rastreabilidade formal de D-11.

**FIGURA C — Recusa de decisão + decisão humana**
Objetivo: agente tentando decidir autonomia, recusado; humano decide.
Comando: `python3 eiac-campo/scripts/governanca.py --arquivo registro/governanca/autonomia/AUT-101.yaml --ator AG-03` seguido do mesmo comando com `--ator "Marina Prado"`
Tela: mensagem de recusa citando "agente não pode decidir autonomia", depois "termo de autonomia gravado".
Por quê: evidência direta e determinística da fronteira EX3/EX4.

**FIGURA D — P10: ciclos e drift**
Objetivo: recorrência de P10 com drift detectado.
Arquivo: `.projectdocs/evidencias/sprint2/2.6.6/caso-controle-CAL-101-C02.yaml`
Tela: `drift_detectado: true`, `drift_quantificacao`, `recomendacao_agente`, `decisao: recalibrar` com `decisor: Marina Prado`.
Por quê: único artefato que mostra detecção agêntica + decisão humana no mesmo objeto.

**FIGURA E — Inegociáveis e portões avaliados**
Objetivo: 5 inegociáveis + 6 portões em execução real.
Arquivo: `.projectdocs/evidencias/sprint2/2.6.6/teste-2.6.6-saida-completa.txt`
Tela: trecho com `I1 | satisfeito=True` … `I5`, seguido de `E3-D`/`E3-E` "AUTORIZADO".
Por quê: prova textual, na mesma tela, de todo o núcleo semântico da Ação 2.6.

**FIGURA F — Entregável materializado (E3)**
Objetivo: E3-D + E3-E consolidados em um único arquivo.
Arquivo: `.projectdocs/evidencias/sprint2/2.6.6/caso-controle-E3.md`
Tela: "Parte A — Decisão" e "Parte B — Blueprint do agente" no mesmo documento.
Por quê: evidência direta de D-12 resolvido e da regra "um único E3 ao cliente".

**FIGURA G — Resultado final do caso + suíte**
Objetivo: percurso F0–P10 completo e regressão final.
Comando: `python3 testes/campo_2_6_6.py` seguido de `bash testes/negativos.sh`
Tela: "43 verificacoes do pacote 2.6.6, 0 falhas" e "todas as travas recusam como devem".
Por quê: fecha o argumento com prova executável, reproduzível por qualquer leitor.

---

Fontes: EMCIA-RTE-01 (oficial) · S2-BL (HEAD `9a54017`) · evidências
`.projectdocs/evidencias/sprint2/2.6.0`–`2.6.6` · commits reais
`f3ae15e`…`6f4bb2f`. Nenhum valor inventado; nenhuma implementação
reexecutada para esta síntese.
