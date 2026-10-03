# Habilitação — fluxo operacional

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-HAB-fluxo-operacional-proposta | **Versão** | 0.2 |
| **Data** | 2026-10 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Anterior a F0 | **Passo** | 0a–0d |

---

## 1. Objetivo
Organizar coleta administrativa, esclarecimentos, formalização, assinatura e passagem para o caso, distinguindo preparação automatizada, decisão humana e evidência preservada.

## 2. Escopo e aplicação
Complementa HAB-01 e ROT-02 com a operação de formulários e de assinatura pelo painel escolhido pelo cliente. Conserva os templates HAB-01/02/03 e a revisão humana da carta. A operação de canais após a abertura segue CAN-01. Nenhuma proposta ou resultado de teste atribui aprovação aos documentos.

## 3. Conteúdo

### 3.1 Fluxo proposto

Cliente responde ao formulário → engenheiro revisa → havendo dúvidas, prepara uma rodada de esclarecimentos → cliente responde → engenheiro resolve ou reabre cada pendência → informações consolidadas → minutas dos três documentos → revisão humana → assinatura das partes → conferência das evidências → acesso efetivo (0c) → abertura → planejamento/provisionamento → definição de canais (ou --canais junto da importação) → importação → gravação de 00-habilitacao pelo validador → selo confirmado (0d) → F0.

O “ok” do engenheiro encerra a revisão das informações. Não equivale a assinatura, concessão de acesso ou conclusão da habilitação. Cada passagem conserva os critérios do protocolo.

O cliente interage com formulários e pessoas. O agente auxilia o engenheiro, conforme a decisão 008 do marketplace. Publicar perguntas e encaminhar documentos exige revisão do engenheiro; respostas nunca autorizam o agente a decidir pelo cliente.

### 3.2 Coleta inicial e esclarecimentos

O formulário inicial reúne declarações sobre 0a, condições de formalização e disponibilidade futura de acesso. Perguntas sobre 0b e 0c não significam que essas etapas foram cumpridas. Não solicitar credenciais, bases de dados ou documentos operacionais nesta coleta.

Antes de existir caso, usar um identificador de habilitação. Manter o expediente fora dos repositórios da ferramenta e do método. Na abertura, registrar a correspondência entre esse identificador e o identificador do caso.

Para cada resposta, conservar identificação do formulário e da submissão, versão das perguntas, data de recebimento, respondente declarado e cópia original. O nome declarado não é prova de identidade nem de competência para assinar. A consolidação deve apontar para as respostas de origem; não substituir os originais.

Cada pendência contém:

| Campo | Conteúdo |
|---|---|
| Identificação | Habilitação, rodada e identificador estável da pendência |
| Origem | Pergunta e resposta que motivaram a dúvida |
| Esclarecimento | Pergunta objetiva aprovada pelo engenheiro |
| Efeito | Etapa ou documento impedido enquanto não for resolvida |
| Resposta | Submissão, respondente declarado e data |
| Decisão | Aberta, respondida, resolvida ou reaberta; motivo, pessoa responsável e data |

Criar um formulário de esclarecimentos por habilitação e rodada, contendo apenas as pendências daquela rodada. Conservar as versões anteriores. Uma resposta nova não apaga a anterior; divergências ficam explícitas para decisão humana. Várias pendências podem ser respondidas no mesmo formulário.

O vínculo entre formulário, rodada e habilitação deve ser conferido no registro interno. Um identificador em URL ou campo oculto não autentica o respondente. Resposta duplicada não gera segunda transição; resposta de rodada antiga não encerra pendência atual automaticamente.

Ausência de resposta mantém o expediente aguardando. Recusa explícita de requisito produz registro com causa e condição necessária para retomada. Nenhuma negativa é silenciosa.

### 3.3 Preparação dos documentos

Após qualificação em 0a e resolução das pendências que afetam a formalização, preencher os templates existentes. Não inventar informações ausentes.

