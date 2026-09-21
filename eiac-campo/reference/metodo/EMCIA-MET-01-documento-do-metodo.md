# Documento do método
## Cinco fases, dez passos, calibragem por nível de complexidade e critérios de encerramento

| Código | EMCIA-MET-01 | Versão | 0.1 |
| :--- | :--- | :--- | :--- |
| **Data** | 09/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | F0 a F4 — todas | **Passo** | 1 a 10 — todos |

---

## 1. Objetivo
Fixar o percurso que a EMCIA aplica em um engajamento de engenharia de IA de campo, de modo que outro engenheiro possa conduzi-lo sem ter participado de sua construção. O documento define as fases, os passos, a profundidade exigida em cada nível de complexidade e a condição verificável que encerra cada passo.

## 2. Escopo e aplicação
Aplica-se ao percurso completo, do enquadramento inicial à calibragem posterior, em organizações de qualquer porte. A profundidade de cada passo é calibrada pelo nível de complexidade apurado na Fase 0.

Não se aplica à construção, à implantação nem à sustentação da solução especificada, que permanecem fora do serviço. O método também não decide pela organização: priorização, nível de autonomia e aceitação pertencem ao cliente, e o percurso estrutura essas decisões sem substituí-las.

## 3. Conteúdo

### 3.1 Princípio de desenho
- **A Fase 0 não levanta requisitos. A Fase 0 decide qual método aplicar.**
- Toda ferramenta tem custo de aplicação. Aplicar o instrumento pesado no cliente errado gera desperdício; aplicar o leve no cliente errado gera risco. A triagem calibra isso antes do início.
- **Nenhum passo é pulado em nenhum nível.** Um passo pode se resolver em uma conversa de trinta minutos em N1 e exigir três semanas em N3, mas acontece nos três. O que varia é a profundidade do instrumento, não a existência do passo.

### 3.2 As cinco fases e os dez passos
O percurso tem duas estruturas sobrepostas. Os dez passos organizam o trabalho técnico; as cinco fases organizam a entrega ao cliente. Cada fase encerra com um entregável, e uma fase só encerra quando todos os seus passos atendem à respectiva condição de encerramento.

| Fase | Passos | Entregável | O que a fase decide |
| :--- | :---: | :--- | :--- |
| **F0 — Enquadramento do problema** | Triagem | E1 — Ficha de enquadramento | Se há caso, qual é a dor e qual método aplicar |
| **F1 — Alinhamento estratégico e diagnóstico** | 1, 2 e 3 | E2 — Diagnóstico e oportunidade | Como o processo funciona de fato e quanto ele custa hoje |
| **F2 — Desenho e arquitetura da solução** | 4 e 5 | E3 — Blueprint da solução | O que será construído, com que tecnologia e sob que limites |
| **F3 — Operacionalização e governança** | 6 e 7 | E4 — Guia operacional | Onde a solução entra no fluxo e até onde ela pode ir sozinha |
| **F4 — Piloto, mensuração e calibragem** | 8, 9 e 10 | E5 — Relatório de piloto | Se funcionou, quanto gerou e quem mantém |

> **Portão do passo 5:** O passo 5 opera como portão de três saídas: agente, caso isolado e habilitador acoplado. O percurso pode encerrar antes de F4 sem que isso caracterize falha. A conclusão de que nenhum agente é necessário é um resultado legítimo do passo 5, e a de que nenhum caso sobrevive à zona de contenção é um resultado legítimo do passo 4.

### 3.3 Fase 0 — pré-diagnóstico e triagem
Porte é atalho, não critério. O que muda o método são três eixos.

| Eixo | Pergunta central | O que calibra |
| :--- | :--- | :--- |
| **Complexidade do dado** | Quantos sistemas-fonte? Dado integrado ou disperso? | Passos 2, 3 e 5 |
| **Formalidade da governança** | Existem papéis, políticas e auditoria formais? | Passos 7 e 8 |
| **Criticidade da decisão** | O erro afeta terceiros, dinheiro ou conformidade? | Nível de autonomia, passos 7 e 8 |

