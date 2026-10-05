# Resultado da revisão jurídica e templates por APR-01

Data: 05/10/2026. Responsável: Celso do Vale.

## Linha de base e escopo

Linha de base do marketplace: `148aca4c70e856d91ee32174aa852c109595826c`, campo
0.8.24. A leitura incluiu AGENTS.md, CLAUDE.md, decisões 022 e 044, o script e a
referência de habilitação. A suíte completa em Python 3.12.12 passou antes das
alterações: **975 verificações em 49 módulos**, sem exclusões ou falhas.

O checkout local de emcia-artefatos contém as minutas em revisão do ciclo 2,
commit `fb60016d1528a667e8416bbeb3211e9841fbfe43`. O pacote aprovado continua
na tag metodo-v1.0, commit `08bfb162d762935ed35f55e0a75bc700b81d5276`.
Para conferir o pacote e os templates contra sua origem aprovada, a linha de
base e a regressão completa foram executadas em checkouts temporários irmãos:
marketplace na linha de base e emcia-artefatos na tag. As minutas locais foram
preservadas. Nenhum módulo foi excluído e a comparação canônica permaneceu ativa.

Na regressão, as alterações locais foram copiadas para o checkout temporário,
incluindo código, versão, testes e fixtures, e esses arquivos foram comparados
byte a byte com o workspace. O HEAD mostrado no relatório integral é o commit
base do checkout temporário; a regressão avaliou as alterações presentes em sua
árvore de trabalho, antes dos commits finais. Os caminhos e a integridade estão
em [integridade.json](integridade.json), e as alterações em
[alteracoes.patch](alteracoes.patch).

## Testes antes da implementação

| Item | Testes novos | Resultado antes da correção | Resultado depois |
| :--- | :--- | :--- | :--- |
| 1 — resultado jurídico | 30–35: resultado ausente ou inválido; aprovado com ciclo e evidência; ciclo inválido; registros legados ou não aprovados ignorados; seleção somente de aprovado | 35 testes executados; 13 falhas e 16 erros. O contrato anterior aceitava revisão sem resultado e recusava os novos argumentos válidos | 35 testes passaram |
| 2 — resolução pelo APR-01 | 36–40: nome atual; próximo nome em base sintética; duas entradas para o código; código ausente apesar de nome e hash; resolução sem cache do APR | 40 testes executados; 8 falhas, incluindo subtestes. O nome fixo ignorava a correspondência por código | 40 testes passaram |

Saídas preservadas:

- [Item 1 antes](habilitacao-item-1-antes.txt) e [depois](habilitacao-item-1-depois.txt).
- [Item 2 antes](habilitacao-item-2-antes.txt) e [depois](habilitacao-item-2-depois.txt).

As falhas iniciais foram corrigidas no script. As fixtures positivas receberam o
novo campo obrigatório; não foi retirada nenhuma recusa nem cobertura anterior.
As negativas verificam Recusa e evento Recusado com autoria fixa, preservação do
estado e ausência de geração de PDF. Somente o renderizador é substituído nos
testes unitários; validações, hashes e operação de revisão são reais.

## Comportamento entregue

- `revisao-juridica` exige a string literal `resultado: "aprovado"`. Campo ausente,
  condição, reprovação, texto livre e outras grafias recusam. Não há dispensa.
- `ciclo` é opcional e, quando presente, texto não vazio. Resultado, ciclo, hashes
  e evidência ficam preservados na revisão e na entrada do evento registrado.
- `gerar` seleciona somente revisão aprovada que cubra o hash exato. Registros
  anteriores sem resultado permanecem, sem liberar nova geração ou serem
  completados por inferência. A emissão conserva a revisão aprovada selecionada.
- TEMPLATES conserva a interface de mapeamento, com códigos estáveis e nomes
  resolvidos pela tabela do APR-01, sem cache ou nomes fixos. Revisão e geração
  usam uma leitura do registro por operação, com código, caminho e hash.
- Cada código HAB-01/02/03 deve ter exatamente um arquivo aprovado. Zero ou duas
  entradas recusam antes de qualquer PDF, mesmo que o nome e o hash antigos
  ainda estejam na tabela associados a outro código.
- O leitor aceita uma única linha de base declarada pelo registro, sem fixar
  metodo-v1.0. A interface aprovacoes conserva o argumento explícito da linha de
  base, usado pelo teste do pacote para conferir a tag do manifesto.

`testes/apoio/templates-hab-v1/` permanece com os bytes aprovados da tag.
`testes/apoio/templates-hab-proxima-base/` contém três templates e um APR-01
exclusivamente sintéticos em metodo-v1.1, com o novo nome de HAB-03. Essa fixture
não aprova documentos reais, não usa as minutas locais e não integra o pacote.

O resultado é declaração do ato humano, conferida deterministicamente. O script
não interpreta o PDF, autentica o revisor ou julga mérito jurídico. Um parecer
condicionado deve permanecer no registro documental dos ciclos, aguardando
ratificação sem condição; declarar aprovado em desacordo com a evidência continua
sendo responsabilidade humana, nos limites da decisão 022.

## Regressão completa

| Conferência | Linha de base | Final |
| :--- | :--- | :--- |
| Python | 3.12.12 | 3.12.12 |
| Verificações | 975 | 986 |
| Módulos | 49 | 49 |
| Módulos com falha | 0 | 0 |
| Exclusões | Nenhuma | Nenhuma |
| habilitacao.py | 29 | 40 |
| habilitacao_0d.py | 35 | 35 |
| metodo_empacotado.py | 8 | 8 |
| manual_a25.py | 5 | 5 |
| catalogo_cat01.py | 11 | 11 |
| citacoes.py | 8 | 8 |

Saídas integrais: [linha de base](suite-inicial-python312.txt) e
[regressão final](suite-final-python312.txt).

Para repetir com checkout canônico irmão na tag aprovada:

```bash
PATH=/caminho/python312/bin:$PATH PYTHONDONTWRITEBYTECODE=1 python3 \
  .projectdocs/evidencias/revisao-juridica-resultado/reexecutar-suite.py /tmp/emcia-suite.txt
```

O executador descobre negativos.sh e todos os módulos Python na raiz de testes;
exige Python 3.12 e não admite exclusões. O checkout canônico de teste deve estar
na tag declarada no manifesto, pois o teste compara os templates efetivamente
disponíveis naquele checkout aos hashes aprovados.

Campo incrementado para **0.8.25**. Os 22 documentos do método e seu manifesto,
23 arquivos, permanecem byte a byte como na linha de base; núcleo e playbook
também permanecem intactos. Não houve reempacotamento ou alteração do canônico.
Documentação atualizada e nota de emenda adicionada à decisão 044. Um commit por
item; nenhum push nesta tarefa.
