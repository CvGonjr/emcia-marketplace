# Interface dos canais externos

Procedimento: EMCIA-CAN-01, MAN-01 §3.2 e
`auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md` §3.6, na origem fixada
em `reference/metodo/manifesto.json`. As cópias empacotadas conservam os bytes
canônicos e seus estados de aprovação.

O playbook declara finalidades e direções; `registro/canais.json` declara ids.
`canais.schema.json` documenta o contrato; o script aplica as mesmas condições
e as relações com o playbook, sem bibliotecas novas nem chamadas de API.

`canais.py planejar` é somente leitura e propõe no drive compartilhado EMCIA
`<caso>/00-habilitacao`, `entrada-documentos`, `entrada-amostras`, `entregas`
e `trabalho-interno`. Os nomes não são referências de roteamento.

No terminal humano, use `canais.py definir --entrada <json>`. Declare `versao`
inteira sequencial, `caso`, `decidido_por` nominal, `data` no formato ISO de data
(AAAA-MM-DD) e `canais`. O evento é atribuído ao responsável fixado no caso;
`decidido_por` registra a pessoa comunicada na declaração.
Cada canal contém os campos da especificação em `registro/canais.schema.json`.
Tally usa `workspace_id`/`formulario_id`; Drive, `drive_id`/`pasta_id`;
Calendar, `calendario_id`. Proprietário é `emcia` ou `cliente`. Filtro Tally
é `{"campo":"caso","valor":"<id-do-caso>"}`; marcador da agenda é
`[{caso}/{etapa}]`, expandido ao registrar a sessão. Todos os ids são reais
informados pelo engenheiro ou retornados pelo conector; não substitua por nomes.

Versões anteriores ficam em `registro/canais/versao-NNNN.json`. O evento
`CanaisDefinidos` fixa o SHA-256 da versão vigente. `resolver <alvo> <direcao>`
recusa ausência, ambiguidade ou adulteração, indicando a definição humana.
O núcleo exige o canal ao carregar e encerrar etapas que o declaram.

## Passagem em 0d

Depois da abertura, planeje e provisione; defina os canais antes da importação
ou na própria importação com `--canais`. Grave o desfecho pelo validador e sele
antes de F0. `planejar` não chama APIs nem grava a declaração.

Prepare os endereços com `/eiac-campo:canais`, com as confirmações de criação
e compartilhamento. O engenheiro define os canais e importa a habilitação.
Alternativamente, `importar_habilitacao.py --expediente <dir> --canais <json>`
usa a declaração humana na própria importação. Antes de F0, valide o desfecho
e sele conforme a decisão 039. Sem canais definidos, F0 continua bloqueado.

Na importação, os ids dos formulários registrados no expediente substituem
os endereços de habilitação, preservando `origem` com id da habilitação, fontes
e hash do expediente. Workspace conhecido no expediente é conferido contra
a declaração humana; quando o expediente antigo não o contém, ele precisa
vir da declaração. Nenhum id é inventado. Rodadas conservam seus formulários.

## Coleta e publicação

Downloads e manifestos são preparação em `rascunho/entrada/`. O engenheiro
executa `receber.py --arquivo <caminho> --manifesto <json>` no caso. O manifesto
traz `ferramenta`, `objeto_id`, `conteiner_id`, `modificado_em` e `coletado_em`;
Tally acrescenta `submissao_id` e `campos_ocultos`. As datas são ISO com fuso.
O arquivo e o manifesto precisam estar em `rascunho/entrada/`. O script
confere que a coleta não antecede a modificação e recusa hash ou objeto
já recebido sem decisão de nova versão. Novas versões requerem `--nova-versao <json>` com decisor, motivo, data e id
do recebimento anterior. A decisão fica em `rascunho/`. Arquivos e manifestos anteriores ficam preservados.

O engenheiro registra a publicação com `entregar.py --entrada <json>`:
`entregavel`, `versao`, `sha256`, `arquivo_id`, `destino_id`, `destinatario`
nominal e `data` (AAAA-MM-DD). A entrada precisa estar em `rascunho/`. O destino precisa ser o canal `entregas`. O hash é conferido
contra a emissão e os bytes locais. Esse registro não é aceite.

Scripts conferem os dados trazidos pelo agente contra a declaração; não
autenticam conteúdo remoto, identidade ou acesso efetivo. Confirmações no
chat são requisitos operacionais do comando, não credenciais dos scripts.

Asserções sobre material recebido usam `fonte: REC-NNNNNN` na marca de
procedência. O validador encontra a origem e confere o hash completo. A marca
de procedência continua dependendo do instrumento: recebimento não transforma
automaticamente uma declaração em verificação.

## Sessões e escopo MCP

Registro de sessão aceita `--referencia-externa <id>` junto com
`--canal-externo <id>` e `--marcador "[<caso>/<etapa>]"`. No template a referência
é opcional; `exige_referencia_externa_por_camada` pode torná-la obrigatória
no playbook do caso. Referência informada sempre exige canal e marcador coerentes.

O teste real confirmou hooks MCP no Claude Code 2.1.283. Os hooks do núcleo
incluem `mcp__.*` e leem `registro/ferramentas-externas.json`. As regras padrão
mostram nomes e argumentos de interfaces MCP; o engenheiro ajusta esses dados
aos nomes e argumentos efetivos do conector instalado, no terminal, sem
afrouxar o escopo. Ferramenta desconhecida recusa. Não existe uma interface
universal de argumentos MCP. A confirmação em chat permanece necessária.

Leitura por id exige manifesto de listagem prévia. O agente prepara JSON em
`rascunho/entrada/` com `ferramenta_externa`, `argumentos`, `conteiner_id`,
`objetos` (lista de ids) e `coletado_em`; o engenheiro confere e executa
`registrar_listagem.py --entrada <json>`. O script exige correspondência entre
argumentos, contêiner e canal, fixa o hash e emite `ListagemRegistrada`.
Registro não autentica a resposta remota. Coleta segue em preparação até o
recebimento humano; listagem não autoriza escrita em `fontes/`.

Para provisionar, declare primeiro um contêiner EMCIA já existente e exclusivo
do caso como endereço inicial. Não use o espaço compartilhado de outros casos
como canal de leitura. O agente cria divisões dentro desse id apenas com confirmação;
o engenheiro então define a versão com os ids provisionados. Sem endereço
inicial declarado ou sem regra compatível, use a interface externa.
Provisionamento de estrutura tem regra própria; escrita de material só vai
para `entregas`. Cada compartilhamento continua exigindo confirmação própria.

Essas guardas dependem do runtime que executa os hooks. Não foi comprovado
disparo em outro ambiente; o resultado do Claude Code não é garantia para
conectores executados por clientes que não suportem esses hooks.

| Ato na fronteira externa | Executor |
|---|---|
| `receber-material` | Engenheiro no terminal, após conferir a coleta |
| `entregar-material` | Engenheiro no terminal, após conferir a publicação |
| `registrar-listagem` | Engenheiro no terminal, após conferir a listagem |
