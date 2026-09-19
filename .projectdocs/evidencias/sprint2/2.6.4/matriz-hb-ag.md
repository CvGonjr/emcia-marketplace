# Matriz final HB/AG — pacote 2.6.4

Estado final, após implementação. Fonte: `eiac-campo/reference/habilidades.json`
e `eiac-campo/reference/agentes.json`.

## HB × AG × EX × Etapas × Skill × Automatizada × Critério × Estado

| HB | AG | EX | Etapas | Skill | Automatizada | Critério de verificação | Estado |
|----|----|----|--------|-------|----------------|----------------------------|--------|
| HB-01 | AG-01 | EX1 | F0 | `hb-enquadrar` | sim | As nove perguntas respondidas e o literal arquivado ao lado da interpretação | CONFORME |
| HB-02 | AG-01 | EX1 | F0 | `hb-enquadrar` | sim | Recálculo manual reproduz o mesmo nível | CONFORME |
| HB-03 | AG-01 | EX1 | F0 | `hb-enquadrar` | sim | Cada campo remete a trecho identificável do relato | CONFORME |
| HB-04 | AG-01 | EX1 | (nenhuma) | (nenhuma) | não | Cadeia confirmada ou corrigida pelo engenheiro antes de avançar | DECLARADA, NÃO REFERENCIADA |
| HB-05 | AG-01 | EX1 | (nenhuma) | (nenhuma) | não | Toda premissa visível e cada número com procedência marcada | DECLARADA, NÃO REFERENCIADA |
| HB-06 | AG-02 | EX2 | (nenhuma) | (nenhuma) | sim | Cada fonte marcada como declarada até verificação em campo | DECLARADA, NÃO REFERENCIADA |
| HB-07 | AG-02 | EX2 | P2 | `hb-extrair-regras` | sim | Definições conflitantes sinalizadas, não conciliadas | CONFORME |
| HB-08 | AG-02 | EX2 | P1 | `hb-mapear-contexto` | sim | Nenhum item sem fonte; sem acesso aberto à internet | CONFORME |
| HB-09 | AG-02 | EX2 | P1 | `hb-mapear-contexto` | sim | Candidatos rastreáveis à etapa do fluxo que os originou | CONFORME |
| HB-10 | AG-02 | EX2 | P4 | `hb-priorizar` | sim | Todos os candidatos presentes, inclusive os descartados | CONFORME |
| HB-11 | AG-03 | EX2 | P5 | `hb-classificar` | não | Classificação confirmada pelo engenheiro antes de virar decisão | CONFORME |
| HB-12 | AG-03 | EX2 | P5 | `hb-classificar` | sim | Premissas expostas e recalculáveis | CONFORME |
| HB-13 | AG-02 | EX2 | (nenhuma) | (nenhuma) | sim | Cada requisito remete a norma citável | DECLARADA, NÃO REFERENCIADA |
| HB-14 | AG-03 | EX2 | P7 | `hb-governar` | não | As três listas preenchidas por decisão humana registrada | CONFORME |
| HB-15 | AG-04 | EX2 | P8 | `hb-pilotar` | não | Conjunto revisado por quem executa o processo | CONFORME |
| HB-16 | AG-04 | EX2 | P8 | `hb-pilotar` | sim | Execução reproduzível a partir do mesmo conjunto | CONFORME |
| HB-17 | AG-04 | EX2 | P9 | `hb-medir-valor` | sim | Apuração determinística e documentada | CONFORME |
| HB-18 | AG-04 | EX2 | P10 | `hb-recalibrar` | sim | Limiar definido antes do piloto, não ajustado a posteriori | CONFORME |

**"DECLARADA, NÃO REFERENCIADA" não é defeito do catálogo** — é o
estado real do contrato congelado em 2.6.0: HB-04, HB-05, HB-06 e
HB-13 existem no método (CAT-01) mas nenhuma etapa do playbook as
utiliza hoje. O catálogo registra isso explicitamente
(`estado_relacao_etapa: "nao_referenciada_no_playbook"`) em vez de
forçar uma etapa ou omitir a HB.

## AG × HB autorizadas × Implementação física × EX permitido × Estado

| AG | HB autorizadas | Implementação física | EX permitido | Estado |
|----|-------------------|------------------------|-----------------|--------|
| AG-01 | HB-01, HB-02, HB-03, HB-04, HB-05 | nenhuma (skill `hb-enquadrar` cobre HB-01/02/03) | EX1 | MAPEAMENTO CONFORME (lógico); sem runtime físico dedicado |
| AG-02 | HB-06, HB-07, HB-08, HB-09, HB-10, HB-13 | `eiac-campo/agents/extrator-documental.md` | EX2 | MAPEAMENTO CONFORME |
| AG-03 | HB-11, HB-12, HB-14 | `eiac-campo/agents/classificador-tecnologico.md` | EX2 | MAPEAMENTO CONFORME |
| AG-04 | HB-15, HB-16, HB-17, HB-18 | nenhuma (skills `hb-pilotar`/`hb-medir-valor`/`hb-recalibrar` cobrem sem subagent dedicado) | EX2 | MAPEAMENTO CONFORME (lógico); sem runtime físico dedicado |

Nenhum AG opera em EX3/EX4 — confirmado estruturalmente (T20) e pelos
quatro valores de `camada` no catálogo (EX1, EX2, EX2, EX2).

Dois AG (AG-01, AG-04) não possuem runtime físico dedicado —
isso **não é defeito**: a arquitetura permite HB serem carregadas
diretamente pela skill de etapa (`hb-enquadrar`, `hb-pilotar` etc.) sem
exigir um subagent Claude Code por AG. O baseline tinha 2 agentes
físicos; este pacote não criou nenhum arquivo físico novo — os quatro
AG lógicos resolvem sobre a infraestrutura já existente (2 subagents +
skills de etapa), conforme diretriz explícita da seção 24 do pacote.
