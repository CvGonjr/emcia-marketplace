# Inventário HB/AG — estado inicial (pacote 2.6.4)

HEAD: `418a91635b96742a443e36ad4976146c4b04894a`

Fonte da coluna "Nome oficial/Critério": EMCIA-CAT-01, Anexo A. Fonte
da coluna "Skill atual": `eiac-campo/skills/` antes das edições deste
pacote. Fonte da coluna "Etapa": `eiac-campo/template-caso/registro/playbook.json`
(campo `hb` por etapa) — nunca inferência textual.

## Tabela 1 — HB-01 a HB-18

| HB | Nome oficial | Skill atual (antes do pacote) | AG (CAT-01 Anexo A) | Etapa (playbook) | Critério (CAT-01) | Estado inicial |
|----|---------------|-------------------------------|----------------------|-------------------|---------------------|-----------------|
| HB-01 | Condução da triagem | `hb-enquadrar` (sem `hb:` no frontmatter) | AG-01 | F0 | As nove perguntas respondidas e o literal arquivado ao lado da interpretação | MAPEAMENTO PARCIAL (skill correta, sem código estável) |
| HB-02 | Apuração do nível de complexidade | `hb-enquadrar` (sem `hb:`) | AG-01 | F0 | Recálculo manual reproduz o mesmo nível | MAPEAMENTO PARCIAL |
| HB-03 | Estruturação da dor | `hb-enquadrar` (sem `hb:`) | AG-01 | F0 | Cada campo remete a trecho identificável do relato | MAPEAMENTO PARCIAL |
| HB-04 | Condução dos cinco porquês | nenhuma | AG-01 | (nenhuma) | Cadeia confirmada ou corrigida pelo engenheiro antes de avançar | SEM MAPEAMENTO |
| HB-05 | Cálculo do custo do problema | nenhuma | AG-01 | (nenhuma) | Toda premissa visível e cada número com procedência marcada | SEM MAPEAMENTO |
| HB-06 | Inventário de fontes de dados | nenhuma | AG-02 | (nenhuma) | Cada fonte marcada como declarada até verificação em campo | SEM MAPEAMENTO |
| HB-07 | Coleta de termos do glossário | `hb-extrair-regras` (sem `hb:`) | AG-02 | P2 | Definições conflitantes sinalizadas, não conciliadas | MAPEAMENTO PARCIAL |
| HB-08 | Consulta à base de referência | `hb-mapear-contexto` (sem `hb:`) | AG-02 | P1 | Nenhum item sem fonte; sem acesso aberto à internet | MAPEAMENTO PARCIAL |
| HB-09 | Varredura do mapa de valor | `hb-mapear-contexto` (sem `hb:`) | AG-02 | P1 | Candidatos rastreáveis à etapa do fluxo que os originou | MAPEAMENTO PARCIAL |
| HB-10 | Montagem da matriz de priorização | `hb-priorizar` (sem `hb:`) | AG-02 | P4 | Todos os candidatos presentes, inclusive os descartados | MAPEAMENTO PARCIAL |
| HB-11 | Classificação Problema→Tecnologia | `hb-classificar` (sem `hb:`) | AG-03 | P5 | Classificação confirmada pelo engenheiro antes de virar decisão | MAPEAMENTO PARCIAL |
| HB-12 | Estimativa de custo e latência | `hb-classificar` (sem `hb:`) | AG-03 | P5 | Premissas expostas e recalculáveis | MAPEAMENTO PARCIAL |
| HB-13 | Levantamento regulatório | nenhuma | AG-02 | (nenhuma) | Cada requisito remete a norma citável | SEM MAPEAMENTO |
| HB-14 | Minuta do termo de autonomia | `hb-governar` (com `hb: ["HB-14"]`, desde 2.6.2) | AG-03 | P7 | As três listas preenchidas por decisão humana registrada | MAPEAMENTO CONFORME |
| HB-15 | Geração de casos de teste | `hb-pilotar` (com `hb: ["HB-15","HB-16"]`, desde 2.6.3) | AG-04 | P8 | Conjunto revisado por quem executa o processo | MAPEAMENTO CONFORME |
| HB-16 | Execução da suíte de avaliação | `hb-pilotar` (idem) | AG-04 | P8 | Execução reproduzível a partir do mesmo conjunto | MAPEAMENTO CONFORME |
| HB-17 | Consolidação de indicadores | `hb-medir-valor` (com `hb: ["HB-17"]`, desde 2.6.3) | AG-04 | P9 | Apuração determinística e documentada | MAPEAMENTO CONFORME |
| HB-18 | Monitoramento de desvio | `hb-recalibrar` (com `hb: ["HB-18"]`, desde 2.6.3) | AG-04 | P10 | Limiar definido antes do piloto, não ajustado a posteriori | MAPEAMENTO CONFORME |

**Estado inicial agregado:** HB declaradas formalmente 0/18 (catálogo
não existia); HB com código estável em skill 5/18 (as já herdadas de
2.6.2/2.6.3: HB-14, HB-15, HB-16, HB-17, HB-18); HB referenciadas pelo
playbook 14/18; skills físicas 13 (antes de `hb-governar`,
`hb-operacionalizar`, `hb-pilotar`, `hb-medir-valor`, `hb-recalibrar` —
que já existiam desde 2.6.2/2.6.3, portanto 18 skills físicas já
presentes no início deste pacote, coerente com a estrutura herdada);
agentes físicos 2 (`classificador-tecnologico`, `extrator-documental`).

## Tabela 2 — AG-01 a AG-04

| AG | Nome oficial | HB autorizadas (CAT-01 Anexo A) | Agente físico | Estado inicial |
|----|---------------|-----------------------------------|-----------------|-----------------|
| AG-01 | Agente de enquadramento | HB-01 a HB-05 | nenhum | SEM MAPEAMENTO FORMAL (skill hb-enquadrar cobre HB-01/02/03 na prática, sem catálogo declarativo) |
| AG-02 | Agente de análise documental | HB-06 a HB-10, HB-13 | `extrator-documental.md` | SEM MAPEAMENTO FORMAL (agente físico existe e cobre HB-07 na prática; HB-06/08/09/10/13 sem vínculo declarado) |
| AG-03 | Agente de especificação | HB-11, HB-12, HB-14 | `classificador-tecnologico.md` | SEM MAPEAMENTO FORMAL (agente físico existe e cobre HB-11 na prática; HB-12/14 sem vínculo declarado) |
| AG-04 | Agente de avaliação | HB-15 a HB-18 | nenhum | SEM MAPEAMENTO FORMAL |

**Nota honesta:** nenhuma das quatro relações AG→HB estava formalmente
declarada antes deste pacote — mesmo onde a skill/agente físico já
existia e já era coerente com o mapa canônico do CAT-01, não havia
arquivo declarativo que resolvesse a pergunta "este AG está autorizado
a usar esta HB?" de forma programática. Isso é exatamente D-11.
