# Fronteira de delegação
## Camadas de execução e catálogo de agentes e habilidades

| Código | EMCIA-CAT-01 | Versão | 1.0 |
| :--- | :--- | :--- | :--- |
| **Data** | 03/10/2026 | **Estado** | Aprovado |
| **Responsável** | Celso do Vale | **Aprovação** | Celso do Vale · 03/10/2026 |
| **Fase** | F0 a F4 — todas | **Passo** | 1 a 10 — todos |

---

## 1. Objetivo
Separar, ao longo dos dez passos do método, o que pode ser delegado a agentes do que exige julgamento humano, e catalogar as atividades delegáveis com insumo, saída e critério de verificação. O catálogo é o que torna a delegação auditável: sem ele, a fronteira existe como intenção e não como controle.

## 2. Escopo e aplicação
Aplica-se ao trabalho do engenheiro de campo apoiado pelo estúdio. Os agentes aqui catalogados operam para o engenheiro, não para a organização cliente: o interlocutor de um agente é sempre quem conduz o método.

Não se aplica aos agentes especificados para o cliente no blueprint. Aqueles são objeto do passo 5 e do entregável E3; estes são instrumento de execução do próprio percurso.

## 3. Conteúdo

### 3.1 O critério de corte
Uma atividade pode ser delegada a agente se passar nos três testes. Falhar em qualquer um a devolve ao humano.

| Teste | Pergunta | Falha quando |
| :--- | :--- | :--- |
| **Fonte** | A resposta está no que a organização consegue declarar? | Depende de regra não documentada ou de observação em campo |
| **Verificabilidade** | O erro é detectável por quem recebe a saída? | O erro passa despercebido ou parece plausível |
| **Compromisso** | A saída é informação, ou é recomendação que alguém assina? | Gera decisão de investimento, contrato ou risco |

> **Regra prática:** o agente responde “o que é”; o humano responde “o que fazer”. Descrever o estado é delegável. Decidir o movimento não é.

### 3.2 As três naturezas de trabalho

| Natureza | Definição |
| :--- | :--- |
| **Automatizado** | A saída do agente avança sem decisão humana intermediária. Cabe apenas onde os três testes passam com folga. |
| **Híbrido** | A saída é produzida por agente e não avança sem decisão humana registrada. Não é automação suavizada: se a decisão pode ser pulada, a atividade é automatizada; se o agente não consegue produzir a saída, é humana. |
| **Humano** | A atividade não é executada por agente em nenhuma etapa. O agente pode organizar o material de apoio, mas não produz a saída. |

### 3.3 As quatro camadas de execução

| Camada | Natureza | O que executa e o que entrega |
| :--- | :--- | :--- |
| **EX1 — Conversacional** | Automatizado e híbrido | Triagem, estruturação da dor, coleta declarativa e apuração do nível. Entrega a ficha de enquadramento. |
| **EX2 — Analítica** | Automatizado e híbrido | Consulta de referência, mapa de valor, classificação tecnológica, estimativas, minutas e avaliação. Entrega dossiê estruturado, com hipóteses marcadas como hipóteses. |
| **EX3 — Verificação** | Humano | Confronto entre declarado e observado e validação da linha de base. Entrega o dossiê verificado, com as correções registradas. |
| **EX4 — Julgamento** | Humano | Levantamento das regras não documentadas, priorização, camada de contexto, autonomia e recomendação assinada. Entrega o blueprint. |

> **Alcance desta fronteira.** As quatro camadas descrevem a passagem de trabalho dentro da EMCIA. Não constituem arranjo a reproduzir no processo do cliente: ali a fronteira é desenhada caso a caso, sobre evidência de campo, e fica registrada em B1 do blueprint. Transpõem-se os três testes e as regras; o resultado, nunca.

Nenhum agente decide nem encerra etapa em EX3 ou EX4. Nessas camadas, o agente só prepara: organiza material, minuta e propõe; a decisão e o encerramento são do engenheiro. A separação é de camada, não de qualidade do agente: melhorar o modelo não move a fronteira, porque o que falta em EX3 e EX4 não é capacidade de inferência, e sim acesso ao que ninguém escreveu.

O levantamento das regras não documentadas está em EX4, e não em EX3, porque não confere um conteúdo existente: produz a regra que a camada de contexto vai codificar. Não há declaração anterior a verificar, só o que quem executa sabe e não escreveu.

**Camada de encerramento e camada de preparação.** A camada declarada para a etapa no playbook é sua camada de encerramento e decisão. Cada HB conserva a camada de preparação declarada no Anexo A, EX1 ou EX2, que não pode ser superior à camada da etapa no mesmo nível de complexidade, na ordem EX1 < EX2 < EX3 < EX4. A verificação dessa relação é determinística. A preparação em EX2 de uma etapa encerrada em EX3 ou EX4 não constitui contradição de camada e não autoriza o agente a decidir ou encerrar. Essa regra substitui a leitura de contradição entre HB e etapa registrada para P5, P8 e P9 em docs/cruzamento-cat01.md do marketplace.

