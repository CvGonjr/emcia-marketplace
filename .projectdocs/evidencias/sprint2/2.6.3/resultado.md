# Pacote 2.6.3 — P8, P9 e P10

## 1. Identificação

Ação: 2.6 — Agentes e Protocolos
Pacote: 2.6.3
Branch: master
HEAD inicial: `3431e6fd6dbcbaa24112e2d99c033fcd4d672ac8`
HEAD final: ver §28 (hash real do commit deste pacote)
Data: 2026-09-19

## 2. Documentos consultados

Obrigatórios: EMCIA-MET-01 §3.4.8-3.4.10, EMCIA-CAT-01 §3.4.5,
EMCIA-ESP-01 §3.5/§3.9, EMCIA-TRA-01, EMCIA-E4, EMCIA-E5 §1-6/Anexos
B/C/D, EMCIA-GLO-01, EMCIA-ARQ-01 §3.8, EMCIA-VER-01 (§8.3, escopo
declarado — não define lógica de comparação P8/P9). Consultados também:
EMCIA-CAM-01 (Protocolo de Campo por Passo, §3.4/3.5/3.6 — fonte
primária dos contratos executáveis, entrada/atividade/saída/encerramento
e Anexos B/C/D), EMCIA-CTX-01, EMCIA-FER-01 (entrada IA-10, detecção de
desvio), EMCIA-HAB-01, evidências de 2.6.0/2.6.1/2.6.2.

## 3. Baseline relacionado

P8 ausente; P9 ausente; P10 ausente; P10 recorrente ausente
operacionalmente; E5 implementado mas divergente; D-10 (P7/P10
ausentes) parcialmente resolvido após 2.6.2 (P7 tratado, P10
pendente).

## 4. Estado inicial

`playbook.json` já declarava P8 (`depende_de: P7`, EX3, `hb-pilotar`),
P9 (`depende_de: P8`, EX3, `hb-medir-valor`) e P10 (`depende_de: P9`,
`recorrente: true`, `cadencia_obrigatoria: true`,
`responsavel_obrigatorio: true`, `delegavel: false`, EX4 na decisão/EX2
no monitoramento) desde o 2.6.0. O núcleo já suportava genericamente
recorrência, cadência, responsável nominal e satisfação de inegociáveis
por caminho autorizado desde o 2.6.1 (`avancar.registrar_recorrencia`,
`avancar.satisfazer_inegociavel`) — nenhuma dessas primitivas exigiu
alteração neste pacote. Não existia nenhum script, schema ou skill de
campo para P8/P9/P10.

## 5. Contrato e implementação de P8

Fonte: EMCIA-CAM-01 §3.4/Anexo B. Entrada: P7 encerrado, termo de
autonomia decidido, linha de base do passo 3 registrada. Saída:
conjunto de casos de teste com saída esperada, modo/duração acordados,
plano de reversão escrito. Implementado em
`eiac-campo/scripts/piloto.py` (`gravar_conjunto`), schema
`registro/piloto.schema.json`, artefato `registro/piloto/CT-NNN.yaml`.
Skill `hb-pilotar`, comando `/pilotar`.

## 6. Casos de teste e saída esperada

Cada caso segue o Anexo B literal (identificador, origem, entrada,
saída esperada, critério de aprovação, categoria, revisor, data da
revisão), mais três campos não nomeados no Anexo B mas exigidos pelo
pacote (§11/§13): `esperado_definido_em`/`esperado_definido_por`
(congelamento contra viés retrospectivo) e `resultado` (calculado pela
comparação determinística `saida_obtida == saida_esperada`, nunca
escrito manualmente — T08 confirma a recusa de forjar esse campo). O
conjunto exige ao menos um caso `categoria: celula_critica` — conjunto
só com casos comuns é recusado.

## 7. Evidência para inegociável 3

`avancar.py --satisfazer-inegociavel 3` com evidência referenciando o
arquivo real `registro/piloto/CT-*.yaml` (estado `revisado`, contagem
de casos e célula crítica) — nunca um booleano solto. Verificado no
caso de controle e em T09/T35/T36.

## 8. Contrato e implementação de P9

Fonte: EMCIA-CAM-01 §3.5/Anexo C. Entrada: P8 encerrado, piloto
executado, linha de base disponível. Saída: plano de medição com ao
menos uma métrica de resultado apurada. Implementado em
`eiac-campo/scripts/metrica.py` (`gravar_metrica`), schema
`registro/metricas.schema.json`, artefato
`registro/metricas/MET-NNN.yaml`. Skill `hb-medir-valor`, comando
`/medir-valor`. `piloto_ref` resolve contra `registro/piloto/` e exige
estado `revisado` (relação P8→P9).

## 9. Baseline e métricas

Campo `tipo` aceita três valores (Anexo C: `resultado`, `uso`,
`qualidade`) — métrica de uso é aceita no plano, mas isoladamente não
satisfaz o inegociável 4 (T12/T14). A linha de base (`linha_base_data`)
precisa ser anterior a `resultado_apurado_data` — baseline inventada
depois do piloto é recusada explicitamente (T17).

