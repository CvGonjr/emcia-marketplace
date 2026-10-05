# 047 — Habilitação simplificada e abertura sem Drive

**Data:** 05/10/2026 · **Autor:** Celso do Vale · **Estado:** firme por instrução do engenheiro

## Contexto

O engenheiro aprovou simplificar os atos administrativos anteriores ao percurso:
cliente responde um formulário permanente e assina três documentos separados;
engenheiro envia o link, deposita uma exportação e os PDFs assinados e confirma
três conjuntos de atos. Esta decisão emenda a 045. F0 a P10, decisões de método,
camadas, procedência e autoria nominal conservam suas regras.

## Decisão

1. Um formulário Tally permanente por tipo fica em `~/.emcia/config.json`, com
   formId, versão/hash do contrato, data e hash do relatório conferido. O link
   acrescenta `?caso=<caso>`. Alteração do contrato ou nova leitura do formulário
   invalida a conferência até novo relatório sem divergência e “conferido”.
2. O engenheiro deposita o CSV em `~/emcia-op/entrada/`. A leitura local filtra
   pelo caso reservado antes de qualquer persistência. Preserva somente linhas
   desse caso, hash do filtrado e hash do original, sem copiar o original.
   Zero ou várias submissões aguardam indicação humana; não há escolha automática.
   A fonte usa `tally-exportacao`. A API ampla continua recusada.
3. Lacunas geram perguntas; resposta colada vira fonte `manual`, com rodada,
   sem exigir formulário novo ou operações pendencia/resolver/reabrir. Essas
   operações permanecem na alternativa manual.
4. As condições administrativas configuradas são aplicadas automaticamente,
   com referência e hash. Só condição diferente exige esclarecimento específico.
5. Três confirmações, sem frase obrigatória, conservam resumo, trecho literal,
   data, pessoa e hashes: revisão conjunta dos três documentos, cobrindo revisar/
   gerar/liberar; conferência dos três PDFs assinados e evidências; abertura,
   importação, validação de 00-habilitacao e selo. Silêncio não é aprovação.
6. A matriz deriva das respostas 0c e é apresentada para confirmar/corrigir em
   mensagem; restrições conservam o mecanismo vigente. Não se presume acesso
   concedido, disponibilidade ou agenda a partir de resposta ambígua.
7. A abertura declara Tally e calendário, sem pastas Drive. O provisionamento
   ocorre em P2, com aprovação da criação e compartilhamento. P2 continua
   bloqueada sem os canais que exige; nenhum caso existente migra automaticamente.
8. `/eiac-campo:iniciar` carrega somente o cartão operacional de uma página e
   usa `iniciar.py proximo`: uma chamada por avanço, saída curta, retomada pelo
   estado e parada na próxima informação ou aprovação humana necessária.

## Limites e documentação

APR-01 continua resolvendo os três templates por código e hash. Não há edição
ou reempacotamento do método. Ratificação/aceitação revogável seguem a 045.
A configuração inicial do ambiente, conferência dos formulários, perfil e
situação jurídica são preparação reutilizável, fora das três confirmações por
caso. Compartilhamento em P2 é aprovação posterior, fora da abertura.

A conferência de PDF e assinatura continua testemunho humano, sem autenticação
criptográfica. Hash fixa bytes, não identidade nem mérito. Decidir-prosseguimento,
apuração de nível, sessões e demais decisões de método continuam no terminal.
F0 liberado não significa F0 encerrado. Nenhuma mensagem é enviada automaticamente.

Mudanças de HAB-01, ROT-02, CAN-01 e MAN-01 são propostas no arquivo correspondente.
A25 conserva exatamente a falha conhecida da 045:
`ato humano selar-apos-P2 ausente das seções 3.3 e 3.4`, em test_01; quatro
negativas passam. A lista exata é conferida, sem ocultar saída do teste.
Qualquer divergência nova interrompe a regressão e os commits.

## Verificação

Linha de base no commit 70702c6: 1109 verificações em 53 módulos em Python
3.12.12; 1111 em 3.14.4. Uma falha conhecida A25, zero falhas inesperadas.
As duas verificações adicionais correspondem à disponibilidade de PyYAML.
Evidência: `.projectdocs/evidencias/habilitacao-simplificada/`.

### Entrega e conferência final

Campo 0.8.30 e playbook 0.4.22; núcleo 0.2.48 intacto. O template exige triagem
e calendário em F0, sem Drive; documentos/entrada continua exigido em P2.
Canônicos/manifesto/APR e templates permanecem byte a byte, sem reempacotamento.

Percurso sintético: três confirmações com literal ok, dois depósitos, uma rodada
por mensagem e sete chamadas públicas proximo até F0 liberado. A fixture anterior
modela 93 chamadas públicas (aprovar/executar/retomar/retorno), cinco grupos de
aprovação e uma conferência de formulário por caso, excluindo perfil/aceitação
reutilizáveis. São operações da fixture, não medição do runtime Claude.

P2 usa seis criações e quatro compartilhamentos com uma aprovação posterior;
raiz e trabalho-interno permanecem privados. Não compartilha a raiz para evitar
herança de acesso ao trabalho-interno. A associação automática do PDF assinado
exige texto integral do enviado; Poppler/pdftotext é necessário. PDF sem texto
ou cuja organização pelo painel impeça essa comparação usa a alternativa manual.
A confirmação humana e o caráter de testemunho continuam, sem autenticar assinatura.

Regressão integral: 1140 verificações/54 módulos em Python 3.12.12 e 1142/54
em 3.14.4, uma falha conhecida A25, zero inesperadas. PyYAML explica a diferença.
Depois da regressão, o negativo de campos extras no payload da coleta reproduziu
um risco de preservar entrada ignorada no histórico; a operação passou a recusá-los
antes da persistência. Os 31 específicos passaram nas duas versões após a correção.
Isso impede que um lote de outros casos seja anexado ao payload da coleta.

