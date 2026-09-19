# Caso de controle — P8/P9/P10

ID: `caso-controle-2-6-3` (case template `eiac-campo/template-caso`, aberto via `novo-caso.sh`)

HEAD: `3431e6fd6dbcbaa24112e2d99c033fcd4d672ac8` (HEAD_INICIAL_2.6.3)

Data: 2026-09-19

## 1. Pré-condições

Percurso F0→P7 concluído: nível N2 apurado; F0-P5 encerradas com sessão
registrada onde exigido; `OP-001` (especificação operacional, P6)
validada por Marina Prado; `AUT-001` (termo de autonomia, P7) decidido
por Marina Prado, referenciando `OP-001`. Sessão P7 registrada, etapa
P7 encerrada — caso avança para P8.

## 2. Baseline

Linha de base do passo 3, registrada em `MET-001.linha_base`: **45
minutos** (tempo de ciclo de triagem), procedência `V` (verificado),
data 2026-08-01 — anterior a qualquer resultado apurado no piloto.

## 3. P8 — casos de teste

Conjunto `CT-001` (`registro/piloto/CT-001.yaml`), modo assistido,
duração 4 semanas, plano de reversão escrito, critério de aprovação de
escala definido em 2026-09-10 (antes do início).

### Caso CT-001-01 (célula crítica)
esperado: `Prioridade alta`
obtido: `Prioridade alta`
resultado: `aderente`

### Caso CT-001-02 (comum)
esperado: `Prioridade normal`
obtido: `Prioridade normal`
resultado: `aderente`

Conjunto revisado por Marina Prado (`revisado_por`), cobrindo a célula
crítica (CT-001-01, categoria `celula_critica`) — não apenas casos
comuns.

## 4. Evidência do inegociável 3

`avancar.py --satisfazer-inegociavel 3` com evidência
`registro/piloto/CT-001.yaml (estado: revisado, 2 casos, 1
celula_critica, revisado_por: Marina Prado)`. Evento
`InegociavelSatisfeito` registrado. Não marcado como booleano — a
evidência referencia o artefato real.

## 5. P9 — métricas

`MET-001` (tipo `resultado`): Tempo de ciclo de triagem.
`MET-002` (tipo `uso`): Número de guias processadas pelo assistente —
aceito no plano, mas não conta sozinho para o inegociável 4.

## 6. Métrica de resultado

`MET-001`: linha de base 45 minutos (2026-08-01, `V`) → resultado
apurado 31 minutos (2026-09-20, `V`). `fatores_externos_declarados`:
"Nenhum identificado; volume de guias estável no período" — declaração
explícita, sem inferência causal automática ("a solução causou a
redução" não é afirmado; apenas o valor observado e o fator externo
declarado).

## 7. Evidência do inegociável 4

`avancar.py --satisfazer-inegociavel 4` com evidência
`registro/metricas/MET-001.yaml (tipo: resultado, estado: apurada,
45min -> 31min)`. Evento `InegociavelSatisfeito` registrado.

## 8. P10 — responsável

`CAL-001.responsavel`: **Marina Prado** (pessoa nomeada,
`responsavel_ciente: true`). Testado e recusado com `responsavel:
"equipe"` antes de aceitar o valor nominal (mesma convenção lexical do
núcleo, `avancar._ator_valido`).

## 9. P10 — cadência

`CAL-001.cadencia`: **mensal**, `data_primeira_revisao: 2026-10-19`.
Recorrência registrada via mecanismo genérico do núcleo:
`avancar.py --registrar-recorrencia P10 --cadencia mensal --responsavel
"Marina Prado"` (evento `RecorrenciaRegistrada`).

## 10. Ciclo 1

`CAL-001-C01`, `data_verificacao: 2026-10-19`, `drift_detectado: false`.
Caminho positivo: verificação executada, nenhum desvio relevante,
mantém o estado atual — sem exigir recomendação nem decisão.

## 11. Ciclo 2

`CAL-001-C02`, `data_verificacao: 2026-11-19`, `drift_detectado: true`.

## 12. Drift detectado

`drift_descricao`: "Tempo de ciclo subiu de 31 para 41 minutos no
último mês (32% de aumento)". `drift_quantificacao`: "Média móvel de
30 dias: 31min (out/2026) → 41min (nov/2026)". Limiar violado (definido
em `CAL-001.limiares_desvio`: "Variação > 15%").

## 13. Recomendação do agente

`recomendacao_agente`: "Recalibrar o limiar de prioridade da célula
crítica; investigar aumento de volume no período" — preparada antes da
gravação, sem decisão anexada. Uma tentativa de gravar o mesmo ciclo com
`decisao: recalibrar` e `decisor: AG-04` foi feita e **recusada**
(`declarado_por`/`registrado_por`/`decisor` não podem ser agente; evento
`CicloCalibragemRecusado`, duas ocorrências na trilha — uma pela
autoria do rascunho, outra pela tentativa de decisão).

## 14. Decisão humana

Marina Prado decidiu `decisao: recalibrar`, `data_decisao: 2026-11-20`,
`justificativa_decisao`: "Drift confirmado contra o limiar definido
antes do piloto (>15%); recalibrar limiar de prioridade e investigar
causa do aumento de volume". Evento `DecisaoRecalibragemRegistrada`.

## 15. Evidência do inegociável 5

`avancar.py --satisfazer-inegociavel 5` com evidência
`registro/calibragem/CAL-001.yaml (responsavel: Marina Prado, cadencia:
mensal, ciente: true)`. Evento `InegociavelSatisfeito` registrado.

## 16. Insumos disponíveis para E5

`registro/piloto/CT-001.yaml`, `registro/metricas/MET-001.yaml`,
`registro/metricas/MET-002.yaml`, `registro/calibragem/CAL-001.yaml`,
`registro/calibragem/CAL-001-C01.yaml`,
`registro/calibragem/CAL-001-C02.yaml` — todos presentes e rastreáveis.
Tentativa estrutural de `avancar.py --emitir E5` não realizada neste
caso (E5 exige P10 encerrada e os portões correspondentes, verificação
semântica final pertence ao 2.6.5) — ver §19 do resultado.md.

## 17. Eventos

45 eventos na trilha (`eventos.jsonl`, cópia em
`.projectdocs/evidencias/sprint2/2.6.3/eventos.jsonl`), incluindo:
`ConjuntoPilotoRegistrado`, `ConjuntoPilotoRevisado`,
`InegociavelSatisfeito` (×3, para os inegociáveis 3, 4 e 5),
`MetricaRegistrada`, `MetricaApurada` (×2), `RotinaCalibragemRegistrada`,
`RecorrenciaRegistrada`, `CicloCalibragemRegistrado`,
`CicloCalibragemRecusado` (×2), `DecisaoRecalibragemRegistrada`,
`RecusaMaquina` (×2, tentativas de fluxo fora de ordem durante a
montagem do caso).

## 18. Resultado

Percurso P7→P10 completo, com fronteira agente×humano observada em
todos os pontos de decisão: P8 (revisão do conjunto por humano), P9
(interpretação de causa deixada em aberto, sem inferência automática),
P10 (decisão de recalibragem exclusivamente humana, tentativa de agente
recusada duas vezes com evento). Evidências reais e rastreáveis
disponíveis para os inegociáveis 3, 4 e 5. `E5` não foi emitido neste
caso. Estado final do caso: `etapa_atual: P10`, `camada_atual: EX4`
(recorrente).
