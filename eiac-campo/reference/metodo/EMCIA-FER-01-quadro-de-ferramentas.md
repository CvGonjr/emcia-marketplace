# Quadro de ferramentas
## Instrumentos administrativos, de negócio, de IA e de Big Data selecionados por fase

| Código | EMCIA-FER-01 | Versão | 0.1 |
| :--- | :--- | :--- | :--- |
| **Data** | 10/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | F0 a F4 — todas | **Passo** | 1 a 10 — todos |

---

## 1. Objetivo
Registrar quais instrumentos são efetivamente aplicados em cada fase do método, com que finalidade e a partir de que nível de complexidade se tornam exigidos. O quadro é uma seleção, e não um inventário: seu valor está tanto no que inclui quanto no que deixa de fora, com a razão da exclusão registrada.

## 2. Escopo e aplicação
Aplica-se ao trabalho do engenheiro de campo ao longo das cinco fases. A coluna de exigência indica o nível a partir do qual o instrumento é obrigatório; nos níveis abaixo dele, o instrumento permanece disponível, mas sua ausência não impede o encerramento do passo.

Cinco documentos auxiliares detalham a aplicação de cada instrumento, um por fase, nos códigos EMCIA-FER-F0-01 a EMCIA-FER-F4-01. Este quadro registra a seleção; os auxiliares registram como aplicar, o erro comum e quando parar.

Não se aplica às ferramentas de construção da solução especificada, que pertencem a quem a constrói. A fronteira é a mesma do método: este documento cobre o que se usa para especificar, não o que se usa para implantar.

## 3. Conteúdo

### 3.1 Critério de seleção
Um instrumento entra no quadro quando atende aos três critérios. Falhar em qualquer um o mantém no acervo de referência, sem uso obrigatório.

| Critério | Pergunta | Falha quando |
| :--- | :--- | :--- |
| **Pertinência** | O instrumento responde à pergunta que o passo precisa responder? | Produz informação que nenhuma decisão do passo consome |
| **Proporcionalidade** | O custo de aplicá-lo é compatível com o nível do cliente? | Exige estrutura que a organização não tem, em nível que não a exige |
| **Executabilidade** | Existe componente que o execute, ou ele depende de trabalho manual indefinido? | Instrumento sem componente não escala; componente sem instrumento produz saída sem método |

### 3.2 Natureza dos instrumentos
Os instrumentos são classificados em quatro naturezas, correspondentes aos domínios que o trabalho articula.

| Prefixo | Natureza | O que caracteriza | Itens |
| :---: | :--- | :--- | :---: |
| **ADM** | Administrativa | Gestão, decisão, escopo, risco e avaliação financeira. Produz decisão registrada. | 24 |
| **NEG** | Negócio | Processo, conhecimento e comportamento organizacional. Produz descrição verificável do que acontece. | 10 |
| **IA** | Inteligência artificial | Escolha de tecnologia, especificação de comportamento e avaliação de desempenho. | 10 |
| **BD** | Big Data | Fontes, arquitetura, qualidade, linhagem, acesso e observabilidade do dado. | 13 |

Cada instrumento recebe sigla estável no formato prefixo e número sequencial, atribuída na ordem de primeira aplicação ao longo das fases. A sigla identifica o instrumento de forma permanente: ela não muda se o instrumento for reposicionado em outro passo, e é por ela que os demais artefatos do método fazem referência ao quadro.

*Instrumentos assinalados com ★ são proprietários e constituem contribuição do próprio método, e não aplicação de referencial existente.*

### 3.3 Ordem de aplicação dos instrumentos proprietários
Três instrumentos proprietários se sucedem em ordem obrigatória, porque cada um consome a saída do anterior.

