# Protocolo de canais externos
### Endereços do caso, efeitos externos e registros humanos

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-CAN-01 | **Versão** | 0.1 |
| **Data** | 2026-10 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Habilitação e F0–F4 | **Passo** | Todos |

---

## 1. Objetivo
Definir como o serviço recebe declarações e material, organiza sessões e publica entregáveis sem confundir organizações, casos ou versões. O canal identifica a finalidade e o endereço autorizado de uma operação; seu registro permite conferir a coerência da coleta ou da entrega com o caso.

## 2. Escopo e aplicação
Aplica-se aos formulários, ao drive compartilhado e ao calendário usados pelo engenheiro de campo. A preparação pode ser delegada, mas os atos que constituem evidência no caso são humanos. O cliente interage com pessoas e canais; o agente trabalha para o engenheiro.

Assinatura eletrônica, aceite do cliente, gravação e transcrição estão fora deste protocolo. A formalização por painel segue o EMCIA-HAB-01 e o EMCIA-ROT-02. A publicação de um entregável e o registro de sua entrega não constituem aceite.

## 3. Conteúdo

### 3.1 Declaração do método e declaração do caso
O método declara no playbook as finalidades, ferramentas, direções e etapas ou entregáveis a que se aplicam. O caso declara os endereços concretos por id, proprietário, acesso do cliente, sensibilidade, filtro e marcador. Cada definição tem versão, pessoa responsável e data; versões anteriores são preservadas e a definição gera evento com hash.

| Finalidade | Direção | Uso declarado no playbook 0.4.18 |
| :--- | :--- | :--- |
| habilitacao | Entrada | Formulários do expediente, vinculados à origem administrativa na importação; previstos em F0 |
| triagem | Entrada | Respostas ao instrumento de F0; perguntas do TRI-01 §3.3 e pontuação do §3.4 |
| documentos | Entrada | Documentação e fontes de P2 |
| amostras | Entrada | Material da linha de base em P3a e da medição em P9 |
| entregas | Saída | Publicação de E1–E5, incluindo as autorizações E3-D e E3-E |
| trabalho-interno | Entrada | Material interno EMCIA, sem acesso do cliente e sem etapa de coleta atribuída no template |
| sessoes | Agenda | Sessões de F0 e P1–P10, incluindo P3a, P3b e P3d |
| ciclo | Entrada | Monitoramento da recorrência em P10; decisão de recalibragem separada |

O template exige canal de entrada ao carregar e encerrar F0, P2, P3a, P9 e P10, nas respectivas finalidades. A presença das demais finalidades no planejamento não cria uma coleta obrigatória em cada etapa. Casos existentes conservam o próprio playbook; a migração é deliberada pelo engenheiro.

### 3.2 Propriedade e convenção por cliente
O padrão é propriedade EMCIA: drive compartilhado, workspace de formulários e calendário sob sua administração. Propriedade do cliente só é admitida quando declarada explicitamente no caso; não presume autorização de acesso.

No drive compartilhado destinado ao cliente atendido, organizar uma raiz exclusiva para cada caso, com cinco divisões: **00-habilitacao**, **entrada-documentos**, **entrada-amostras**, **entregas** e **trabalho-interno**. Os nomes orientam o provisionamento; somente os ids são usados para roteamento. A divisão interna não admite acesso do cliente. Os demais acessos devem ser definidos e confirmados por destinatário e papel.

No workspace de formulários, usar o campo oculto **caso**, com o identificador reservado ou aberto. Conservar os ids dos formulários e de cada submissão, inclusive as rodadas da habilitação. O link é preparado por `formularios.py`; publicação e envio requerem confirmação. Respostas de outro caso são excluídas da preparação local. Campo oculto e id não autenticam o respondente. Sem conector compatível, a exportação manual conserva as mesmas referências.

No calendário, cada sessão usa o marcador **[caso/etapa]**. O engenheiro confere calendário por id, participantes, data, horário e fuso antes da confirmação do evento ou convite. A referência externa de sessão é opcional no template; quando informada, deve corresponder ao canal e ao marcador. O playbook do caso pode torná-la obrigatória por camada.

### 3.3 Planejamento, provisionamento e definição em 0d
Após abrir o caso, preparar o plano por `/eiac-campo:canais` ou `canais.py planejar`. O engenheiro confere proprietário, finalidades, ids conhecidos e acessos propostos. Não procurar endereços por nome.

Para provisionar pelo MCP, o engenheiro precisa primeiro declarar um contêiner já existente e exclusivo do caso como endereço inicial. Após a confirmação no chat, o agente cria as divisões dentro desse id, conforme a regra do conector. O engenheiro define então a versão com os ids retornados. Se faltar endereço inicial declarado ou regra compatível, usar a interface externa e recolher os ids para a definição humana.

Antes da importação, executar `canais.py definir` no terminal humano, ou fornecer a declaração por `--canais` a `importar_habilitacao.py`. A importação conserva os ids dos formulários do expediente e seu vínculo com a habilitação e o hash de origem. Workspace ausente no expediente deve vir da declaração humana. Depois, gravar 00-habilitacao pelo validador e selar antes de F0, conforme o EMCIA-ROT-02 e o EMCIA-MAN-01 §3.2.

### 3.4 Preparação, confirmação e execução