Os atos humanos continuam reservados ao engenheiro mesmo quando a etapa declara EX1 ou EX2. Em F0, a camada EX1 das HBs não delega a apuração registrada do nível nem a decisão de prosseguimento. O Anexo C é a fonte canônica da correspondência entre etapa, HB e agente interno; o playbook e o catálogo operacional devem reproduzi-la mediante revisão controlada.

### 3.4 Fronteira por passo
A tabela abaixo distribui as atividades de cada fase entre as três naturezas. A coluna final registra por que a atividade cai de um lado ou de outro — é ela que permite discutir a classificação em vez de aceitá-la.

#### 3.4.1 Fase F0 — Enquadramento do problema

| Passo | Atividade | Natureza | Onde está a fronteira |
| :---: | :--- | :--- | :--- |
| F0 | Aplicar o instrumento de triagem | Automatizado | Perguntas fechadas sobre fato declarável |
| F0 | Apurar o nível de complexidade | Automatizado | Aritmética determinística, fora do modelo de linguagem; o registro do nível é ato do engenheiro (3.5.5) |
| F0 | Estruturar a dor em 5W2H | Automatizado | Organização do relato, sem juízo sobre ele |
| F0 | Conduzir os cinco porquês | Híbrido | Causa raiz declarada não é causa raiz real |
| F0 | Calcular o custo do problema | Híbrido | O cálculo é auditável; os números de entrada costumam estar errados |
| F0 | Decidir o prosseguimento | Humano | Compromisso: inicia engajamento e aloca recurso |

**Condição de encerramento.** Nos três níveis, o engenheiro registra o ato humano `decidir-prosseguimento` no próprio terminal, fora da sessão do agente, com base no conteúdo da ficha E1 preparado para o enquadramento. O registro da decisão, com decisor, data, desfecho e motivo, é condição de encerramento de F0, além da apuração do nível e dos critérios substantivos do MET-01 §3.3.3. Os desfechos são prosseguir e não prosseguir; ambos encerram F0. Não prosseguir bloqueia as etapas seguintes até nova decisão que autorize prosseguir, preservando o registro anterior. A emissão formal de E1 continua posterior ao portão de F0 e sujeita à resolução de RH pendente; o ato não exige uma E1 já emitida nem substitui esses controles. O ato está implementado no playbook 0.4.19, conforme a decisão 043 do marketplace.

*Fase quase inteiramente delegável: alto volume, baixa consequência, saída verificável. O que a fase produz é nível declarado, nunca nível diagnosticado.*

#### 3.4.2 Fase F1 — Alinhamento estratégico e diagnóstico

| Passo | Atividade | Natureza | Onde está a fronteira |
| :---: | :--- | :--- | :--- |
| 1 | Levantar objetivos declarados e posicionar nas quatro frentes | Automatizado | Declarativo e verificável contra documento |
| 1 | Consultar referência setorial na base curada | Automatizado | Consulta a acervo com fonte identificada |
| 1 | Avaliar se há patrocínio real, e não apenas interesse | Humano | Distância entre objetivo declarado e objetivo real |
| 2 | Inventariar sistemas-fonte e coletar termos do glossário | Automatizado | Coleta do que a organização consegue declarar |
| 2 | Verificar se o dado existe e se presta | Humano | Exige acesso ao dado, não conversa sobre o dado |
| 2 | Detectar divergência entre definição declarada e uso real | Humano | Só aparece no confronto entre áreas |
| 3 | Varrer o mapa de valor sobre o estado declarado selado em P2 | Automatizado | Candidatos rastreáveis ao fluxo declarado; não decide prioridade |
| 3 | Desenhar o estado atual declarado | Automatizado | Estruturação do que foi descrito |
| 3 | Preparar o confronto entre declarado e observado | Híbrido | Organização do placar e dos registros; o operador decide cada item |
| 3 | Levantar as regras não documentadas | Humano | Fonte: quem executa não sabe que sabe. Exige presença |
| 3 | Distinguir processo documentado de processo praticado | Humano | A ausência não é detectável por leitura |
| 3 | Registrar a linha de base | Híbrido | O agente estrutura a medição; o número é validado por quem opera |

