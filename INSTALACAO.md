# Instalação — marketplace emcia

Instale os plugins, conecte Tally e Google, e execute o bloco inicial conduzido.
O ambiente exige Python 3.12 ou superior, Git com identidade e Chrome/Chromium.
A regressão cobre Python 3.12 e o ambiente 3.14.4. Núcleo 0.2.48, campo 0.8.31, playbook 0.4.22.

## 1. Instalar os plugins

No Claude Code:

```text
/plugin marketplace add CvGonjr/emcia-marketplace
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

Se o marketplace já estiver instalado, atualize os dois plugins e reinicie a sessão.
Confira as versões instaladas. A alteração de playbook vale somente para casos novos;
caso existente conserva seu contrato e exige migração humana deliberada.

Caso real usa somente a linha de base aprovada **metodo-v1.0**, registrada no
[APR-01](eiac-campo/reference/metodo/EMCIA-APR-01-registro-de-aprovacoes.md).
Documento em revisão ou fora da aprovação não entra em caso real. O pacote é
byte a byte o da tag `metodo-v1.0`; a autorização operacional da decisão 045 não
reescreve documentos canônicos. O MAN-01 ainda requer revisão: A25 é falha conhecida.

Para testar o checkout da ferramenta, mantenha um checkout irmão de
`emcia-artefatos` na tag `metodo-v1.0`; os testes conferem também os templates
canônicos usados pela habilitação contra os hashes do APR-01.

## 2. Conectar o Tally

No terminal:

```bash
claude mcp add tally --transport http --scope user https://api.tally.so/mcp
```

Conclua a autenticação do conector. A orientação e o endpoint estão na
[documentação oficial do Tally](https://tally.so/help/mcp).
Não grave credenciais, tokens ou respostas de clientes neste repositório.

## 3. Confirmar os conectores Google

Abra `/mcp` e confirme Google Drive e Google Calendar, com as contas EMCIA.
Consulte a [documentação dos conectores Google no Claude](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors).
Na habilitação, esses conectores operam sem perfil e sem escopo por id.
Leitura, listagem e rascunho não têm aprovação própria; publicar, enviar convite/
mensagem ou compartilhar pede “ok” registrado com resumo/data. Depois da abertura,
o perfil aprovado do caso recusa ferramenta/parâmetro incompatível e ids não declarados.

## 4. Rodar o bloco inicial

```text
/eiac-campo:iniciar
```

A primeira execução verifica ambiente e prepara `~/.emcia/config.json` com:
responsável nominal, base local de casos, base local de expedientes, id do workspace
Tally, id do calendário e navegador. Pasta Drive é opcional até P2. O agente obtém ids pelos
MCPs quando possível e pergunta somente o que faltar. As bases ficam fora de
repositórios da ferramenta e do método. A configuração é privada e reutilizada.

Antes da abertura, confirme o permanente por load_form, que admite qualquer
formId, e conferir-formulario, sem aprovação própria. O relatório MD fixa texto,
ordem, tipo e campo oculto caso; “conferido” fixa a conferência. Divergência bloqueia
publicação; publicar ainda exige “ok”. PDF conferido permanece alternativa manual.

A coleta padrão usa fetch_submissions: leia todas as páginas e entregue o retorno
completo a iniciar.py retorno. O script registra somente a submissão cujo campo
oculto caso coincide com o expediente. Zero/várias exigem indicação humana.
Não transcreva o lote na conversa nem o copie para fonte/evento. CSV filtrado é
alternativa, selecionada por coleta: csv e exportacao com o caminho original.
~/emcia-op/entrada/ permanece opcional, sem exigir movimentação de arquivos.

Disponibilize o inventário real para a preparação da abertura, no formato
ferramentas/nome/inputSchema/parametros (padrão ~/emcia-op/ensaio/inventario-mcp.json;
inventario na entrada permite outro caminho). É a fonte dos nomes/parâmetros para
o perfil. Se faltar, a abertura para e pede o arquivo. O script calibra e apresenta
perfil/hash e ids dos canais junto do desfecho; a terceira confirmação aprova
perfil/escopo e abertura. Não há calibração exigida no começo da habilitação.

No caso aberto, continuam as restrições: create_file de pasta sob pai declarado,
arquivo comum somente em entregas, busca por query restrita à pasta, leitura por
fileId depois da listagem e compartilhamento com destinatário/papel aprovados.
Calendar usa calendarId declarado; Tally usa workspace/formulário declarados.
fetch_submissions conserva a recusa do perfil do caso por ausência de filtro remoto.
Não edite estado, expediente ou perfil com Write/Edit direto.

Sem revisão jurídica aprovada para os hashes das minutas, a primeira execução pede
**“uso as minutas sem ratificação jurídica”**. Essa aceitação nominal e datada é
revogável. Sem revisão aprovada ou aceitação ativa, a geração recusa. Revisão aprovada
prevalece para o hash coberto. Parecer condicionado não é registrado como aprovado.
A situação jurídica fica no expediente e no checklist, nunca no documento do cliente.

Após confirmar cada formulário, declare formulario-permanente na configuração,
com tipo, formId e relatório. Contrato/formulário alterado exige nova conferência.
Configure tratamento_administrativo com condicoes e provedor; o script aplica
o padrão com referência e hash antes da coleta. Consulte o cartão operacional.

Por caso, o engenheiro envia o link; a sessão coleta pelo conector e recebe os
três PDFs assinados pelo Drive ou pelos caminhos originais. A sessão baixa os
bytes exatos pelo download_file_content, sem conversão do PDF assinado, em
temporário externo, e prepara assinados/evidencias para o script importar com
hashes. Relatórios são opcionais. Não pede exportação ou movimentação manual
para ~/emcia-op/entrada/; essa pasta e a coleta CSV permanecem alternativas.
Confirma três conjuntos: documentos apresentados; assinaturas; perfil/escopo e
abertura/importação/validação/selo. Mensagens completam lacunas e confirmam/corrigem a matriz de acessos.
“ok” é suficiente para o conjunto apresentado, com trecho real e hashes preservados.
Associação automática de PDFs requer Poppler (`pdftotext`, pacote poppler-utils
em Debian/Ubuntu); PDF sem texto ou com reorganização exige a alternativa manual.

O comando carrega somente reference/cartao-habilitacao.md e usa iniciar.py proximo:
uma chamada por avanço e saída curta. A abertura declara Tally/calendário, importa,
valida 00-habilitacao e sela. Drive aguarda P2 e uma aprovação do plano de criação
e compartilhamento. Raiz e trabalho-interno permanecem privados. P2 conserva
a exigência de documentos/entrada. Nenhuma decisão de método muda.

## 5. Retomar e conferir

Execute `/eiac-campo:iniciar HAB-0001 caso-0001` após interrupção. A sessão consulta
expediente e caso e continua pela saída ausente. Retorno MCP perdido exige conferir
objeto remoto por id antes de repetir criação, publicação ou compartilhamento.

O relatório também pode ser executado no terminal:

```bash
python3 /caminho/eiac-campo/scripts/saida_inicial.py \
  --expediente /base/expedientes/HAB-0001 --caso /base/casos/caso-0001
