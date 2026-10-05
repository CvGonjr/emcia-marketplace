# Interface dos canais externos

O fluxo inicial é conduzido por `/eiac-campo:iniciar`, conforme decisão 045.
O procedimento canônico é EMCIA-CAN-01, MAN-01 §3.2 e ROT-02 §3.6 na linha de
base do manifesto. As diferenças aprovadas estão em `propostas-artefatos.md`;
o pacote permanece byte a byte o da tag.

## Planejar, provisionar e definir

`canais.py planejar` é somente leitura: propõe a raiz do caso com
`00-habilitacao`, `entrada-documentos`, `entrada-amostras`, `entregas` e
`trabalho-interno`. Roteamento usa ids, não nomes. O agente executa os MCPs
somente depois de registrar e conferir as aprovações dos efeitos externos.

Uma aprovação cobre a árvore inteira, apresentada junto da decisão de abrir.
Outra cobre o conjunto de compartilhamentos: destinatário, pasta/id e papel
em cada linha. Trabalho-interno tem acesso do cliente `nenhum`. Uma alteração
de destino, destinatário ou papel exige aprovação atualizada.

A calibração usa exclusivamente o inventário fornecido; neste ensaio,
`~/emcia-op/ensaio/inventario-mcp.json`. O formato contém `ferramentas`, `nome`,
`inputSchema` e `parametros`. Nomes e parâmetros são literais, sem aliases.
Os perfis embutidos estão em `reference/perfis-conectores.json`; `iniciar.py`
confere cada campo contra o inventário e gera `ferramentas-externas.json`.
O engenheiro aprova perfil/inventário antes de usar. Schema parcial permite
somente tipos simples explicitamente transcritos; estruturas sem schema e
parâmetro extra são recusados. O relatório lista a garantia faltante e a ação manual.

| Operação | Ferramenta e parâmetros reais | Restrição |
|---|---|---|
| Buscar | `mcp__claude_ai_Google_Drive__search_files`, `query` | Somente `'<pasta_id>' in parents`, opcional `and trashed = false` |
| Ler/metadados/download | `get_file_metadata`, `read_file_content`, `download_file_content` do mesmo namespace, `fileId` | Id presente em listagem íntegra do contêiner declarado |
| Criar pasta | `create_file`, `title`, `parentId`, `contentMimeType` | Tipo `application/vnd.google-apps.folder`; pai declarado; nenhum conteúdo |
| Criar arquivo | `create_file`, mesmos campos, `textContent` ou `base64Content` | Pai com finalidade `entregas`/direção `saida`; conteúdo exclusivo |
| Compartilhar | `share_file`, `fileId`, `emailAddress`, `role` | Pasta declarada; valores exatos da aprovação; raiz EMCIA recusada |
| Agenda | `mcp__claude_ai_Google_Calendar__list_events`/`create_event`, `calendarId` | Calendário declarado; criar exige aprovação dos parâmetros |
| Criar formulário | `mcp__tally__create_new_form`, `title`, `workspaceId` | Workspace declarado, sem usar o padrão implícito do servidor |
| Ler formulário | `mcp__tally__load_form`, `formId` | Somente formulário criado/declarado no expediente ou caso corrente; retorno bruto preservado |
| Publicar formulário | `mcp__tally__publish_form`, `formId` | Formulário declarado; conferência vigente sem divergências, literal “conferido” e aprovação |
| Submissões | `mcp__tally__fetch_submissions`, `formId` | **Recusada**: inventário não oferece filtro pelo campo oculto do caso |

`finalidade` da pasta é declaração na entrada local aprovada de `iniciar.py`,
sem envio à API. Retorno guarda chamada, finalidade, ids e hashes, vinculados
ao evento; alteração posterior recusa. Antes de ler/download, registre a
listagem: no expediente, retorno da busca com `conteiner_id` e `objetos`; no
caso, também `registrar_listagem.py` com o manifesto e evento no contrato local.
IDs retornados só entram no contexto do expediente e da operação correspondente.
Retorno não autentica servidor nem comprova permissão remota.

### Conferência automática e confirmação humana

Após preparar o formulário no painel, a sessão autoriza `load_form` pelo wrapper,
chama o conector e registra o retorno inteiro, sem resumir/reconstruir os blocos:

```json
{
  "chamada": {
    "habilitacao": "HAB-0001", "caso": "caso-0001",
    "ferramenta": "mcp__tally__load_form", "argumentos": {"formId": "FORM-ID"}
  },
  "resultado": {"resposta": {"data": {"formId": "FORM-ID", "workspaceId": "WORK-ID", "blocks": []}}}
}
```