O posicionamento nas quatro frentes do passo 1 e o mapa de valor do passo 3 são instrumentos distintos, conforme MET-01 §§3.4.1 e 3.4.3 e resolução humana da D5. A HB-09 permanece no passo 3, em P3d: recebe o estado declarado preservado pelo selo posterior ao encerramento de P2 e produz candidatos para P4. Não redesenha esse estado a partir do observado. A preparação do confronto por HB-20 não substitui a distinção humana entre processo documentado e praticado. O MET-01 permanece inalterado.

*O passo 3 é o limite arquitetural do trabalho automatizado. Delegá-lo produz camada de contexto plausível e errada, que é o pior artefato possível, porque não parece errado.*

#### 3.4.3 Fase F2 — Desenho e arquitetura da solução

| Passo | Atividade | Natureza | Onde está a fronteira |
| :---: | :--- | :--- | :--- |
| 4 | Montar a matriz de priorização com os casos levantados | Automatizado | Organização de candidatos, sem escolha entre eles |
| 4 | Estimar viabilidade técnica | Híbrido | Estimativa depende de restrição não declarada |
| 4 | Estimar impacto e decidir o que atacar primeiro | Humano | Depende de prioridade estratégica e contexto político |
| 4 | Classificar na zona de contenção | Híbrido | O agente sinaliza risco regulatório; o humano confirma |
| 5 | Aplicar a Matriz Problema→Tecnologia | Híbrido | Classificação por regra, com confirmação antes de virar decisão |
| 5 | Estimar custo por tarefa e latência | Automatizado | Cálculo paramétrico com premissas expostas |
| 5 | Construir a camada de contexto | Humano | Codifica regra levantada em campo, não regra declarada |
| 5 | Decidir escolhas de construção e integração | Humano | Compromisso de investimento |

*A classificação tecnológica é regra, e por isso delegável. A camada de contexto é a codificação das regras levantadas no passo 3, e não é delegável pela mesma razão que o passo 3 não é.*

#### 3.4.4 Fase F3 — Operacionalização e governança

| Passo | Atividade | Natureza | Onde está a fronteira |
| :---: | :--- | :--- | :--- |
| 6 | Mapear pontos de integração e permissões necessárias | Automatizado | Inventário técnico verificável |
| 6 | Documentar o estado futuro | Híbrido | Redação automatizada, desenho decidido com as áreas |
| 6 | Redesenhar o processo com as áreas | Humano | Negociação, não documentação |
| 6 | Redigir o guia operacional e o material de treinamento | Híbrido | Minuta automatizada sobre conteúdo já decidido |
| 7 | Levantar requisitos regulatórios aplicáveis | Automatizado | Consulta a fonte pública identificada |
| 7 | Minutar o termo de autonomia | Híbrido | O agente minuta a forma; o humano decide os limites |
| 7 | Definir o nível de autonomia e os limites de valor | Humano | Regra que não admite exceção, ver 3.5.1 |
| 7 | Nomear responsáveis e aprovar a política | Humano | Compromisso assinado |

*O agente documenta bem o fluxo que lhe é descrito. Não percebe a resistência da equipe, a disputa entre áreas, nem quem perde poder com a mudança — e são esses fatores que decidem se o redesenho pega.*

#### 3.4.5 Fase F4 — Piloto, mensuração e calibragem

| Passo | Atividade | Natureza | Onde está a fronteira |
| :---: | :--- | :--- | :--- |
| 8 | Gerar casos de teste a partir do dossiê e da camada de contexto | Híbrido | Cobertura proposta, revisada por quem executa o processo |
| 8 | Executar a suíte de avaliação e consolidar falhas | Automatizado | Execução e contagem |
| 8 | Julgar se a falha é aceitável ou impeditiva | Humano | Oito erros em cem podem ser ruído ou inaceitáveis |
| 8 | Aprovar a passagem de sombra para assistido, e a escala | Humano | Compromisso operacional |
| 9 | Coletar métricas e comparar com a linha de base | Automatizado | Apuração determinística |
| 9 | Interpretar por que a métrica se moveu | Humano | Atribuição de causa não está nos dados |
| 9 | Apresentar o resultado ao patrocinador | Humano | Recomendação assinada |
| 10 | Monitorar desvio de desempenho e degradação de saída | Automatizado | Detecção por limiar |
| 10 | Propor ajuste de regra ou parâmetro | Híbrido | Proposta que não se aplica sozinha |
| 10 | Diagnosticar a causa da degradação | Humano | O agente detecta que o mundo mudou, não como mudou |
| 10 | Decidir recalibrar, expandir ou descontinuar | Humano | Compromisso |

*Instrumentação é trabalho delegável: coletar, comparar e reportar. Separar o efeito da solução da sazonalidade ou de um esforço paralelo da equipe é julgamento, e é disso que depende a credibilidade do número.*

### 3.5 Regras invioláveis

