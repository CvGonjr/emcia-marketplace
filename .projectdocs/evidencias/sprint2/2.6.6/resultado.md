# Pacote 2.6.6 — Verificação integral F0–P10

## 1. Identificação

Ação: 2.6 — Agentes e Protocolos
Pacote: 2.6.6
Branch: `master`
HEAD inicial: `bcc85a62fc2b8c72b4704ecd43e5e901cce39d63`
HEAD final: `31ffff2260f40c06a323087791cf8e17062a4ee5` (commit de correção) +
commit de evidência a seguir
Data: 2026-09-19

## 2. Documentos consultados

EMCIA-RTE-01 (oficial, atualizado em §73 abaixo), EMCIA-MET-01,
EMCIA-CAT-01, EMCIA-CAM-01 (via referências dos scripts), EMCIA-E1 a
EMCIA-E5 (estrutura dos entregáveis, reconfirmada contra os já
materializados em 2.6.5), evidências `.projectdocs/evidencias/sprint2/`
de 2.6.0 a 2.6.5. Não foi necessário reler ESP-01/HAB-01/CTX-01/VER-01/
TST-01/GLO-01/ARQ-01/IMP-01 na íntegra: seus efeitos executáveis já
estão consolidados no código verificado (nenhuma leitura adicional
alterou uma decisão de implementação neste pacote, que é só de
verificação).

## 3. Baseline S2-BL

HEAD `9a54017411c20cf54ab3a28fa488678c945a34b1`, 26 PASS / 0 FAIL.
Indicadores relevantes preservados como referência histórica: etapas
8/13, HB referenciadas 9/18 (0/18 código estável), AG mapeados 0/4,
portões 2/6, inegociáveis 0/5, entregáveis materiais ausentes, percurso
F0–P10 ausente. Este baseline não foi alterado.

## 4. Estado dos pacotes 2.6.0–2.6.5

Todos registrados como "Concluído" em RTE-01 §3.10 antes do início deste
pacote: 2.6.0 (contrato 13/13 etapas), 2.6.1 (núcleo genérico de
protocolos), 2.6.2 (P6/P7), 2.6.3 (P8/P9/P10), 2.6.4 (18 HB/4 AG
formalizados, D-11 PARCIAL), 2.6.5 (6 portões, 5 inegociáveis, E1-E5
materializáveis, D-12 RESOLVIDO). Confirmado por leitura de RTE-01 §3.10
e dos `resultado.md` de cada pacote antes de iniciar 2.6.6.

## 5. Caso de controle

Caso novo, criado a partir do template padrão do Estúdio
(`eiac-campo/template-caso/`), sem reaproveitar estado residual de
nenhum caso anterior. Nível N2 (justificativa em `caso-controle.md`).
Cenário simulado: fluxo de reembolsos, responsáveis fictícios (Celso do
Vale, Fernanda Lima, Rafael Nogueira, Marina Prado), sem dados pessoais
reais. Percurso completo, driver reproduzível em
`caso-controle-driver.py`, log completo em `caso-controle-log-comandos.txt`
e `teste-2.6.6-saida-completa.txt`.

## 6. Percurso F0–P10

13/13 etapas atingidas em ordem, sem bypass. Ver `matriz-f0-p10.md` para
o detalhamento etapa a etapa. Nenhuma etapa foi encerrada fora de ordem
(testado e recusado: tentativa de encerrar P3a com a etapa corrente em
P1). Resultado: **PASS**.

## 7. Contexto e dados

RN-101 curada via `curar.py` (caminho autorizado); escrita direta em
`contexto/regras/` testada e recusada (G2b). Ação 2.5 permanece íntegra
— nenhuma alteração em `eiac-nucleo/scripts/curar.py`,
`eiac-nucleo/scripts/estrutura.py` ou nos schemas de CTX neste pacote;
regressão de `testes/contexto.py`, `curadoria.py`, `ctx_v.py`, `p3d.py`,
`integracao.py` confirmada sem falhas.

## 8. Fronteira EX1–EX4

Ver `matriz-fronteira.md`. Quatro pares negativo/positivo de fronteira
humana demonstrados: P3b (agente recusado / humano com sessão), validação
de P6 (agente recusado / humano valida), decisão de P7 (agente recusado /
humano decide), decisão de recalibragem em P10 (agente recusado / humano
decide). Nenhum dos quatro agentes lógicos está declarado em EX3/EX4.

## 9. Sessões humanas

