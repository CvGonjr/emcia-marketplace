# 045 — Bloco inicial conduzido com aprovação nominal no chat

**Data:** 05/10/2026 · **Estado:** firme por instrução do engenheiro

## Contexto

O engenheiro decidiu que ambiente, habilitação administrativa 0a–0d e abertura
até F0 liberado sejam conduzidos pela sessão do Claude Code. A saída verificável
rege a entrega. O pedido aprova a mudança de autoridade dos atos administrativos,
a aceitação de minutas sem ratificação e o agrupamento dos efeitos externos.
O método documental aprovado permanece metodo-v1.0, tag 08bfb16, sem reempacotamento.

## Decisão

Todas as operações de habilitacao.py, canais definir, importação do expediente,
listagem e recebimento durante o bloco inicial, validação e selo de 00-habilitacao
podem ser executados pela sessão depois de aprovação explícita registrada.
Cada ato conserva operação, resumo, trecho literal, data e responsável, com
contexto, comando/entrada e hashes dos arquivos conferidos. Conferência humana
da carta e dos PDFs permanece obrigatória; execução administrativa é do agente.

Aprovação no chat é **testemunho registrado, não autenticação**. Não se verifica
criptograficamente autor do chat, identidade profissional ou mérito do parecer.
O responsável nomeado da configuração/expediente/caso continua autor fixo.
O disco é a fronteira de confiança, conforme 019 e 022; nome de agente não vira autor.

Apuração do nível, decidir-prosseguimento, sessões, vincular-restricao, autonomia,
recalibragem, encerramentos EX3/EX4 e selo após P2 continuam atos humanos no terminal.
A guarda recusa a sessão mesmo com testemunho nominal. O núcleo recebe contratos
genéricos e continua sem instrumentos, conectores ou atos do método em seu código.

O template retira de decisoes_humanas somente importar-habilitacao, definir-canais,
receber-material e registrar-listagem. As operações são declaradas em
operacoes_sessao, com etapas autorizadas, entradas e hashes. Receber/listar fora
do bloco inicial é recusado pela sessão. O selo após P2 é explicitamente humano,
por condição genérica apos_etapa. Demais decisões permanecem intactas.
Casos abertos conservam o playbook copiado, conforme 002; não há migração automática.

O comando /eiac-campo:iniciar verifica ambiente, reutiliza ~/.emcia/config.json,
calibra perfis pelas assinaturas MCP e conduz até o checklist final.
Perfis embutidos são restritos: parâmetro de contêiner, formulário ou calendário,
expressão de pai limitada ou objeto previamente listado. Assinatura sem perfil
é recusada e relatada; a presença dos três conectores não supre operação ausente.
A confirmação inicial vincula inventário e perfil; nenhuma expressão ampla é gerada.

No percurso sem retrabalho, cinco aprovações cobrem envio/plano administrativo de
rodadas, carta, PDFs/plano de retorno, abertura com árvore inteira/plano local e
compartilhamentos. A aprovação de abertura contém a aprovação da árvore inteira;
a do conjunto de compartilhamentos é separada e lista destinatário, pasta e papel.
O mesmo trecho pode cobrir os atos mecânicos descritos nesse plano; não autoriza
novo conteúdo, destinatário ou papel. Mudança exige atualização. Perfil e aceitação
são confirmações da primeira execução. Retorno de assinatura e sua conferência
precisam ser indicados pelo engenheiro, sem aprovação presumida por silêncio.

## Situação jurídica e emissão

Revisao-juridica permanece e exige resultado exato aprovado, hashes e evidência;
ciclo é texto opcional. Parecer condicionado não é convertido em aprovado.
Quando existe revisão aprovada para o hash usado, ela prevalece.

Sem ratificação, gerar aceita somente a declaração nominal explícita “uso as
minutas sem ratificação jurídica”, com texto, data e responsável na configuração.
A aceitação é reutilizada e revogável. Sem ela e sem revisão aprovada, gerar recusa
com as duas saídas possíveis. Revogação impede novas emissões, preservando anteriores.
Não há flag que dispense guarda, conferência da carta ou conferência dos PDFs.

