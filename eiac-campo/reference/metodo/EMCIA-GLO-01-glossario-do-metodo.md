# Glossário do método
## Vocabulário padronizado do percurso, índice de artefatos e índice de siglas

| Código | EMCIA-GLO-01 | Versão | 0.1 |
| :--- | :--- | :--- | :--- |
| **Data** | 14/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Todas | **Passo** | Todos |

---

## 1. Objetivo
Fixar o vocabulário do método, de modo que um engenheiro que não participou de sua construção o aplique com o mesmo sentido. O glossário não descreve o método; ele impede que a descrição seja lida de mais de uma maneira.

## 2. Escopo e aplicação
Cobre os termos do percurso, os termos institucionais da EMCIA, o índice dos artefatos produzidos e o índice de siglas em uso. Aplica-se a todos os documentos do método e aos entregáveis ao cliente.

Não cobre o vocabulário do negócio da organização atendida. Termos como pedido, apólice ou sinistro pertencem ao glossário do processo, levantado no passo 2 e registrado na parte B do E2. Confundir os dois é erro comum: um é vocabulário de quem aplica o método, o outro é vocabulário de quem opera o processo.

## 3. Conteúdo

### 3.1 Critério de inclusão
Um termo entra no glossário se a leitura equivocada dele mudar o que alguém faz.

O critério exclui vocabulário geral de inteligência artificial, que o leitor encontra em outro lugar, e inclui termos aparentemente banais cuja ambiguidade custa caro. “Regra” é o caso exemplar: sem distinguir regra escrita de regra praticada, o passo 3 se reduz a leitura de documentação.

### 3.2 Formato da entrada
Cada entrada tem quatro campos, e o terceiro é o que faz o trabalho. A maior parte da ambiguidade não vem da ausência de definição, e sim do significado vizinho: “verificado” só fica preciso quando contrastado com “confirmado verbalmente pelo interlocutor”, que é o sentido que a maioria atribui.

### 3.3 Percurso e estrutura

| Termo | Definição | O que não é | Onde aparece |
| :--- | :--- | :--- | :--- |
| **Percurso** | Sequência completa das cinco fases e dez passos aplicada a um engajamento | O projeto de construção da solução especificada | MET-01 |
| **Fase** | Agrupamento de passos que encerra com um entregável ao cliente | Etapa de cronograma | MET-01 · E1 a E5 |
| **Passo** | Unidade de trabalho do método, com calibragem, corte e critério de encerramento | Tarefa ou atividade isolada | MET-01 |
| **Engajamento** | Aplicação do percurso a uma organização, da habilitação ao passo 10 | Contrato comercial | HAB-01 |
| **Corte** | Condição que interrompe ou redireciona o percurso. Responde “devo continuar?” | Critério de encerramento | MET-01 |
| **Critério de encerramento** | Condição verificável de que o passo terminou: artefato versionado, confirmação nominal e procedência registrada | Corte; tampouco a entrega do documento | MET-01 |
| **Calibragem** | Ajuste da profundidade do passo ao nível apurado | Supressão do passo — nenhum passo é pulado em nenhum nível | MET-01 |
| **Nível de complexidade** | N1, N2 ou N3. Resultado da triagem; define a profundidade de todo o percurso | Porte da organização | TRI-01 |
| **Eixo** | Dimensão da triagem: DAD, GOV ou CRI | Categoria de risco | TRI-01 |
| **Habilitação** | Etapas 0a a 0d que antecedem o percurso e decidem se ele começa | Fase do método | HAB-01 |
| **Entregável** | Artefato entregue ao cliente ao encerramento de uma fase, E1 a E5 | Artefato interno da EMCIA | E1 a E5 |
| **Artefato** | Documento controlado da EMCIA, com código, versão e condição de aceite | Instrumento ou componente | Todos |
| **Instrumento** | Ferramenta metodológica aplicada em um passo, com sigla no quadro de ferramentas | Componente técnico que a executa | FER-01 |
| **Componente** | Recurso técnico que executa um instrumento | Instrumento | FER-01 · CAT-01 |

### 3.4 Conhecimento e procedência

