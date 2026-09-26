# Interface do expediente de habilitação

Procedimento: documentos canônicos em https://github.com/CvGonjr/emcia-artefatos/,
`EMCIA-HAB-01-protocolo-de-habilitacao.md` e os dois documentos de fluxo/roteiro em
`auxiliares/`. Esta referência descreve a interface técnica, não substitui o método.

## Inicialização humana

Antes da sessão do agente, no terminal do engenheiro:

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

`estado`, `concluir-0b` e `preparar-0d` dispensam `--entrada`.
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
  "escopo": "administrativo"
}
```

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

`gerar`:

```json
{"templates":"/checkout/emcia-artefatos/auxiliares","navegador":"google-chrome"}
```

Usa HAB-01, HAB-02 e HAB-03 do checkout indicado, preservando a cópia exata e o hash
de cada template, campos com origem, Markdown e PDF. Não atualiza templates pela
rede nem presume aprovação porque o arquivo existe. Mantém versões anteriores.
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
`preparar-0d` confere prontidão e apresenta o desfecho proposto. O engenheiro abre o
caso com o identificador reservado usando `novo-caso.sh`, importa o expediente
com os mecanismos autorizados e segue o roteiro canônico para registrar e selar.
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