Cada emissão guarda versão/hash da minuta, data e situação ratificada ou sem
ratificação, referindo revisão/aceitação. Controle do modelo, histórico interno,
aviso jurídico e aceitação não entram no MD/PDF do cliente. O estado da emissão
é Para assinatura. O checklist mostra minutas sem ratificação como pendência
não bloqueante; isso não representa aprovação jurídica nem documental de minuta nova.

## Relação com decisões e documentos anteriores

Esta decisão supera parcialmente 003 e 027 quanto aos atos administrativos do
bloco inicial; mantém a reserva terminal das decisões de método. Supera a exigência
de inicialização anterior à sessão em 019/022 para esse fluxo, preservando autoria
fixa e assinatura como testemunho. Ajusta 039/040 quanto ao executor da importação,
definição, recebimento/listagem e agrupamento dos compartilhamentos. Supera somente
a obrigatoriedade de ratificação jurídica da 044 para geração com aceitação explícita;
suas regras de APR-01, hashes, controle interno, resultado aprovado e base documental
permanecem. As decisões anteriores conservam seus textos históricos.

HAB-01, ROT-02, CAN-01, CAT-01 e MAN-01 precisam incorporar a interface aprovada:
propostas-artefatos.md registra as propostas, sem editar reference/metodo/.
O MAN-01 v1.0 não declara selar-apos-P2 no quadro transversal. A divergência exata
é **ato humano selar-apos-P2 ausente das seções 3.3 e 3.4**. manual_a25.py permanece
inalterado e falha em test_01; as quatro negativas continuam passando. Falha conhecida
é conferida por código, nome do teste e lista exata de divergências, nunca por
continue-on-error genérico. Nova divergência interrompe regressão e commit.

## Verificação e limites

Núcleo 0.2.46, campo 0.8.26 e playbook 0.4.20. A evidência em
.projectdocs/evidencias/bloco-inicial-conduzido/ registra linha de base integral
986/49 em Python 3.12.12, testes negativos anteriores à implementação, regressão
final integral, comparação do pacote e busca de vocabulário no núcleo.

O percurso sintético usa MCP simulado e scripts reais; cobre rodadas, PDFs,
assinaturas/evidências sintéticas, árvore, compartilhamento, canais, importação,
validação, Git e três retomadas. Não há cliente real ou conexão com conta de cliente.
A guarda depende dos hooks do runtime; a suíte não comprova todas as versões de
interfaces Google/Tally. Perfis desconhecidos continuam recusados.

Retomada lê estado e saídas; não repete operação já confirmada. API interrompida
antes da preservação do retorno exige conferir objeto remoto por id antes de
repetir. Não se promete execução única de efeitos externos sem essa conferência.
F0 liberado para execução não é F0 encerrado e não decide prosseguimento.

A busca identificou remissões antigas a instrumentos em comentários/mensagens do
núcleo. Os rótulos de diagnóstico da curadoria foram declarados no schema do campo;
condições de autoria, procedência, versão, histórico e referência permanecem iguais.
Casos sem rótulos continuam recusando pelas mesmas condições, com diagnóstico genérico.
Remissões em comentários foram retiradas. Saída de grep anterior/final e teste de
ausência de vocabulário de instrumentos/conectores acompanham a evidência.

## Nota de emenda — perfis dos conectores reais, 05/10/2026

O engenheiro determinou substituir as assinaturas hipotéticas pelo inventário
fornecido em ~/emcia-op/ensaio/inventario-mcp.json, única fonte de nomes/parâmetros.
Perfis literais conferidos por contrato ficam no campo. O núcleo apenas valida
schemas, alternativas, constantes/ids e eventos declarados, sem vocabulário de
ferramenta ou método. Parâmetro extra é recusado. Casos anteriores conservam seu
contrato; a fixture do perfil anterior verifica essa compatibilidade.

Drive search_files usa query com pai declarado; fileId de leitura/download
exige listagem registrada. create_file separa pasta pelo tipo MIME, sem conteúdo,
de arquivo comum só em entregas. parentId sempre é explícito. share_file exige
fileId de pasta declarada e emailAddress/role idênticos à aprovação. Calendar
usa calendarId, nunca o calendário padrão implícito. Tally create_new_form
exige workspaceId; publish_form exige formId declarado e conferência registrada
da preparação. Retornos ficam vinculados à chamada, finalidade e evento por hash.

