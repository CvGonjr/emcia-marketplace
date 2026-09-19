# Matriz dos inegociáveis — pacote 2.6.5

Estado final, após implementação. Fonte: `eiac-campo/template-caso/registro/playbook.json`
(`inegociaveis`), `eiac-campo/scripts/inegociaveis.py`.

| ID | Requisito | Evidência esperada | Verificador | Negativo | Positivo | Estado |
|----|-----------|---------------------|-------------|----------|----------|--------|
| I1 | Linha de base registrada antes do piloto, apuração proporcional ao nível (estimada em N1, medida em N2/N3) | `registro/baseline/BL-*.yaml` (indicador, valor_atual, apuracao, data, nível) | `inegociaveis.verificar_i1` | T01 (sem baseline), T02b (apuracao=estimado fora de N1, recusado em `baseline.py`) | T02 | CONFORME |
| I2 | Termo de autonomia escrito, decidido por humano | `registro/governanca/autonomia/AUT-*.yaml`, `estado: decidido` | `inegociaveis.verificar_i2` | T03 (estado=proposto) | T04 | CONFORME |
| I3 | Casos de teste com saída esperada | `registro/piloto/CT-*.yaml`, `estado: revisado`, todos os casos com `saida_esperada`/`esperado_definido_em` | `inegociaveis.verificar_i3` | T05 (conjunto em rascunho, sem saída esperada) | T06 | CONFORME |
| I4 | Ao menos uma métrica de resultado, não só de uso | `registro/metricas/MET-*.yaml`, `tipo: resultado`, `estado: apurada` | `inegociaveis.verificar_i4` | T07 (tipo=uso) | T08 | CONFORME |
| I5 | Responsável nomeado pela recalibragem | `registro/calibragem/CAL-*.yaml`, `responsavel` pessoa nomeada, `cadencia` definida | `inegociaveis.verificar_i5` | T09 (`responsavel: equipe`, recusado em `calibragem.py`), T09b (`responsavel: equipe de TI`, recusado no verificador semântico) | T10 | CONFORME |

## Contra o booleano mágico (T11/T12)

Nenhum inegociável é satisfeito por escrita direta em `estado.json`. O
único caminho autorizado é `eiac-nucleo/scripts/avancar.py --satisfazer-inegociavel`,
e este pacote garante que ele só é chamado **depois** que
`inegociaveis.py` inspecionou um artefato real e devolveu
`satisfeito=True` — nunca a partir de um valor gravado manualmente
(T11: flags manuais sem artefato real nunca produzem uma chamada
legítima ao verificador; T12: evidência real produz um registro
estruturado `{satisfeito, evidencia, autor, data}` cuja `evidencia`
referencia o nome do verificador e o artefato, não apenas `"true"`).

## Dupla camada de proteção em I5 (T09/T09b)

`calibragem.py::_ator_pessoa_nomeada` (mecanismo já existente desde
2.6.2/2.6.3) recusa palavras genéricas exatas (`equipe`, `area`, `time`
etc.), mas uma frase composta como `"equipe de TI"` passa por essa
checagem lexical de palavra inteira. `inegociaveis.py::verificar_i5`
tokeniza o campo `responsavel` e recusa se qualquer token colidir com o
conjunto de coletivos genéricos — capturando o caso que escapa da
primeira camada. Nenhuma das duas foi enfraquecida; a segunda é a
autoridade final sobre I5.
