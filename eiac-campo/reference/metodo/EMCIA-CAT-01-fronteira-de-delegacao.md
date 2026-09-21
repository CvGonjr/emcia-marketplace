# Fronteira de delegação
## Camadas de execução e catálogo de agentes e habilidades

| Código | EMCIA-CAT-01 | Versão | 0.2 |
| :--- | :--- | :--- | :--- |
| **Data** | 14/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
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
| **EX3 — Verificação** | Humano | Confronto entre declarado e observado, levantamento das regras não documentadas, validação da linha de base. Entrega o dossiê verificado, com as correções registradas. |
| **EX4 — Julgamento** | Humano | Priorização, camada de contexto, autonomia e recomendação assinada. Entrega o blueprint. |

> **Alcance desta fronteira.** As quatro camadas descrevem a passagem de trabalho dentro da EMCIA. Não constituem arranjo a reproduzir no processo do cliente: ali a fronteira é desenhada caso a caso, sobre evidência de campo, e fica registrada em B1 do blueprint. Transpõem-se os três testes e as regras; o resultado, nunca.

Nenhum agente opera em EX3 ou EX4. A separação é de camada, não de qualidade do agente: melhorar o modelo não move a fronteira, porque o que falta em EX3 não é capacidade de inferência, e sim acesso ao que ninguém escreveu.

### 3.4 Fronteira por passo
A tabela abaixo distribui as atividades de cada fase entre as três naturezas. A coluna final registra por que a atividade cai de um lado ou de outro — é ela que permite discutir a classificação em vez de aceitá-la.

#### 3.4.1 Fase F0 — Enquadramento do problema

| Passo | Atividade | Natureza | Onde está a fronteira |
| :---: | :--- | :--- | :--- |
| F0 | Aplicar o instrumento de triagem | Automatizado | Perguntas fechadas sobre fato declarável |
| F0 | Apurar o nível de complexidade | Automatizado | Aritmética determinística, fora do modelo de linguagem |
| F0 | Estruturar a dor em 5W2H | Automatizado | Organização do relato, sem juízo sobre ele |
| F0 | Conduzir os cinco porquês | Híbrido | Causa raiz declarada não é causa raiz real |
| F0 | Calcular o custo do problema | Híbrido | O cálculo é auditável; os números de entrada costumam estar errados |
| F0 | Decidir o prosseguimento | Humano | Compromisso: inicia engajamento e aloca recurso |

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
| 3 | Varrer o mapa de valor e desenhar o estado atual declarado | Automatizado | Estruturação do que foi descrito |
| 3 | Levantar as regras não documentadas | Humano | Fonte: quem executa não sabe que sabe. Exige presença |
| 3 | Distinguir processo documentado de processo praticado | Humano | A ausência não é detectável por leitura |
| 3 | Registrar a linha de base | Híbrido | O agente estrutura a medição; o número é validado por quem opera |

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

#### 3.5.4 Procedência obrigatória
Toda saída de EX1 e EX2 carrega a procedência de cada informação: declarada, inferida ou verificada. Sem essa marcação, EX3 não tem o que verificar e o dossiê inteiro vira autodeclaração com aparência de diagnóstico. A marca não é atribuída por modelo de linguagem.

### 3.6 Deslocamento da fronteira por nível
O engenheiro conduz o percurso inteiro nos três níveis. O que muda é até onde a preparação automatizada é admitida antes da verificação obrigatória: quanto maior a consequência do erro, mais cedo o trabalho humano precisa entrar.

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Alcance da preparação automatizada** | Até o passo 4 | Até o passo 2 | Fase F0 apenas |
| **Verificação obrigatória a partir de** | Passo 5 | Passo 3 | Passo 1 |
| **Consequência do erro** | Baixa e reversível | Média | Alta e regulada |

## 4. Condição de aceite
Este artefato está pronto quando toda atividade dos dez passos tem natureza atribuída e justificativa registrada; quando toda atividade automatizada ou híbrida consta do catálogo com insumo, saída e critério de verificação; e quando um engenheiro que não participou da construção consegue decidir, diante de uma atividade nova, de que lado da fronteira ela cai aplicando os três testes.

## 5. Referências
- *Services: The New Software*, Sequoia Capital (2024)
- *The Tacit Dimension*, Polanyi (1966)
- *The Knowledge-Creating Company*, Nonaka e Takeuchi (1995)
- *AI Risk Management Framework*, NIST (2023)
- Artefatos relacionados: EMCIA-MET-01, EMCIA-TRI-01, EMCIA-GLO-01.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 10/09/2026 | Celso do Vale | Versão inicial: critério de corte, três naturezas, quatro camadas, fronteira por passo e catálogo | — |
| 0.2 | 14/09/2026 | Celso do Vale | Habilidades renomeadas para HB; camadas de execução renomeadas para EX; alcance da fronteira delimitado ao trabalho interno | — |

