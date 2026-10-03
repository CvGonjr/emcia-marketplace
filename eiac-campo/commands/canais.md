---
description: Planeja e resolve canais externos do caso; definição e registros são humanos.
argument-hint: "planejar | resolver <etapa|entregavel> <direcao>"
---

Consulte `reference/canais.md`, `reference/habilitacao.md` e o roteiro canônico
`auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md` §3.6 e EMCIA-CAN-01,
na origem fixada pelo manifesto. As cópias exatas estão em `reference/metodo/`.
O procedimento permanece nos documentos canônicos.

Depois da abertura, planeje/provisione e entregue a definição humana antes de
importar o expediente, ou a declaração completa para `--canais`. Depois seguem
importação → gravação validada de `00-habilitacao` → selo → F0.
Provisionamento MCP exige contêiner exclusivo do caso previamente declarado;
sem ele, use a interface externa e depois declare os ids.

Execute `scripts/canais.py planejar` para preparar o provisionamento. Apresente
o id do drive compartilhado EMCIA e os nomes propostos. Peça confirmação
explícita antes de criar qualquer divisão pelo MCP. Não faça busca por nome.
Se faltarem ids, peça-os ao engenheiro e espere. Registre os ids retornados
somente no rascunho da declaração; o engenheiro define pelo terminal.

Antes de **cada** compartilhamento, liste a pessoa que receberá acesso,
seu endereço, id do destino e papel proposto. Peça confirmação própria para
esse compartilhamento. Sem confirmação, o engenheiro usa a interface do Drive.
`trabalho-interno` permanece sem acesso do cliente.

Use `scripts/canais.py resolver <alvo> <entrada|saida|agenda>` antes de consultar
ou preparar envio. Consulte somente ids retornados. Nunca liste todo o espaço
do cliente nem procure por nome. A leitura de arquivo por id exige listagem
prévia do contêiner declarado registrada pelo engenheiro no manifesto local.

Para receber, baixe para `rascunho/entrada/` e prepare o manifesto de coleta.
Para entregar, confira a emissão e o hash antes de propor upload à finalidade
`entregas`. Upload nessa finalidade publica para o cliente: peça confirmação
explícita do engenheiro. Depois entregue o comando humano de registro.

Preparar um formulário não autoriza publicação nem envio de link. Ambos exigem
instrução expressa. Links carregam `caso=<id>`; filtre submissões pelo mesmo
campo, ignorando respostas de outros casos antes de preparar material local.
Sem MCP Tally, use exportação manual com ids de formulário e submissão.
Perguntas de F0 vêm de `reference/formularios/triagem.json`, sem reescrita.

Na agenda, apresente calendário por id, participantes, data, horário, fuso e
marcador `[<caso>/<etapa>]`. Peça confirmação explícita antes de criar evento
ou enviar convite. Não leia gravações nem transcrições.

Não execute `definir`, `receber.py`, `entregar.py` ou registro de sessão pela
sessão do agente. Entregue caminhos absolutos e argumentos conferidos ao
engenheiro. Confirmação no chat não substitui esses atos no próprio terminal.
