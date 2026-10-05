# Propostas canônicas — bloco inicial conduzido

**Data:** 05/10/2026 · **Autor:** Celso do Vale · **Estado:** proposta de revisão documental

A decisão operacional 045 foi aprovada no pedido. Estas propostas registram o que
os documentos canônicos precisam incorporar; não aprovam nova versão, não alteram
seus bytes nem conferem aprovação a minutas em revisão. Base atual: metodo-v1.0,
commit 08bfb162d762935ed35f55e0a75bc700b81d5276, APR-01.

| Documento | Alteração proposta | Limite preservado |
|---|---|---|
| EMCIA-HAB-01 | Bloco 0a–0d executável pela sessão após aprovação humana registrada; aceitação revogável sem ratificação, com situação por emissão | Tratamento administrativo prévio, carta/PDFs conferidos e assinatura como testemunho; dados operacionais após abertura |
| EMCIA-ROT-02 | Fluxo /iniciar, configuração reutilizada, cinco aprovações, aprovação da árvore incluída na abertura, conjunto de compartilhamentos, retomada e checklist | Nenhum efeito externo sem aprovação; retorno de assinatura e decisão de abrir explícitos |
| EMCIA-CAN-01 | Definir, listar e receber no bloco com testemunho; calibração por perfis embutidos/assinatura; conjunto de compartilhamentos aprovado | Escopo por id, filtro de caso, manifesto/hash e trabalho-interno sem cliente |
| EMCIA-CAT-01 | Separar execução operacional autorizada no chat das decisões de camada/procedência/método reservadas ao terminal | Nenhuma decisão determinística delegada a modelo; encerramentos EX3/EX4 humanos |
| EMCIA-MAN-01 | Descrever iniciar e testemunhos, alternativa manual, situação jurídica, executor dos atos administrativos e selo após P2 humano | F0 liberado não é encerrado; apurar-nivel e decidir-prosseguimento continuam humanos |

A25 acusa exatamente `ato humano selar-apos-P2 ausente das seções 3.3 e 3.4`.
O teste permanece inalterado, com falha conhecida restrita a essa lista e ao teste
01. Não há camada, produto ou comando de etapa alterado. Revisão do MAN-01 e
aprovação de nova linha de base pertencem ao canônico; não se cria cópia local
ajustada para silenciar a divergência. Qualquer divergência adicional é bloqueante.

## Complemento — assinaturas reais dos conectores

Proposta para EMCIA-CAN-01 e ROT-02: inventário é a fonte exclusiva de nomes e
parâmetros. Drive usa `query`, `fileId`, `parentId` e `create_file` para pasta
por `contentMimeType`; arquivo comum permanece só em entregas. `share_file`
confere pasta, destinatário e papel com aprovação. Calendar exige `calendarId`.
Tally exige `workspaceId` na criação e `formId` na publicação. Não há filtro
pelo campo oculto em `fetch_submissions`: a coleta dessa API fica recusada;
o engenheiro filtra/exporta pelo painel e a decisão/evidência ficam registradas.
Montagem do formulário e publicação sem assinatura disponível também ficam
manuais. A falta da garantia não autoriza parâmetro fictício ou filtro local
após coleta ampla. CAN-01 conserva o filtro de caso e a listagem antes da leitura.
A emenda da decisão 045 autoriza o executor e registra esse limite, sem mudar
documento controlado nem reempacotar o método.

## Complemento — habilitação simplificada (decisão 047)

| Documento | Revisão solicitada | Regra preservada |
|---|---|---|
| EMCIA-HAB-01 | Formulário permanente por tipo; CSV local filtrado antes da escrita; mensagem com rodada; condições padrão; três confirmações administrativas; matriz de 0c pré-preenchida | Três documentos APR separados, origem/hash, assinaturas conferidas, restrições e dados operacionais após abertura |
| EMCIA-ROT-02 | Link com caso; dois depósitos; revisar/gerar/liberar conjunto; assinatura por pasta; abertura/importação/validação/selo agrupados; cartão e retomada | Aprovações reais, sem inferir silêncio; decisões de método no terminal |
| EMCIA-CAN-01 | Tally/calendário na abertura; declaração/conferência reutilizável de formulários; exportação local; Drive em P2 com uma aprovação de criação/compartilhamento | API ampla recusada; ids exatos; raiz e trabalho-interno privados; P2 bloqueada sem documentos/entrada |
| EMCIA-MAN-01 | Descrever proximo, três confirmações, mensagens, dois depósitos, abertura sem Drive e preparação de P2; manter revisão canônica do selo após P2 | F0–P10, camadas, produtos, procedência e decisões de método preservados |

A25 conserva a divergência exata anterior; nenhuma nova divergência na tabela
3.3/atos 3.4. As diferenças da habilitação/abertura ficam propostas, sem editar
o pacote aprovado ou alterar hash dos templates. A decisão 047 aprova a interface
operacional; aprovação de nova linha de base documental pertence ao canônico.

## Complemento — decisão 047, item 9 (substitui limites anteriores na habilitação)

HAB-01/ROT-02/MAN-01: coleta padrão por fetch_submissions, todas as páginas
conferidas, somente uma submissão com campo oculto caso correspondente entra
no expediente; zero/múltiplas requerem indicação. CSV permanece alternativa,
com um depósito adicional. Mantêm-se mensagem, matriz e três documentos separados.
CAN-01: Tally/Drive/Calendar sem perfil/escopo por id antes da abertura; leituras,
listagens, rascunhos e comparação sem aprovação própria; publicar, enviar convite/
mensagem ou compartilhar exige ok/resumo/data. load_form sem restrição de id.
Perfil/escopo gerados e aprovados com a abertura e exigidos de F0 a P10.
Substitui a recusa de API ampla e calibração prévia propostas acima somente
nesse período administrativo. Dentro do caso, contratos de ids e procedência
permanecem; nenhuma listagem administrativa amplia permissões. Sem edição do pacote.