| Operação | Preparação do agente | Confirmação e execução do engenheiro |
| :--- | :--- | :--- |
| Planejar | Levantar finalidades e preparar endereços por ids disponíveis | Conferir o plano; planejamento local não cria recurso externo |
| Definir | Preparar a declaração versionada | Executar `canais.py definir` no próprio terminal, fora da sessão do agente |
| Provisionar | Apresentar contêiner declarado e divisões propostas | Confirmar a criação no chat; agente executa pelo conector compatível ou engenheiro pela interface externa |
| Compartilhar | Apresentar pessoa, endereço, id de destino e papel | Confirmar cada compartilhamento separadamente no chat, antes do efeito externo |
| Publicar ou enviar | Preparar formulário, link ou arquivo emitido e destino | Confirmar publicação, upload ou envio no chat; preparação não autoriza publicação |
| Receber | Resolver canal, coletar em rascunho/entrada e preparar manifesto | Conferir coleta e executar `receber.py` no próprio terminal |
| Registrar listagem | Listar somente contêiner declarado e preparar manifesto com ids | Conferir a listagem e executar `registrar_listagem.py` no próprio terminal, antes da leitura de objetos por id |
| Entregar | Conferir emissão, versão, hash e canal de saída; preparar a publicação | Confirmar a publicação no chat; depois conferir e executar `entregar.py` no próprio terminal |
| Agendar | Apresentar calendário, participantes, horário, fuso e marcador | Confirmar criação ou convite no chat; registro de sessão permanece humano no terminal |

A confirmação no chat autoriza o efeito externo apresentado; não delega definição de canais, recebimento, registro de listagem, registro de entrega ou registro de sessão. O agente entrega o comando preparado ao engenheiro. A autoria dos registros do caso vem de pessoa nomeada.

### 3.5 Recebimento, listagem e entrega
Antes da leitura de objeto por id, registrar a listagem limitada ao contêiner declarado. O manifesto identifica a ferramenta, os argumentos da chamada, o contêiner, os objetos e a data de coleta com fuso. `registrar_listagem.py` confere o escopo, fixa o hash do registro e produz ListagemRegistrada. Listagem não autoriza escrita em fontes.

A coleta permanece em rascunho/entrada até o recebimento humano. `receber.py` confere canal da etapa corrente, objeto, contêiner, datas com fuso, filtro de caso quando aplicável e hash dos bytes. O material recebe identificador REC e origem preservada em fontes. Objeto ou hash já recebido exige decisão explícita de nova versão, com referência ao recebimento anterior; os anteriores permanecem.

Para entregar, materializar e emitir pelo Estúdio, confirmar a publicação no canal **entregas** e conservar o id remoto retornado. `entregar.py` confere a versão e o hash da emissão contra os bytes locais, o destino declarado e o destinatário nomeado; produz EntregavelEntregue. O registro não comprova leitura pelo destinatário nem aceite.

### 3.6 Limites de confiança e trava MCP
Os scripts conferem coerência dos dados locais e dos manifestos trazidos pelo agente. Não chamam APIs nem autenticam resposta remota, identidade real, permissões efetivas, conteúdo remoto ou realização da sessão. SHA-256 fixa bytes; não prova veracidade. Acesso humano de escrita ao disco permanece uma fronteira de confiança. Confirmação no chat é requisito operacional, cuja ocorrência não é comprovada pela guarda de escopo.

A trava MCP lê as regras do caso e confere nomes de ferramentas e argumentos contra os ids e operações declarados. Ferramenta desconhecida ou chamada fora do contrato é recusada com TentativaNegada. Provisionamento de estrutura possui operação própria; publicação de material só vai ao canal de entregas.

O engenheiro deve ajustar os dados às assinaturas do conector instalado, mantendo o escopo. Não existe formato universal de argumentos MCP. O disparo real de hooks foi demonstrado no Claude Code 2.1.283 com MCP stdio local sintético, conforme a decisão 040; isso não comprova suporte em outro runtime ou conector. A autorização operacional deve respeitar essa limitação.

## 4. Condição de aceite
Este protocolo está pronto quando cada operação distingue preparação, confirmação e execução; cada endereço é resolvido por id; o planejamento identifica proprietário e acessos; listagem, recebimento e entrega preservam origem, autoria e integridade; e o engenheiro consegue reconhecer os limites da conferência local e da trava MCP sem atribuir autenticação ou aceite aos registros.

## 5. Referências
- EMCIA-HAB-01 — Protocolo de habilitação, §3.3.4 e §3.4.
- EMCIA-ROT-02 — Roteiro de habilitação, em auxiliares.
- EMCIA-MAN-01 — Manual de aplicação, §3.2–3.6; playbook operacional 0.4.18.
- EMCIA-CAT-01, EMCIA-CAM-01, EMCIA-CTX-01 e EMCIA-TRA-01.
- emcia-marketplace — decisões 039–042; referências de canais e habilitação; scripts de abertura, importação, canais, formulários, listagem, recebimento e entrega; evidências de habilitação-0d, canais-externos e parte-a-operacional.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 2026-10 | Celso do Vale | Versão inicial conforme a operação entregue nas decisões 039–042: canais por id, propriedade, confirmações, atos humanos, integridade e limites MCP | pendente |
