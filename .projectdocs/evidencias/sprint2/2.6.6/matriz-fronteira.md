# Matriz humano × agente — pacote 2.6.6

| Operação | Etapa | Automatizável | Agente | Humano | Resultado |
|----------|-------|---------------|--------|--------|-----------|
| Apurar nível e eixos | F0 | Sim (cálculo) | — | Celso do Vale registra | PASS |
| Encerrar F0–P2, P3d, P4 | F0–P4 | Sim (mecânica de etapa) | — | Celso do Vale (ator) | PASS |
| Curar RN-101 | P2 | Parcial (estrutura) | — | Celso do Vale via `curar.py` | PASS |
| Registrar linha de base | P3a | Não (declaração humana) | — | Marina Prado (declarante), Celso do Vale (registrado_por) | PASS |
| **Sessão de campo (P3b)** | **P3b** | **Não — não delegável** | **AG-01 tenta encerrar sem sessão** | **Celso do Vale registra sessão e encerra** | **NEGATIVO (agente recusado) / POSITIVO (humano com sessão)** |
| Propor especificação operacional | P6 | Sim (preparação) | AG-02 propõe | — | PASS (papel legítimo de agente) |
| **Validar especificação operacional (P6)** | **P6** | **Não — decisão humana** | **AG-02 tenta validar a própria proposta** | **Rafael Nogueira valida** | **NEGATIVO (agente recusado) / POSITIVO (humano valida)** |
| Preparar minuta de autonomia | P7 | Sim (preparação) | AG-03 prepara/propõe | — | PASS (papel legítimo de agente) |
| **Decidir autonomia (P7)** | **P7** | **Não — decisão humana** | **AG-03 tenta decidir** | **Marina Prado decide** | **NEGATIVO (agente recusado) / POSITIVO (humano decide)** |
| Gerar/revisar casos de teste | P8 | Sim (elaboração) | — | Celso do Vale elabora, Marina Prado revisa | PASS |
| Apurar métricas | P9 | Sim (cálculo) | — | Marina Prado apura | PASS |
| Registrar ciclo de calibragem (sem decisão) | P10 | Sim (detecção/quantificação/recomendação) | AG-04 registra ciclos 1 e 2 | — | PASS (papel legítimo de agente, ver docstring de `calibragem.py`) |
| **Decidir recalibragem (P10, ciclo com drift)** | **P10** | **Não — decisão humana (CAM-01 3.6)** | **AG-04 tenta gravar `decisao: recalibrar`** | **Marina Prado decide** | **NEGATIVO (agente recusado) / POSITIVO (humano decide)** |
| Resolver papel × capacidade (fronteira formal) | transversal | Sim (estrutural) | AG-01 × HB-17 (não autorizado) / AG-04 × HB-17 (autorizado) | — | NEGATIVO (AG-01) / POSITIVO (AG-04) |

## Camadas dos quatro agentes (catálogo formal)

| AG | Camada declarada | Pode operar em EX3/EX4? |
|----|---|---|
| AG-01 | EX1 | Não |
| AG-02 | EX2 | Não |
| AG-03 | EX2 | Não |
| AG-04 | EX2 | Não |

Nenhum agente lógico está declarado em EX3 ou EX4 (`eiac-campo/reference/agentes.json`).
A fronteira humana em P3b, na validação de P6, na decisão de P7 e na
decisão de recalibragem de P10 não depende de um agente "se comportar
bem" — decorre de checagens determinísticas em `operacional.py`,
`governanca.py` e `calibragem.py` (`E.autor_e_agente(ator)`), confirmadas
pelos quatro negativos acima, todos reproduzidos no caso de controle e
nas verificações C05, C09, C11, C18 (`testes/campo_2_6_6.py`).
