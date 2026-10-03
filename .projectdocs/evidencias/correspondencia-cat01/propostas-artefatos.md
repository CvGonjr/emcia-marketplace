# Proposta de correção canônica — MAN-01 e produto de F0

**Resolvida por decisão humana em 03/10/2026.** O engenheiro aprovou a
expressão **Decisão de prosseguimento registrada**, abrangendo os dois
desfechos. `não prosseguir` encerra F0 e bloqueia as etapas seguintes.
A alteração canônica limita-se à célula, versão 0.4 e histórico;
commit `989e1e73796a356b660be8ed55b686ba716787ac`. A pré-validação antes
do commit retornou `[]`; saída em `correcao-manual-precommit.json`.
O texto abaixo preserva a proposta anterior, cuja expressão sugerida foi
substituída pela redação aprovada. A decisão 043 registra a resolução.

Data: 2026-10-03. Autor: Celso do Vale. Estado: proposta para decisão humana.

Fonte canônica examinada: emcia-artefatos, commit
`2cf4ebd913b7a4de2ca7f5a2322a991bc69c1cbe`, MAN-01 v0.3, CAT-01 v0.5.
Marketplace de referência: `ebb6bbda55ea7403bc0e09a0bc316f0a1071cf4f`,
playbook 0.4.18. Nenhum documento canônico foi alterado.

## Divergência que interrompe a implementação

A tabela 3.3 do MAN-01 v0.3 declara `decidir-prosseguimento` como ato humano
de F0, mas mantém `—` na coluna “Produto conferido pelo Estúdio”. O pedido
de implementação exige esse registro como condição de encerramento de F0
pelo mecanismo genérico de produtos. Esse mecanismo lê
`produtos_encerramento`; o A25 compara sua descrição com a célula do manual.

A pré-validação usa a função original `conferir()` de `testes/manual_a25.py`
e o manual extraído diretamente do commit canônico. Foram comparados três
contratos, sem gravação do playbook:

| Contrato | Resultado de conferir() |
|---|---|
| Playbook atual 0.4.18 | `["F0: ato decidir-prosseguimento não declarado"]` |
| Cópia em memória com o ato declarado, sem produto | `[]` |
| Cópia em memória com ato e produto obrigatório de F0 | `["F0: produto diferente da descrição do playbook"]` |

A terceira comparação demonstra a incompatibilidade entre os requisitos
do pedido e a tabela canônica. Não é uma falha de um playbook já implementado:
a implementação foi interrompida antes de alterar arquivos operacionais.
O item 3.2 do pedido determina: “Se não retornar, pare: o erro está no
documento canônico.” Não se modifica o A25 nem se usa descrição `—` para
ocultar um produto obrigatório.

## Correção proposta para o canônico

Na linha F0 da tabela 3.3 do MAN-01, substituir o produto `—` por
**Decisão de prosseguir registrada**. Essa expressão será reproduzida
literalmente em `descricao` do produto de encerramento do novo playbook.

Preservar em 3.4 a decisão baseada na ficha de enquadramento preparada,
anterior à emissão formal de E1, com pessoa nomeada e execução no terminal
humano. Registrar no histórico a correção da célula e sua relação com o
produto obrigatório. A nova revisão e o commit canônico deverão ser
identificados antes do reempacotamento; não há emenda local ao pacote.

O contrato operacional deverá aceitar somente a decisão vigente com desfecho
`prosseguir` para o encerramento. Um desfecho `não prosseguir` deve bloquear
o avanço até nova decisão, preservando o histórico. Isso permanece requisito
de implementação; a pré-validação documental não comprova essas travas.

## Divergência anterior preservada

CAT-01 v0.5 Anexo D.3 já registra HB-16 como automatizada no Anexo A e
como híbrida em CAM-01 §3.4. Essa natureza não foi rediscutida nem alterada.
O catálogo deverá reproduzir o Anexo A conforme o pedido.