P3b, P7 e P10 exigiram e registraram sessão via
`avancar.py --registrar-sessao` antes do encerramento correspondente
(P3b, P7) ou antes do registro de recorrência (P10). Nenhuma sessão de
outra etapa foi aceita para liberar uma etapa diferente (mecanismo G1 do
núcleo, inalterado desde 2.6.1).

## 10. P6/P7

P6: AG-02 propõe (papel legítimo), AG-02 tentando validar a própria
proposta é recusado, Rafael Nogueira (humano) valida. P7: AG-03 prepara
minuta e propõe (papel legítimo), AG-03 tentando decidir é recusado,
Marina Prado (humano nominal) decide. Ambos **PASS** nos pares
negativo/positivo (C09/C11/C12).

## 11. P8/P9/P10

P8: CT-101 revisado com 2 casos, um aderente e um **divergente**
(honesto, calculado por `piloto.py`, nunca declarado manualmente) — a
falha funcional não impediu o Estúdio de prosseguir, pois I3 exige saída
esperada declarada, não 100% de acerto. P9: MET-101 (resultado,
`baseline_ref: BL-101`) e MET-102 (uso), distinção preservada e nenhuma
causalidade declarada além do que os dados sustentam. P10: CAL-101
configurada com responsável e cadência; dois ciclos executados (ver §12).

## 12. Recorrência

Ciclo 1 sem drift, persistido sem decisão exigida. Ciclo 2 com drift
detectado e quantificado por AG-04 (agente pode preparar o ciclo inteiro,
conforme já documentado em `calibragem.py`); AG-04 tentando gravar a
decisão é recusado; Marina Prado decide recalibrar. Os dois ciclos
permanecem preservados lado a lado (`CAL-101-C01.yaml`,
`CAL-101-C02.yaml`), nenhum sobrescrito. Resultado: **PASS**.

## 13. HB

18/18 declaradas, 18/18 estruturalmente resolvíveis (catálogo válido,
todas as referências `hb` do playbook resolvem), 14/18 usadas neste
caso de controle concreto (HB-04/05/06/13 não são exigidas por nenhuma
etapa do contrato declarado — mesma situação de `D-11 PARCIAL` já
registrada em 2.6.4, não uma lacuna nova). Ver `matriz-hb-ag-final.md`.

## 14. AG

4/4 declarados, 4/4 mapeados, 3/4 (AG-02, AG-03, AG-04) participaram
ativamente deste caso; AG-01 verificado pela fronteira formal
(`catalogo.py --resolver-papel-capacidade`), não pela participação
direta. 0 agentes com autoridade EX3/EX4 indevida.

## 15. Critérios de verificação

Todas as 13 HB automatizadas do catálogo possuem
`criterio_de_verificacao` não vazio (C22). As HB híbridas/manuais
(HB-04, HB-05, HB-11, HB-14, HB-15) também declaram critério; a
checagem estrita cobre as automatizadas, que é o que o playbook exige
estruturalmente via `playbook.py::capacidade_valida()`.

## 16. Cinco inegociáveis

I1–I5 semanticamente satisfeitos a partir de artefato real (nenhuma flag
manual usada como prova). Ver `matriz-inegociaveis-final.md`. **5/5**.

## 17. Seis autorizações

E1, E2, E3-D, E3-E (AUTORIZADO — caso agêntico), E4, E5 — todas
avaliadas corretamente. Ver `matriz-portoes-final.md`. **6/6 aplicáveis
conformes**.

## 18. Cinco entregáveis

E1–E5 materializados como arquivos reais e não vazios em
`caso/entregaveis/`, cada um com evento `EntregavelEmitido` apontando
para o arquivo e a versão. E3 consolida E3-D+E3-E em um único documento.
Ver `matriz-entregaveis-final.md`. **5/5**.

## 19. Eventos

56 eventos persistidos no caso de controle (`eventos.jsonl`), cobrindo
todas as categorias mínimas exigidas: início do caso, mudanças de etapa,
recusas (de etapa, de escrita direta, de validação por agente, de
decisão por agente), sessões humanas, curadoria, decisões de autonomia e
recalibragem, casos de teste, calibragem, portões e emissões. Ver §7 de
`caso-controle.md`.

## 20. Proteção de registro/contexto

Escrita direta em `registro/estado.json` testada e recusada (G5, exit 2,
evento `TentativaNegada`). Escrita direta em `contexto/regras/` testada
e recusada (G2b, exit 2). Nenhum caminho do percurso completo recorreu a
bypass manual — confirmado pelo log integral do driver (56 chamadas, uma
por linha em `caso-controle-log-comandos.txt`), todas via subprocess
contra os scripts oficiais.

## 21. Rastreabilidade ponta a ponta