| Instrumento | Passo | Função e pergunta que responde |
| :--- | :---: | :--- |
| **NEG-07 · Mapa de Valor** | 3 | **Descoberta.** Onde na organização há concentração de oportunidade. |
| **ADM-09 · Matriz de Priorização** | 4 | **Decisão.** O que atacar primeiro, e com que grau de cautela. |
| **IA-01 · Matriz Problema→Tecnologia** | 5 | **Classificação.** Com que tecnologia resolver o caso já escolhido. |

> **Regra de ordem:** Aplicar a Matriz Problema→Tecnologia antes da priorização inverte a lógica e faz o caso de uso ser escolhido pela tecnologia disponível — exatamente o desperdício que o instrumento existe para evitar.

### 3.4 Quadro por fase

#### 3.4.1 Fase F0 — Enquadramento do problema

| Sigla | Ferramenta | Passo | Pergunta que responde | Exigida em |
| :--- | :--- | :---: | :--- | :--- |
| **NEG-01** | 5W2H | F0 | Qual é exatamente a dor, e de quem | Todos |
| **NEG-02** | Cinco porquês | F0 | A causa é raiz ou é sintoma | Todos |
| **NEG-03** | Diagrama de causa e efeito | F0 | A causa está em pessoas, processo, tecnologia ou política | N2 e N3 |
| **ADM-01** | Custo do problema | F0 | Quanto a dor custa hoje | Todos |
| **ADM-02** | Objetivos SMART | F0 | O objetivo é mensurável e datado | Todos |
| **ADM-03** | Delimitação de escopo | F0 | O que fica de fora do engajamento | Todos |
| **ADM-04** | Instrumento de triagem em três eixos ★ | F0 | Qual método aplicar a este cliente | Todos |

#### 3.4.2 Fase F1 — Alinhamento estratégico e diagnóstico

| Sigla | Ferramenta | Passo | Pergunta que responde | Exigida em |
| :--- | :--- | :---: | :--- | :--- |
| **ADM-05** | Maturidade de IA em cinco níveis, Gartner | 1 | Onde a organização está e onde quer chegar | Todos |
| **ADM-06** | Maturidade de IA, IBM | 1 | Leitura alternativa para triangular o diagnóstico | N3 |
| **NEG-04** | Quatro frentes de incorporação | 1 | Em quantas superfícies do negócio a IA já entrou | Todos |
| **NEG-05** | Pirâmide DIKW | 1 | A organização opera com dado, informação ou conhecimento | N2 e N3 |
| **ADM-07** | Caso de negócio com VPL e TIR | 1 | O retorno se sustenta financeiramente | N3 |
| **BD-01** | Modelo de maturidade de dados, CMMI | 2 | A gestão de dados sustenta o caso pretendido | N2 e N3 |
| **BD-02** | Taxonomia de dados por estrutura | 2 | Que natureza de dado o processo consome | Todos |
| **BD-03** | Inventário de fontes internas e externas | 2 | De onde vem cada dado do processo-alvo | Todos |
| **NEG-06** | Glossário de negócio | 2 | As áreas usam os termos com o mesmo sentido | Todos |
| **BD-04** | Catálogo de dados | 2 | Os ativos críticos estão documentados e têm dono | N3 |
| **BD-05** | Linhagem de dados | 2 | É possível rastrear o dado da origem ao uso | N2 e N3 |
| **NEG-07** | Mapa de Valor ★ | 3 | Onde na organização há concentração de oportunidade | Todos |
| **NEG-08** | Mapeamento do fluxo atual | 3 | Como o processo funciona hoje, etapa a etapa | Todos |
| **NEG-09** | Levantamento de regras não documentadas | 3 | O que se faz e não está escrito em lugar nenhum | Todos |
| **ADM-08** | Linha de base de tempo, custo, erro e retrabalho | 3 | Quanto o processo custa antes de qualquer mudança | Todos |

#### 3.4.3 Fase F2 — Desenho e arquitetura da solução