#### 3.5.1 Um agente não define autonomia
> **Regra.** Nenhum agente define a própria autonomia nem a de outro agente. Este é o único ponto da fronteira que não se flexibiliza por nível de complexidade, por prazo ou por pressão comercial.

#### 3.5.2 O passo 3 é o limite arquitetural
O levantamento das regras não documentadas é o ponto em que o trabalho automatizado para. A instrução que decide o resultado costuma ser omitida pela fonte, e não contradita por ela: ausência não é detectável por leitura, apenas por experiência de quem já errou. Como a camada de contexto se alimenta dessas regras, delegar o passo 3 produz uma camada plausível e errada.

#### 3.5.3 Trava de camada
Toda habilidade carrega a camada em que opera. Habilidade marcada como híbrida não conclui sem decisão registrada, e a tentativa de execução fora da camada é registrada em log de desvio. A trava é condição de validade, não instrução: não depende de o agente escolher respeitá-la.

A trava considera a origem da chamada, e não o nome informado nela. O que chega pela sessão do agente é do agente, ainda que venha assinado com o nome do engenheiro. Decisão humana só é executada pelo engenheiro, fora da sessão do agente.

#### 3.5.4 Procedência obrigatória
Toda saída de EX1 e EX2 carrega a procedência de cada informação: declarada, inferida ou verificada. Sem essa marcação, EX3 não tem o que verificar e o dossiê inteiro vira autodeclaração com aparência de diagnóstico. A marca não é atribuída por modelo de linguagem.

#### 3.5.5 Atos sobre o registro
Além das atividades do percurso, são reservados ao engenheiro os atos que alteram a evidência do caso: registrar o nível, registrar sessão e campo, satisfazer inegociável, registrar recorrência, encerrar etapa em EX3 ou EX4 e alterar o estado do caso. O agente pode preparar o comando; não pode executá-lo. Esses atos não produzem conteúdo, mas decidem o que o registro passa a afirmar, e por isso são os primeiros que um agente tenta contornar.

Também são humanos, no próprio terminal e fora da sessão do agente: importar a habilitação, definir canais, receber material, registrar listagem, registrar entrega e vincular ou dispensar restrição. O ato vincular-restricao, por `restricoes.py`, ocorre inicialmente em P2 e associa RH-xx a fonte F-xxx curada ou registra dispensa com motivo. Revisão exige decisão explícita sobre a versão anterior e preserva histórico. Confirmação no chat não autoriza o agente a executar esses atos; informar o nome do engenheiro na chamada não muda sua origem.

#### 3.5.6 Efeitos externos e limite de confiança
O agente lê pelos ids autorizados, prepara planos, formulários, manifestos e comandos, e apresenta ao engenheiro o efeito externo proposto. Criação de recurso, compartilhamento, publicação, convite e envio exigem confirmação explícita no chat antes da execução pelo conector. Cada compartilhamento exige confirmação própria, identificando pessoa, endereço, id de destino e papel. Planejar ou preparar link não autoriza publicar ou enviá-lo.

O procedimento segue CAN-01: roteamento exclusivamente por id, listagem restrita ao contêiner declarado e registrada pelo engenheiro antes da leitura de objeto; coleta em rascunho até recebimento; publicação de material somente em entregas. Os scripts conferem coerência local, origem declarada e hashes; não autenticam resposta remota, identidade real ou permissões efetivas. A guarda MCP depende das regras correspondentes ao conector instalado e do suporte a hooks no runtime; não comprova que houve confirmação no chat. Registro de entrega não é aceite. Assinatura eletrônica, gravação e transcrição permanecem fora do escopo dos canais.

### 3.6 Deslocamento da fronteira por nível
O engenheiro conduz o percurso inteiro nos três níveis. O que muda é até onde a preparação automatizada é admitida antes da verificação obrigatória: quanto maior a consequência do erro, mais cedo o trabalho humano precisa entrar.

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Alcance da preparação automatizada** | Até o passo 4 | Até o passo 2 | Fase F0 apenas |
| **Verificação obrigatória a partir de** | Passo 5 | Passo 3 | Passo 1 |
| **Consequência do erro** | Baixa e reversível | Média | Alta e regulada |

O deslocamento altera onde a verificação passa a ser obrigatória, não quem decide. As atividades humanas da seção 3.4 continuam humanas nos três níveis, inclusive nos passos em que a preparação automatizada é admitida: decidir o prosseguimento (F0), avaliar o patrocínio real (passo 1), verificar o dado (passo 2) e decidir a prioridade (passo 4).