Elemento selecionado: RN-101 (curada em P2) → consultada em P4 → P5
(classificação agêntica) → E3 (Blueprint) → P6/P7 (especificação +
autonomia) → P8/P9 (`MET-101.baseline_ref = "BL-101"`, preservando o
vínculo com a linha de base de P3a sem reinvenção) → P10 → E5 (cita a
linha de base e o resultado apurado literalmente). IDs preservados sem
reescrita em todo o percurso (C42).

## 22. Não invenção

Testado diretamente (C41): materializar E2 antes de qualquer linha de
base registrada é recusado com mensagem explícita ("nenhuma linha de
base em `registro/baseline/`"), não com um documento genérico
preenchido com texto padrão. Os cinco entregáveis materializados citam
apenas dados presentes nos artefatos do caso (valores de BL-101, MET-101,
CT-101 etc.), nunca inventados — mesmo padrão de não invenção já
verificado em 2.6.5 (`_exige()` em `entregaveis.py`, inalterado).

## 23. Testes C01–C42 (+ C43 de regressão)

43 verificações, 0 falhas. Ver `teste-2.6.6-C01.txt` a
`teste-2.6.6-C43.txt` e a saída consolidada em
`teste-regressao-final.txt`.

## 24. Regressão

Inicial (antes deste pacote, ao HEAD `bcc85a6`): 404 verificações, 0
falhas (`teste-regressao-inicial.txt`). Final (após C01–C43 e a correção
de `calibragem.py`): 447 verificações, 0 falhas
(`teste-regressao-final.txt`). O aumento de 43 corresponde exatamente às
novas verificações deste pacote — nenhuma suíte anterior mudou de
contagem.

## 25. Defeitos encontrados

**D-2.6.6-01** — `calibragem.py::checar_autoria()` bloqueava
`declarado_por`/`registrado_por` como agente também para
`ciclo_calibragem`, contradizendo o próprio contrato documentado do
módulo ("o agente pode preparar um ciclo inteiro"). Detectado ao
construir o caso de controle (primeira vez que um ciclo de calibragem
com autoria de agente foi exercitado ponta a ponta — 2.6.3 sempre usou
`declarado_por`/`registrado_por` humanos em suas fixtures, mesmo
passando um agente como `--ator`). Severidade: média (bloqueava um
caminho já especificado, sem risco de segurança — a decisão humana
continuava protegida por `checar_decisao()`, uma checagem independente).

**Achado documental (não é defeito de código, reafirmação do 2.6.5)** —
não existe script executável (`eiac-campo/scripts/classificar.py`) para
gravar `classificacao_tecnologica` de P5 de forma estruturada; a única
skill (`hb-classificar`) produz apenas `caso/P5-classificacao.md` em
texto livre. O caso de controle registra o campo diretamente em
`st["cumprimentos"]["P5"]`, com evidência preservada, e o achado é
documentado em vez de corrigido (este pacote não introduz capacidade
nova).

## 26. Correções e retestes

`calibragem.py::checar_autoria()` mantida inalterada para
`rotina_calibragem` (autoria sempre humana); nova função
`checar_autoria_ciclo()` introduzida para `ciclo_calibragem`, permitindo
agente em `declarado_por`/`registrado_por` e preservando a vedação de
`decisao` a agente (já garantida por `checar_decisao()`, não tocada).
Commit `31ffff2` (`fix(field): allow agent authorship of calibration
cycle records`). Reteste: `testes/campo_2_6_3.py` (57/57, sem
regressão — os testes anteriores usavam autoria humana e continuam
passando), `testes/campo_2_6_6.py` (43/43), suíte completa (447/447, 0
falhas).

## 27. Comparação S2-BL → final da Ação 2.6

| Indicador | S2-BL | Final Ação 2.6 |
|-----------|-------|----------------|
| Etapas | 8/13 | 13/13 declaradas e operacionalmente executáveis |
| P7 | ausente | operacional, decisão humana protegida |
| P10 | ausente | operacional, recorrente, dois ciclos demonstrados |
| HB referenciadas/formalizadas | 9/18, 0/18 códigos | 18/18 declaradas, 18/18 resolvíveis, 14/18 fisicamente implementadas (D-11 PARCIAL, 4/18 sem skill própria) |
| AG mapeados | 0/4 | 4/4 mapeados, 0 com autoridade EX3/EX4 indevida |
| Portões | 2/6 | 6/6 aplicáveis conformes |
| Inegociáveis | 0/5 | 5/5 semanticamente verificáveis e satisfeitos |
| registro/ protegido | não | sim (G5) |
| eventos da máquina | parcial | completo (todo caminho crítico auditável) |
| entregáveis materiais | ausentes | 5/5 materializados e rastreáveis |
| percurso F0–P10 | ausente | demonstrado integralmente em caso novo |

## 28. Situação D-07–D-13

D-07 (8/13 etapas): **RESOLVIDO** (desde 2.6.0, reconfirmado aqui).
D-08 (registro/ desprotegido): **RESOLVIDO** (desde 2.6.1, reconfirmado
em C07/C37).
D-09 (recusas sem evento): **RESOLVIDO** (desde 2.6.1, reconfirmado em
C36/C37).
D-10 (P7/P10 ausentes): **RESOLVIDO** (desde 2.6.3, reconfirmado em
C10/C15).
D-11 (HB/AG sem relações formais): **PARCIAL**, inalterado desde 2.6.4 —
catálogo 18/18 completo e resolvível, mas 4/18 HB (HB-04/05/06/13)
continuam sem implementação física própria. Este pacote não altera essa
situação (não é uma feature nova a introduzir).
D-12 (emissão sem materialização): **RESOLVIDO** (desde 2.6.5,
reconfirmado neste pacote com um novo caso completo — 5/5 entregáveis
materializados, todos rastreáveis a arquivo real).
D-13 (sem percurso F0–P10): **RESOLVIDO neste pacote** — percurso
integral demonstrado em caso de controle novo, 13/13 etapas, 0 falhas
inesperadas.

## 29. Indicadores finais

```
ETAPAS DECLARADAS: 13/13
ETAPAS OPERACIONALMENTE EXECUTÁVEIS: 13/13
PERCURSO F0–P10: PASS
HB DECLARADAS: 18/18
HB RESOLVÍVEIS: 18/18
HB AUTOMATIZADAS COM CRITÉRIO: 13/13
AG DECLARADOS: 4/4
AG MAPEADOS: 4/4
AG COM AUTORIDADE HUMANA INDEVIDA: 0
INEGOCIÁVEIS: 5/5
PORTÕES: 6/6
ENTREGÁVEIS: 5/5
P10 RECORRENTE: SIM
PROTEÇÃO registro/: SIM
PROTEÇÃO contexto/: SIM
EVENTOS DE RECUSA: CONFORME
DECISÃO DE AUTONOMIA HUMANA: CONFORME
DECISÃO DE RECALIBRAGEM HUMANA: CONFORME
```

## 30. Evidências

`.projectdocs/evidencias/sprint2/2.6.6/`: este `resultado.md`,
`caso-controle.md`, `caso-controle-driver.py`,
`caso-controle-log-comandos.txt`, `matriz-f0-p10.md`,
`matriz-fronteira.md`, `matriz-inegociaveis-final.md`,
`matriz-portoes-final.md`, `matriz-entregaveis-final.md`,
`matriz-hb-ag-final.md`, `teste-regressao-inicial.txt`,
`teste-regressao-final.txt`, `teste-2.6.6-C01.txt`…`C43.txt`,
`teste-2.6.6-saida-completa.txt`, `eventos.jsonl`,
`estado-final-caso.json`, `caso-controle-{RN-101,BL-101,OP-101,AUT-101,
CT-101,MET-101,MET-102,CAL-101,CAL-101-C01,CAL-101-C02}.yaml`,
`caso-controle-E{1..5}.md`, `diff.patch`, `git-show.txt`.

## 31. Commit(s)

`31ffff2260f40c06a323087791cf8e17062a4ee5` —
`fix(field): allow agent authorship of calibration cycle records`
(correção funcional, ver §25/§26).

Commit de testes/evidência registrado a seguir neste mesmo pacote (ver
`git-show.txt` para o hash real e o diffstat completo).

## 32. Estado final da Ação 2.6

**CONFORME** quanto ao escopo executável verificável: 13/13 etapas
operacionais, 6/6 portões, 5/5 inegociáveis, 5/5 entregáveis, proteção de
registro/contexto confirmada, fronteira humana preservada em todos os
pontos críticos testados, percurso F0–P10 demonstrado integralmente em
caso novo, D-07/D-08/D-09/D-10/D-12/D-13 resolvidos.

Ressalva única, já registrada e não nova: **D-11 permanece PARCIAL**
(4/18 HB sem implementação física própria — HB-04/05/06/13, nenhuma
delas referenciada pelo contrato F0–P10 congelado em 2.6.0). Essa
ressalva não bloqueia a declaração de CONFORME da Ação 2.6, pois nenhuma
dessas HB é exigida pelo percurso executável demonstrado; ela é
transferida como nota de escopo, não como pendência que impeça o
fechamento.
