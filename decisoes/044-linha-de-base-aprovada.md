# 044 — Linha de base aprovada e geração da habilitação

**Data:** 04/10/2026 · **Estado:** firme por instrução do engenheiro

## Contexto

Celso do Vale aprovou a primeira linha de base documental em 03/10/2026,
conforme EMCIA-APR-01. A tag anotada publicada `metodo-v1.0` de emcia-artefatos
resolve para `08bfb162d762935ed35f55e0a75bc700b81d5276`. O APR-01 registra
13 documentos controlados em v1.0, cinco modelos E1–E5 em v0.1 e três templates
HAB em v0.2, com SHA-256. O hash do próprio registro fica fora de sua tabela.

Os templates HAB aprovados possuem controle e histórico internos e, em HAB-02
e HAB-03, aviso de revisão jurídica. A geração anterior os copiava para o cliente
e procurava um metadado Template que já não existia, deixando de indicar o estado
da emissão. Os templates aprovados não podem ser editados para corrigir a saída.

## Decisão

1. Caso real utiliza somente pacote de linha de base aprovada. Documento em
   revisão ou fora do APR-01 não entra no caso real. Alteração posterior exige
   revisão documental, nova aprovação do responsável e nova tag metodo-vX.Y
   antes do uso real. Aprovação é ato humano e não pode ser delegada.
2. O manifesto v6 mantém o nome operacional `manifesto.json`, cita tag e commit,
   declara linha_de_base e fixa caminhos e hashes. O pacote é extraído dos objetos
   Git da tag: 21 arquivos aprovados e APR-01, 22 documentos no total. ESP-01,
   VER-01 e o fluxo auxiliar, excluídos pelo APR-01, são retirados do pacote;
   seu histórico permanece no canônico e no Git do marketplace.
3. Modelos e templates são conferidos por hash no APR-01, sem inferir aprovação
   de metadados internos. Os templates HAB empacotados e os do checkout canônico
   usado para geração precisam ter os hashes aprovados. A suíte confere a tag,
   os bytes Git, o manifesto e o registro, incluindo negativa com APR-01 alterado
   e manifesto coerente. O CI obtém o checkout canônico pela tag publicada.
4. O template original e seu hash são preservados no expediente. A geração
   retira deterministicamente a seção Controle do modelo até a seção seguinte,
   os blocos de citação iniciados por Revisão jurídica e o histórico de revisões
   do modelo. Identificação do caso, cláusulas e controle de assinatura permanecem.
   O rodapé indica Estado de emissão: Para assinatura. Marcas esperadas ausentes
   ou duplicadas recusam com motivo. Markdown e PDF emitidos têm hashes próprios.
5. `revisao-juridica` é ato humano anterior à geração de HAB-02 e HAB-03.
   Registra revisor e decisor nomeados, data, documentos com hashes exatos de
   templates aprovados e evidência importada com SHA-256. Registros anteriores
   permanecem; cada emissão conserva a revisão que cobre seu template. Sem
   cobertura exata para ambos, `gerar` recusa antes de qualquer PDF e informa a
   operação faltante. Não há flag de dispensa. A revisão precisa estar registrada
   antes do primeiro cliente; aprovação documental não substitui revisão jurídica.

## Relação com decisões anteriores

A 044 supera somente as declarações de aprovação documental pendente nas
decisões 026, 038 e 043: elas descrevem seus commits e versões históricos.
A correspondência e os atos da 043 permanecem. A 022 recebe a pré-condição
jurídica e a separação entre modelo interno e emissão ao cliente. A 002 continua
fixando playbook e método copiados no caso; nenhum caso existente é migrado
automaticamente. A 009 continua impedindo reprodução do método em habilidades.

## Consequência e verificação

Campo 0.8.24, núcleo 0.2.45, playbook 0.4.19 e manifesto v6. Não há regra
de aprovação ou de habilitação acrescentada ao núcleo. O expediente conserva
sua autoria fixa e a fronteira local de confiança da 022; o registro jurídico
testemunha o ato, sem autenticar identidade ou qualificação nem julgar mérito
jurídico por modelo de linguagem.

Testes negativos precederam a correção. A evidência em
`.projectdocs/evidencias/linha-de-base-v1/` contém a linha de base completa em
Python 3.12, regressão final, conferência de tag/bytes/hashes e exemplos reais
de PDFs com dados e revisão jurídica exclusivamente sintéticos, antes e depois.

## Nota de emenda — resultado jurídico e resolução dos templates, 05/10/2026

Por instrução do engenheiro, `revisao-juridica` exige o campo `resultado`, cujo
único valor aceito é a string exata `aprovado`. O campo `ciclo` é texto opcional
para identificar o ciclo. Parecer condicionado ou reprovado não é registrado
como revisão autorizadora no expediente; uma tentativa inválida produz evento
`Recusado`, com o mesmo tipo de erro das demais validações. Não há dispensa.

`gerar` seleciona somente revisões com resultado `aprovado` e cobertura do hash
exato. Registros anteriores sem resultado permanecem no histórico e não liberam
nova geração. É necessário registrar o ato e sua evidência sem inferir ou completar
o resultado de uma revisão legada. Uma revisão não aprovada não substitui a
revisão aprovada usada pela emissão.

Os arquivos de HAB-01, HAB-02 e HAB-03 passam a ser localizados pelo código na
tabela do APR-01 do pacote. Cada código exige exatamente um arquivo aprovado;
ausência ou ambiguidade recusa revisão e geração antes de produzir PDF. Os hashes
continuam sendo conferidos contra a mesma tabela. A resolução é feita na operação,
sem congelar nomes na importação do módulo, e aceita a linha de base declarada no
registro, sem fixar metodo-v1.0 no script. A conferência do pacote continua exigindo
que o APR-01 corresponda à tag declarada em seu manifesto.

Campo 0.8.25; núcleo 0.2.45 e playbook 0.4.19 permanecem. Não há reempacotamento,
alteração de documento canônico nem liberação das minutas do ciclo 2. A próxima
linha de base aprovada poderá declarar o novo nome de HAB-03 sem nova alteração
do script; a fixture metodo-v1.1 é exclusivamente sintética e não aprova documento
real. A emenda conserva a fronteira de confiança da 022: o resultado é declarado
pelo responsável humano, o script não interpreta o parecer nem autentica seu mérito.

Testes de recusa precederam as implementações dos dois itens. Linha de base,
falhas iniciais, regressão e conferências estão em
`.projectdocs/evidencias/revisao-juridica-resultado/`.
