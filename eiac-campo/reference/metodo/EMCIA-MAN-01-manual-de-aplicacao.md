# Manual de aplicação do método
### Ordem de leitura, percurso e atos do engenheiro de campo

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-MAN-01 | **Versão** | 0.4 |
| **Data** | 2026-10 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Todas | **Passo** | Todos |

---

## 1. Objetivo
Permitir que um engenheiro de campo que não participou da construção do método o aplique com o Estúdio, na ordem de uso, sabendo em cada etapa o que o agente prepara, o que só ele decide e o que encerra a etapa.

## 2. Escopo e aplicação
Aplica-se a quem conduz um caso. Pressupõe a leitura do EMCIA-MET-01. Não se aplica à manutenção do Estúdio, que segue o EMCIA-ESP-01, o EMCIA-ARQ-01 e o EMCIA-IMP-01. Substitui o Guia do Engenheiro de Campo de setembro de 2026, que descrevia a versão 0.3.0 do playbook.

Esta revisão toma como referência o playbook operacional **0.4.18**, campo **0.8.22** e núcleo **0.2.44**, após as decisões 039–042, e incorpora a decisão humana de prosseguimento em F0 definida no CAT-01 v0.5. O ato ainda depende de implementação no marketplace, conforme a validação da seção 4; o manual não afirma que a versão atual já o executa. O ESP-01 permanece como documento da prova de conceito; não é a referência da lista de limites operacionais desta versão. Casos existentes conservam o playbook com que foram abertos; migração exige decisão humana.

## 3. Conteúdo

### 3.1 Ordem de leitura

| Momento | Documento | Para quê |
| :--- | :--- | :--- |
| Antes do primeiro caso | EMCIA-MET-01 | O percurso, os inegociáveis e as regras do método |
| Antes do primeiro caso | EMCIA-CAT-01 | O que o agente pode fazer e o que é do engenheiro |
| Antes do primeiro caso | EMCIA-TRI-01 | Como o nível do caso é apurado |
| Antes de F0 | EMCIA-HAB-01 e EMCIA-ROT-02 | Habilitação e checklist de abertura, importação e selo |
| Na preparação de canais | EMCIA-CAN-01 | Endereços por id, confirmações e registros na fronteira externa |
| Durante o caso | EMCIA-CAM-01 | O protocolo de cada passo em campo |
| Durante o caso | EMCIA-TRA-01 | Procedência, pendências e validações transversais |
| Durante o caso | EMCIA-ROT-01 | O levantamento presencial das regras não documentadas |
| Durante o caso | EMCIA-CTX-01 | O registro da camada de contexto |
| Durante o caso | EMCIA-E1 a EMCIA-E5 | Os modelos dos entregáveis |
| Quando surgir dúvida de termo | EMCIA-GLO-01 | Definições do método |
| Não usar como critério | EMCIA-VER-01 | Plano substituído, mantido como registro |

### 3.2 Antes do caso
Conclua 0a–0c pelo EMCIA-HAB-01 e pelo EMCIA-ROT-02, em expediente administrativo separado: revisão humana, formalização vigente, assinaturas conferidas e acesso efetivo. Informações administrativas anteriores ao caso seguem o HAB-01 §3.7. Instale o Estúdio e rode os testes negativos conforme o INSTALACAO.md do marketplace antes de abrir caso real.

Em 0d, execute a sequência abaixo:

1. **Abrir.** Execute novo-caso.sh com o identificador reservado e o responsável nomeado. abrir_caso.py confere e copia o pacote controlado do método e seu manifesto, antes de criar o caso, e confere a cópia. Informar --expediente é opcional nessa chamada e confere prontidão e identidade; não importa o expediente.
2. **Planejar e provisionar.** No caso aberto, use /eiac-campo:canais e canais.py planejar. Confira o plano, os ids e a propriedade EMCIA ou do cliente explicitamente declarada. Cada criação, compartilhamento, publicação, convite ou envio exige confirmação no chat. Para provisionar pelo MCP, declare primeiro um contêiner exclusivo do caso; sem endereço ou regra compatível, use a interface externa, conforme CAN-01.
3. **Definir.** No próprio terminal, execute canais.py definir com os ids provisionados. Alternativamente, forneça a declaração humana completa por --canais na importação. Canais precisam existir antes da importação ou ser definidos junto dela; não ficam para depois.
4. **Importar.** Execute importar_habilitacao.py no terminal humano, fora da sessão do agente. O expediente é obrigatório: confere prontidão, identidade reservada e responsável, copia PDFs assinados, evidências e matriz, preserva origem e hashes e registra HabilitacaoImportada. Os ids de formulários do expediente são conservados nos canais. Não copie material operacional diretamente para fontes.
5. **Gravar 00-habilitacao.** Confira o rascunho produzido e grave caso/00-habilitacao.md por validar.py. As marcas documentais V não transformam declarações de acesso em verificação independente. Gravação e selo são operações distintas.
6. **Selar.** Execute selar.py e confira o selo no estado e no histórico Git. O commit precisa confirmar o selo posterior à importação e conter o evento e o prefixo correspondente da trilha. SeloAplicado isolado, commit recusado ou Git inacessível mantém F0 bloqueado.
7. **Iniciar F0.** Somente após as condições anteriores, carregue o enquadramento. O caso conserva a versão do método em que foi aberto, conforme MET-01 §3.7.6.