## 10. Métrica de resultado

Pelo menos uma métrica com `tipo: resultado` disponível e apurada
(T13/T15). No caso de controle: tempo de ciclo de triagem, 45min → 31min
(31% de redução), com `fatores_externos_declarados` preenchido
explicitamente — nunca vazio quando `estado: apurada` (T18/T18b).

## 11. Evidência para inegociável 4

`avancar.py --satisfazer-inegociavel 4` com evidência referenciando o
arquivo real `registro/metricas/MET-*.yaml` (tipo, estado, valores
observados) — nunca booleano (T37/T38).

## 12. Contrato e implementação de P10

Fonte: EMCIA-CAM-01 §3.6/Anexo D (camada declarada textualmente: "EX4
na decisão, EX2 no monitoramento" — confirma o desenho já presente no
playbook desde o 2.6.0). Entrada: P9 encerrado, solução em operação ou
piloto concluído. Saída: rotina de recalibragem instalada, responsável
nomeado, cadência em calendário. Implementado em
`eiac-campo/scripts/calibragem.py` (`gravar_rotina` + `gravar_ciclo`),
schema `registro/calibragem.schema.json` (dois objetos:
`rotina_calibragem` e `ciclo_calibragem`), artefatos
`registro/calibragem/CAL-NNN.yaml` (rotina) e
`registro/calibragem/CAL-NNN-CNN.yaml` (ciclos). Skill `hb-recalibrar`
(`delegavel: false`, mesma marcação de `hb-governar` em P7), comando
`/recalibrar`.

## 13. Recorrência

O mecanismo de recorrência em si (cadência, responsável, histórico de
ciclos, `estado_recorrente`) é o já existente
`avancar.py --registrar-recorrencia`, genérico desde o 2.6.1 — não foi
alterado. O que este pacote acrescenta, em `eiac-campo/scripts/`, é o
que o núcleo não pode conhecer: o conteúdo da rotina (Anexo D) e, por
ciclo, se houve drift, a recomendação do agente e a decisão humana. Os
dois mecanismos coexistem: a recorrência do núcleo controla
`estado_recorrente` em `registro/estado.json`; os ciclos de campo
controlam os artefatos `CAL-NNN-CNN.yaml` com o conteúdo do drift e da
decisão.

## 14. Responsável e cadência

`responsavel` exige pessoa nomeada — recusado com valor genérico
("equipe"), aceito com nome próprio (T19/T20), reaproveitando a mesma
convenção lexical do núcleo (`_ator_pessoa_nomeada`, idêntica à usada em
`avancar._ator_valido`, `operacional.py` e `governanca.py`). `cadencia`
é campo obrigatório do schema — ausência recusada (T21).

## 15. Drift

Drift (mudança na distribuição do dado ou na relação que a solução
aprendeu — EMCIA-FER-01, entrada IA-10) é representado por
`drift_detectado` (booleano), com `drift_descricao`/
`drift_quantificacao` obrigatórios quando verdadeiro. Um ciclo sem
drift é caminho positivo legítimo — não exige recomendação nem decisão
(T27). O limiar (`limiares_desvio`) é declarado na rotina, antes do
piloto — o schema não impede alteração posterior via nova versão, mas
nenhum mecanismo deste pacote permite ajustar o limiar silenciosamente
depois de observado o comportamento.

## 16. Fronteira agente × humano

Estruturalmente aplicada em `calibragem.py::checar_decisao`: o campo
`decisao` (`recalibrar`/`expandir`/`descontinuar` — as únicas três
opções nomeadas em CAT-01/CAM-01/ESP-01, texto idêntico nas três
fontes) exige ator humano nomeado; tentativa de agente é recusada com
evento `CicloCalibragemRecusado` (T30/T30b). O agente pode detectar,
quantificar e recomendar (T28/T29) — nunca decidir. **Achado corrigido
durante este pacote:** a primeira versão de `gravar_ciclo` recusava
qualquer segunda gravação do mesmo identificador, mesmo para
complementar um ciclo pendente (drift detectado, sem decisão) com a
decisão humana — o que o caso de controle integrado expôs ao tentar
reproduzir o fluxo real "agente detecta e recomenda; humano decide
depois". Corrigido para permitir complementar um ciclo pendente sem
decisão, mantendo bloqueada a sobrescrita de um ciclo já decidido ou a
alteração dos fatos do drift na complementação (T29b/T29c). Ver §25/§26.

## 17. Evidência para inegociável 5

`avancar.py --satisfazer-inegociavel 5` com evidência referenciando o
arquivo real `registro/calibragem/CAL-*.yaml` (responsável, cadência,
ciência) — nunca booleano (T39/T40).

## 18. Caso de controle