O inventário fornecido tem duas limitações: não há schema auditável para montar
perguntas/campo oculto no Tally; fetch_submissions.filter só expõe datas/status,
sem filtro pelo campo oculto do caso. O engenheiro prepara no painel e filtra/
exporta manualmente as submissões do formulário declarado. O comando oferece
caminho-manual, com decisão explícita, responsável, evidência/hash, motivo e
aprovação nominal registrada. A API recusada não é executada por essa operação.
Se não houver publicação no inventário, publicar fica como ação do engenheiro;
se faltar workspaceId, criar também fica manual. Não há dispensa ou coleta
ampla seguida de filtro local. O critério de não recusar as ferramentas do
bloco se aplica às chamadas cuja garantia existe; o próprio pedido determina
o caminho manual onde a garantia falta.

create_event tem inputSchema integral não transcrito, mas parâmetros listados.
Somente campos de tipo simples explícito têm perfil; objetos sem schema e
parâmetros depreciados ficam recusados e aparecem no relatório. Não se inventam
nomes de campos de objetos nem ferramentas para publicação.

Núcleo 0.2.47, campo 0.8.27, playbook 0.4.21. Evidência em
.projectdocs/evidencias/perfis-conectores/: linha de base e regressão integral
em Python 3.12.12 e 3.14.4, inventário/hash, negativas anteriores à correção,
contrato, percurso sintético e grep. A25 conserva a mesma falha conhecida já
registrada acima, sem alteração no teste ou no método empacotado. PyYAML está
presente somente no ambiente 3.14 e acrescenta duas verificações; não é dependência
nova. Não há chamadas a contas reais nem alteração do pacote do método.

## Nota de emenda — conferência automática de formulário, 05/10/2026

Por instrução do engenheiro, o perfil incorpora `mcp__tally__load_form` com o
único parâmetro `formId`, conforme o inventário real. Somente ids criados ou
declarados no expediente/caso corrente são permitidos; outro id produz
TentativaNegada. Ferramentas fora do perfil e parâmetros extras continuam recusados.

A sessão lê o formulário pelo conector, preserva seu retorno bruto e executa a
comparação determinística com o modelo escolhido em reference/formularios/.
Texto exato, ordem, tipo e campo oculto caso são conferidos; triagem também
confere as alternativas. O adaptador utiliza o schema público de blocos Tally,
referenciado na evidência; retorno desconhecido recusa, sem reconstrução por IA.
O ciclo não fixa texto de perguntas e mantém conferência humana com PDF.
Não se altera modelo nem método canônico por inferência.

O relatório MD, com hash e vínculo ao modelo/retorno/contexto, passa a ser a
evidência. Sem divergência, o responsável confirma com o literal “conferido”.
confirmar-formulario vincula testemunho e hash; arquivo externo adicional não é
obrigatório. A alternativa manual exige PDF completo e o mesmo literal.
Divergências impedem publicação e aparecem no diagnóstico. Cada leitura nova
invalida a confirmação anterior; após correção, repete-se leitura, comparação
e confirmação. Aprovação anterior não sobrepõe relatório divergente.

A pré-condição genérica do núcleo admite seleção do último evento, valores
esperados e campo de diagnóstico, declarados pelo contrato do campo. O núcleo
continua sem modelos, blocos, conectores ou vocabulário do método. Contratos
anteriores preservam seu comportamento quando esses campos opcionais não existem.

Núcleo 0.2.48 e campo 0.8.28; playbook 0.4.21. Evidência em
.projectdocs/evidencias/conferencia-formulario/: linha de base e regressão
integral em Python 3.12.12 e 3.14.4, negativas anteriores à implementação,
fixtures sintéticas do schema oficial, relatórios/hash e calibração real.
Permanece somente a divergência A25 já registrada nesta decisão, sem alteração
do teste ou pacote canônico. Não foram chamadas contas remotas. Os dois testes
adicionais em 3.14 correspondem à disponibilidade de PyYAML.