| Termo | Definição | O que não é | Onde aparece |
| :--- | :--- | :--- | :--- |
| **Regra escrita** | Regra registrada na documentação da organização | Regra praticada | Passo 3 · E2 |
| **Regra praticada** | Regra efetivamente aplicada por quem executa o processo | Regra escrita | Passo 3 · E2 |
| **Regra não documentada** | Regra praticada e ausente da documentação, registrada com autoria nominal | Conhecimento tácito, que é o insumo e não a saída; tampouco regra dispensável | Passo 3 · E2 · CA4 |
| **Levantamento** | Atividade de tornar explícita a regra praticada, com presença e leitura de volta | Entrevista. O termo “elicitação” é recusado, ver anexo C | Passo 3 |
| **Leitura de volta** | Devolução da regra escrita a quem a enunciou, para confirmação ou correção | Aprovação de documento | Passo 3 · E2 |
| **Declarado [D]** | Informação que a organização afirma | Informação verificada | Todos |
| **Inferido [I]** | Informação deduzida pelo engenheiro ou por agente a partir de outras | Informação declarada | Todos |
| **Verificado [V]** | Informação confirmada contra dado, documento-fonte ou leitura de volta | Informação confirmada verbalmente pelo interlocutor | Todos |
| **Procedência** | Marca obrigatória de origem de toda informação registrada | Fonte bibliográfica | CAT-01 · E1 a E5 |
| **Divergência** | Diferença registrada entre o declarado e o observado | Erro do cliente | Passo 2 e 3 · E2 |
| **Placar** | Instrumento que classifica cada regra em alinhada, divergente, não documentada, órfã ou inacessível | Indicador de verificação | Passo 3 |
| **Linha de base** | Medição ou estimativa do processo antes de qualquer intervenção, datada | Meta do projeto | Passo 3 · E2 · E5 |
| **Dossiê** | Conjunto do que o diagnóstico produziu, declarado ou verificado | Entregável. O E2 é o entregável; o dossiê é o conteúdo | E2 |
| **Autodeclaração** | Conjunto de informação apenas declarada, sem verificação | Diagnóstico | VER-01 |

### 3.5 Delegação e autonomia

| Termo | Definição | O que não é | Onde aparece |
| :--- | :--- | :--- | :--- |
| **Atividade delegável** | Atividade que passa nos três testes: fonte, verificabilidade e compromisso | Atividade fácil ou repetitiva | CAT-01 |
| **Trabalho automatizado** | Saída de agente que avança sem decisão humana intermediária | Trabalho híbrido | CAT-01 |
| **Trabalho híbrido** | Saída de agente que não avança sem decisão humana registrada | Automação com revisão facultativa | CAT-01 |
| **Trabalho humano** | Atividade que agente nenhum executa em nenhuma etapa | Atividade sem apoio de ferramenta | CAT-01 |
| **Camada de execução** | EX1 conversacional, EX2 analítica, EX3 verificação, EX4 julgamento | Camadas do agente, CA1 a CA5 | CAT-01 |
| **Trava de camada** | Condição de validade que impede execução fora da camada declarada | Instrução ao agente. A trava não depende de o agente escolher respeitá-la | CAT-01 |
| **Desvio de camada** | Tentativa registrada de execução fora da camada | Erro de execução | CAT-01 · ação 3.7 |
| **Habilidade** | Capacidade modular com insumo, saída e critério de verificação. Siglas HB-01 a HB-18 | Agente | CAT-01 |
| **Agente interno** | Agente que opera para o engenheiro de campo. Siglas AG-01 a AG-04 | Agente especificado ao cliente | CAT-01 |
| **Agente especificado** | Unidade descrita no blueprint para a organização cliente | Agente interno | E3, parte B |
| **Arquétipo** | Analítico, criativo, interacional ou validador | Tecnologia empregada | Passo 4 · E3 |
| **Autonomia** | O que a unidade faz sozinha, o que exige aprovação e o que nunca faz | Capacidade técnica da unidade | Passo 7 · E3 · E4 |
| **Termo de autonomia** | Documento assinado no passo 7 que torna a autonomia vinculante | Matriz de autonomia do E3, que é proposta | Passo 7 · E4 |
| **Zona de contenção** | Delimitação de risco aplicada sobre os casos candidatos | Lista de requisitos regulatórios | Passo 4 · E3 |
| **Bloqueio** | Política determinística aplicada no ponto de passagem | Instrução ao modelo, que é probabilística | E3, CA1 |

### 3.6 Verificação

