# Matriz de inegociáveis — pacote 2.6.6

| ID | Evidência | Resultado |
|----|-----------|-----------|
| I1 | `registro/baseline/BL-101.yaml` (`apuracao: medido`, `nivel: N2`, `valor_atual: "3 dias uteis"`, `data: 2026-09-01`) verificado por `inegociaveis.py::verificar_i1` e satisfeito por Marina Prado antes de qualquer emissão de P6+ | PASS |
| I2 | `registro/governanca/autonomia/AUT-101.yaml` (`estado: decidido`, `decisor: Marina Prado`, `data_decisao`, `justificativa_decisao` preenchidos) verificado por `verificar_i2`, satisfeito por Marina Prado | PASS |
| I3 | `registro/piloto/CT-101.yaml` (`estado: revisado`, 2 casos, ambos com `saida_esperada` preenchida — um `aderente`, um `divergente`, ambos com saída esperada declarada antes da execução) verificado por `verificar_i3` | PASS |
| I4 | `registro/metricas/MET-101.yaml` (`tipo: resultado`, `estado: apurada`, `resultado_apurado: "1 dia util"`) verificado por `verificar_i4`, distinto de `MET-102.yaml` (`tipo: uso`) | PASS |
| I5 | `registro/calibragem/CAL-101.yaml` (`responsavel: Marina Prado`, pessoa nomeada, `cadencia: mensal`) verificado por `verificar_i5` | PASS |

**5/5 inegociáveis semanticamente satisfeitos**, todos verificados a
partir de artefato real via `eiac-campo/scripts/inegociaveis.py`
(nenhuma flag manual usada como prova — `avancar.py --satisfazer-inegociavel`
só foi chamado depois de cada `verificar_iN` retornar `satisfeito=True`).
