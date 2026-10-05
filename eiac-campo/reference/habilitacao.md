# Interface do expediente de habilitação

Procedimento: EMCIA-HAB-01 §3.3.4 e §3.4, EMCIA-CAN-01 e
`auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md` §3.6, na tag canônica
da linha de base e no commit fixados em `reference/metodo/manifesto.json`
(atualmente `metodo-v1.0`).
O pacote contém cópias exatas; `caminhos_canonicos` identifica os auxiliares
e sua origem. `EMCIA-APR-01-registro-de-aprovacoes.md` registra a aprovação
por hash dos modelos e templates. Metadado interno do template não substitui
o hash aprovado. Documento fora desse registro não rege caso real.
Esta referência descreve a interface técnica, sem substituir o procedimento.

## Fluxo simplificado

Use `/eiac-campo:iniciar` e `reference/cartao-habilitacao.md`. A decisão 047 emenda
as operações administrativas da 045. `iniciar.py proximo --entrada <json-local>`
executa os atos automáticos e para na próxima informação ou aprovação necessária.
Uma chamada por avanço; saída contém resumo, próximo passo e artefatos pertinentes,
sem o estado inteiro. A retomada confere hashes e não repete atos já registrados.

O percurso nominal tem três confirmações: revisão conjunta dos três documentos
(inclui qualificação, revisar/gerar/liberar); conferência dos PDFs assinados e
suas evidências; abertura/importação/validação/selo. “ok” é suficiente quando
aprova o conjunto apresentado. O registro conserva o trecho real, resumo, data,
pessoa e hashes; não autentica chat nem assinatura. Mudança exige nova conferência.
Criar expediente, aplicar condições padrão e receber respostas não têm aprovação
própria. Decisões de método continuam no terminal.

### Preparação reutilizável

A configuração exige responsavel, base_casos, base_expedientes, workspace_tally,
calendario_casos e navegador. pasta_drive é opcional até P2. entrada_dir é opcional
para instalações com outra pasta administrativa; padrão `~/emcia-op/entrada/`.
A pasta de entrada é alternativa; arquivos indicados por caminho original não
precisam ser movidos. A sessão recebe pelo conector quando disponível.
As bases/pasta de entrada devem ser externas aos repositórios. Não coloque caso
ou dado de cliente na ferramenta. Tratamento padrão é:

```json
{"tratamento_administrativo":{"condicoes":"Texto das condições administrativas comunicadas","provedor":"Ambiente autorizado"}}
```

`tratamento-padrao` aplica o texto antes da coleta, com referência à configuração,
SHA-256 e cópia só das condições. Condição diferente usa a operação `tratamento`
a seguir, com evidência e indicação explícita do engenheiro. Não altera HAB-03.
Ratificação ou aceitação revogável seguem a 045. Perfil/escopo são gerados e aprovados na abertura, pela emenda do item 9 da 047.

`formulario-permanente` em `iniciar.py executar`, após comparação sem divergências
e `confirmar-formulario`, declara modelo e formulario_id. A configuração guarda
`formularios_permanentes: tipo → {formId, versao_contrato, contrato_sha256,
data_conferencia, relatorio_sha256, relatorio, workspace_id, responsavel,
habilitacao, caso}`. Modelo sem versão usa `sha256:<hash>` como versão do contrato.
Na abertura também se exige formulário permanente de triagem, sem mudar F0.
Uma nova leitura ou alteração do contrato invalida a conferência; coleta recusa
até novo relatório e “conferido”. Não recrie formulário por cliente.

### Coleta direta e esclarecimentos

Na habilitação, Tally, Drive e Calendar não exigem perfil nem escopo por id.
Leitura, listagem, rascunho e comparação não pedem aprovação própria.
load_form admite qualquer formId; conferir-formulario executa sem --aprovacao.
Confirmação humana “conferido”, integridade e comparação do permanente permanecem.
Publicar, enviar mensagem/convite ou compartilhar pede “ok” com resumo/data:
use iniciar.py aprovar para operacao mcp e preserve a chamada no testemunho.
Sem esse registro, o hook recusa.