## 4. Condição de aceite
Este artefato está pronto quando toda atividade dos dez passos tem natureza atribuída e justificativa registrada; quando toda atividade automatizada ou híbrida tem cobertura no Anexo A, com insumo, saída e critério de verificação, ou ausência de execução comprovada registrada no Anexo B; quando o Anexo C cobre todas as etapas do playbook; e quando um engenheiro que não participou da construção consegue decidir, diante de uma atividade nova, de que lado da fronteira ela cai aplicando os três testes. A presença no Anexo B não autoriza execução por agente. Aprovação documental e implementação operacional são verificações distintas.

## 5. Referências
- *Services: The New Software*, Sequoia Capital (2024)
- *The Tacit Dimension*, Polanyi (1966)
- *The Knowledge-Creating Company*, Nonaka e Takeuchi (1995)
- *AI Risk Management Framework*, NIST (2023)
- Artefatos relacionados: EMCIA-MET-01, EMCIA-TRI-01, EMCIA-GLO-01, EMCIA-CAN-01, EMCIA-HAB-01, EMCIA-CTX-01 e EMCIA-MAN-01.
- Referência operacional: emcia-marketplace, decisões 039–043 e playbook 0.4.19, núcleo 0.2.45 e campo 0.8.23.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 10/09/2026 | Celso do Vale | Versão inicial: critério de corte, três naturezas, quatro camadas, fronteira por passo e catálogo | — |
| 0.2 | 14/09/2026 | Celso do Vale | Habilidades renomeadas para HB; camadas de execução renomeadas para EX; alcance da fronteira delimitado ao trabalho interno | — |
| 0.3 | 29/09/2026 | Celso do Vale | Consolidação da Sprint 4 (registro da ação 4.3): trava por origem da chamada (A4); levantamento das regras não documentadas movido para EX4 (D2); agente só prepara em EX3 e EX4 (D3); regra dos atos sobre o registro (D4); decisões humanas mantidas em todos os níveis (D1); situação das habilidades e atividades sem habilidade (D5) | — |
| 0.4 | 2026-10 | Celso do Vale | Fronteira de ações externas, confirmação por efeito e compartilhamento; atos humanos de canais, importação, recebimento, listagem, entrega e vínculo de restrição | pendente |
| 0.5 | 2026-10 | Celso do Vale | Aplicação das decisões humanas D2–D8: HB-04/05 em F0, HB-06 em P2 e HB-13 em P7/AG-03; D5 resolvida com instrumentos distintos, HB-09 mantida no passo 3/P3d, estado declarado selado em P2 como entrada e candidatos para P4 como saída, sem alterar MET-01; varredura e desenho discriminados, preservando natureza automatizada e registrando desenho sem execução comprovada; HB-19 a HB-21 criadas somente com evidência textual dos SKILL.md; Anexo B restrito à execução não comprovada; correspondência canônica no Anexo C; camadas de encerramento e preparação; ato humano decidir-prosseguimento em F0. Evidências e dependências operacionais no Anexo D | pendente |
| 0.6 | 2026-10 | Celso do Vale | Aprovação documental por Celso do Vale; implementação da correspondência registrada na decisão 043; dois desfechos de F0 alinhados ao contrato; HB-16 mantida automatizada por decisão humana, com correção correspondente no CAM-01 | Celso do Vale — 03/10/2026 |
| 1.0 | 03/10/2026 | Celso do Vale | Primeira linha de base aprovada (metodo-v1.0), sem alteração de conteúdo em relação à v0.6 | Celso do Vale |

---

## Anexo A — Catálogo de agentes e habilidades
Os agentes agrupam habilidades por camada. Nenhum agente reúne habilidades de camadas distintas, e nenhum decide ou encerra etapa em EX3 ou EX4.

| Código | Agente | Camada | Habilidades |
| :--- | :--- | :---: | :--- |
| **AG-01** | Agente de enquadramento | EX1 | HB-01 a HB-05 |
| **AG-02** | Agente de análise documental | EX2 | HB-06 a HB-10, HB-19, HB-20 |
| **AG-03** | Agente de especificação | EX2 | HB-11 a HB-14, HB-21 |
| **AG-04** | Agente de avaliação | EX2 | HB-15 a HB-18 |

<br>