| Documento | Conteúdo a consolidar |
|---|---|
| HAB-01 — Carta de escopo | Organização, processo e limites, participantes, escopo, entregáveis e restrições |
| HAB-02 — Confidencialidade | Partes, finalidade, informações abrangidas e condições de tratamento |
| HAB-03 — Consentimento | Autorizações de gravação, fontes, processamento por IA, ambientes permitidos e restrições |

Separar dados declarados pelo cliente, decisões registradas pelo engenheiro e cláusulas do template. Todo campo preenchido deve ter origem recuperável. Campos desconhecidos impedem finalizar a minuta quando necessários ao compromisso; não usar “não se aplica” por suposição.

Conferir signatários por documento: a pessoa que responde, o patrocinador e a pessoa competente para assinar podem ser diferentes. Os templates atuais também preveem assinatura da parte EMCIA. Conferir a revisão jurídica já exigida pelo HAB-02 antes do uso contratual.

### 3.4 Assinatura como etapa própria de 0b

Gerar os três documentos finais em PDF, revisar e congelar suas versões, encaminhá-los para assinatura e recolher os arquivos assinados com as evidências disponíveis.

**Orientação operacional confirmada:** começar apenas pelo painel da ferramenta de assinatura, sem integração com o plugin. O cliente pode escolher a ferramenta em cada engajamento. Não há fornecedor obrigatório. Essa escolha não resolve as demais decisões de método pendentes.

#### Operação inicial pelo painel

1. O plugin prepara os documentos e o engenheiro revisa os PDFs finais e os signatários exigidos.
2. O cliente indica a ferramenta. Cliente e engenheiro combinam quem operará o painel e recolherá os arquivos finais.
3. A pessoa responsável pela operação carrega os PDFs revisados no painel, cadastra os signatários e encaminha a solicitação de assinatura.
4. As partes assinam pela ferramenta escolhida. O acompanhamento de pendências, recusas e prazos é manual.
5. A pessoa responsável baixa os documentos assinados e os comprovantes ou relatórios disponíveis e os entrega ao engenheiro.
6. O engenheiro confere as evidências e registra os arquivos e o resultado da conferência no expediente de habilitação, pelos mecanismos autorizados. O controle de 0b usa esses registros.

Nesta versão, o plugin não acessa o serviço de assinatura por API ou MCP, não recebe webhooks e não consulta automaticamente o andamento. Sua responsabilidade é preparar os documentos e registrar o retorno e a conferência humana. Uma integração futura depende de escopo próprio; não é condição para operar a habilitação.

A ferramenta escolhida deve permitir recolher os três documentos finais com as assinaturas exigidas e evidências suficientes para a conferência descrita abaixo. A escolha do fornecedor não dispensa essas condições.

O método deve exigir evidência, sem depender de um fornecedor específico. Para cada documento registrar:

- código e versão do template; versão e hash do PDF encaminhado;
- pessoas e papéis exigidos para assinatura, com competência conferida pelo engenheiro;
- identificador da solicitação ou envelope, quando houver;
- estado por signatário: aguardando, assinado, recusado, expirado ou cancelado;
- arquivo final assinado, hash próprio e comprovante ou relatório de assinatura disponível;
- data, pessoa e resultado da conferência, incluindo vínculo entre versão enviada e versão assinada.

Não exigir igualdade entre o hash do PDF enviado e o do PDF assinado: a assinatura pode modificar o arquivo. Guardar ambos e conferir sua vinculação. Um status de fornecedor, isoladamente, não substitui o documento final nem a conferência.

O registro do engenheiro de que o cliente aceitou continua sendo testemunho, conforme a decisão 008; não constitui por si a assinatura.

**Passagem de 0b:** todos os documentos exigidos estão na versão vigente, assinados pelas pessoas competentes e com evidência conferida. Falta de assinatura, recusa, expiração, signatário divergente ou conteúdo alterado mantém a etapa pendente ou registra a recusa pertinente.