Navegador e retornos MCP são substituídos por fixtures sintéticas no percurso;
nenhuma conta real foi acessada. Configuração opcional pode ser completada pela
operação configurar, sem trocar responsável ou bases fixados. Modelos, minutas,
habilidades e decisões de método conservam seus contratos. Retomada é idempotente
nos atos confirmados; API com retorno perdido ainda exige conferência remota.

## Emenda — item 9: conectores administrativos antes da abertura

**Data:** 05/10/2026 · **Autor:** Celso do Vale · **Origem:** instrução expressa do engenheiro.

Esta emenda substitui, no período anterior à abertura, a exigência de perfil e
escopo por id e a recusa de fetch_submissions dos itens 1–2 e da preparação
reutilizável. A habilitação usa Tally, Google Drive e Google Calendar sem
calibração, sem escopo por id e sem aprovação por leitura, listagem, rascunho
ou comparação. A seleção do modelo, os hashes e a confirmação “conferido” do
formulário permanente conservam seu contrato; load_form admite qualquer formId.

Publicar formulário, enviar mensagem/convite ou compartilhar arquivo exige
confirmação simples (“ok”), com resumo, data, autor e chamada fixada. Sem
confirmação, o hook recusa com TentativaNegada. Publicação também exige comparação
vigente sem divergências e “conferido”. O script registra a autorização; a sessão
executa o conector, sem envio automático por parte do script.

A coleta padrão lê fetch_submissions. O script confere todas as páginas, reconhece
o campo oculto caso e grava somente uma submissão do caso reservado, com hash.
Zero ou várias submissões exigem indicação do engenheiro; seleção de id de outro
caso recusa. O lote não entra em mcp-retornos, fonte, evento ou diagnóstico.
O temporário administrativo de leitura é removido inclusive na recusa. A exportação
CSV filtrada permanece alternativa manual, com coleta: csv.

O perfil é calibrado a partir do inventário na preparação da abertura; relatório,
inventário/hash e ids dos canais são apresentados ao engenheiro e incluídos na
terceira confirmação. Na abertura, o script instala o perfil aprovado no caso.
A existência do caso encerra a autorização administrativa: F0–P10 conservam
perfil, escopo por id, listagem prévia, aprovação dos efeitos e negativas vigentes.
Retornos de listagens administrativas não ampliam ids permitidos dentro do caso.
Não existe flag para desativar a guarda, nem mudança no núcleo ou no playbook.
Drive administrativo pode criar rascunhos antes da abertura; os canais e pastas
do caso continuam provisionados em P2, com o contrato existente.

Campo 0.8.31. Evidência do item 9 em
`.projectdocs/evidencias/habilitacao-simplificada/item-9/`.
A divergência A25 já registrada permanece visível; nenhuma revisão do pacote.

### Verificação do item 9

Linha de base: 1140/54 em Python 3.12.12 e 1142/54 em 3.14.4. Final: 1154/55 e
1156/55 respectivamente, sem exclusões, somente A25 conhecida e zero inesperadas.
Os 14 testes novos cobrem a fronteira administrativa, filtragem/paginação e caso
aberto; as negativas anteriores de ids continuam no caso pelo hook real. O caminho
manual também instala o perfil na abertura, com hash incluído na aprovação.
Percurso padrão sintético: três confirmações, um depósito, sete avanços proximo
e um registro de coleta direta. MCP e PDFs do percurso são simulados; nenhuma conta
real foi acessada. Cartão renderizado pelo Chrome em uma página A4. Núcleo,
playbook e documentos/templates do pacote permanecem sem alterações.

## Emenda — recebimento sem movimentação para a entrada

**Data:** 05/10/2026 · **Autor:** Celso do Vale · **Origem:** instrução expressa do engenheiro.

Esta emenda substitui a obrigatoriedade dos depósitos dos itens 2 e 5 no
percurso normal. A coleta Tally direta permanece padrão. A sessão recebe os
PDFs assinados pelo Drive ou por caminhos locais originais; não pede ao
engenheiro exportação ou movimentação para a pasta de entrada. Para o Drive,
usa download_file_content com fileId e entrega os bytes exatos baixados em
temporário externo ao script, preservando o documento assinado. O script
continua sem executar APIs; a sessão prepara as entradas técnicas.

proximo e preparar-assinaturas aceitam assinados (lista dos três caminhos) e
evidencias (mapa opcional por código HAB). A associação continua pelo conteúdo
integral enviado, com hashes do enviado, recebido e comprovante, e confirmação
humana do conjunto. Nomes e pastas podem variar. CSV manual aceita o caminho
original em exportacao. Symlinks, repositórios e casos não são locais de entrada.
Caminho explícito inválido recusa com evento, sem substituir por arquivo da
pasta de entrada. Esta permanece alternativa para instalações existentes.
Depois da importação, a sessão remove somente os temporários que criou.

Não há novo efeito externo, aprovação por download, alteração de assinatura,
dispensa de conferência ou mudança de perfil após a abertura. Núcleo, playbook
e pacote canônico permanecem intactos. Campo 0.8.32. Evidência em
`.projectdocs/evidencias/recebimento-sem-deposito/`.

Recebimento sem depósito: regressão integral 1158/55 em Python 3.12.12 e
1160/55 em 3.14.4, somente A25 conhecida e zero inesperadas. Percurso sintético
com coleta direta, três confirmações e zero depósitos na entrada. Evidência em
`.projectdocs/evidencias/recebimento-sem-deposito/`.