```

Cada item sai como presente ou ausente. Saída 0 exige todos os itens bloqueantes;
“Minutas sem ratificação jurídica” é pendência não bloqueante. O selo precisa estar
confirmado no Git e conter `00-habilitacao`; um evento sem commit não basta.

F0 liberado para execução não é encerrado. Apuração de nível, sessão e decisão de
prosseguimento continuam no terminal humano, assim como restrições, autonomia,
recalibragem, encerramentos EX3/EX4 e selo após P2. A aprovação no chat não libera
essas decisões pela sessão.

## Alternativa manual

As interfaces completas e JSON de entrada estão em
[reference/habilitacao.md](eiac-campo/reference/habilitacao.md) e
[reference/canais.md](eiac-campo/reference/canais.md). O engenheiro pode executar
os scripts administrativos diretamente no terminal; as conferências de conteúdo,
assinatura, integridade, origem e situação jurídica permanecem. Casos anteriores
continuam seguindo seu próprio playbook.

Aprovação e assinatura registradas são testemunhos, sem autenticação. O ambiente
local e os hooks do runtime são a fronteira de confiança; a suíte sintética não
comprova permissões remotas reais nem suporte universal dos conectores.

Instrumento de contexto:
[EMCIA-CTX-01](eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md).
Use essa referência controlada ao conferir termos, regras e fontes.