Reimportação só é admitida antes de encerrar qualquer etapa e exige decisão explícita que cite a importação anterior, motivo, pessoa responsável e data; exige novo selo. Não é mecanismo de retomada após perda de pré-requisito durante o percurso. Em caso com RH pendente, E1 aguarda vínculo ou dispensa em P2 antes da materialização.

### 3.3 O percurso
Para cada etapa: o comando que o agente executa, os atos que só o engenheiro executa, o produto que o Estúdio confere para encerrá-la e o entregável que ela alimenta. Atos marcados com níveis entre parênteses só são exigidos nesses níveis.

| Etapa | Camada N1 · N2 · N3 | Comando do agente | Ato do engenheiro | Produto conferido pelo Estúdio | Entregável |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F0 | EX1 · EX1 · EX1 | `/eiac-campo:enquadrar` | `apurar-nivel`, `decidir-prosseguimento` | Decisão de prosseguimento registrada | E1 |
| P1 | EX2 · EX2 · EX3 | `/eiac-campo:mapear-contexto` | `encerrar-camada-humana` (N3) | — | E2 |
| P2 | EX2 · EX2 · EX3 | `/eiac-campo:mapear-fontes` | `vincular-restricao`, `encerrar-camada-humana` (N3) | Todos os RH-xx vinculados a fontes ou dispensados com motivo | E2 |
| P3a | EX2 · EX3 · EX3 | `/eiac-campo:medir` | `registrar-sessao`, `encerrar-camada-humana` (N2, N3) | Linha de base registrada | E2 |
| P3b | EX4 · EX4 · EX4 | — | `registrar-sessao`, `encerrar-camada-humana` | — | E2 |
| P3d | EX3 · EX3 · EX3 | `/eiac-campo:confrontar` | `registrar-sessao`, `encerrar-camada-humana` | — | E2 |
| P4 | EX2 · EX3 · EX3 | `/eiac-campo:priorizar` | `encerrar-camada-humana` (N2, N3) | — | E3 |
| P5 | EX3 · EX3 · EX3 | `/eiac-campo:classificar` | `registrar-campo`, `encerrar-camada-humana` | Classificação tecnológica registrada | E3 |
| P6 | EX3 · EX3 · EX3 | `/eiac-campo:operacionalizar` | `validar-operacional`, `encerrar-camada-humana` | OP validado | E4 |
| P7 | EX4 · EX4 · EX4 | `/eiac-campo:governar` | `decidir-autonomia`, `encerrar-camada-humana` | AUT decidido | E4 |
| P8 | EX3 · EX3 · EX3 | `/eiac-campo:pilotar` | `revisar-piloto`, `encerrar-camada-humana` | Conjunto revisado | E5 |
| P9 | EX3 · EX3 · EX3 | `/eiac-campo:medir-valor` | `encerrar-camada-humana` | Métrica de resultado apurada | E5 |
| P10 | EX4 · EX4 · EX4 | `/eiac-campo:recalibrar` | `definir-rotina`, `decidir-recalibragem`, `registrar-recorrencia`, `encerrar-camada-humana` | Rotina com responsável e cadência | E5 |

P3b não tem comando, por desenho: o levantamento é presencial e não delegável, e segue o EMCIA-ROT-01. Em P10, o monitoramento opera em EX2 e a decisão em EX4. Os entregáveis são materializados com `/eiac-campo:emitir`, depois que todas as etapas do seu portão estiverem encerradas.

A camada da tabela é a camada de encerramento e decisão; as HBs conservam a camada de preparação do CAT-01 Anexo A, que não pode ser superior à camada da etapa no mesmo nível. A fonte da correspondência etapa → HBs → AG é o CAT-01 v0.5 Anexo C. As decisões humanas resolveram essa correspondência no método; sua reprodução no catálogo e no playbook depende da revisão do marketplace, conforme o Anexo D do CAT-01.