proximo indica coletar-submissoes e formId. Execute fetch_submissions e passe
o retorno completo ao iniciar.py retorno, sem transcrever respostas na conversa.
Entrada: chamada {habilitacao, caso, ferramenta, argumentos} e resultado
{resposta: <JSON real>}. fonte opcional fica na chamada (padrão S1); submissao
seleciona um id entre as submissões daquele caso; respondente informa a pessoa
quando o retorno não a identifica. Esses campos locais não são enviados à API.
O campo oculto caso precisa coincidir exatamente com caso_reservado. Um campo
visível de mesmo nome não serve. Zero/várias respostas recusam e pedem indicação,
mostrando somente ids do caso. O lote nunca entra em mcp-retornos ou no expediente;
o temporário do script é removido inclusive na recusa. Fonte tally conserva
CSV somente da submissão escolhida, hash do filtrado e hash do retorno original.

O adaptador lê o [formato público de submissões Tally](https://developers.tally.so/api-reference/endpoint/forms/submissions/list):
questions com id/title/type e submissions.responses com questionId/answer; também
aceita responses/fields com label/type e hiddenFields.caso. Preserve metadados
que demonstram que caso é oculto. Campos/formato ambíguos não são aproximados.
Leia todas as páginas: para várias, resposta.paginas contém páginas completas
em ordem, desde a primeira; hasMore precisa ser true nas anteriores e false
na última. Aceita também pagination.page/totalPages explícitos. Página incompleta
não registra fonte; não invente a indicação de última página.

### Exportação manual

O engenheiro envia o link `https://tally.so/r/<formId>?caso=<caso>`.
Como alternativa manual, coleta: csv em proximo solicita o CSV exportado. A entrada
opcional `exportacao` indica o caminho original, em qualquer pasta externa a
repositórios e casos, sem symlinks. Sem caminho explícito, continua a busca na
pasta de entrada. CSV UTF-8 exige cabeçalho único, `caso`, `Submission ID` e `Respondente`;
`coluna_submissao`/`coluna_respondente` declaram os nomes reais se forem diferentes,
e `respondente` pode indicar nominalmente quem respondeu. Não adivinhe colunas.
`formId`/`workspaceId`, se presentes, precisam coincidir com a configuração.
O script filtra pelo valor exato de `caso` antes de gravar; nunca copia o original.
Fonte `tally-exportacao` conserva apenas o CSV filtrado, seu hash e hash do original.
Zero ou múltiplas submissões recusam e pedem indicação, listando somente ids do caso; `submissao` seleciona uma
das linhas daquele caso. No caso já aberto, fetch_submissions conserva a recusa
do perfil por falta de filtro remoto; a exceção administrativa terminou.

As lacunas são apresentadas; o comando redige a pergunta e o engenheiro cola a
resposta do cliente. `mensagem` contém `id`, `pergunta`, `texto`, `respondente` e,
opcionalmente, `origem`. Vira fonte manual com rodada posterior e literal intacto.
Não exige formulário, pendencia/resolver/reabrir; esses comandos continuam abaixo.
Informe `campos` com valor e fonte; consolidação recusa campo sem fonte.
Não presuma resposta, qualificação, competência ou acesso pela ausência de texto.

### Entradas das três confirmações

Toda entrada de `proximo` identifica `habilitacao` e `caso`.
Na preparação da abertura, inventario indica o arquivo fornecido (padrão
~/emcia-op/ensaio/inventario-mcp.json). O script gera a proposta de perfil e
apresenta arquivo/hash e ids dos canais junto do desfecho. A terceira confirmação
aprova esse perfil/escopo e a abertura; só então o perfil é instalado no caso.
A partir da existência do caso, a guarda e o escopo por id valem de F0 a P10.
Listagens administrativas anteriores não dão acesso a ids dentro do caso. A sessão prepara os
campos/plano a partir das fontes e apresenta os documentos ao engenheiro:

```json
{"habilitacao":"HAB-0001","caso":"caso-0001","plano_documentos":{"qualificacao_0a":true,"conteudo_conferido":true,"liberacao":{"ferramenta":"Painel escolhido","operador":"Nome Cliente","signatarios":[{"nome":"Nome Cliente","papel":"organizacao","competencia":"Representante autorizado"},{"nome":"Nome Engenheiro","papel":"emcia","competencia":"Responsável EMCIA"}]}}}
```

O componente gera preparações, sem revisão humana presumida. `preparar-documentos`
não libera emissão; a primeira confirmação incorpora revisar, gerar e liberar.
A emissão reutiliza exatamente os PDFs apresentados, com templates resolvidos
pelo APR-01, sem controle interno ou aviso jurídico no documento do cliente.

```json
{"habilitacao":"HAB-0001","caso":"caso-0001","aprovacao":{"ponto":"documentos","confirmado":true,"trecho":"ok"}}
```

Depois do recebimento dos assinados, `plano_assinaturas` indica referência e signatários
com nome, papel e data real; pode ser lista comum ou mapa por HAB-01/02/03.
`preparar-assinaturas` associa por texto integral extraído dos PDFs enviados,
com espaços de paginação normalizados; o assinado deve preservar esse texto.
O recebimento aceita `assinados`: lista dos três caminhos locais originais ou
baixados pela sessão. `evidencias` é um mapa opcional de código HAB para o caminho
do comprovante; nomes e pastas podem ser diferentes. Os arquivos precisam estar
fora de repositórios e casos, sem symlinks. O script importa cópias com hashes,
preservando os originais. Não é preciso mover arquivos para a pasta de entrada.

Para o Drive, a sessão usa `mcp__claude_ai_Google_Drive__download_file_content`
com `fileId`, salva os bytes exatos retornados em temporário administrativo e
entrega os caminhos ao script. Não há download/exportação manual pelo engenheiro
nem nova aprovação para essa leitura anterior ao caso. Depois da importação
bem-sucedida, a sessão remove somente seus temporários. Não converta ou reconstrua
PDF assinado; leitura de texto não substitui o download do arquivo original.

```json
{"habilitacao":"HAB-0001","caso":"caso-0001","assinados":["/pasta-de-trabalho/retorno-1.pdf","/outra-pasta/retorno-2.pdf","/outra-pasta/retorno-3.pdf"],"evidencias":{"HAB-02":"/pasta-de-trabalho/comprovante.pdf"}}
```

Sem `assinados`, permanece a busca automática na pasta de entrada. Um caminho
explícito inválido recusa; não usa arquivos da entrada para substituí-lo.
Exige Poppler/pdftotext. PDF de outro caso, conteúdo alterado, duplicata ou ausência
recusa. PDFs sem texto ou com reorganização pelo painel usam o registro manual,
com conferência humana; não há flag para ignorar divergência. Relatórios opcionais
usam `HAB-01-relatorio.pdf` etc. na busca pela entrada; com caminhos explícitos,
use `evidencias`. Sem relatório separado, o próprio PDF é evidência.
Comparação não autentica assinaturas nem certificados. A confirmação `assinaturas`
registra os três retornos com hash enviado/assinado, evidências, nomes e datas.

`planejar-acessos` pré-preenche literalmente as respostas de 0c (colunas com ids
ou perguntas exatas do contrato). Não presume concessão. `acessos` em `proximo`
recebe `{confirmado: true, trecho: <mensagem real>, matriz: <entrada acessos abaixo>}`;
a mensagem confirma/corrige patrocinador, executor, sessão, itens e restrições.
A terceira confirmação usa `ponto: abertura` e cobre abrir, declarar Tally/calendário,
importar, validar 00-habilitacao e selar. Drive aguarda P2 e aprovação posterior.

Os comandos manuais permanecem alternativas e conservam suas travas específicas.

## Inicialização manual alternativa

Como alternativa ao comando conduzido, no terminal do engenheiro:

```bash
python3 /caminho/eiac-campo/scripts/habilitacao.py iniciar \
  --expediente "$HOME/habilitacoes/HAB-0001" \
  --id HAB-0001 --caso caso-0001 --responsavel "Nome Sobrenome"
```

A pasta deve ser nova e estar fora de qualquer repositório/caso. O identificador
reservado não significa abertura do caso. A autoria é fixada nesta inicialização;
as operações posteriores não aceitam substituição. Dados ficam no expediente,
nunca neste repositório. O script usa somente a biblioteca padrão Python; a geração
de PDF requer Google Chrome ou Chromium instalado, indicado por `navegador`.

O script não autentica pessoas nem protege contra adulteração por um usuário com
acesso de escrita ao disco. Atribui registros ao responsável fixado e registra o
ator comunicado para decisões humanas, seguindo a separação da decisão 019.
Conferência de assinatura é testemunho registrado; não valida certificados.

## Invocação

```bash
python3 /caminho/eiac-campo/scripts/habilitacao.py OPERACAO \
  --expediente "$HOME/habilitacoes/HAB-0001" --entrada /pasta-de-trabalho/entrada.json
```

`estado`, `concluir-0b` e `preparar-0d` usam objeto vazio e dispensam `--entrada`.
As entradas são JSON UTF-8. Exemplos abaixo são sintéticos e devem ser preenchidos
com dados reais pelo engenheiro; caminhos de arquivos precisam existir.

## Condições administrativas antes da consulta MCP

Operação `tratamento`, antes de receber qualquer fonte:

```json
{
  "escopo": "administrativo",
  "condicoes": "Finalidade, categorias de dados, acesso, retenção e condições comunicadas para a habilitação",
  "provedor": "Ambiente de IA autorizado para esta finalidade",
  "decisor": "Nome Sobrenome",
  "evidencia": "/pasta-de-trabalho/condicoes-registradas.pdf"
}
```

O registro refere-se ao tratamento administrativo anterior ao caso; não substitui
HAB-03 nem autoriza dados operacionais. O script confere sua presença e escopo,
não interpreta juridicamente nem classifica automaticamente o conteúdo recebido.

## Respostas e rodadas

`receber` preserva uma cópia do arquivo e seu hash; recusa pares
`formulario`/`submissao` duplicados. A versão das perguntas deve corresponder a uma
exportação preservada no arquivo de entrada (perguntas e respostas juntas).

```json
{
  "id": "S1",
  "arquivo": "/pasta-de-trabalho/resposta-com-perguntas.json",
  "formulario": "identificador-retornado-pelo-tally",
  "submissao": "identificador-da-submissao",
  "respondente": "Nome Respondente",
  "versao_perguntas": "2026-09-25-r0",
  "rodada": 0,
  "canal": "tally-mcp",
  "workspace_id": "identificador-retornado-pelo-tally",
  "escopo": "administrativo"
}
```

`workspace_id` é opcional no expediente; se presente, precisa conferir com a
declaração dos canais na importação. O script exige tratamento prévio para
`tally-mcp`; receber exportação manual não tem essa trava específica.

`canal` também aceita `manual`. Essa opção é para exportação recebida e revisada
humanamente, não autoriza buscar conteúdo pelo MCP sem registrar tratamento.

`pendencia`:

```json
{"id":"P1","origem":"S1","pergunta":"Onde termina o processo?","efeito":"Impede finalizar a carta","rodada":1}
```

O formulário da rodada é preparado pelo comando com o MCP Tally e revisado pelo
engenheiro. Registre a resposta como nova fonte (`S2`), com `rodada: 1`.

`resolver`:

```json
{"id":"P1","resposta":"S2","decisor":"Nome Engenheiro","motivo":"Limite esclarecido e confirmado"}
```

`reabrir`:

```json
{"id":"P1","rodada":2,"decisor":"Nome Engenheiro","motivo":"Nova resposta diverge do limite registrado"}
```

A resposta de uma rodada anterior não resolve uma rodada nova.

## Consolidação e revisão

`consolidar` recebe o conjunto completo de campos. Cada valor tem uma fonte
registrada. Informações complementadas pelo engenheiro também precisam de uma
fonte registrada, por exemplo uma nota administrativa recebida pelo canal manual.

```json
{"campos":{"organizacao":{"valor":"Organização Exemplo","fonte":"S1"},"processo_alvo":{"valor":"Processo Exemplo","fonte":"S2"}}}
```

Esse exemplo não contém todos os campos dos templates: `gerar` informa os ausentes
e recusa sem criar uma nova versão parcial. `caso_id`, `responsavel_emcia` e campos
de controle da assinatura são preenchidos pelo componente. Datas de assinatura
ficam indicadas como pendentes até o ato real; não são inventadas.

`revisar` exige qualificação de 0a, conferência do conteúdo canônico (inclusive a
carta mantida conforme decisão humana), pessoa e evidência da revisão:

```json
{"decisor":"Nome Engenheiro","motivo":"Conteúdo conferido e qualificação confirmada","qualificacao_0a":true,"conteudo_conferido":true,"evidencia":"/pasta-de-trabalho/revisao.md"}
```

Novas respostas, pendências ou consolidações invalidam a revisão, os documentos e
os acessos anteriores. O histórico permanece. A ação é conservadora: exige nova
revisão mesmo se a nova informação não mudar uma cláusula.

## Geração e liberação dos PDFs

A operação `revisao-juridica` permanece disponível, executada pela sessão após
aprovação humana registrada ou pelo terminal. Seu JSON é:

```json
{
  "revisor": "Nome Jurista",
  "decisor": "Nome Engenheiro",
  "data": "2026-10-05",
  "resultado": "aprovado",
  "ciclo": "identificador-do-ciclo-aprovado",
  "documentos": {
    "HAB-02": "cd86b77fc51afa5e9fc5cbe042b03020c5c8f1bd42889329849c9f57d644c0b4",
    "HAB-03": "00c0f39ce36de8013fc7389a71292d6b4f60510de94f2e66feb5a5211f975f96"
  },
  "evidencia": "/pasta-de-trabalho/revisao-juridica.pdf"
}
```

```bash
python3 /caminho/eiac-campo/scripts/habilitacao.py revisao-juridica \
  --expediente /base/habilitacoes/HAB-0001 --entrada /pasta-de-trabalho/revisao-juridica.json
```

Os nomes e a data devem corresponder ao ato real; os hashes acima são os dos
templates aprovados em metodo-v1.0. A evidência é importada com SHA-256.
`resultado` é obrigatório e aceita somente a string exata `aprovado`.
Campo ausente, `condicionado`, `reprovado`, texto livre ou outra grafia recusam
com `Recusado`, como as demais validações. `ciclo` é opcional; quando informado,
deve ser texto não vazio e identifica o ciclo de revisão.

Parecer condicionado não é registrado no expediente como revisão jurídica:
permanece no registro documental dos ciclos até ratificação sem condição sobre
os hashes exatos. O engenheiro só declara `aprovado` se esse for o resultado
real da evidência; não converte condição em aprovação. Uma tentativa inválida
produz evento `Recusado`, sem acrescentar revisão autorizadora.

Cada registro preserva revisor, decisor, data, resultado, ciclo quando informado,
documentos e evidência;
registros anteriores permanecem. A revisão pode cobrir os documentos em atos
separados, mas ambos os hashes precisam estar cobertos antes de `gerar`.
`gerar` considera somente registros com resultado `aprovado`; registros legados
sem resultado são preservados e não liberam nova geração. É necessário registrar
o resultado do ato humano com sua evidência, sem completar dados antigos por
inferência. A emissão conserva a revisão aprovada selecionada para cada hash.
Ausência de revisão aprovada pode ser coberta somente pela aceitação explícita
descrita abaixo. Aprovação documental não é ratificação jurídica; o registro testemunha o ato humano e não verifica por modelo
o mérito jurídico, a identidade ou a qualificação profissional do revisor.

## Aceitação das minutas e revogação

Sem revisão aprovada para o hash, o engenheiro pode aceitar uma única vez o texto
exato **“uso as minutas sem ratificação jurídica”**. `aceitar-minutas` em
`iniciar.py executar` recebe habilitacao, caso e texto; a aprovação mantém o mesmo
texto literal. A configuração guarda texto, data, responsável, testemunho e
revogada_em. `revogar-minutas` recebe habilitacao e caso e exige testemunho de
revogação; impede emissões futuras, sem apagar as anteriores.

A aceitação é reutilizada nas execuções seguintes. O responsável precisa coincidir
com o expediente. Revisão aprovada para os hashes usados prevalece sobre aceitação.
Sem uma dessas duas condições, `gerar` recusa antes de qualquer PDF, informando
`revisao-juridica` ou aceitação explícita. Não há flag de dispensa da guarda.

Cada versão registra `minuta` (código, arquivo, versão e SHA-256),
`situacao_juridica` (“ratificada” ou “sem ratificação”), data e referência à revisão
ou aceitação. Nenhum metadado jurídico ou de aceitação é inserido no MD ou PDF.
O checklist mostra minutas sem ratificação como pendência não bloqueante.
A emissão conduzida lê a configuração; na alternativa manual, `gerar` pode informar
`config_emcia` para o arquivo de configuração, mantendo responsável e aceitação exatos.

`gerar`:

```json
{"templates":"/checkout/emcia-marketplace/eiac-campo/reference/metodo","navegador":"google-chrome"}
```

Resolve os nomes de HAB-01, HAB-02 e HAB-03 pelo código na tabela do APR-01 do
pacote, sem nomes de arquivo fixos. Cada código deve ter exatamente um arquivo
aprovado; ausência ou ambiguidade recusa tanto `revisao-juridica` quanto `gerar`,
antes de produzir PDF. A tabela deve pertencer a uma única linha de base;
metadados do template não substituem o registro.

Usa os arquivos resolvidos do diretório indicado e exige seus hashes exatos no
APR-01. Também aceita `auxiliares/` de um checkout canônico na tag declarada
pelo manifesto do pacote, com os mesmos hashes. A resolução admite o nome atual
ou o novo nome de HAB-03 quando declarado em uma próxima linha de base aprovada;
não aprova minutas nem atualiza o pacote. Preserva a cópia exata e o hash de cada
template, campos com origem, Markdown e PDF, cada um com seu hash.
Remove deterministicamente a seção “Controle do modelo” até a seção seguinte,
os blocos de citação iniciados por “Revisão jurídica” e o histórico interno do
modelo. Marcas esperadas ausentes ou duplicadas recusam com motivo.
A identificação do caso, as cláusulas e o controle de assinatura permanecem;
o rodapé declara “Estado de emissão: Para assinatura”. O registro da versão
emitida conserva também a revisão jurídica que cobre aquele hash de template.
Não atualiza templates pela rede nem presume aprovação porque o arquivo existe.
Mantém versões anteriores.
O HTML é escapado e não carrega recursos remotos. Chrome/Chromium roda com perfil
temporário e sandbox padrão; a falta do navegador recusa a geração.

`estado` mostra os caminhos dos artefatos, relativos ao expediente. Abra cada PDF
e confira conteúdo e apresentação antes de liberar. O controle de assinatura no
PDF descreve a emissão; os dados de conclusão ficam no expediente e nas evidências,
sem editar o PDF já assinado.

`liberar`, uma vez por documento e versão:

```json
{
  "documento":"HAB-01","versao":1,"decisor":"Nome Engenheiro","pdf_conferido":true,
  "ferramenta":"Ferramenta escolhida pelo cliente","operador":"Nome Operador",
  "signatarios":[
    {"nome":"Nome Cliente","papel":"organizacao","competencia":"Representante autorizado"},
    {"nome":"Nome Responsavel","papel":"emcia","competencia":"Responsável pelo serviço"}
  ]
}
```

Repita para HAB-02 e HAB-03 com os signatários competentes de cada documento.
O operador encaminha os PDFs pelo painel; não há integração com assinatura.

## Retorno das assinaturas

`assinatura`, após a conferência humana de cada documento:

```json
{
  "documento":"HAB-01","versao":1,"decisor":"Nome Engenheiro",
  "arquivo":"/pasta-de-trabalho/HAB-01-assinado.pdf",
  "evidencia":"/pasta-de-trabalho/relatorio-assinatura.pdf",
  "referencia":"Envelope ou referência manual da assinatura",
  "conteudo_conferido":true,"evidencias_conferidas":true,
  "signatarios":[
    {"nome":"Nome Cliente","papel":"organizacao","data":"2026-09-25"},
    {"nome":"Nome Responsavel","papel":"emcia","data":"2026-09-25"}
  ]
}
```

Se o relatório estiver anexado ao PDF assinado, os dois caminhos podem apontar
para o mesmo arquivo. Hashes do PDF enviado e do assinado são distintos e ambos
ficam preservados. Signatários divergentes, faltantes e versões anteriores recusam.

`ocorrencia` registra recusa, cancelamento ou expiração e invalida a versão:

```json
{"documento":"HAB-01","versao":1,"decisor":"Nome Engenheiro","status":"recusado","motivo":"Cliente solicitou alteração de escopo"}
```

`concluir-0b` confere os três documentos; não abre caso nem inicia F0.

## Acessos e preparação de 0d

`acessos`, somente depois de 0b:

```json
{
  "patrocinador":"Nome Patrocinador","autoridade_patrocinador":"Responsável pelo processo",
  "executor":"Nome Executor","executor_liberado":true,"agenda_reservada":true,
  "data_sessao":"2026-10-01","decisor":"Nome Engenheiro",
  "itens":[{"item":"Fonte identificada","status":"concedido","evidencia":"Referência à conferência humana de acesso"}]
}
```

Não importe dados operacionais para comprovar acesso antes de 0d; registre a
conferência administrativa humana. Item negado exige `motivo` e `restricao`.
`preparar-0d` confere prontidão e apresenta o desfecho proposto. O engenheiro aprova o desfecho; a sessão abre com `iniciar.py`, importa pelos
mecanismos aprovados, valida e sela. O terminal com `novo-caso.sh` permanece
alternativa. A preparação não decide o prosseguimento de F0.
Nenhuma operação deste script escreve no caso ou muda a guarda de F0.

`nao-prosseguir` registra a decisão negativa e invalida documentos/revisões:

```json
{"decisor":"Nome Engenheiro","motivo":"Executor não liberado","condicao_retomada":"Confirmar liberação do executor"}
```

## Persistência e limites

`expediente.json` contém estado e histórico no mesmo arquivo, atualizado
atomicamente sob trava de processo. As cópias ficam em `arquivos/`, com nomes
únicos e SHA-256. Cada operação confere sua integridade. Recusas em um expediente
válido geram evento atribuído ao responsável. Falhas anteriores à existência de
um expediente válido são erros de inicialização, sem autoria inventada.
Arquivos sem referência, deixados por falha de operação, não contam como evidência
nem mudam o estado. Preserve o diretório completo no encaminhamento para 0d.


## Importação aprovada no caso e alternativa manual

No fluxo simplificado, a sequência é abertura → definir Tally/calendário →
importar → gravar `00-habilitacao` pelo validador → selar → F0. Drive é
planejado/provisionado em P2, com aprovação. A alternativa manual conserva
planejar/provisionar antes de definir quando quiser preparar esses canais.

Nos casos novos com canais externos, prepare a declaração com
`/eiac-campo:canais` e confira `reference/canais.md`. No terminal humano,
defina os endereços por ids antes de importar, ou acrescente
`--canais /caminho/declaracao.json` ao importador. A declaração identifica
o workspace da habilitação; a importação migra os ids dos formulários e
seu vínculo com o expediente, preservando o hash. Não invente workspace
ausente em expediente antigo: ele precisa vir da declaração humana.
Sem declaração coerente, a importação e o acesso a F0 recusam.

Depois de abrir o caso com o identificador reservado, no terminal do engenheiro,
fora da sessão do agente e no diretório do caso:

```bash
python3 /caminho/eiac-campo/scripts/importar_habilitacao.py --expediente /caminho/expediente
```

O importador exige formalização vigente, acesso efetivo, qualificação registrada,
integridade, mesmo caso reservado e mesmo responsável. Recusa expediente com
decisão de não prosseguir e caso com etapa encerrada. No playbook novo, a sessão pode executar pelo plano de abertura aprovado;
chamada sem testemunho recusa. Casos antigos conservam o contrato humano.

Somente os três PDFs assinados, suas evidências e a matriz entram em
`fontes/habilitacao/importacao-NNN-AAAA-MM-DD/`. A matriz é conferida contra o
hash da entrada administrativa preservada no histórico do expediente.
`registro/habilitacao.json` conserva origem, desfecho, restrições RH-xx e hashes.
O schema está em `registro/habilitacao.schema.json`.

O rascunho `rascunho/00-habilitacao.md` usa marcas determinísticas V para
os documentos conferidos e D para declarações e desfecho. A marca V da matriz
identifica o documento registrado, sem transformar suas declarações em prova
independente do acesso. Gravar pelo validador e selar são atos separados.

Reimportação antes de encerrar qualquer etapa exige `--decisao-reimportacao`
apontando para JSON com `decisor` igual ao responsável, `motivo`, `data` e
`importacao_anterior` igual ao id vigente. Preserva registros e arquivos anteriores.
Não é mecanismo de retomada após perda de pré-requisito durante o percurso.

Antes de carregar ou encerrar F0, o novo playbook exige `HabilitacaoImportada`
e selo posterior confirmado pelo histórico Git, cujo commit contém a linha
importada. Após a importação, grave o rascunho pelo validador e sele:

```bash
python3 /caminho/eiac-nucleo/scripts/validar.py --arquivo caso/00-habilitacao.md
python3 /caminho/eiac-nucleo/scripts/selar.py --nota "habilitação importada e conferida"
```

Sem histórico acessível ou após falha no commit do selo, F0 continua bloqueado.
Casos existentes conservam seu playbook; a mudança alcança novos casos.

Na abertura, `--expediente` é opcional; quando informado, confere prontidão,
identificador reservado e responsável antes de criar o caso. A importação
continua sendo uma operação separada, aprovada no fluxo ou executada no terminal:

```bash
/caminho/emcia-marketplace/novo-caso.sh caso-0001 --responsavel "Nome Sobrenome" /base/casos --expediente /caminho/expediente
```

A abertura sempre confere e copia o pacote controlado e seu manifesto SHA-256.
`/eiac-nucleo:estado` informa a integridade da referência copiada, sem bloquear
operações nem registrar eventos. Alterações no manifesto do caso também ficam
visíveis na trilha Git; o diagnóstico não autentica a origem do manifesto.
Recusas antes de existir caso emitem TentativaNegada em JSON no stderr e, se a
base já existir fora de repositórios, preservam `.emcia-abertura-eventos.jsonl`.
Não se cria um caso ou base apenas para registrar uma negativa. Falhas de
identidade no bootstrap não inventam autor humano.

## Restrição vinculada em P2

A decisão 041 completou o contrato do pacote D da 039. O engenheiro executa
`restricoes.py vincular --restricao RH-xx --fontes F-xxx,F-yyy`, ou
`restricoes.py dispensar --restricao RH-xx --motivo <motivo>`, no terminal.
O ato `vincular-restricao` é humano e a guarda recusa sua execução pela sessão.
Vínculo inicial só cabe em P2 corrente e aberta, com fontes já curadas.

Todo RH importado precisa ter vínculo ou dispensa motivada para encerrar P2.
A coleção vazia satisfaz a cobertura. O registro conserva importação, versões,
autoria e histórico. Revisão usa `--nova-versao <json>` em `rascunho/` com
`restricao`, `versao_anterior`, `decisor`, `motivo` e `data`; fora de P2 só
revisa vínculo existente após P2 encerrada. Nunca cria vínculo inicial tardio.

RH pendente bloqueia materialização antes da escrita, preservando a versão
anterior. Em caso restrito, E1 aguarda a resolução em P2. Cada valor afetado
recebe marca localizada com RH, fonte F, item negado, restrição e motivo.
REC resolve por relação `recebimentos` explícita em fonte curada; relação
ausente recusa. Não se infere destino por texto nem se substitui por ressalva.
Procedimento: EMCIA-HAB-01 §3.4 e EMCIA-CTX-01 §3.7; instrumento em
`reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md`.


## Saída e decisões de método

`saida_inicial.py --expediente <dir> --caso <dir>` confere respostas, campos com
fonte, carta, três PDFs assinados com evidência, matriz/desfecho, método, canais,
importação, validação, selo Git e F0 liberado. `--json` retorna o mesmo checklist.
Ausência bloqueante retorna 1. Pendência jurídica retorna 0 se os demais itens
estiverem presentes. Não altera estado nem registra encerramento de F0.

Apuração, decidir-prosseguimento, sessões, restrições, autonomia, recalibragem,
encerramentos EX3/EX4 e selo após P2 continuam no terminal. Aprovação no chat
não autoriza o agente a executá-los. Casos abertos conservam seu playbook.

## Conferência do formulário antes da publicação

A sessão lê o formulário declarado por `mcp__tally__load_form(formId)` e preserva
o retorno bruto. `iniciar.py` executa `conferir-formulario` contra o modelo de
`reference/formularios/`, produzindo relatório MD com SHA-256. O engenheiro
confirma com o literal “conferido”; `confirmar-formulario` vincula essa decisão
ao hash do relatório sem divergências. Não é necessário arquivo externo adicional.
Texto, ordem, tipo ou campo oculto divergente impede publicação e aparece no
relatório. Nova leitura invalida a confirmação anterior. A conferência manual
com PDF permanece disponível por `caminho-manual`, passo `preparar-formulario`,
com o mesmo literal. Consulte `reference/canais.md` para entradas e limites.