| Código | Habilidade | Camada | Insumo | Saída | Critério de verificação |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **HB-01** | Condução da triagem | EX1 · Aut. | Respostas do cliente ao instrumento | Pontuação por eixo, com a resposta literal preservada | As nove perguntas respondidas e o literal arquivado ao lado da interpretação |
| **HB-02** | Apuração do nível de complexidade | EX1 · Aut. | Pontuação por eixo | Nível N1, N2 ou N3, registrado pelo engenheiro | Recálculo manual reproduz o mesmo nível |
| **HB-03** | Estruturação da dor | EX1 · Aut. | Relato do patrocinador | Quadro 5W2H preenchido | Cada campo remete a trecho identificável do relato |
| **HB-04** | Condução dos cinco porquês | EX1 · Híb. | Dor estruturada | Cadeia causal proposta | Cadeia confirmada ou corrigida pelo engenheiro antes de avançar |
| **HB-05** | Cálculo do custo do problema | EX1 · Híb. | Volumes e tempos informados | Custo estimado, com premissas expostas | Toda premissa visível e cada número com procedência marcada |
| **HB-06** | Inventário de fontes de dados | EX2 · Aut. | Declaração da organização e documentos | Lista de fontes com criticidade | Cada fonte marcada como declarada até verificação em campo |
| **HB-07** | Coleta de termos do glossário | EX2 · Aut. | Documentos e entrevistas transcritas | Termos com definição declarada e ocorrências | Definições conflitantes sinalizadas, não conciliadas |
| **HB-08** | Consulta à base de referência | EX2 · Aut. | Setor e processo-alvo | Referências com fonte identificada | Nenhum item sem fonte; sem acesso aberto à internet |
| **HB-09** | Varredura do mapa de valor | EX2 · Aut. | Estado atual declarado, preservado pelo selo posterior ao encerramento de P2 | Pontos candidatos a intervenção para P4 | Cada candidato rastreável à etapa do fluxo declarado que o originou, sem reescrever a entrada selada |
| **HB-10** | Montagem da matriz de priorização | EX2 · Aut. | Casos candidatos | Matriz preenchida, sem escolha | Todos os candidatos presentes, inclusive os descartados |
| **HB-11** | Classificação Problema→Tecnologia | EX2 · Híb. | Caso descrito e camada de contexto | Tecnologia adequada, com justificativa | Classificação confirmada pelo engenheiro antes de virar decisão |
| **HB-12** | Estimativa de custo e latência | EX2 · Aut. | Desenho da solução | Custo por tarefa e teto mensal | Premissas expostas e recalculáveis |
| **HB-13** | Levantamento regulatório | EX2 · Aut. | Setor e natureza do dado tratado | Requisitos aplicáveis, com fonte | Cada requisito remete a norma citável |
| **HB-14** | Minuta do termo de autonomia | EX2 · Híb. | Arquétipo e zona de contenção | Minuta com as três listas em branco | As três listas preenchidas por decisão humana registrada |
| **HB-15** | Geração de casos de teste | EX2 · Híb. | Dossiê verificado e camada de contexto | Casos com saída esperada | Conjunto revisado por quem executa o processo |
| **HB-16** | Execução da suíte de avaliação | EX2 · Aut. | Casos de teste e solução em piloto | Resultado por caso e falhas agrupadas | Execução reproduzível a partir do mesmo conjunto |
| **HB-17** | Consolidação de indicadores | EX2 · Aut. | Medições do piloto e linha de base | Comparativo contra a linha de base | Apuração determinística e documentada |
| **HB-18** | Monitoramento de desvio | EX2 · Aut. | Saídas em operação | Alerta de degradação | Limiar definido antes do piloto, não ajustado a posteriori |
| **HB-19** | Registro da linha de base | EX2 · Híb. | Amostras, período, indicador e fonte; em N1, estimativa declarada com quem opera | Linha de base estruturada, datada, com valor, método de apuração e procedência | Cálculo reproduzível; estimativa somente em N1; número confirmado por quem opera antes de avançar; narrativa não substitui registro estruturado |
| **HB-20** | Preparação do confronto declarado × observado | EX2 · Híb. | Estado declarado selado após P2, sessão de P3b registrada e evidências do observado | Placar e registros propostos de divergência, com referências, justificativa e autoria nominal | Cada item liga declarado e observado; o operador decide cada item; correção cria registro novo e preserva o original, sem promoção automática de procedência |
| **HB-21** | Documentação do estado futuro | EX2 · Híb. | E3-E ou candidato correspondente, classificação de P5, contexto curado e desenho decidido com as áreas | Proposta de especificação operacional: fluxo futuro, ponto de inserção, entrada, saída, interface, exceção e retorno ao humano | Proposta rastreável aos insumos; ponto de inserção e responsável nomeados por decisão humana; aprovação registrada pelo engenheiro antes de avançar |

*Legenda: EX1 · Aut. = camada conversacional, automatizada. EX1 · Híb. = camada conversacional, híbrida. EX2 = camada analítica. Habilidades híbridas não concluem sem decisão humana registrada.*

## Anexo B — Atividades delegáveis sem habilidade catalogada

Atividades automatizadas ou híbridas da seção 3.4 sem execução integral comprovada pelo texto dos SKILL.md examinados. Enquanto não houver essa comprovação e revisão do catálogo, são conduzidas pelo engenheiro. Remissão ao método, título genérico ou preparação de parte da atividade não comprovam a atividade completa; o Anexo D registra o exame.