| Termo | Definição | O que não é | Onde aparece |
| :--- | :--- | :--- | :--- |
| **Execução declarada** | Execução do método apoiada apenas no que a organização informa, conduzida sem intervenção humana nas etapas de produção | Execução malfeita ou apressada | VER-01 · Sprint 2 |
| **Execução de campo** | Execução com observação, leitura de volta e acesso às fontes | Execução completa em oposição a parcial | VER-01 · Sprint 3 |
| **Selamento** | Fechamento datado e não alterável da execução declarada, anterior a qualquer contato de campo | Arquivamento | VER-01 · ação 2.9 |
| **Predição registrada** | Afirmação sobre o que a comparação encontrará, com critério de refutação declarado antes da execução | Hipótese | VER-01 |
| **Indicador** | Medida com fórmula, fonte, valor de sucesso e limiar de falha | Predição | VER-01 |
| **Falha da verificação** | Condição que invalida a comparação e impede qualquer conclusão | Refutação da hipótese | VER-01 |
| **Refutação** | Resultado que contradiz a hipótese. É resultado legítimo e deve ser relatado | Falha da verificação | VER-01 |
| **Restrição registrada** | Limitação de verificação ligada ao item específico que ela afeta | Ressalva genérica ao final do documento | HAB-01 · E1 a E5 |
| **Pendência bloqueante** | Pendência que impede o encerramento da fase | Item em aberto | VER-01 · E5 |
| **Reclassificação** | Recálculo do nível após a verificação contradizer o declarado, com registro da mudança | Correção de erro de apuração | TRI-01 |

### 3.7 Contexto e solução

| Termo | Definição | O que não é | Onde aparece |
| :--- | :--- | :--- | :--- |
| **Camada de contexto** | Conjunto versionado de glossário, entidades, regras verificadas e política de decisão que governa a solução | Base de conhecimento para recuperação | Passo 5 · E3, CA4 |
| **Ontologia** | Modelo de entidades e relações do domínio, com donos nomeados | Camada de contexto, que a contém | E3, CA4 |
| **Glossário do método** | Este documento. Vocabulário de quem aplica o método | Glossário do processo | GLO-01 |
| **Glossário do processo** | Termos do negócio do cliente, levantados no passo 2 | Glossário do método | Passo 2 · E2, parte B |
| **Entidade** | Objeto do domínio do cliente, com atributos e relações | Termo do glossário | E3, CA4 |
| **Contrato de dados** | Acordo formal sobre estrutura, significado e qualidade de uma fonte | Autorização de acesso | E3, CA4 e CA5 |
| **Blueprint da solução** | O entregável E3 por inteiro, incluindo a decisão de não construir agente algum | Blueprint do agente | E3 |
| **Blueprint do agente** | A parte B do E3, que só existe se houver caso classificado como agêntico | Blueprint da solução | E3, parte B |
| **Unidade de solução** | Objeto especificado na parte B, seja ele agente ou não | Agente | E3, parte B |
| **Caso isolado** | Caso resolvido por automação, aprendizado de máquina ou processamento de linguagem, sem agente | Caso descartado | Passo 5 · E3 |
| **Habilitador acoplado** | Caso não agêntico de que um caso agêntico depende | Caso isolado | Passo 5 · E3 |
| **Ponto de inserção** | Quem, em que momento e em que sistema a solução entra no fluxo | Integração técnica | Passo 6 · E4 |
| **Ponto de passagem** | Componente que aplica políticas entre o agente e o que ele aciona | Integração | E3, CA1 |

### 3.8 Termos institucionais

| Termo | Definição | O que não é | Onde aparece |
| :--- | :--- | :--- | :--- |
| **EMCIA** | Engenharia de Métodos e Contexto em IA Aplicada | — | Todos |
| **Serviço** | Aplicação do método a uma organização por engenheiro de campo | Produto | Institucional |
| **Produto** | Ambiente de apoio que instrumenta as etapas delegáveis do método | Serviço | Institucional |
| **Estúdio** | Nome do ambiente de apoio | Plataforma entregue ao cliente | Institucional |
| **Engenheiro de campo** | Quem conduz o percurso e responde pela verificação | Consultor, ver anexo C | Institucional |
| **Engenheiro de IA** | Quem constrói e mantém o estúdio, a camada de contexto e as integrações | Engenheiro de campo | Institucional |
| **Organização participante** | Organização em que o percurso é aplicado para fins de verificação | Cliente | VER-01 · Sprint 3 |
| **Documento controlado** | Artefato com código estável, versão, responsável e condição de aceite | Documento de trabalho | Todos |

