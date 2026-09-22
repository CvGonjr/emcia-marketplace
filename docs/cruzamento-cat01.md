# Cruzamento entre CAT-01, catálogo de HB e playbook executável

**Data da auditoria:** 22/09/2026

**Documentos cruzados:** `EMCIA-CAT-01` v0.2, `reference/habilidades.json`
v0.1.0 e `template-caso/registro/playbook.json` v0.4.1.

## Objetivo e critério

Este documento torna explícita a correspondência que os três artefatos ainda
não declaram em conjunto. Ele não altera o método nem cria novas habilidades.

Para P3, o CAT-01 descreve o passo 3 como uma unidade, enquanto o playbook o
divide em P3a, P3b e P3d. As atividades foram distribuídas abaixo apenas quando
o nome e a saída da subetapa tornam a correspondência inequívoca. A varredura do
mapa de valor aparece em P3d por pertencer ao passo 3 no CAT-01, embora o
playbook associe a HB-09 a P1; esse desalinhamento fica registrado, não
resolvido.

Uma atividade automatizada ou híbrida só é marcada como coberta quando há HB no
Anexo A com a mesma atividade/saída. Semelhança genérica não foi usada para
inventar correspondência. Atividade humana não requer HB.

## Cruzamento das treze etapas

| Etapa | Camada por nível no playbook | Atividades do CAT-01 e natureza | HB que cobre atividade automatizada/híbrida | Habilidade do playbook | Divergência observada |
|---|---|---|---|---|---|
| F0 | N1/N2/N3: EX1 | Aplicar triagem — **Automatizado**;<br>apurar nível — **Automatizado**;<br>estruturar dor em 5W2H — **Automatizado**;<br>conduzir cinco porquês — **Híbrido**;<br>calcular custo do problema — **Híbrido**;<br>decidir prosseguimento — **Humano** | HB-01; HB-02; HB-03; HB-04; HB-05; atividade humana: n/a | `hb-enquadrar` (referencia somente HB-01/02/03) | EX1 corresponde às atividades automatizadas/híbridas. Porém HB-04 e HB-05 existem no catálogo e não são referenciadas pelo playbook; a decisão humana de prosseguimento não é representada pela camada única da etapa. |
| P1 | N1: EX2; N2: EX2; N3: EX3 | Levantar objetivos declarados e posicionar nas quatro frentes — **Automatizado**;<br>consultar referência setorial — **Automatizado**;<br>avaliar patrocínio real — **Humano** | **nenhuma**; HB-08; atividade humana: n/a | `hb-mapear-contexto` (HB-08 e HB-09) | N1/N2 em EX2 representam a preparação, mas não a avaliação humana. N3 em EX3 antecipa verificação conforme CAT-01 §3.6. A HB-09 usada aqui pertence, no CAT-01, à varredura do passo 3, não às atividades do passo 1. |
| P2 | N1: EX2; N2: EX2; N3: EX3 | Inventariar sistemas-fonte e coletar termos — **Automatizado**;<br>verificar existência/aptidão do dado — **Humano**;<br>detectar divergência entre definição declarada e uso real — **Humano** | HB-06 e HB-07; atividades humanas: n/a | `hb-extrair-regras` (somente HB-07) | N1/N2 em EX2 representam apenas a coleta declarativa; N3 em EX3 antecipa verificação conforme CAT-01 §3.6. HB-06 cobre parte da atividade automatizada, mas não é referenciada pelo playbook. |
| P3a | N1: EX2; N2/N3: EX3 | Registrar linha de base — **Híbrido** | **nenhuma** | `hb-medir` (sem HB) | N1/EX2 é compatível com a natureza híbrida. N2/N3 em EX3 representam a validação humana antecipada, mas não existe HB catalogada para produzir a parte delegável da medição. |
| P3b | N1/N2/N3: EX4; `delegavel: false` | Levantar regras não documentadas — **Humano** | n/a | `hb-levantar-regras` (sem HB) | Contradição direta: CAT-01 §3.3 define EX3 como a camada que levanta regras não documentadas; o playbook atribui EX4. Ambos mantêm a atividade humana e não delegável. |
| P3d | N1/N2/N3: EX3 | Varrer mapa de valor e desenhar estado atual declarado — **Automatizado**;<br>distinguir processo documentado do praticado — **Humano** | HB-09; atividade humana: n/a | `hb-confrontar` (sem HB) | EX3 corresponde ao confronto humano. A preparação automatizada tem HB-09, mas o playbook a associa a P1 e não à habilidade de P3d; por isso P3d fica sem AG resolvível por sua habilidade. |
| P4 | N1: EX2; N2/N3: EX3 | Montar matriz de priorização — **Automatizado**;<br>estimar viabilidade técnica — **Híbrido**;<br>estimar impacto e decidir prioridade — **Humano**;<br>classificar zona de contenção — **Híbrido** | HB-10; **nenhuma**; atividade humana: n/a; **nenhuma** | `hb-priorizar` (HB-10) | N1/EX2 cobre apenas a montagem da matriz; N2/N3 antecipam verificação. A decisão de prioridade é humana e o CAT-01 §3.3 a situa conceitualmente em EX4, mas a etapa não chega a EX4. Duas atividades híbridas não têm HB. |
| P5 | N1/N2/N3: EX3 | Aplicar Matriz Problema→Tecnologia — **Híbrido**;<br>estimar custo e latência — **Automatizado**;<br>construir camada de contexto — **Humano**;<br>decidir construção e integração — **Humano** | HB-11; HB-12; atividades humanas: n/a | `hb-classificar` (HB-11 e HB-12) | Contradição direta de camada: HB-11/HB-12 e suas atividades são EX2 no CAT-01, enquanto a etapa inteira é EX3 no playbook. A parte humana inclui construção de contexto, situada em EX4 pela definição do CAT-01, mas não há camada separada na etapa. |
| P6 | N1/N2/N3: EX3 | Mapear integrações e permissões — **Automatizado**;<br>documentar estado futuro — **Híbrido**;<br>redesenhar processo com as áreas — **Humano**;<br>redigir guia operacional/treinamento — **Híbrido** | **nenhuma**; **nenhuma**; atividade humana: n/a; **nenhuma** | `hb-operacionalizar` (sem HB) | EX3 representa a negociação/verificação humana, mas três atividades delegáveis não têm HB no catálogo. A habilidade executável posterior ao CAT-01 não resolve AG formal. |
| P7 | N1/N2/N3: EX4; `delegavel: false` | Levantar requisitos regulatórios — **Automatizado**;<br>minutar termo de autonomia — **Híbrido**;<br>definir autonomia/limites — **Humano**;<br>nomear responsáveis/aprovar política — **Humano** | HB-13; HB-14; atividades humanas: n/a | `hb-governar` (somente HB-14) | EX4 corresponde às decisões de autonomia. A preparação delegável permanece EX2 no catálogo; HB-13 existe, mas não é referenciada pelo playbook. A camada única não distingue preparação e decisão. |
| P8 | N1/N2/N3: EX3 | Gerar casos de teste — **Híbrido**;<br>executar suíte/consolidar falhas — **Automatizado**;<br>julgar aceitabilidade — **Humano**;<br>aprovar progressão/escala — **Humano** | HB-15; HB-16; atividades humanas: n/a | `hb-pilotar` (HB-15 e HB-16) | Contradição direta de camada: HB-15/HB-16 são EX2 no CAT-01, enquanto a etapa inteira é EX3 no playbook. EX3 representa a revisão humana, mas não a preparação e execução automatizada. |
| P9 | N1/N2/N3: EX3 | Coletar métricas/comparar linha de base — **Automatizado**;<br>interpretar causa — **Humano**;<br>apresentar resultado ao patrocinador — **Humano** | HB-17; atividades humanas: n/a | `hb-medir-valor` (HB-17) | Contradição direta de camada: HB-17 é EX2 no CAT-01, enquanto a etapa inteira é EX3. A camada única agrega apuração automatizada e interpretação humana. |
| P10 | N1/N2/N3: EX4; monitoramento: EX2 | Monitorar desvio/degradação — **Automatizado**;<br>propor ajuste — **Híbrido**;<br>diagnosticar causa — **Humano**;<br>decidir recalibrar/expandir/descontinuar — **Humano** | HB-18; **nenhuma**; atividades humanas: n/a | `hb-recalibrar` (HB-18) | O playbook separa corretamente EX2 para monitoramento e EX4 para decisão. Falta HB para a proposta híbrida de ajuste; a habilidade associa apenas HB-18. |