#### 3.3.1 Regra de classificação
Cada eixo reúne três perguntas pontuadas de 1 a 3, somando de 3 a 9 pontos. O maior dos três eixos define o nível, e não a média: um eixo alto isolado já obriga o método mais pesado naquele domínio.

| Maior soma entre os eixos | Nível |
| :---: | :--- |
| **3 a 4 pontos** | N1 — Ágil |
| **5 a 7 pontos** | N2 — Estruturado |
| **8 a 9 pontos** | N3 — Corporativo |

O instrumento com as nove perguntas e a regra de pontuação está no artefato EMCIA-TRI-01. A apuração é determinística: nenhum modelo de linguagem decide o nível.

#### 3.3.2 Perfil dos três níveis

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Porte típico** | Startup ou pequena empresa | Média empresa | Grande empresa ou setor regulado |
| **Dado** | Disperso, em planilhas | Sistema de gestão consolidado, integração parcial | Múltiplas fontes, área dedicada |
| **Governança** | Informal | Emergente | Formal e auditada |
| **Decisão** | Centralizada | Por área | Distribuída, com comitês |
| **Ciclo do projeto** | Semanas | Meses | Trimestres |
| **Risco dominante** | Falta de dado confiável | Adoção e integração | Conformidade e auditoria |

#### 3.3.3 Encerramento da Fase 0
> **Encerramento.** A ficha de enquadramento existe com dor delimitada, causa raiz identificada, custo do problema estimado, nível apurado pelos três eixos e objetivo mensurável definido; o patrocinador confirmou o enquadramento; cada número tem origem registrada como declarada, inferida ou verificada.

### 3.4 Os dez passos
Cada passo apresenta a calibragem por nível, o corte e o critério de encerramento. O corte responde à pergunta “devo continuar?”; o encerramento responde a “este passo terminou?”. São perguntas distintas e ambas precisam de resposta antes de avançar.

#### 3.4.1 Passo 1 — Alinhe a IA à estratégia (Fase F1)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Modelo de maturidade** | Conversa com o decisor | Gartner, cinco níveis | Gartner e IBM, triangulados |
| **Amplitude, quatro frentes** | Qualitativa, uma sessão | Nível por frente | Nível por frente, com lacuna e alvo |
| **Patrocinador** | Fundador ou sócio | Diretor de área | Alta direção, formalizado |
| **Caso de negócio** | Estimativa de custo evitado | Retorno projetado | Retorno com VPL e TIR |

- **Corte:** Em N1, se não houver um decisor único disponível em uma reunião, o projeto ainda não está maduro para começar.
- **Encerramento:** O nível de maturidade está registrado nas quatro frentes; o patrocinador está nomeado e confirmou por escrito a prioridade do processo-alvo; cada número do caso de negócio tem origem identificada.

#### 3.4.2 Passo 2 — Mapeie e qualifique os dados (Fase F1)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Instrumento** | Entrevista guiada | Autoavaliação nos domínios críticos | Avaliação completa, com evidências |
| **Inventário de fontes** | Lista simples | Lista com criticidade | Catálogo de dados formal |
| **Glossário** | Dez a vinte termos do processo-alvo | Do domínio | Corporativo, com responsáveis |
| **Qualidade** | Inspeção amostral | Métricas nos campos críticos | Índice de qualidade e acordos de nível |
| **Linhagem** | Não se aplica | Documentada no processo-alvo | Ferramenta de linhagem |

- **Corte:** Em N1, se o levantamento passar de duas semanas, o caso de uso está errado — escolha outro.
- **Encerramento:** O inventário de fontes existe com criticidade atribuída; o glossário do processo-alvo está escrito e confirmado por quem opera o processo; nenhuma fonte crítica permanece classificada apenas como declarada.

