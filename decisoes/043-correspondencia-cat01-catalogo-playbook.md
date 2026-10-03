# 043 — Correspondência CAT-01, catálogo e playbook

**Data:** 03/10/2026 · **Estado:** firme por instrução do engenheiro

## Contexto

CAT-01 v0.5 fixa a correspondência completa no Anexo C, após decisões humanas
D2–D8 e resolução explícita da D5. A fonte canônica deste pacote é
emcia-artefatos, commit `989e1e73796a356b660be8ed55b686ba716787ac`.
O pacote conserva Estado Em revisão e Aprovação pendente; esta decisão
autoriza as alterações operacionais solicitadas, sem aprovar os documentos.

A pré-validação encontrou MAN-01 v0.3 com o ato de F0 e produto `—`.
O engenheiro aprovou a correção canônica v0.4 para a expressão literal
**Decisão de prosseguimento registrada**. Antes do commit canônico,
conferir() retornou lista vazia contra o rascunho e contrato em memória.
O mesmo texto é a descrição do produto no playbook.

## Decisão

Esta decisão **supera explicitamente a 020**, inclusive a regra provisória
de atribuição por identificador `hb-*` e camada substituída. O cruzamento
de 22/09/2026 passa a registro histórico. Não se infere correspondência:
catálogo literal do Anexo A e relação do Anexo C são conferidos por teste.

| Etapa | HBs de preparação | AG |
|---|---|---|
| F0 | HB-01, HB-02, HB-03, HB-04, HB-05 | AG-01 |
| P1 | HB-08 | AG-02 |
| P2 | HB-06, HB-07 | AG-02 |
| P3a | HB-19 | AG-02 |
| P3b | — | —; não realizada por agente |
| P3d | HB-09, HB-20 | AG-02 |
| P4 | HB-10 | AG-02 |
| P5 | HB-11, HB-12 | AG-03 |
| P6 | HB-21 | AG-03 |
| P7 | HB-13, HB-14 | AG-03 |
| P8 | HB-15, HB-16 | AG-04 |
| P9 | HB-17 | AG-04 |
| P10 | HB-18 | AG-04 |

D5: posicionamento nas quatro frentes (MET-01 §3.4.1) e mapa de valor
(MET-01 §3.4.3) são instrumentos distintos. HB-09 permanece no passo 3,
em P3d: estado declarado selado após P2 como entrada, candidatos para P4
como saída. A habilidade não reescreve o estado selado com o observado;
a saída nasce D ou I. P1 não recebe HB nova.

D7: a camada da etapa é a de encerramento e decisão. Cada HB conserva
sua camada de preparação, menor ou igual à da etapa no mesmo nível.
Em P10 a comparação utiliza a camada de monitoramento. A relação EX2
de preparação e EX3/EX4 de encerramento não é contradição nem delega decisão.

D8: decidir-prosseguimento é operação humana declarada no playbook,
negada pela guarda quando invocada pela sessão, com TentativaNegada e
comando exato. O engenheiro registra decisor, data, desfecho e motivo,
com referência e hash da ficha E1 preparada. O mecanismo genérico de
produtos exige a decisão vigente para encerrar F0.

Por esclarecimento aprovado do engenheiro, **os dois desfechos encerram F0**.
`não prosseguir` bloqueia as etapas seguintes até nova decisão `prosseguir`.
O registro anterior é preservado em arquivo próprio, com versão crescente;
nenhuma decisão é sobrescrita. A materialização de E1 apresenta a decisão.
A autorização de emissão continua sujeita aos portões e RH pendentes.

As sete atividades do CAT-01 Anexo B permanecem com o engenheiro, sem HB
inventada. HB-19/20/21 somente remetem ao catálogo: a preparação já existia
nas habilidades examinadas. AG identifica o agrupamento da preparação,
nunca autoria de pessoa em evento, asserção ou decisão. P3b permanece
sem HB e sem AG por desenho, registrada como não realizada por agente.

## Consequência e verificação

Núcleo 0.2.45, campo 0.8.23, playbook 0.4.19, manifesto 5. Casos já abertos
conservam o contrato copiado, conforme decisão 002. O núcleo compara
condições declaradas e integridade de arquivos; não contém as novas
expressões, desfechos ou instrumentos do método como regras de código.

Testes catalogo_cat01.py e prosseguimento.py exercitam negativas antes
dos controles positivos. A25 confere MAN-01 v0.4 diretamente, sem emenda
local. Empacotamento usa bytes dos objetos Git e SHA-256, sem edição manual.
Evidência inicial, final, pré-validação, inspeção e diff:
`.projectdocs/evidencias/correspondencia-cat01/`.

A divergência de natureza de HB-16 entre CAT-01 e CAM-01 permanece
registrada no Anexo D.3 canônico; o catálogo reproduz CAT-01 conforme
instrução. Não se modifica sua natureza por inferência.
