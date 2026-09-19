# Pacote 2.6.4 — Formalização das 18 HB e 4 AG

## 1. Identificação

Ação: 2.6 — Agentes e Protocolos
Pacote: 2.6.4
Branch: master
HEAD inicial: `418a91635b96742a443e36ad4976146c4b04894a`
HEAD final: ver §28 (hash real do commit)
Data: 2026-09-19

## 2. Documentos consultados

Obrigatórios: EMCIA-CAT-01 (Anexo A — fonte primária literal das 18 HB
e 4 AG), EMCIA-HAB-01 (protocolo de habilitação — conceito distinto,
não relacionado a HB/AG, ver §11), EMCIA-MET-01, EMCIA-ESP-01 (§3.1,
§3.4, §3.10 G6 — origem do mecanismo genérico de critério de
verificação), EMCIA-ARQ-01, EMCIA-TRA-01, EMCIA-GLO-01 (§3.5, Anexo B —
definições e índice de siglas), EMCIA-TST-01. Consultados: EMCIA-E1–E5
(zero referências a código HB/AG confirmado), CTX-01, FER-01, VER-01,
IMP-01 (confirma o mapa canônico), CAM-01 (confirma HB-14–HB-18 por
código explícito), evidências de 2.6.0–2.6.3.

## 3. Baseline relacionado

13 skills físicas; 9/18 HB referenciadas no playbook (S2-BL); 0/18
códigos estáveis; 2 agentes físicos; 0/4 AG formalmente mapeados; D-11
aberto.

## 4. Estado inicial

Playbook já referenciava 14/18 HB (crescimento de 9→14 por 2.6.2/2.6.3,
que introduziram HB-14 a HB-18 com código já embutido nas respectivas
skills). Nenhum catálogo declarativo existia — nenhuma resolução
programática HB→AG, AG→HB, HB→skill. 5 skills já carregavam `hb:` no
frontmatter (herdadas de 2.6.2/2.6.3); as 13 restantes, não. Ver
`inventario-hb-ag.md` para o detalhamento completo por HB e AG.

## 5. Contrato oficial das 18 HB

Extraído literalmente de EMCIA-CAT-01, Anexo A: id, nome oficial,
camada/natureza (EX1/EX2, automatizada/híbrida), insumo, saída,
critério de verificação. Nenhum nome foi inferido a partir dos arquivos
de skill existentes.

## 6. Contrato oficial dos 4 AG

Extraído literalmente do mesmo Anexo A: AG-01 Agente de enquadramento
(EX1, HB-01–05), AG-02 Agente de análise documental (EX2, HB-06–10 +
HB-13), AG-03 Agente de especificação (EX2, HB-11/12/14), AG-04 Agente
de avaliação (EX2, HB-15–18). Confirmado idêntico em ESP-01 §3.4 e
IMP-01 §3.5-3.7 — nenhuma divergência documental encontrada no mapa
canônico. "Nenhum agente reúne habilidades de camadas distintas, e
nenhum opera em EX3 ou EX4" (CAT-01, literal).

## 7. Arquitetura catálogo × playbook × skill

`eiac-campo/reference/habilidades.json` e `agentes.json` são o
catálogo declarativo, separado do playbook (que continua representando
apenas etapas/dependências/portões/contrato do percurso, sem
duplicação do conteúdo das HB). `eiac-nucleo/scripts/catalogo.py` é o
resolvedor genérico — não conhece HB, AG, "habilidade" nem "agente";
opera apenas sobre dois tipos de objeto (`capacidade`, `papel`) com
`id`, reaproveitando `playbook.capacidade_valida()` (2.6.1) para a
regra "automatizada sem critério é inválida". A relação HB↔etapa vem
exclusivamente de `playbook.json` (campo `hb`), nunca de inferência
textual — por decisão explícita, preservando a pendência já registrada
sobre correspondência entregável×passo.

## 8. Inventário das skills