---

## Anexo A — Catálogo de agentes e habilidades
Os agentes agrupam habilidades por camada. Nenhum agente reúne habilidades de camadas distintas, e nenhum opera em EX3 ou EX4.

| Código | Agente | Camada | Habilidades |
| :--- | :--- | :---: | :--- |
| **AG-01** | Agente de enquadramento | EX1 | HB-01 a HB-05 |
| **AG-02** | Agente de análise documental | EX2 | HB-06 a HB-10, HB-13 |
| **AG-03** | Agente de especificação | EX2 | HB-11, HB-12, HB-14 |
| **AG-04** | Agente de avaliação | EX2 | HB-15 a HB-18 |

<br>

| Código | Habilidade | Camada | Insumo | Saída | Critério de verificação |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **HB-01** | Condução da triagem | EX1 · Aut. | Respostas do cliente ao instrumento | Pontuação por eixo, com a resposta literal preservada | As nove perguntas respondidas e o literal arquivado ao lado da interpretação |
| **HB-02** | Apuração do nível de complexidade | EX1 · Aut. | Pontuação por eixo | Nível N1, N2 ou N3 | Recálculo manual reproduz o mesmo nível |
| **HB-03** | Estruturação da dor | EX1 · Aut. | Relato do patrocinador | Quadro 5W2H preenchido | Cada campo remete a trecho identificável do relato |
| **HB-04** | Condução dos cinco porquês | EX1 · Híb. | Dor estruturada | Cadeia causal proposta | Cadeia confirmada ou corrigida pelo engenheiro antes de avançar |
| **HB-05** | Cálculo do custo do problema | EX1 · Híb. | Volumes e tempos informados | Custo estimado, com premissas expostas | Toda premissa visível e cada número com procedência marcada |
| **HB-06** | Inventário de fontes de dados | EX2 · Aut. | Declaração da organização e documentos | Lista de fontes com criticidade | Cada fonte marcada como declarada até verificação em campo |
| **HB-07** | Coleta de termos do glossário | EX2 · Aut. | Documentos e entrevistas transcritas | Termos com definição declarada e ocorrências | Definições conflitantes sinalizadas, não conciliadas |
| **HB-08** | Consulta à base de referência | EX2 · Aut. | Setor e processo-alvo | Referências com fonte identificada | Nenhum item sem fonte; sem acesso aberto à internet |
| **HB-09** | Varredura do mapa de valor | EX2 · Aut. | Estado atual declarado | Pontos candidatos a intervenção | Candidatos rastreáveis à etapa do fluxo que os originou |
| **HB-10** | Montagem da matriz de priorização | EX2 · Aut. | Casos candidatos | Matriz preenchida, sem escolha | Todos os candidatos presentes, inclusive os descartados |
| **HB-11** | Classificação Problema→Tecnologia | EX2 · Híb. | Caso descrito e camada de contexto | Tecnologia adequada, com justificativa | Classificação confirmada pelo engenheiro antes de virar decisão |
| **HB-12** | Estimativa de custo e latência | EX2 · Aut. | Desenho da solução | Custo por tarefa e teto mensal | Premissas expostas e recalculáveis |
| **HB-13** | Levantamento regulatório | EX2 · Aut. | Setor e natureza do dado tratado | Requisitos aplicáveis, com fonte | Cada requisito remete a norma citável |
| **HB-14** | Minuta do termo de autonomia | EX2 · Híb. | Arquétipo e zona de contenção | Minuta com as três listas em branco | As três listas preenchidas por decisão humana registrada |
| **HB-15** | Geração de casos de teste | EX2 · Híb. | Dossiê verificado e camada de contexto | Casos com saída esperada | Conjunto revisado por quem executa o processo |
| **HB-16** | Execução da suíte de avaliação | EX2 · Aut. | Casos de teste e solução em piloto | Resultado por caso e falhas agrupadas | Execução reproduzível a partir do mesmo conjunto |
| **HB-17** | Consolidação de indicadores | EX2 · Aut. | Medições do piloto e linha de base | Comparativo contra a linha de base | Apuração determinística e documentada |
| **HB-18** | Monitoramento de desvio | EX2 · Aut. | Saídas em operação | Alerta de degradação | Limiar definido antes do piloto, não ajustado a posteriori |

*Legenda: EX1 · Aut. = camada conversacional, automatizada. EX1 · Híb. = camada conversacional, híbrida. EX2 = camada analítica. Habilidades híbridas não concluem sem decisão humana registrada.*