## 4. Regra de manutenção
Termo entra quando uma divergência de leitura aparece, e não por antecipação. Glossário redigido preventivamente registra os termos que o autor imaginou ambíguos, e não os que de fato o são.

Cada versão é datada. A alteração de uma definição exige registro do que mudou, porque artefato produzido sob a definição anterior permanece válido sob ela — e a data é o que permite saber qual definição vigorava.

## 5. Condição de aceite
Este artefato está pronto quando todo termo empregado nos demais artefatos com sentido próprio consta aqui; quando cada entrada declara o que o termo não é; quando os termos padronizados registram o sinônimo recusado; e quando um engenheiro que não participou da construção lê um artefato do método sem precisar perguntar o que uma expressão significa.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 14/09/2026 | Celso do Vale | Versão inicial: 77 termos em seis grupos, quatro anexos, índice de artefatos e índice de siglas | — |

---

## Anexo A — Índice de artefatos
Artefatos produzidos na Sprint 1. O código é estável ao longo das versões; a versão muda a cada revisão aprovada.

| Código | Artefato | O que fixa | Ação |
| :--- | :--- | :--- | :---: |
| **EMCIA-MET-01** | Documento do método | Cinco fases, dez passos, calibragem por nível, cortes e critérios de encerramento | 1.1 |
| **EMCIA-CAT-01** | Fronteira de delegação | Três testes de delegação, naturezas de trabalho, camadas de execução e catálogo de agentes e habilidades | 1.2 |
| **EMCIA-FER-01** | Quadro de ferramentas | Instrumentos aplicados por fase, exclusões registradas e lacunas de cobertura | 1.3 |
| **EMCIA-HAB-01** | Protocolo de habilitação | Etapas 0a a 0d, quatro pré-requisitos e três desfechos | 1.4 |
| **EMCIA-TRI-01** | Instrumento de triagem | Nove perguntas em três eixos, regra de leitura e verificação posterior | 1.5 |
| **EMCIA-E1-01** | Modelo · Ficha de enquadramento | Estrutura do entregável da Fase F0 | 1.6 |
| **EMCIA-E2-01** | Modelo · Diagnóstico e oportunidade | Estrutura do entregável dos passos 1 a 3, em três partes por público | 1.6 |
| **EMCIA-E3-01** | Modelo · Blueprint da solução | Estrutura do entregável dos passos 4 e 5, com portão entre decisão e especificação | 1.6 |
| **EMCIA-E4-01** | Modelo · Guia operacional | Estrutura do entregável dos passos 6 e 7 | 1.6 |
| **EMCIA-E5-01** | Modelo · Relatório de piloto | Estrutura do entregável dos passos 8 a 10 | 1.6 |
| **EMCIA-FER-F0-01 a F4-01** | Ferramentas em detalhe, um por fase | Ficha de cada instrumento: para que serve, quando e como aplicar, erro comum e encerramento | 1.3 |
| **EMCIA-VER-01** | Plano de verificação | Duas execuções, selamento, predições, indicadores e critérios de falha | 1.7 |
| **EMCIA-GLO-01** | Glossário do método | Vocabulário padronizado, índice de artefatos e índice de siglas | 1.8 |

*O modelo de documento controlado é gabarito de formatação, e não artefato do método.*

## Anexo B — Índice de siglas

