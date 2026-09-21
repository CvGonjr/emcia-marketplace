# Evidência final — integração com a execução de contraste

**Data:** 21/09/2026

**Branch:** `feat/execucao-contraste`

O marketplace foi preparado para ser consumido tanto pelo núcleo de campo quanto
pelo controle de contraste, sem modo de desvio no núcleo e sem alteração no texto
das habilidades.

## Alterações verificadas

- G6 protege `fontes/` contra Write, Edit e mutações por Bash, sempre com evento;
  leitura continua permitida.
- O núcleo recusa um caso que contenha marcador durável `execucao: contraste` ou a
  configuração legada explícita do plugin de contraste.
- O registro de esforço do campo usa a camada EX lida do playbook e o mesmo formato
  do contraste.
- O cálculo de quadro tem uma única implementação em `eiac-campo/scripts/quadro.py`;
  núcleo e contraste usam adaptadores.
- Os oito gravadores do campo aceitam a raiz do controle por
  `EIAC_NUCLEO_SCRIPTS`, permitindo substituir o controle sem duplicar o método.
- O plugin do núcleo foi versionado para `0.2.18`.
- As decisões 014, 015 e 016 registram separação, isolamento/medição/cálculo e
  identidade de runtime substituível.

## Regressão

Foram executados os 15 arquivos `testes/*.py` e `testes/negativos.sh`. Todos
terminaram com código zero. A suíte cobre os pacotes 2.6.2 a 2.6.6, contexto,
curadoria, integração, núcleo, YAML, P3d, playbook, esforço, G6 e isolamento.

O teste de contrato do repositório `emcia-contraste` confirmou que ambos os
controles fornecem `/eiac-nucleo:*`, com 13 verificações e zero falhas.

## Integridade do campo

`git diff -- eiac-campo/skills` não produz saída. Nenhuma habilidade foi modificada.
O contraste consome playbook, esquemas, scripts e habilidades da fonte única no
`eiac-campo`.