#### 3.4.3 Passo 3 — Identifique gargalos e decisões críticas (Fase F1)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Mapeamento do estado atual** | Fluxo em quadro branco | Fluxo documentado por etapa | Modelagem formal do processo |
| **Mapa de valor** | Uma sessão | Completo | Por unidade de negócio |
| **Regras não documentadas** | Levantamento com o executor | Levantamento e observação | Levantamento estruturado, com validação em comitê |
| **Linha de base** | Estimativa com o dono do processo | Medição amostral | Medição sistemática |

- **Corte:** A linha de base é obrigatória nos três níveis. Estimada em N1, medida em N2 e N3, mas sempre registrada antes do piloto.
- **Encerramento:** O fluxo do estado atual está desenhado; as regras não documentadas estão escritas com autoria nominal e passaram por leitura de volta com o executor do processo; a linha de base está registrada e datada; as divergências entre regra escrita e regra praticada estão anotadas.

#### 3.4.4 Passo 4 — Priorize casos de uso (Fase F2)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Matriz de priorização** | Com o decisor | Com donos de área | Validada em comitê |
| **Zona de contenção** | Aplicada | Aplicada | Aplicada, com parecer jurídico |
| **Casos priorizados** | Um | Um a dois | Dois a três, com sequenciamento |
| **Ganho rápido** | Obrigatório como primeiro | Recomendado | Recomendado, para gerar adesão |

- **Corte:** Se nenhum candidato sobrevive à zona de contenção, o percurso encerra aqui com recomendação de não seguir. Esse é um resultado válido do método, não uma falha de aplicação.
- **Encerramento:** Existe decisão do patrocinador registrada sobre o caso a seguir, inclusive quando a decisão é não seguir; a zona de contenção está delimitada por escrito; o critério de priorização foi aplicado a todos os candidatos, e não apenas ao escolhido.

#### 3.4.5 Passo 5 — Defina a arquitetura da solução (Fase F2)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Matriz Problema→Tecnologia** | Aplicada | Aplicada | Aplicada |
| **Camada de contexto** | Glossário e regras em documento | Glossário, catálogo e contratos de dados | Camada semântica formal, versionada, com responsáveis |
| **Arquitetura de dados** | Acesso direto às fontes | Zona curada e acesso governado | Zonas bruta, curada e analítica |
| **Segurança** | Menor privilégio e criptografia | Com classificação da informação | Com gestão de identidade, segregação de funções e duplo fator |
| **Custo e latência** | Estimativa por tarefa | Estimativa com teto mensal | Modelo de custo por caso de uso |

- **Corte:** Em N1, a camada de contexto é um documento, não uma plataforma. Se exigir ferramenta nova, o escopo estourou.
- **Encerramento:** Cada caso priorizado está classificado na Matriz Problema→Tecnologia com justificativa escrita, em uma de três saídas — agente, caso isolado ou habilitador acoplado; a camada de contexto existe no formato previsto para o nível; a estimativa de custo e latência está registrada; os casos que não exigem agente receberam encaminhamento proporcional, e não foram descartados. A especificação por camadas só se abre quando ao menos um caso é classificado como agente.

#### 3.4.6 Passo 6 — Operacionalize a solução (Fase F3)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Integração** | Um a dois sistemas, por interface direta | Sistema de gestão com camada intermediária | Orquestração entre múltiplos sistemas |
| **Redesenho do processo** | Ajuste no fluxo existente | Estado futuro documentado | Estado futuro aprovado pelas áreas |
| **Gestão da mudança** | Conversa com a equipe | Treinamento e comunicação | Plano formal, com recursos humanos |
| **Automação complementar** | Scripts | Automação de tarefas pontual | Automação de tarefas integrada |