Caso `caso-controle-2-6-3`, percurso completo F0→P10: nível N2 apurado;
P6 (`OP-001`, validado); P7 (`AUT-001`, decidido); P8 (`CT-001`, dois
casos, um célula crítica, revisado); inegociável 3 satisfeito; P9
(`MET-001` tipo resultado, `MET-002` tipo uso); inegociável 4
satisfeito; P10 (`CAL-001`, responsável e cadência); recorrência
registrada; ciclo 1 sem drift; ciclo 2 com drift — tentativa de decisão
por agente recusada duas vezes (autoria e decisão), decisão humana
válida registrada; inegociável 5 satisfeito. 45 eventos na trilha.
Detalhe completo em `caso-controle.md`.

## 19. Relação com E5

P8/P9/P10 produzem insumos rastreáveis (`CT-*`, `MET-*`, `CAL-*`)
suficientes para futura avaliação do portão E5 (T43). **E5 não foi
declarado emitido neste pacote.** No caso de controle, `E5` permanece
não emitido; o playbook já exige P10 encerrada como pré-condição
estrutural de portão (T44), mas a validação semântica completa dos
inegociáveis 3, 4 e 5 e a geração material do relatório de piloto
pertencem ao 2.6.5.

## 20. Testes

57 verificações em `testes/campo_2_6_3.py` (T01-T48 do pacote, mais
sub-verificações T05a, T10b/T11b análogas ao padrão de 2.6.2, T29b/T29c
para o achado do ciclo em duas fases, e G5a-c para a proteção genérica
de `registro/`). 0 falhas. Log completo em
`teste-2.6.3-saida-completa.txt`, logs individuais
`teste-2.6.3-T01.txt` a `teste-2.6.3-T48.txt` (e variantes).

## 21. Pares negativo/positivo

Todos os nove pares exigidos pela seção 55 do pacote estão cobertos:
caso sem/com saída esperada (T04/T03); resultado divergente/aderente
(T07/T06); P9 sem/com baseline (T11/T10); métrica de uso/resultado
(T12/T13); P10 sem/com responsável (T19/T20); P10 sem/com cadência
(T21/T22); agente decide/humano decide recalibragem (T30/T31); drift
sem/com decisão rastreável (T34/T33); booleanos dos inegociáveis
3-5/evidências reais (T35,T37,T39/T36,T38,T40).

## 22. Eventos

Novos tipos de evento neste pacote: `ConjuntoPilotoRegistrado`,
`ConjuntoPilotoRevisado`, `ConjuntoPilotoRecusado`, `MetricaRegistrada`,
`MetricaApurada`, `MetricaRecusada`, `RotinaCalibragemRegistrada`,
`RotinaCalibragemRecusada`, `CicloCalibragemRegistrado`,
`CicloCalibragemRecusado`, `DecisaoRecalibragemRegistrada`. Toda
recusa produz evento — nenhum caminho de erro silencioso.

## 23. Hard-code

Busca por P8/P9/P10/piloto/baseline/metrica/drift/calibragem/
recalibragem/E5 em `eiac-nucleo/scripts/*.py`: 3 ocorrências, todas não
comportamentais (uma linha de docstring de exemplo de uso em
`avancar.py`, duas linhas de comentário explicativo sobre o baseline
2.6-BL26) — 0 ocorrências em condicional (`if`) testando esses termos.
`eiac-nucleo/` não foi alterado neste pacote (confirmado por
`git status --short eiac-nucleo/`, saída vazia).

## 24. Regressão

Antes: 235/235 (Ação 2.5 + 2.6.0 + 2.6.1 + 2.6.2). Depois: 292/292 — os
57 novos deste pacote, 0 falhas em nenhuma suíte anterior.

## 25. Defeitos encontrados

Um defeito real em `calibragem.py::gravar_ciclo` (não pré-existente —
introduzido e corrigido dentro deste mesmo pacote, antes do commit):
recusava incondicionalmente qualquer segunda gravação de um
identificador de ciclo já existente, mesmo para complementar um ciclo
pendente (drift detectado, sem decisão) com a decisão humana — fluxo
que o caso de controle integrado exigiu ao reproduzir "agente detecta e
recomenda; humano decide depois, sobre o mesmo ciclo".

## 26. Correções e retestes

Adicionada `checar_ciclo_existente()`: permite complementar um ciclo
pendente (drift detectado, sem `decisao` ainda) com a decisão humana no
mesmo identificador; continua recusando sobrescrever um ciclo já
decidido, um ciclo sem drift já registrado, ou alterar
`drift_descricao`/`drift_quantificacao` na complementação. T29b/T29c
adicionados à suíte; suíte completa reexecutada (57/57) e regressão
completa reexecutada (292/292) após a correção.

## 27. Itens adiados

2.6.4 — Formalização das 18 HB e 4 AG.
2.6.5 — Portões, inegociáveis (validação semântica final) e geração de
entregáveis (E4/E5 materiais).
2.6.6 — Verificação integral F0–P10.

## 28. Commit

Ver `git-show.txt` e `diff.patch` neste diretório para o hash real, o
diffstat e o diff completo.

## 29. Estado final

**CONFORME.**
