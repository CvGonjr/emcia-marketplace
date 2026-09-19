# Matriz HB/AG final — pacote 2.6.6

HB: 18/18
AG: 4/4

## HB — catálogo e uso no caso de controle

| HB | Etapa(s) no playbook | Implementação física | Usada no caso de controle |
|----|---|---|---|
| HB-01 | F0 | `hb-enquadrar` | Sim (F0) |
| HB-02 | F0 | `hb-enquadrar` | Sim (F0) |
| HB-03 | F0 | `hb-enquadrar` | Sim (F0) |
| HB-04 | — (não referenciada no playbook) | Nenhuma (ver D-11, 2.6.4) | Não |
| HB-05 | — (não referenciada no playbook) | Nenhuma (ver D-11, 2.6.4) | Não |
| HB-06 | — (não referenciada no playbook) | Nenhuma (ver D-11, 2.6.4) | Não |
| HB-07 | P2 | `hb-extrair-regras` | Sim (P2, curadoria de RN-101) |
| HB-08 | P1 | `hb-mapear-contexto` | Sim (P1) |
| HB-09 | P1 | `hb-mapear-contexto` | Sim (P1) |
| HB-10 | P4 | `hb-priorizar` | Sim (P4, consulta a RN-101) |
| HB-11 | P5 | `hb-classificar` | Sim (P5, classificação agêntica) |
| HB-12 | P5 | `hb-classificar` | Sim (P5) |
| HB-13 | — (não referenciada no playbook) | Nenhuma (ver D-11, 2.6.4) | Não |
| HB-14 | P7 | `hb-governar` | Sim (P7, minuta de autonomia) |
| HB-15 | P8 | `hb-pilotar` | Sim (P8, casos de teste) |
| HB-16 | P8 | `hb-pilotar` | Sim (P8, execução da suíte) |
| HB-17 | P9 | `hb-medir-valor` | Sim (P9, apuração) |
| HB-18 | P10 | `hb-recalibrar` | Sim (P10, ciclos 1 e 2) |

**18/18 HB declaradas, 18/18 estruturalmente resolvíveis (catálogo
válido, todas as referências `hb` do playbook resolvem — ver
`teste-2.6.6-C19.txt`), 14/18 usadas neste caso de controle concreto.**
HB-04/05/06/13 não são exigidas por nenhuma etapa do contrato declarado
(campo `etapas: []`, `estado_relacao_etapa: "nao_referenciada_no_playbook"`)
— sua ausência de implementação física é a mesma situação já registrada
como `D-11 PARCIAL` em 2.6.4, não uma lacuna nova; "não utilizada neste
caso" aqui é sinônimo de "não referenciada no contrato", não de "faltante".

## AG — catálogo e participação no caso de controle

| AG | Camada | HB autorizadas | Implementação física | Participou do caso de controle |
|----|---|---|---|---|
| AG-01 | EX1 | HB-01–05 | Nenhuma (skills carregam HB-01/02/03 sem subagent dedicado) | Não (apenas referenciado no teste negativo de fronteira C21) |
| AG-02 | EX2 | HB-06/07/08/09/10/13 | `eiac-campo/agents/extrator-documental.md` (HB-07) | Sim (P6, proposta operacional) |
| AG-03 | EX2 | HB-11/12/14 | `eiac-campo/agents/classificador-tecnologico.md` (HB-11) | Sim (P7, minuta de autonomia) |
| AG-04 | EX2 | HB-15/16/17/18 | Nenhuma (skills carregam sem subagent dedicado) | Sim (P10, ciclos de calibragem) |

**4/4 AG declarados, 4/4 mapeados, 3/4 participaram efetivamente deste
caso de controle específico** (AG-01 não teve papel ativo porque F0 foi
conduzida diretamente pelo humano neste caso; sua fronteira formal foi
verificada de outro modo — C21, AG-01 recusado para HB-17).
**AG COM AUTORIDADE EX3/EX4 INDEVIDA: 0** (confirmado — nenhum dos
quatro agentes está declarado em camada EX3 ou EX4;
`eiac-campo/reference/agentes.json`).