Se o conteúdo mudar após envio, cancelar ou substituir a solicitação e emitir nova versão para assinatura. Preservar a anterior como histórico. Mudança após assinatura exige nova formalização do conteúdo afetado antes de utilizá-lo.

#### Alternativa: assinatura no Tally

O Tally oferece assinatura eletrônica simples, conserva a assinatura como imagem e permite exportar a submissão assinada em PDF. Isso foi confirmado na [documentação oficial](https://tally.so/help/electronic-signatures), consultada em 25/09/2026.

Essa capacidade não comprova, sozinha, o fluxo exigido para estes três documentos e ambas as partes. Para adotá-la, demonstrar que o conteúdo integral e a versão de cada documento estão vinculados ao ato de assinatura, que todas as partes exigidas assinam e que as evidências podem ser preservadas e conferidas. Não colar uma imagem de assinatura em um documento gerado posteriormente.

A escolha da modalidade e sua adequação contratual ficam pendentes de decisão humana. A existência do campo de assinatura não resolve essa escolha.

### 3.5 Acesso e abertura

Somente depois de 0b concluída, confirmar em 0c patrocinador, executor liberado, agenda reservada e acesso efetivo a pelo menos uma fonte do processo. Registrar acesso concedido, negado, motivo e restrição por item. Declaração de disponibilidade no formulário não comprova acesso efetivo.

Em 0d, seguir o checklist do EMCIA-ROT-02: abrir com pacote e manifesto conferidos; planejar e provisionar; definir canais antes ou junto da importação; importar pelo terminal humano; gravar 00-habilitacao pelo validador; selar com commit confirmado no Git; somente então iniciar F0. A importação conserva PDFs assinados, evidências e matriz, com origem, datas, hashes e vínculo com o expediente. Material operacional é coletado em rascunho e recebido pelo engenheiro, sem colocação direta em fontes. Procedência não é atribuída por julgamento de modelo nem elevada pelo recebimento.

Registrar o desfecho e selar o estado inicial antes de F0. Uma falha técnica em 0d é registrada e corrigida com repetição da etapa. A restrição nunca dispensa um dos quatro pré-requisitos; acompanha o item afetado nos entregáveis. Perda superveniente de pré-requisito suspende o percurso conforme o protocolo.

### 3.6 Decisões recebidas e limite documental

1. **Processamento anterior a 0d — aprovado:** somente informações administrativas, em expediente separado, com origem e condições de tratamento previamente registradas. O protocolo incorpora essa exceção na seção 3.7. Dados operacionais continuam aguardando 0d.
2. **Conteúdo da carta — manter com revisão humana:** o usuário decidiu manter o template atual e exigir revisão humana antes da emissão. A divergência de conteúdo permanece explícita; o agente não altera fases, entregáveis ou limites por inferência.
3. **Identificador antes do caso — aprovado:** reservar o identificador do futuro caso e indicar nos documentos que ele ainda não foi aberto.

### 3.7 Implementação e verificação

O expediente administrativo é operado por /eiac-campo:habilitacao e habilitacao.py, com condições de tratamento, respostas e rodadas, revisão humana, documentos versionados, geração de PDFs, assinatura por painel e conferência de prontidão. Os templates HAB permanecem intactos; sua existência não implica aprovação. O agente não decide competência, assinatura, acesso ou desfecho.

A operação posterior foi entregue pelas decisões 039–042, no playbook 0.4.18, campo 0.8.21 e núcleo 0.2.44:

| Entrega | Comportamento disponível | Limite |
| :--- | :--- | :--- |
| 039 — passagem ao caso | Abertura com pacote e manifesto conferidos; importação humana de PDFs assinados, evidências e matriz; rascunho para validador; F0 exige evento importado e selo confirmado no Git | A abertura não substitui importação; reimportação exige decisão explícita antes de qualquer etapa encerrada e não implementa retomada durante o percurso |
| 040 — canais externos, E1–E7 | Finalidades e direções no método, ids no caso; provisionamento com confirmação, migração de formulários do expediente, formulários com campo oculto caso, recebimento REC, registro de listagem e de entrega, referência de sessão e guarda de escopo MCP | Confere coerência local; não autentica origem, identidade ou permissões. Assinatura, aceite, gravação e transcrição fora do escopo; hooks dependem do runtime e da assinatura do conector |
| 041 — destino das restrições | RH-xx vinculado a F curada ou dispensado com motivo pelo engenheiro em P2; cobertura obrigatória no encerramento; histórico e revisão explícita; marcas no ponto de cada asserção afetada | Não concede acesso negado nem deduz vínculo de nomes; E1 de caso restrito aguarda resolução em P2; relação REC → F precisa ser explícita e íntegra |
| 042 — selo após encerramento | P3b exige selo confirmado no Git após o último encerramento de P2, incluindo o prefixo correspondente da trilha | Evento isolado, commit comum posterior à tentativa recusada ou Git inacessível não satisfaz; habilidade humana continua não delegável |

O contrato parcial de restrições da 039 foi completado pela 041; não permanece pendência de destino. As instruções técnicas de habilitação do marketplace que ainda descrevem o pacote D como parcial são anteriores à 041; o comportamento atual está em restricoes.py, entregaveis.py e no produto de P2 do playbook. O procedimento revisado não incorpora a limitação histórica como vigente.

A evidência final da parte A registra **919 verificações em 46 módulos**, aprovadas em Python 3.12.12, sem PyYAML, além de dois percursos completos sintéticos, com e sem restrição. Os percursos chegaram a F0–P10 e emitiram E1–E5; o restrito adiou E1 até P2. Esses resultados são evidência da implementação, não aprovação destes documentos nem validação em cliente real.

O teste MCP real documentado em E7 confirmou chamada e hook no Claude Code 2.1.283 com ferramenta stdio local sintética, e recusa com TentativaNegada para ferramenta não declarada. Não comprova funcionamento em outro runtime ou conector. Os scripts não executaram efeitos externos em canais reais de clientes. A confirmação no chat permanece exigida para criação, compartilhamento, publicação, convite e envio; atos de registro são humanos no terminal.

Conservar o ajuste editorial pendente do formulário publicado: explicar que o envio inicia revisão e pode gerar esclarecimentos, formalização e assinatura; perguntas de 0c registram disponibilidade declarada, sem comprovar acesso efetivo. Condições de gravação e ambiente permitido exigem definição própria; um “sim” não autoriza tratamento irrestrito. Os formulários publicados e os templates não foram alterados por estas implementações.

## 4. Condição de aceite
O fluxo está pronto quando cada passagem possui registro recuperável, a formalização exige documentos e evidências conferidos, os quatro pré-requisitos precedem F0, e o checklist de 0d distingue abertura, canais, importação, gravação e selo confirmado. A descrição de implementação deve corresponder às decisões 039–042 e ao playbook 0.4.18, respeitando seus limites.

## 5. Referências
EMCIA-HAB-01, EMCIA-ROT-02, EMCIA-CAN-01, EMCIA-MAN-01, EMCIA-CTX-01 e EMCIA-TRA-01; templates HAB-01/02/03. emcia-marketplace: decisões 039–042, referências e comandos de habilitação/canais, scripts operacionais e evidências habilitacao-0d, canais-externos e parte-a-operacional. A fonte oficial Tally citada na seção 3.4 conserva a data de consulta da edição anterior.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.2 | 2026-10 | Celso do Vale | Revisão da edição anterior de 25/09/2026 sem versão explícita; remissão ao ROT-02 e sequência de 0d; implementação e evidência entregues pelas decisões 039–042, com limites e pendências editoriais preservados | pendente |
