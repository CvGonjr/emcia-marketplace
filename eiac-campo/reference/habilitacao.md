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

Antes de gerar HAB-02 e HAB-03, o engenheiro registra a operação humana
`revisao-juridica` no terminal, com entrada JSON:

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
Ausência ou divergência recusa com o nome da operação que falta, antes de
iniciar qualquer PDF. Não há dispensa. Aprovação documental não substitui
revisão jurídica; o registro testemunha o ato humano e não verifica por modelo
o mérito jurídico, a identidade ou a qualificação profissional do revisor.

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


## Importação humana no caso

A sequência é abertura → planejar/provisionar → definir (ou `--canais`) →
importar → gravar `00-habilitacao` pelo validador → selar → F0.

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
decisão de não prosseguir e caso com etapa encerrada. A guarda recusa essa
operação pela sessão e devolve o comando exato para o terminal humano.

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
continua sendo uma operação humana separada:

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