| Sigla | Ferramenta | Passo | Pergunta que responde | Exigida em |
| :--- | :--- | :---: | :--- | :--- |
| **ADM-09** | Matriz de Priorização com zona de contenção ★ | 4 | O que atacar primeiro e com que cautela | Todos |
| **ADM-10** | Matriz de impacto e esforço | 4 | Quais lacunas compensam o esforço de fechar | N2 e N3 |
| **ADM-11** | Identificação de ganho rápido | 4 | O que gera adesão antes do resultado maior | Todos |
| **IA-01** | Matriz Problema→Tecnologia ★ | 5 | Que tecnologia a natureza do problema exige | Todos |
| **IA-02** | Distinção entre IA discriminativa e generativa | 5 | O caso pede prever ou pede criar | Todos |
| **BD-06** | Arquitetura em zonas bruta, curada e analítica | 5 | Como o dado é organizado antes de ser consumido | N2 e N3 |
| **BD-07** | Fluxo de ingestão e tipos de carga | 5 | Com que frescor o dado chega, e a que custo | N2 e N3 |
| **BD-08** | Metadados de negócio e contratos de dados | 5 | O significado do dado está formalizado entre áreas | N2 e N3 |
| **IA-03** | Regras de negócio como testes automáticos | 5 | A regra é verificável em execução, não apenas escrita | N3 |
| **BD-09** | Menor privilégio, controle de acesso e criptografia | 5 | Quem e o que acessa cada dado | Todos |
| **ADM-12** | Classificação da informação | 5 | O controle é proporcional à sensibilidade | N2 e N3 |
| **ADM-13** | Estimativa de custo por tarefa e latência | 5 | A solução cabe no orçamento e no tempo de resposta | Todos |

#### 3.4.4 Fase F3 — Operacionalização e governança

| Sigla | Ferramenta | Passo | Pergunta que responde | Exigida em |
| :--- | :--- | :---: | :--- | :--- |
| **NEG-10** | Redesenho de processo com visão sistêmica | 6 | A solução entra no fluxo ou fica ao lado dele | Todos |
| **BD-10** | Integração com sistema de gestão | 6 | Onde a solução lê e onde escreve | N2 e N3 |
| **IA-04** | Automação determinística complementar | 6 | O que não precisa de modelo para ser resolvido | N2 e N3 |
| **IA-05** | Biblioteca de padrões de instrução | 6 | Como o comportamento esperado é especificado | Todos |
| **ADM-14** | Gestão de mudança | 6 | Quem muda de rotina, e quem conduz essa mudança | Todos |
| **ADM-15** | Termo de autonomia ★ | 7 | O que a solução faz sozinha, aprova ou nunca faz | Todos |
| **ADM-16** | Política de uso e papéis formais | 7 | Quem responde por quê | N2 e N3 |
| **ADM-17** | Avaliação de impacto sobre proteção de dados | 7 | O tratamento de dado pessoal é lícito e proporcional | N3 |
| **BD-11** | Trilha de auditoria das ações da solução | 7 | É possível reconstruir o que a solução fez | Todos |
| **ADM-18** | Segregação de funções | 7 | Quem administra não é quem audita | N3 |
| **IA-06** | Auditoria de desempenho por subgrupo | 7 | A solução trata grupos distintos de forma equivalente | N3 |

#### 3.4.5 Fase F4 — Piloto, mensuração e calibragem