- **Corte:** Nos três níveis, a solução entra no fluxo de trabalho, e não ao lado dele. Entrega que para na conversa não cumpre o passo.
- **Encerramento:** O ponto de inserção está identificado nominalmente — quem, em que momento e em que sistema; o estado futuro está descrito no formato previsto para o nível; o plano de mudança tem responsável nomeado.

#### 3.4.7 Passo 7 — Estabeleça governança e conformidade (Fase F3)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Documento de governança** | Termo de autonomia, uma página | Política de uso e papéis nomeados | Política completa, comitê e encarregado de dados |
| **Avaliação de impacto** | Não se aplica | Lista de verificação de risco | Relatório de impacto formal |
| **Auditoria** | Registro das ações da solução | Registro com revisão periódica | Trilha completa e auditável |
| **Níveis de autonomia** | Definidos e registrados | Definidos, com limite de valor | Definidos, com limite e segregação de funções |
| **Viés** | Revisão qualitativa das saídas | Avaliação por subgrupo | Métricas formais de equidade |

- **Corte:** O termo de autonomia é inegociável nos três níveis. Uma página em N1, mas sempre escrito: o que a solução faz sozinha, o que exige aprovação, o que nunca faz.
- **Encerramento:** O termo de autonomia está assinado, com as três listas explícitas; os gatilhos que devolvem a decisão ao humano estão escritos; o registro de auditoria está definido; a avaliação de impacto existe no formato previsto para o nível.

#### 3.4.8 Passo 8 — Pilote, valide e escale (Fase F4)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Modo de piloto** | Assistido direto | Sombra, depois assistido | Sombra, assistido e fatia limitada |
| **Casos de teste** | Quinze a trinta | Cinquenta a cem | Conjunto por cenário e por subgrupo |
| **Duração** | Duas a quatro semanas | Seis a doze semanas | Um a dois trimestres |
| **Reversão** | Desligar a solução | Plano documentado | Plano testado, com portões de qualidade |
| **Aprovação para escalar** | Decisor único | Dono da área, com dados | Comitê |

- **Corte:** Nenhum nível pilota sem conjunto de casos de teste. É o item mais rígido dos dez passos.
- **Encerramento:** O conjunto de casos de teste existe com saída esperada por caso e foi revisado por quem executa o processo; o modo e a duração do piloto estão acordados; o plano de reversão está escrito; o critério de aprovação para escalar foi definido antes do início do piloto.

#### 3.4.9 Passo 9 — Meça o valor gerado (Fase F4)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Métricas mínimas** | Tempo e taxa de acerto | Com adoção e retrabalho | Com nível de serviço, tempo de recuperação e viés por subgrupo |
| **Comparação** | Contra a estimativa da linha de base | Contra a medição da linha de base | Contra a medição, com grupo de controle |
| **Financeiro** | Custo evitado | Retorno realizado | Retorno, VPL e TIR |
| **Reporte** | Conversa com o decisor | Relatório mensal | Painel executivo e placar trimestral |

- **Corte:** Medir adoção não é medir valor. Nos três níveis, ao menos uma métrica precisa ser de resultado do processo, e não de uso da ferramenta.
- **Encerramento:** Ao menos uma métrica de resultado foi apurada contra a linha de base do passo 3; o método de apuração é determinístico e está documentado; o resultado foi reportado ao patrocinador no formato previsto para o nível.

#### 3.4.10 Passo 10 — Aprenda, recalibre e evolua (Fase F4)

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Cadência de revisão** | Mensal, informal | Trimestral, com métricas | Trimestral, com revisão anual de maturidade |
| **Dono da recalibragem** | O decisor | Dono do processo | Papel formal nomeado |
| **Monitoramento** | Revisão de amostras | Observabilidade nos dados críticos | Observabilidade completa, com alertas |
| **Desvio de desempenho** | Percepção do usuário | Verificação periódica | Detecção automatizada |
| **Análise pós-incidente** | Conversa após o incidente | Registro estruturado | Processo formal, com foco em causa e não em culpa |