18 skills físicas em `eiac-campo/skills/`. 9 delas carregam `hb:` no
frontmatter (identidade lógica rastreável): `hb-enquadrar`,
`hb-extrair-regras`, `hb-mapear-contexto`, `hb-priorizar`,
`hb-classificar` (5 adicionadas neste pacote) + `hb-governar`,
`hb-pilotar`, `hb-medir-valor`, `hb-recalibrar` (4 herdadas de
2.6.2/2.6.3). As 9 restantes (`hb-emitir-e1` a `-e5`, `hb-confrontar`,
`hb-levantar-regras`, `hb-medir`, `hb-operacionalizar`) são
classificadas como infraestrutura ou capacidade não catalogada por
CAT-01: emissão de entregável (E1-E5) não corresponde a nenhuma das 18
HB; P3d, P3a, P3b e P6 não possuem HB atribuída pelo Anexo A (P3b em
particular é EX4, fora do domínio dos 4 AG por definição). Detalhe
completo em `inventario-hb-ag.md`.

## 9. Catálogo HB

18/18 formalizadas em `eiac-campo/reference/habilidades.json`. Todas
com id, nome, camada, automatizada, insumo, saída, critério de
verificação e `ag_autorizado`. 14/18 com `skill_ref` resolvendo para
arquivo real. 4/18 (HB-04, HB-05, HB-06, HB-13) sem skill física ainda
— honestamente marcadas, não forçadas.

## 10. Catálogo AG

4/4 formalizados em `eiac-campo/reference/agentes.json`. Cada um com
id, nome, camada, `hb_autorizadas` (conjunto exato do mapa canônico) e
`implementacao_fisica` (2 resolvem para subagent físico existente
— `extrator-documental.md`, `classificador-tecnologico.md` — 2 não
possuem runtime dedicado, cobertos por skills de etapa).

## 11. Critérios de verificação

Todas as 13 HB marcadas `automatizada: true` possuem critério não vazio
e não genérico, extraído literalmente de CAT-01. As 5 HB híbridas
(HB-04, HB-05, HB-11, HB-14, HB-15) também têm critério documental
próprio, mesmo não sendo "automatizada" no sentido estrito — o campo
do schema é `criterio_de_verificacao`, aplicável a toda HB, não só às
automatizadas (a checagem estrutural do núcleo só *exige* o campo
quando automatizada; HB híbrida com critério vazio não seria recusada
pelo mecanismo genérico, mas o catálogo real não tem nenhum caso assim).
**`criterio_de_habilitacao` não existe como conceito nos documentos
fonte** — HAB-01 trata de um "habilitação" completamente diferente
(gate de onboarding do engajamento, etapas 0a-0d), não da autorização
AG→HB. Este campo não foi criado no catálogo; a autorização é
representada estruturalmente pela lista `hb_autorizadas` de cada AG.

## 12. Relação AG → HB

Resolução determinística via `catalogo.py --resolver-papel-capacidade`,
testada positiva (AG-04×HB-17) e negativa (AG-01×HB-17, AG-03×HB-17) —
nenhuma cadeia `if AG-01 and HB-17` no núcleo; a checagem é
pertencimento de conjunto em `hb_autorizadas`.

## 13. Relação HB → skill

14/18 HB resolvem para `skill_ref` real (T07). 4/18 sem implementação
física ainda (HB-04, HB-05, HB-06, HB-13) — não são defeito de
catálogo; são o estado real do sistema, que o próprio catálogo declara.

## 14. Relação playbook → HB

Todas as 14 referências `hb` presentes no playbook oficial resolvem
contra o catálogo (T25). Fixture negativa confirma recusa determinística
para referência inexistente (T26).

## 15. Agentes físicos × agentes lógicos