| Sigla | Ferramenta | Passo | Pergunta que responde | Exigida em |
| :--- | :--- | :---: | :--- | :--- |
| **IA-07** | Conjunto de casos de teste com saída esperada ★ | 8 | A solução acerta o que precisa acertar | Todos |
| **IA-08** | Modo sombra e liberação gradual | 8 | Como limitar o alcance de uma falha | N2 e N3 |
| **ADM-19** | Plano de reversão | 8 | Como voltar ao estado anterior, e em quanto tempo | Todos |
| **IA-09** | Métricas de precisão, revocação e F1 | 8 | O acerto é real ou é efeito de base desbalanceada | N2 e N3 |
| **ADM-20** | Comparação contra a linha de base | 9 | O processo melhorou em relação ao que era | Todos |
| **ADM-21** | Retorno financeiro com VPL e TIR | 9 | O investimento se pagou | N3 |
| **BD-12** | Painel de acompanhamento | 9 | O patrocinador enxerga o resultado sem pedir | N2 e N3 |
| **IA-10** | Detecção de desvio de dado e de conceito | 10 | O mundo mudou desde que a solução foi calibrada | N2 e N3 |
| **BD-13** | Observabilidade de dados | 10 | Frescor, volume e distribuição continuam normais | N3 |
| **ADM-22** | Roteiro de resposta a incidente | 10 | O que fazer quando a solução erra | N2 e N3 |
| **ADM-23** | Análise pós-incidente focada em processo | 10 | Por que o erro foi possível | Todos |
| **ADM-24** | Reavaliação de maturidade em 12 a 18 meses | 10 | A organização evoluiu de nível | N2 e N3 |

### 3.5 Instrumentos do acervo não selecionados
A exclusão é registrada para que a seleção possa ser contestada. Em todos os casos abaixo, o instrumento é legítimo e a exclusão decorre do escopo do serviço, não de julgamento sobre sua qualidade.

| Instrumento | Razão da exclusão |
| :--- | :--- |
| **Segundo modelo de maturidade de dados** | Sobreposição integral com o modelo adotado. Dois instrumentos que produzem a mesma decisão dobram o esforço de aplicação sem alterar o resultado. |
| **Repositório de atributos para modelos** | Pressupõe treinamento de modelo próprio. O serviço especifica a solução e não a constrói. |
| **Redução de dimensionalidade para remoção de atributos** | Pertence à construção do modelo, etapa fora do escopo do serviço. |
| **Teste A/B entre versões de modelo** | Exige duas versões em operação simultânea, o que só existe depois da implantação. |
| **Particionamento e formatos colunares** | Decisão de implantação, não de especificação. Entra no blueprint como recomendação, não como instrumento aplicado. |
| **Bibliotecas de mitigação de viés** | Instrumento de quem constrói. No nível N3, o blueprint registra a exigência de avaliação por subgrupo e deixa a escolha da biblioteca para a equipe de construção. |

### 3.6 Lacunas de cobertura
Quatro elementos técnicos aplicados no passo 5 não têm cobertura no acervo de estudo: **geração aumentada por recuperação**, **protocolo de contexto entre modelo e ferramentas**, **armazenamento vetorial** e **camada de memória**. São instrumentos de arquitetura de inteligência, necessários à especificação da solução e sustentados por referencial externo, não pelo acervo.

O registro da lacuna é deliberado: apresentar esses elementos como se derivassem do acervo seria atribuir-lhes lastro que não possuem.

## 4. Condição de aceite
Este artefato está pronto quando todo passo do método tem ao menos um instrumento associado; quando cada instrumento selecionado declara a pergunta que responde e o nível a partir do qual é exigido; quando as exclusões estão registradas com razão; e quando as lacunas de cobertura bibliográfica estão nomeadas em vez de dissimuladas.

## 5. Referências
- *Data Management Maturity Model*, CMMI Institute
- *AI Maturity Model*, Gartner
- *AI Risk Management Framework*, NIST (2023)
- *Product Leadership*, Cooper (1999)
- *Why ontologies matter, why they fail and how to build them as products*, Thoughtworks (2026)
- *Building the foundations for agentic AI at scale*, McKinsey & Company (2026)
- Artefatos relacionados: EMCIA-MET-01, EMCIA-CAT-01, EMCIA-TRI-01, EMCIA-FER-F0-01 a EMCIA-FER-F4-01.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 10/09/2026 | Celso do Vale | Versão inicial: critério de seleção, quatro naturezas, siglas, quadro por fase, exclusões e lacunas | — |