| Passo | Atividade | Natureza |
| :---: | :--- | :--- |
| 1 | Levantar objetivos declarados e posicionar nas quatro frentes | Automatizado |
| 3 | Desenhar o estado atual declarado | Automatizado |
| 4 | Estimar viabilidade técnica | Híbrido |
| 4 | Classificar na zona de contenção | Híbrido |
| 6 | Mapear pontos de integração e permissões necessárias | Automatizado |
| 6 | Redigir o guia operacional e o material de treinamento | Híbrido |
| 10 | Propor ajuste de regra ou parâmetro | Híbrido |

## Anexo C — Correspondência canônica entre etapa, habilidades e agentes

Esta tabela é a fonte da relação etapa → HBs → AG. Declara a correspondência desta revisão do método, reproduzida no playbook 0.4.19 e conferida por testes conforme a decisão 043 do marketplace. Os identificadores e a ordem das treze etapas são os do playbook. A camada de encerramento conserva os valores atuais por nível; as HBs conservam sua camada de preparação do Anexo A.

| Etapa | Camada de encerramento N1 · N2 · N3 | Habilidade do Estúdio | HBs de preparação | AG |
| :--- | :--- | :--- | :--- | :--- |
| F0 | EX1 · EX1 · EX1 | hb-enquadrar | HB-01, HB-02, HB-03, HB-04, HB-05 | AG-01 |
| P1 | EX2 · EX2 · EX3 | hb-mapear-contexto | HB-08 | AG-02 |
| P2 | EX2 · EX2 · EX3 | hb-extrair-regras | HB-06, HB-07 | AG-02 |
| P3a | EX2 · EX3 · EX3 | hb-medir | HB-19 | AG-02 |
| P3b | EX4 · EX4 · EX4 | hb-levantar-regras — protocolo humano | — | — |
| P3d | EX3 · EX3 · EX3 | hb-confrontar | HB-09, HB-20 | AG-02 |
| P4 | EX2 · EX3 · EX3 | hb-priorizar | HB-10 | AG-02 |
| P5 | EX3 · EX3 · EX3 | hb-classificar | HB-11, HB-12 | AG-03 |
| P6 | EX3 · EX3 · EX3 | hb-operacionalizar | HB-21 | AG-03 |
| P7 | EX4 · EX4 · EX4 | hb-governar | HB-13, HB-14 | AG-03 |
| P8 | EX3 · EX3 · EX3 | hb-pilotar | HB-15, HB-16 | AG-04 |
| P9 | EX3 · EX3 · EX3 | hb-medir-valor | HB-17 | AG-04 |
| P10 | EX4 · EX4 · EX4 | hb-recalibrar | HB-18 | AG-04 |

F0 executa HB-04 e HB-05 pela habilidade de enquadramento. P3b permanece sem HB e sem AG por desenho: levantamento presencial e não delegável. Em P7 e P10, a preparação EX2 não altera a natureza humana da decisão EX4. O monitoramento de P10 permanece em EX2. Os agentes agrupam a preparação conforme as fases já existentes: AG-01 no enquadramento, AG-02 na análise e priorização, AG-03 na especificação e governança e AG-04 na avaliação; nenhum reúne camadas distintas.

## Anexo D — Evidência de cobertura e dependências da implementação

### D.1 Fonte e critério

Exame histórico que fundamentou a revisão 0.5: leitura dos SKILL.md em eiac-campo/skills/hb-*/, de eiac-campo/reference/habilidades.json, do playbook 0.4.18 em eiac-campo/template-caso/registro/playbook.json, de decisoes/020-pendencia-cruzamento-cat01.md e de docs/cruzamento-cat01.md na branch master do emcia-marketplace, commit `ebb6bbda55ea7403bc0e09a0bc316f0a1071cf4f`, em 2026-10. Os caminhos abaixo são relativos à raiz desse repositório. Os trechos citados comprovam preparação documental, não aprovação humana nem execução em produção. As novas HBs pertencem somente a EX2, segundo a regra da seção 3.3, ainda que o front matter da habilidade declare EX3 para a etapa.

### D.2 Exame das candidatas