- **Corte:** O passo 10 precisa de um nome próprio como responsável nos três níveis. Sem dono, a recalibragem não acontece.
- **Encerramento:** O responsável pela recalibragem está nomeado e ciente; a cadência está registrada em calendário; existe canal definido para registro de incidente; a primeira revisão tem data marcada.

### 3.5 Arquétipo e autonomia
O nível não define o arquétipo da solução, mas condiciona a autonomia viável.

| Arquétipo | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Analítico** | Age sozinho | Age sozinho | Age sozinho |
| **Criativo** | Age sozinho | Sugere, humano publica | Sugere, humano publica |
| **Interacional** | Age com aprovação | Age com aprovação | Sombra antes de assistir |
| **Validador** | Sugere | Sugere | Sugere, com revisão dupla |

*Recomendação de entrada:* em N1, arquétipo criativo ou analítico, por retorno rápido e risco baixo; em N2, interacional ou validador em processo de médio impacto; em N3, validador em processo crítico, em modo sombra prolongado.

### 3.6 Os cinco inegociáveis
Cinco exigências não escalam para baixo. Se alguma faltar, o método não foi aplicado, qualquer que seja o nível.

| # | Exigência | Passo |
| :---: | :--- | :---: |
| **1** | Linha de base registrada antes do piloto | Passo 3 |
| **2** | Termo de autonomia escrito: o que faz sozinho, o que aprova, o que nunca faz | Passo 7 |
| **3** | Conjunto de casos de teste com saída esperada | Passo 8 |
| **4** | Ao menos uma métrica de resultado, e não apenas de uso | Passo 9 |
| **5** | Um responsável nomeado pela recalibragem | Passo 10 |

### 3.7 Regras do método

#### 3.7.1 Procedência da informação
Toda informação registrada no percurso recebe uma das três marcas de procedência: **declarada**, quando vem do que a organização informa; **inferida**, quando o engenheiro ou uma ferramenta deduziu a partir de outras informações; **verificada**, quando foi confirmada por observação, documento-fonte ou leitura de volta com quem executa o processo.

Informação inferida não avança para o diagnóstico sem confirmação explícita. A marca de procedência não é atribuída por modelo de linguagem.

#### 3.7.2 Apuração determinística
Classificação de complexidade, custo do problema e indicadores são apurados por critério determinístico. Se um modelo julgasse se uma informação foi verificada, a trava se tornaria probabilística e o risco que ela mitiga retornaria.

#### 3.7.3 Modalidade de contato
O enquadramento admite trabalho assíncrono e a calibragem posterior é remota e recorrente. O levantamento das regras não documentadas, no passo 3, exige presença física: videoconferência produz concordância nominal, enquanto a presença produz decisão assumida.

## 4. Condição de aceite
Este artefato está pronto quando as cinco fases e os dez passos estão descritos com calibragem, corte e critério de encerramento; quando o vocabulário empregado é o do glossário EMCIA-GLO-01; e quando um engenheiro que não participou da construção consegue, lendo apenas este documento, identificar em que passo está e o que falta para encerrá-lo.

## 5. Referências
- *The Knowledge-Creating Company*, Nonaka e Takeuchi (1995)
- *The Tacit Dimension*, Polanyi (1966)
- *Product Leadership*, Cooper (1999)
- *Artificial Intelligence: A Modern Approach*, Russell e Norvig
- *AI Risk Management Framework*, NIST (2023)
- *The GenAI Divide: State of AI in Business*, MIT NANDA (2025)
- Artefatos relacionados: EMCIA-TRI-01, EMCIA-HAB-01, EMCIA-CAT-01, EMCIA-GLO-01, EMCIA-VER-01.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 09/09/2026 | Celso do Vale | Versão inicial: consolidação das cinco fases, dez passos, calibragem e critérios de encerramento | — |
