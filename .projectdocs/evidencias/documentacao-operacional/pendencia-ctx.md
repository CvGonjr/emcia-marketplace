# Documentação operacional — decisão documental pendente

Data: 03/10/2026. Estado: aguardando decisão humana conforme item 5 do pedido.

Marketplace: `d5924c0e6b4771ac4b8fc8fb35d0a50775ce10c9`.
Commit canônico: `1d6d1e8bfc1739594ea7a119257ecae28c8e5af4`.

A regressão inicial completa passou em Python 3.12.12: 919 verificações,
46 módulos, nenhuma exclusão e nenhuma falha. Inclui negativos.sh e contexto.py.
A saída integral está em regressao-inicial-3.12.txt. O executor utilizado é
.projectdocs/evidencias/parte-a-operacional/reexecutar-suite.py, com o binário
Python 3.12 no PATH para os subprocessos.

## Divergência

CTX-01-instrumento-camada-contexto.md na raiz e em eiac-campo/reference/
são idênticos entre si, mas diferem do EMCIA-CTX-01 canônico v0.5.
Declaram compatibilidade com v0.4, conservam estrutura própria de treze seções
e uma nota de implementação que ainda remete a pacotes posteriores.
A decisão 021 registra a manutenção e a alteração das duas cópias;
o commit a6ad092 confirma essa manutenção. As decisões 038–042 não determinam
se elas devem ser retiradas ou substituídas por cópias integrais do canônico.
Hashes, histórico e texto da decisão estão em levantamento-ctx.txt.

## Consulta

Adotar uma das alternativas: retirar ambas e usar somente o documento
empacotado, ou substituir ambas por cópias idênticas do canônico.
A recomendação apresentada é retirar as duplicatas, preservando o histórico Git.
Nenhuma alternativa foi aplicada. O item 5 do pedido exige parar e consultar
quando o destino não estiver evidente; a regra do AGENTS.md também proíbe
resolver divergência documental por inferência.

## Estado do trabalho

Leituras obrigatórias concluídas, incluindo históricos dos documentos revisados
no commit canônico. Nenhum arquivo funcional, documento operacional, pacote do
método ou teste foi alterado. Foram acrescentadas somente estas evidências.
Nenhum commit ou push realizado. A pasta .projectdocs/figuras/ já existia como
não rastreada e permanece intacta.

O arquivo real do manifesto é reference/metodo/manifesto.json; o pedido usa
manifest.json. Na retomada, preservar o nome efetivamente consumido pelos scripts.

## Decisão humana recebida

O engenheiro determinou retirar ambas as cópias, apontar as remissões para
reference/metodo/EMCIA-CTX-01, cobrir a retirada no teste de citações e registrar
nota de emenda na decisão 021, além de refletir o destino em map.md.
A pendência está resolvida; o trabalho prossegue conforme essa instrução.