| Etapa e atividade | SKILL.md e trecho literal ou ausência relevante | Resultado |
| :--- | :--- | :--- |
| P1 — levantar objetivos declarados e posicionar nas quatro frentes | eiac-campo/skills/hb-mapear-contexto/SKILL.md: “Levanta o contexto de negocio e o mapa de valor da organizacao.” O texto não declara levantamento de objetivos e posicionamento nas quatro frentes; remeter ao passo 1 não comprova sua execução | Sem nova HB; Anexo B |
| P3a — registrar a linha de base | eiac-campo/skills/hb-medir/SKILL.md: “Saída estruturada (linha de base, evidência do inegociável 1):” e “grave o indicador em `rascunho/BL-NNN.yaml`”; “O cálculo é feito em código, não por leitura.” | HB-19, EX2, híbrida, AG-02 |
| P3d — preparação do confronto | eiac-campo/skills/hb-confrontar/SKILL.md: “Você prepara o confronto; o operador decide cada item.” e “escreva o registro em `rascunho/DIV-*.yaml`”; instrumentos: “placar regra escrita × praticada, registro de divergência.” | HB-20, EX2, híbrida, AG-02; verificação e decisão permanecem humanas |
| P3d — desenhar o estado atual declarado | eiac-campo/skills/hb-confrontar/SKILL.md prepara placar e divergências, mas não declara desenho do fluxo atual. HB-09 recebe o estado declarado já selado; varrê-lo não comprova desenhá-lo | Sem nova HB; Anexo B |
| P4 — estimar viabilidade técnica | eiac-campo/skills/hb-priorizar/SKILL.md cruza frequência × consequência do erro e remete à Matriz Problema→Tecnologia; não declara cálculo ou proposta de viabilidade técnica | Sem nova HB; Anexo B |
| P4 — classificar na zona de contenção | eiac-campo/skills/hb-priorizar/SKILL.md: “Esta habilidade prepara; não decide.” e “Priorização e zona de contenção são EX4, e são decisão do cliente”; não há trecho que declare produção da classificação proposta | Sem nova HB; Anexo B |
| P6 — mapear pontos de integração e permissões necessárias | eiac-campo/skills/hb-operacionalizar/SKILL.md: “organizar o fluxo, identificar interfaces, estruturar o mapa técnico, gerar rascunho, apontar inconsistências.” Há preparação de interfaces, mas não inventário de permissões necessárias; execução integral não comprovada | Sem nova HB para a atividade completa; Anexo B |
| P6 — documentar o estado futuro | eiac-campo/skills/hb-operacionalizar/SKILL.md: “Ele documenta onde a solução entraria no fluxo.” e “organizar o fluxo, identificar interfaces, estruturar o mapa técnico, gerar rascunho, apontar inconsistências.” A especificação declara ponto de inserção, entrada, saída, interface, exceção e retorno ao humano | HB-21, EX2, híbrida, AG-03; aprovação do desenho permanece humana |
| P6 — redigir guia operacional e material de treinamento | eiac-campo/skills/hb-operacionalizar/SKILL.md produz proposta OP; não declara redação do guia ou do material de treinamento. A emissão de E4 por hb-emitir-e4 não comprova executar essa atividade em P6 | Sem nova HB; Anexo B |
| P10 — propor ajuste de regra ou parâmetro | eiac-campo/skills/hb-recalibrar/SKILL.md: “Quando `drift_detectado: true`, preencha `drift_descricao`, `drift_quantificacao` e `recomendacao_agente`.” Há recomendação sobre o desvio, mas não proposta identificada de ajuste de regra ou parâmetro | Sem nova HB para essa atividade; Anexo B |

### D.3 Divergências e aplicação controlada

As decisões humanas D2–D8 e a resolução da D5 fixam a correspondência desta revisão. As diferenças registradas na revisão 0.5 contra o playbook 0.4.18 foram resolvidas no marketplace pela decisão 043: o playbook 0.4.19 referencia todas as 21 HBs, mantém HB-09 em P3d, atribui HB-13 a AG-03 e declara decidir-prosseguimento como condição de encerramento de F0. A 043 supera explicitamente a autoria provisória da decisão 020. A implementação foi conferida no commit `d9551a90b5ee3cec5006bbbfcbdebca4cbfe0f35`, com núcleo 0.2.45, campo 0.8.23, 958 verificações em 49 módulos e evidência em `.projectdocs/evidencias/correspondencia-cat01/`. Esse commit é a referência da implementação examinada; novos empacotamentos dependem de atualização explícita do manifesto e não migram casos existentes.

P5, P8 e P9 deixam de apresentar contradição entre camada da HB e da etapa pela regra da seção 3.3. P3b já está em EX4 no CAT-01 v0.4; a comparação antiga com EX3 é histórica. Atividades humanas de P1, P2 e P4 continuam humanas em todos os níveis; a regra não cria atos nem comprova produtos ausentes do playbook.

A divergência anterior sobre HB-16 foi resolvida por Celso do Vale em 03/10/2026: HB-16 permanece automatizada, conforme o Anexo A; o CAM-01 v0.5 foi corrigido para distinguir HB-15 híbrida de HB-16 automatizada. A revisão humana do conjunto e o encerramento de P8 continuam obrigatórios; a natureza da execução da suíte não delega esses atos.