## 1. Atividades automatizadas sem HB

- P1: levantar objetivos declarados e posicioná-los nas quatro frentes.
- P6: mapear pontos de integração e permissões necessárias.

## 2. Atividades híbridas sem HB

- P3a: registrar a linha de base.
- P4: estimar viabilidade técnica.
- P4: classificar na zona de contenção.
- P6: documentar o estado futuro.
- P6: redigir o guia operacional e o material de treinamento.
- P10: propor ajuste de regra ou parâmetro.

## 3. Etapas cuja camada contradiz a definição do CAT-01

- **P3b:** o playbook fixa EX4; o CAT-01 inclui o levantamento de regras não
  documentadas na definição de EX3.
- **P5:** o playbook fixa EX3 para uma habilidade que referencia HB-11 e HB-12,
  ambas EX2 no catálogo; a construção humana da camada de contexto é descrita
  como EX4 no CAT-01.
- **P8:** o playbook fixa EX3; HB-15 e HB-16 são EX2 no catálogo.
- **P9:** o playbook fixa EX3; HB-17 é EX2 no catálogo.

P1, P2, P3a, P4, P6 e P7 também agregam atividades de naturezas diferentes sob
uma camada única. Nos casos em que isso coincide com o deslocamento por nível do
CAT-01 §3.6, foi registrado como perda de granularidade, não como contradição.
P10 evita essa contradição explícita ao declarar `camada_monitoramento: EX2`
separadamente de sua camada decisória EX4.

## Consequência operacional provisória

Este cruzamento não autoriza alteração do CAT-01, do catálogo nem do playbook.
Na execução de contraste, toda habilidade de etapa sem AG resolvível no catálogo
usa como autor o próprio identificador `hb-*` e registra
`camada_substituida` com a camada resolvida do playbook. Com o contrato atual,
isso alcança P3a (`hb-medir`), P3b (`hb-levantar-regras`, embora registrada como
`nao_realizado`), P3d (`hb-confrontar`) e P6 (`hb-operacionalizar`). Nenhum código
AG é inventado.