| Família | Faixa | Significado | Lista oficial em |
| :--- | :--- | :--- | :--- |
| **Fases** | F0 a F4 | Enquadramento do problema, Alinhamento e diagnóstico, Desenho e arquitetura, Operacionalização e governança, Piloto, mensuração e calibragem | MET-01 |
| **Níveis** | N1 a N3 | Ágil, Estruturado, Corporativo | MET-01 · TRI-01 |
| **Habilitação** | 0a a 0d | Qualificação do contato, Formalização, Concessão de acesso, Abertura do caso | HAB-01 |
| **Entregáveis** | E1 a E5 | Um por fase, do enquadramento ao relatório de piloto | E1 a E5 |
| **Eixos da triagem** | DAD · GOV · CRI | Complexidade do dado, Formalidade da governança, Criticidade da decisão | TRI-01 |
| **Perguntas da triagem** | DAD-1 a CRI-3 | Três por eixo, nove ao todo | TRI-01 |
| **Camadas de execução** | EX1 a EX4 | Conversacional, Analítica, Verificação, Julgamento | CAT-01 |
| **Agentes internos** | AG-01 a AG-04 | Enquadramento, Análise documental, Especificação, Avaliação | CAT-01 |
| **Habilidades** | HB-01 a HB-18 | Capacidades delegáveis, com insumo, saída e critério de verificação | CAT-01 |
| **Camadas do agente** | CA1 a CA5 | Controle, Agente, Protocolos, Contexto, Dados | E3, parte B |
| **Blocos da Parte B** | B1 a B7 | Fronteira, Camadas, Tecnologias, Requisitos, Avaliação e riscos, Plano de construção, Passagem | E3, parte B |
| **Modos de delegação** | Sombra · Sugestão · Aprovação prévia · Exceção · Autônomo | Arranjo da interação entre agente e humano, por ação delegada | E3, B1 |
| **Ferramentas** | ADM · NEG · IA · BD | Administrativa (24), Negócio (10), Inteligência artificial (10), Big Data (13) | FER-01 |
| **Indicadores do objetivo** | ENT · CRC · MCT · RIV · ESF | Entregáveis, Conhecimento recuperado, Mudança de classificação, Regra inferida sem validação, Esforço | VER-01 |
| **Indicadores complementares** | CE · TDIV · PEND | Cobertura de encerramento, Taxa de divergência, Pendências bloqueantes | VER-01 |
| **Predições** | P1 a P6 | Registradas antes da execução de campo, com critério de refutação | VER-01 |
| **Procedência** | [D] · [I] · [V] | Declarado, Inferido, Verificado | CAT-01 · E1 a E5 |
| **Hipóteses** | H1 a H5 | H4 é a priorizada; H5 é sua condição de eficácia | Seção 2 do relatório |

*As 57 ferramentas aparecem por família com a respectiva contagem. A lista completa permanece no FER-01: repeti-la aqui criaria duas fontes de verdade.*

## Anexo C — Padronizações e sinônimos recusados
Registrar o termo recusado importa tanto quanto o adotado, porque é o recusado que reaparece quando se escreve no automático.

| Termo adotado | Termo recusado | Razão |
| :--- | :--- | :--- |
| **Levantamento** | Elicitação | Sem correspondência estabelecida em português; o termo adotado é compreendido por quem opera o processo |
| **Regra não documentada** | Regra tácita | O que o passo produz é regra escrita; “tácita” descreve o insumo, não a saída |
| **Blueprint da solução** | Blueprint da camada agêntica | O passo 5 conserva autoridade para concluir que nenhum agente é necessário |
| **Ponto de passagem** | Gateway | Descrição funcional é aplicável por quem não conhece o termo em inglês |
| **Engenheiro de campo** | Consultor | O papel responde pela verificação, e não apenas pela recomendação |
| **Organização participante** | Cliente | No contexto da verificação, a organização participa de um estudo, não de um contrato |
| **Repositório analítico central** | Data warehouse · data lake | Instrumento respondido pelo cliente não pode depender de o cliente conhecer a sigla |
| **Encarregado por proteção de dados** | DPO | Mesma razão |

## Anexo D — Termos que o mercado usa em outro sentido

| Termo | Uso corrente no mercado | Sentido neste método |
| :--- | :--- | :--- |
| **Agente** | Qualquer aplicação baseada em modelo de linguagem | Unidade com ferramentas, autonomia declarada e limites conversíveis em política |
| **Ontologia** | Vocabulário controlado ou taxonomia | Modelo de entidades e relações com donos nomeados, parte da camada de contexto |
| **Blueprint** | Documento de arquitetura técnica | Entregável que inclui a decisão de negócio, e não apenas a arquitetura |
| **Contexto** | Conteúdo enviado ao modelo na chamada | Camada versionada de regras verificadas que governa a decisão |
| **Governança** | Conjunto de políticas corporativas | Autonomia declarada, auditoria e avaliação de impacto, calibradas por nível |
| **Maturidade** | Estágio geral de adoção de tecnologia | Posição por frente de incorporação, apurada com instrumento declarado |
| **Piloto** | Teste informal com usuários | Execução com casos de teste, critério de aprovação datado e plano de reversão |