Use a entrada acima em `iniciar.py retorno`; `resposta` recebe o JSON real completo
(o array vazio é somente indicação de formato, nunca uma conferência positiva).
Aceita-se também o envelope MCP `structuredContent.data`. O retorno e a chamada
ficam vinculados por hashes e evento. Não se usa o ledger textual para decidir
conformidade. O adaptador aceita o [schema público dos blocos Tally](https://developers.tally.so/api-reference/openapi.json):
`TITLE` de `groupType: QUESTION`, `payload.html` ou `payload.safeHTMLSchema`
conforme o retorno fornecido do conector (decisão 046), entradas subsequentes e
`HIDDEN_FIELDS.payload.hiddenFields`. Formato desconhecido é divergência explícita.
O ensaio usa fixtures desse schema; não autentica o servidor nem testa conta real.

Execute as operações pelo mesmo `aprovar`/`executar` das demais entradas:

```json
{"operacao":"conferir-formulario","entrada":{"habilitacao":"HAB-0001","caso":"caso-0001","formulario_id":"FORM-ID","modelo":"habilitacao"}}
```

A aprovação dessa entrada fixa a seleção do modelo correspondente. Modelos
permitidos: `habilitacao`, `triagem`, `ciclo`, sempre da pasta `reference/formularios/`.
O relatório MD fica em `conferencias/` junto da configuração; registra contexto,
formulário, modelo/hash, retorno/hash, perguntas observadas e diferenças.
Compara texto, ordem e tipo, e exige uma ocorrência do campo oculto `caso`.
A decisão 046 autoriza somente NFC, NBSP convertido em espaço, remoção de
espaços nas bordas e marcação de formatação. Marcação `**` pareada e marcas
de negrito do schema capturado são ignoradas e registradas no relatório.
Se `html` e `safeHTMLSchema` estiverem presentes, ambos devem coincidir após
essa normalização. Marcas sem mapeamento, estrutura ou tipo inválido recusam
com o caminho `blocks[i]`. Espaços internos, pontuação, palavras e acentos
continuam exatos; não se reformula nem corrige a redação. `texto`
corresponde a uma única entrada `INPUT_TEXT` ou `TEXTAREA`. As alternativas da
triagem exigem escolha única `MULTIPLE_CHOICE_OPTION`, mesmos textos e ordem,
sem seleção múltipla ou aleatorização. O modelo de ciclo não fixa redação de
perguntas; exige a alternativa humana com PDF, sem inventar textos.

Sem diferenças, apresente o relatório e seu hash; o engenheiro responde
**“conferido”**. Registre esse literal e execute:

```json
{"operacao":"confirmar-formulario","entrada":{"habilitacao":"HAB-0001","caso":"caso-0001","formulario_id":"FORM-ID","relatorio_sha256":"<hash-do-relatorio>"}}
```

O relatório automático é a evidência dessa confirmação; não se exige arquivo
externo adicional. Sua integridade e a do modelo/retorno são reconferidas.
Publicação ainda exige aprovação nominal do efeito externo. Cada nova leitura
invalida a confirmação anterior. Divergência bloqueia publicação com a lista das
diferenças; corrija no painel, leia novamente e repita comparação/“conferido”.
Uma aprovação antiga ou um PDF não sobrepõe divergência registrada. O núcleo
aplica somente a pré-condição declarada: último evento e valores esperados,
com diagnóstico fornecido pelo contrato; não compara instrumentos ou blocos.

Na alternativa manual, `caminho-manual`, passo `preparar-formulario`, exige
`formulario_id`, `decisao: executar manualmente`, evidência PDF completo e
aprovação com literal “conferido”. Outros passos manuais conservam seu contrato.

### Garantia ausente e caminho manual

O Tally fornecido cria o formulário vazio, mas as ferramentas para perguntas e
campo oculto têm schema indisponível. O engenheiro prepara/confere no painel,
com a especificação e id de caso entregues pela sessão. O parâmetro `filter`
de `fetch_submissions` aceita apenas datas/status; não permite filtrar `caso`.
A API fica recusada mesmo com formulário declarado. Não se coleta lote para
filtrar localmente. O engenheiro filtra/exporta manualmente o formulário declarado
com o campo oculto `caso` e entrega os bytes; `receber` da habilitação usa `canal: manual`.

Cada caminho manual exige aprovação registrada e evidência com SHA-256:

```json
{
  "operacao": "caminho-manual",
  "entrada": {
    "habilitacao": "HAB-0001", "caso": "caso-0001",
    "passo": "coletar-submissoes", "decisao": "executar manualmente",
    "evidencia": "/base/expedientes/evidencia-da-decisao.txt"
  }
}
```

Use `iniciar.py aprovar` e `executar` como nas demais operações. Passos são
`preparar-formulario` (inclua `formulario_id`), `coletar-submissoes` e, se
faltarem as respectivas garantias/ferramentas, `criar-formulario` ou
`publicar-formulario`. O registro preserva motivo da calibração, responsável,
texto literal, data, evidência/hash e contexto. Ele registra a decisão humana;
a sessão não executa a API recusada nem presume que a ação manual ocorreu.
Sem `workspaceId`, criação também fica manual; sem publicação no inventário,
o engenheiro publica no painel, com a instrução e aprovação preservadas.

Antes de existir caso, `guarda_inicial.py` confere aprovações, tratamento e ids
pela configuração/expediente. Durante o bloco, mantenha a sessão na pasta de
trabalho administrativa para provisionar a raiz antes da declaração dos canais;
ainda não há contrato de canais no caso vazio. Os atos locais usam o wrapper e
entram no caso pelo script. Dentro de caso com canais declarados, a guarda do
núcleo também aplica seu contrato; a autorização local não contorna a guarda.

A ordem é abertura → planejar/provisionar → definir (ou `--canais`) → importar
→ validar `00-habilitacao` → selar → F0 liberado. Na sessão, `iniciar.py executar`
confere testemunho e hashes antes do ato. O responsável fixado é o autor.
O núcleo aplica `operacoes_sessao` declarado no playbook, sem nomes do método.

## Declaração e alternativa manual

No terminal, continua disponível:

```bash
python3 /caminho/eiac-campo/scripts/canais.py definir --entrada /pasta/canais.json
```

O JSON declara `versao` sequencial, `caso`, `decidido_por` nominal, `data` ISO e
`canais`, conforme `registro/canais.schema.json`. Cada canal possui finalidade,
ferramenta, direção, etapas, entregáveis, proprietário, ids, acesso do cliente,
sensibilidade, filtro e marcador. Tally usa workspace_id/formulario_id; Drive,
drive_id/pasta_id; Calendar, calendario_id. Todos os ids vêm da fonte ou conector.
Filtro Tally é `{"campo":"caso","valor":"<caso>"}`. Agenda usa `[{caso}/{etapa}]`.
Não use nomes de organizações como ids nem declare contêiner de outro caso.

Versões anteriores ficam em `registro/canais/versao-NNNN.json`. `CanaisDefinidos`
fixa o hash vigente. `resolver <alvo> <direcao>` recusa falta, ambiguidade e
adulteração. Etapas e emissão conferem os canais que o playbook exige.

`importar_habilitacao.py --expediente <dir> --canais <json>` também define na
importação. Os formulários e rodadas do expediente migram com origem, fontes e
hash, sem perder versões. Workspace informado no expediente precisa coincidir;
workspace ausente em expediente antigo vem da declaração humana, nunca de palpite.

## Coleta, listagem e entrega

Preparação fica em `rascunho/entrada/`. No bloco inicial, `registrar-listagem`
e `receber-material` podem ser executados pela sessão com aprovação registrada.
Fora de F0, a sessão recusa esses atos: o engenheiro usa o terminal. Caso anterior
conserva as exigências de seu playbook.

`registrar_listagem.py --entrada <json>` confere ferramenta_externa, argumentos,
conteiner_id, objetos e coletado_em com fuso; canal e parâmetros devem corresponder.
`ListagemRegistrada` fixa o hash. Leitura por id exige listagem íntegra do contêiner
declarado. Isso não transforma a coleta em prova nem autoriza escrita direta.

`receber.py --arquivo <arquivo> --manifesto <json>` exige preparação no caso,
canal/etapa/filtro e hash. Manifesto traz ferramenta, objeto_id, conteiner_id,
modificado_em e coletado_em; Tally acrescenta submissao_id e campos_ocultos.
Nova versão exige decisor nominal, motivo, data e recebimento_anterior, com
`--nova-versao <json>`; os anteriores permanecem. Procedência da asserção continua
sendo verificada pelo validador, usando `fonte: REC-NNNNNN` e hash completo.

`entregar.py --entrada <json>` permanece humano: confere entregável, versão, hash,
arquivo_id, destino_id, destinatario e data contra a emissão e o canal de entregas.
Registro de publicação não é aceite. Não há mensagem ou publicação automática.

| Ato na fronteira externa | Executor |
|---|---|
| `receber-material` | Sessão aprovada em F0; terminal fora do bloco inicial |
| `registrar-listagem` | Sessão aprovada em F0; terminal fora do bloco inicial |
| `entregar-material` | Engenheiro no terminal, após conferir a publicação |

## Sessões e limites

Sessões continuam humanas. Referência externa opcional no template deve coincidir
com canal, id do calendário e marcador do caso/etapa; o playbook pode exigi-la
por camada. Agendamento não registra realização da sessão.

Os hooks precisam disparar no runtime. A suíte usa MCP simulado; não comprova
permissões em contas reais ou assinatura de todas as versões dos conectores.
Ferramenta incompatível fica recusada e exige perfil conferido, sem ampliar escopo.
Aprovação no chat é testemunho, não autenticação. Disco e autoria fixa mantêm a
fronteira de confiança da 022; não se verifica veracidade remota por modelo.

Após atualizar para o comparador da decisão 046, leia novamente o formulário,
gere o relatório e registre “conferido” para seu novo hash; os relatórios anteriores
não recebem confirmação ou migração automática.