2 agentes físicos existentes (herdados do baseline) cobrem parte de
AG-02 e AG-03. Nenhum arquivo físico novo foi criado neste pacote — os
4 AG lógicos resolvem sobre a infraestrutura existente (2 subagents +
skills de etapa), conforme a diretriz explícita da seção 24 do pacote
("isso NÃO significa automaticamente que precisamos criar mais dois
arquivos físicos").

## 16. Fronteira EX3/EX4

Nenhum dos 4 AG do catálogo recebe camada EX3/EX4 (T20, confirmado por
inspeção direta de `agentes.json`: EX1, EX2, EX2, EX2). HB-14 (P7) e
HB-18 (P10) são marcadas corretamente — a primeira como híbrida, a
segunda como automatizada mas restrita a "monitoramento de desvio", sem
a palavra "decisão" no nome — preservando a fronteira já implementada
em 2.6.2/2.6.3 (skills `hb-governar`/`hb-recalibrar` continuam
recusando estruturalmente a decisão final por agente).

## 17. Regressão G1

Revalidada em P5 (T39/T40): skill EX3/EX4 sem sessão continua
bloqueada; com sessão humana válida da mesma etapa, carrega. Nenhuma
alteração em `guarda.py` neste pacote.

## 18. Caso de controle

Dois pontos do percurso demonstrados: HB-10/P4 (dentro de P1–P5) e
HB-17/P9 (dentro de P6–P10). Cadeia completa etapa→HB→catálogo→AG→
skill→critério→execução autorizada (PASS)→execução não autorizada
(RECUSA) para ambos. Detalhe em `caso-controle.md`.

## 19. Testes

50 verificações em `testes/campo_2_6_4.py` (T01-T46 do catálogo +
T47-T50 de regressão delegada). 0 falhas.

## 20. Pares negativo/positivo

Todos os sete pares exigidos pela seção 51 cobertos: HB sem/com
critério (T09/T10); HB aponta para skill inexistente/skill resolve
(T08/T07); AG executa HB não autorizada/autorizada (T18/T19); playbook
referencia HB inexistente/todas resolvem (T26/T25); AG recebe
capacidade EX3/EX4 indevida (fixture, T20)/AG permanece na fronteira
permitida (T20 positivo, confirmado por inspeção); skill humana sem
sessão/skill de apoio com sessão válida (T39/T40); auto-habilitação em
runtime (T44, ausência confirmada)/catálogo autorizado e estável (T45).

## 21. Hard-code

Busca por HB-01/HB-18/AG-01/AG-04/Enquadramento/Análise
documental/Especificação/Avaliação em `eiac-nucleo/scripts/*.py`: 7
ocorrências, todas não comportamentais (docstrings de exemplo de uso em
`catalogo.py`, um comentário pré-existente em `estado.py` sobre a
convenção lexical "AG-01"). 0 ocorrências em condicional testando esses
termos.

## 22. Regressão

Antes: 292/292. Depois: 342/342 — os 50 novos deste pacote, 0 falhas em
nenhuma suíte anterior.

## 23. Defeitos encontrados

Nenhum defeito de produção pré-existente encontrado neste pacote (ao
contrário de 2.6.2/G1 e 2.6.3/calibragem, este pacote não expôs
nenhuma trava incorreta).

## 24. Correções e retestes

Não aplicável — nenhum defeito encontrado.

## 25. Cobertura final

HB DECLARADAS: 18/18
HB COM CÓDIGO ESTÁVEL: 9/18 (skills com `hb:` no frontmatter)
HB COM CRITÉRIO DE VERIFICAÇÃO: 18/18 (todas, automatizadas e híbridas)
HB COM SKILL/IMPLEMENTAÇÃO RESOLVÍVEL: 14/18 aplicáveis
AG DECLARADOS: 4/4
AG COM MAPEAMENTO HB: 4/4
REFERÊNCIAS HB DO PLAYBOOK RESOLVÍVEIS: 14/14
AG COM CAPACIDADE HUMANA INDEVIDA: 0 (confirmado)

## 26. Situação D-11

**PARCIAL.** 18/18 HB e 4/4 AG possuem representação formal, relações
resolvem, critérios existem onde documentados, playbook resolve HB, e a
fronteira humana permanece preservada — mas nem toda skill possui
identidade HB rastreável ainda (9/18 têm `hb:` no frontmatter, as
outras 9 são infraestrutura/não catalogada, não faltantes) e 4 HB
(HB-04/05/06/13) não têm implementação física. Por critério estrito da
seção 55 do pacote ("skills possuírem identidade" — sem qualificar
"onde aplicável"), o estado correto é PARCIAL, não RESOLVIDO: o
catálogo está completo e correto, mas a cobertura física das 18 HB não
está.

## 27. Itens adiados

2.6.5 — Portões, inegociáveis (validação semântica final) e geração de
entregáveis.
2.6.6 — Verificação integral F0–P10.

## 28. Commit

Ver `git-show.txt` e `diff.patch` neste diretório para o hash real, o
diffstat e o diff completo.

## 29. Estado final

**CONFORME** quanto ao escopo executável do pacote (catálogo formal,
resolução determinística, fronteira preservada, 0 hard-code, 0
regressão); **PARCIAL** quanto a D-11 especificamente, pelos motivos do
§26.