Antes de P3b, aplique um selo confirmado no Git após o último encerramento de P2; a tentativa de selo sem commit confirmado não basta. Em P2, vincular-restricao cobre o vínculo a fonte F curada e a dispensa motivada por restricoes.py, no terminal humano, em todos os níveis. Sem RH importado, a cobertura é vazia. Revisão exige decisão que cite RH e versão anterior, com pessoa, motivo e data; após P2, somente revisão de registro existente. A marca acompanha cada asserção que cita fonte restrita, conforme HAB-01 §3.4 e CTX-01 §3.7.

### 3.4 Atos transversais
Valem em qualquer etapa e são sempre do engenheiro: `registrar-sessao`, `satisfazer-inegociavel`, `satisfazer-inegociavel-campo` e `encerrar-camada-humana`. A selagem do caso também é ato do engenheiro, com autor nomeado.

**Ato específico de F0.** Nos três níveis, `decidir-prosseguimento` é executado pelo engenheiro no próprio terminal, fora da sessão do agente. Ele confere o conteúdo da ficha E1 preparado para o enquadramento e registra a decisão de prosseguir, com pessoa nomeada e referência à ficha que a fundamenta. Esse registro é condição de encerramento de F0 e não é substituído por apurar o nível ou confirmar no chat. A ficha usada como fundamento precede a emissão formal de E1, que continua sujeita ao portão e à resolução de RH pendente. Não há comando operacional deste ato no playbook 0.4.18; sua declaração e sua trava dependem da implementação no marketplace. O agente pode preparar o conteúdo e, quando houver implementação, o comando; não pode registrar a decisão.

Os atos na fronteira externa seguem CAN-01 e são executados no próprio terminal, fora da sessão do agente:

| Ato declarado | Componente | O que o engenheiro confere |
| :--- | :--- | :--- |
| `registrar-listagem` | registrar_listagem.py | Contêiner e argumentos da chamada dentro do escopo declarado, ids de objetos e data com fuso; registrar antes da leitura de objeto por id |
| `receber-material` | receber.py | Coleta em rascunho/entrada, origem, canal da etapa, filtro do caso, datas e hash; nova versão exige decisão explícita |
| `entregar-material` | entregar.py | Emissão, versão, hash dos bytes locais, destino entregas e destinatário nomeado, após publicação confirmada |

O agente lê somente pelos ids autorizados e prepara manifestos e comandos. Criação, compartilhamento, publicação, convite e envio exigem confirmação explícita no chat antes de cada efeito externo; cada compartilhamento apresenta pessoa, endereço, id e papel. Confirmar no chat não autoriza o agente a executar os atos humanos no terminal. Registro de entrega não é aceite.

A referência externa da sessão é opcional no template; quando informada, precisa corresponder ao id do canal e ao marcador [caso/etapa]. O caso pode exigir essa referência por camada. O Estúdio não lê gravações nem transcrições neste escopo.

### 3.5 Quando o Estúdio recusa
Uma recusa é a trava funcionando, e não um erro. Para cada recusa:
1. Leia o motivo na trilha do caso, em `registro/eventos.jsonl`. Recusa real deixa evento `TentativaNegada` com o motivo.
2. Se o motivo for uma decisão humana, peça ao agente o comando pronto e execute-o no seu próprio terminal, no diretório do caso, fora da sessão do agente. Informar o seu nome dentro da sessão do agente não basta: a trava reconhece a origem da chamada (EMCIA-CAT-01 §3.5.3).
3. Se o agente recusar sem que a trilha registre `TentativaNegada`, a recusa foi do modelo, e não da trava. Comportamento correto não é prova de verificação.
4. Consultas de ajuda também geram `TentativaNegada`. Ao contar recusas, leia o motivo de cada uma.

### 3.6 O que esta versão não faz por você
As conferências operacionais incluem manifesto na abertura, importação e selo confirmado antes de F0, canais declarados, coerência local de listagem/recebimento/entrega, cobertura dos RH em P2, marcas localizadas na materialização e selo confirmado após P2 para P3b. As tarefas e limites que permanecem são:

1. Registrar no caso a avaliação do patrocínio em P1, a verificação do dado em P2 e a decisão de prioridade em P4, também nos níveis N1 e N2.
2. Conferir os produtos substantivos de F0, P1, P2, P3b, P3d e P4 antes de encerrar. Em P2, a cobertura de RH é conferida, mas não comprova a qualidade do inventário ou a adequação do dado. A tabela mostra os produtos efetivamente exigidos pelo Estúdio; campos e sessões não comprovam a completude de todo conteúdo do método.
3. Conferir de novo um inegociável já satisfeito quando o artefato ou o responsável mudar, antes de emitir.
4. Manter um único registro vigente de piloto, especificação operacional e termo de autonomia, em versões crescentes. A rotina de recalibragem possui seleção e conferência próprias de versão e responsável; essa conferência não se estende automaticamente aos demais produtos.
5. Não operar fora de um caso aberto: a guarda só confere o que ocorre dentro dele.
6. Conferir origem remota, identidade real, permissões efetivas, conteúdo e autorização de tratamento. Hash fixa bytes, não veracidade; os scripts não autenticam a origem e o diagnóstico do manifesto copiado não autentica o manifesto.
7. Garantir a confirmação no chat antes dos efeitos externos. A guarda MCP confere escopo, não a ocorrência da confirmação. Ajustar regras aos nomes e argumentos do conector instalado e verificar suporte a hooks no runtime utilizado; a evidência existente é do Claude Code 2.1.283.
8. Conduzir assinatura pelo painel escolhido e conferir evidências; obter aceite por procedimento próprio quando aplicável. Assinatura, aceite, gravação e transcrição não são executados pelos canais deste escopo.

### 3.7 Quando algo não fizer sentido
O marketplace mantém em `decisoes/` o registro de cada decisão de construção, com contexto, decisão e consequência. Antes de propor mudança no que parecer burocracia, leia a decisão correspondente.

## 4. Condição de aceite
O manual corresponde integralmente à versão operacional quando a tabela da seção 3.3 coincide com o playbook declarado: mesmas etapas, mesmas camadas, comandos existentes, atos declarados, produtos e portões. Esta revisão foi conferida diretamente pela função conferir() de testes/manual_a25.py, sem alterar código ou playbook, contra o playbook 0.4.18 no commit ebb6bbda55ea7403bc0e09a0bc316f0a1071cf4f do marketplace master. O único resultado admitido nesta revisão é a lista com “F0: ato decidir-prosseguimento não declarado”, dependente da implementação no marketplace. Qualquer outra divergência interrompe a revisão. Os quatro testes negativos de etapa, camada, ato e comando acompanham a conferência. Após a implementação do novo ato, a validação deve devolver lista vazia. A validação não concede aprovação documental; esta permanece pendente.

## 5. Referências
EMCIA-MET-01, EMCIA-CAT-01, EMCIA-TRI-01, EMCIA-CAM-01, EMCIA-TRA-01, EMCIA-ROT-01, EMCIA-ROT-02, EMCIA-CTX-01, EMCIA-HAB-01, EMCIA-CAN-01, EMCIA-GLO-01 e EMCIA-E1 a EMCIA-E5. EMCIA-ESP-01, EMCIA-ARQ-01 e EMCIA-IMP-01 permanecem referências da PoC e da construção. Referência operacional: emcia-marketplace, decisões 039–042, playbook 0.4.18 e evidências habilitacao-0d, canais-externos e parte-a-operacional.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 01/10/2026 | Celso do Vale | Versão inicial, conferida contra o playbook 0.4.9 (ação 4.5); substitui o Guia do Engenheiro de Campo | — |
| 0.2 | 2026-10 | Celso do Vale | Operação das decisões 039–042 e playbook 0.4.18; canais antes ou junto da importação, RH em P2, fronteira externa e limites próprios. Validação autorizada em checkout temporário, sem alterar código: conferir() do A25 retornou lista vazia e os quatro testes negativos passaram; dispensada a expectativa histórica de lacunas do manual v0.1 | pendente |
| 0.3 | 2026-10 | Celso do Vale | Ato humano decidir-prosseguimento em F0 nas seções 3.3 e 3.4, como condição de encerramento baseada na ficha E1; retirada desse item dos limites de 3.6; correspondência canônica de HBs no CAT-01 v0.5, sem manter lacunas da decisão 020 como indefinição de método. Validação sem alterar código: conferir() do A25 contra o playbook 0.4.18 retornou somente “F0: ato decidir-prosseguimento não declarado”; os quatro testes negativos passaram. Divergência dependente da implementação no marketplace; lista vazia exigida após essa implementação | pendente |
| 0.4 | 2026-10 | Celso do Vale | produto de F0 alinhado ao contrato de decidir-prosseguimento | pendente |
