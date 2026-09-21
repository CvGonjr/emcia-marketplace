# Protocolo de Campo por Passo — P6 a P10

*Entrada, atividade, saída e encerramento das fases de operacionalização e piloto*

| | | | |
|---|---|---|---|
| **Código** | EMCIA-CAM-01 | **Versão** | 0.1 |
| **Data** | 17/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Sprint 2 — Implementação | **Passo** | Ação 2.3 |

## 1. Objetivo

Tornar executáveis os cinco passos que o método descreve por calibragem e critério de encerramento, mas não por procedimento: P6 a P10. Cada passo recebe o mesmo enquadramento — entrada, atividade, saída, encerramento, fronteira de delegação e registro no estado — e os quatro formatos que os itens inegociáveis 2 a 5 exigem passam a existir como anexos.

Sem este documento, as fases F3 e F4 não possuem habilidade carregável e os portões E4 e E5 validam a existência de artefatos cujo conteúdo mínimo nunca foi definido.

## 2. Escopo e aplicação

Aplica-se aos passos P6, P7, P8, P9 e P10, nas fases F3 — operacionalização e governança — e F4 — piloto, mensuração e calibragem. Vale nos três níveis, com a calibragem indicada em cada passo.

Na prova de conceito, estes passos são percorridos e produzem seus artefatos, mas **não são apresentados como validados em operação real da solução do cliente**. O protocolo define o procedimento; a execução na PoC demonstra que o percurso e os portões operam, não que o agente do cliente funcionou em produção.

Fica fora: a construção da solução empresarial, a integração com sistemas do cliente e a operação do piloto propriamente dita.

## 3. Conteúdo

### 3.1 Enquadramento comum

Todo passo de F3 e F4 é descrito por seis elementos. A uniformidade é o que permite converter o passo em habilidade sem reinterpretação.

| Elemento | O que declara |
|---|---|
| **Entrada** | O que precisa existir antes; passo sem entrada satisfeita não abre |
| **Atividade** | O que se faz, em ordem |
| **Saída** | O artefato produzido, com formato definido |
| **Encerramento** | Condições verificáveis, não impressão de conclusão |
| **Fronteira** | O que o Estúdio prepara e o que permanece humano |
| **Registro** | O que o estado do caso guarda ao encerrar |

### 3.2 P6 — Operacionalize a solução

**Fase F3 · camada EX3 · modalidade presencial ou remota conforme o nível**

| Elemento | Conteúdo |
|---|---|
| Entrada | E3-E emitido; caso classificado como agente em P5; camada de contexto registrada |
| Saída | Ponto de inserção nominado, estado futuro descrito e plano de mudança com responsável |
| Encerramento | Quem, em que momento e em que sistema está identificado nominalmente; o estado futuro existe no formato do nível; o plano de mudança tem responsável nomeado |

**Atividade, em ordem:**

1. Localizar no fluxo atual o momento exato em que a solução entra — não a área, o momento.
2. Nomear a pessoa que recebe a saída da solução e o que ela faz com ela.
3. Descrever o estado futuro do processo, no formato do nível, marcando o que muda e o que permanece.
4. Registrar as tarefas que deixam de ser feitas e quem hoje as executa.
5. Definir o plano de mudança: quem comunica, quem treina, em que prazo.

**Corte.** A solução entra no fluxo de trabalho, não ao lado dele. Entrega que para na conversa não cumpre o passo.

| Nível | Integração | Estado futuro | Mudança |
|---|---|---|---|
| N1 | Um a dois sistemas, interface direta | Ajuste no fluxo existente | Conversa com a equipe |
| N2 | Sistema de gestão com camada intermediária | Documentado | Treinamento e comunicação |
| N3 | Orquestração entre múltiplos sistemas | Aprovado pelas áreas | Plano formal, com recursos humanos |

**Fronteira.** O Estúdio pode redigir o estado futuro a partir do mapa do Passo 3 e listar candidatos a ponto de inserção. A escolha do ponto e a nomeação das pessoas são humanas — dependem de decisão organizacional que nenhuma leitura de processo revela.

### 3.3 P7 — Estabeleça governança e conformidade

**Fase F3 · camada EX4 · decisão humana registrada**

| Elemento | Conteúdo |
|---|---|
| Entrada | P6 encerrado; arquétipo definido; zona de contenção delimitada em P4 |
| Saída | Termo de autonomia assinado (Anexo A), definição do registro de auditoria e avaliação de impacto no formato do nível |
| Encerramento | As três listas estão explícitas e assinadas; os gatilhos de devolução ao humano estão escritos; o registro de auditoria está definido; a avaliação de impacto existe no formato do nível |

**Atividade, em ordem:**

1. Recuperar o arquétipo e a autonomia viável para o nível.
2. Preencher as três listas do termo — o que a solução faz sozinha, o que exige aprovação, o que nunca faz.
3. Escrever os gatilhos que devolvem a decisão ao humano, com o critério que os aciona.
4. Definir o que o registro de auditoria guarda e por quanto tempo.
5. Produzir a avaliação de impacto no formato do nível.
6. Colher assinatura do responsável pela decisão.

**Corte.** O termo de autonomia é inegociável nos três níveis. Uma página em N1, mas sempre escrito.

| Nível | Documento | Impacto | Autonomia |
|---|---|---|---|
| N1 | Termo de autonomia, uma página | Não se aplica | Definida e registrada |
| N2 | Política de uso e papéis nomeados | Lista de verificação de risco | Com limite de valor |
| N3 | Política completa, comitê e encarregado de dados | Relatório formal | Com limite e segregação de funções |

**Fronteira.** É o segundo ponto humano do percurso, ao lado de P3b. O Estúdio produz a minuta por HB-14, com as três listas em branco. Preencher as listas, definir limites e assinar são atos humanos; tentativa de conclusão por agente é recusada e registrada.

### 3.4 P8 — Pilote, valide e escale

**Fase F4 · camada EX3 · conjunto de testes revisado por quem executa o processo**

| Elemento | Conteúdo |
|---|---|
| Entrada | P7 encerrado; termo de autonomia assinado; linha de base do Passo 3 registrada |
| Saída | Conjunto de casos de teste com saída esperada (Anexo B), modo e duração acordados, plano de reversão escrito |
| Encerramento | Cada caso tem saída esperada e o conjunto foi revisado por quem executa o processo; modo e duração estão acordados; o plano de reversão está escrito; o critério de aprovação para escalar foi definido antes do início do piloto |

**Atividade, em ordem:**

1. Derivar os casos de teste das regras registradas na camada de contexto, priorizando a célula crítica — regras raras de alta consequência.
2. Escrever a saída esperada de cada caso, antes de qualquer execução.
3. Submeter o conjunto à revisão de quem executa o processo.
4. Acordar modo de piloto e duração conforme o nível.
5. Escrever o plano de reversão.
6. Definir o critério de aprovação para escalar — antes de começar, não depois de ver o resultado.

**Corte.** Nenhum nível pilota sem conjunto de casos de teste. É o item mais rígido do método.

| Nível | Modo | Casos | Duração | Reversão |
|---|---|---|---|---|
| N1 | Assistido direto | 15 a 30 | 2 a 4 semanas | Desligar a solução |
| N2 | Sombra, depois assistido | 50 a 100 | 6 a 12 semanas | Plano documentado |
| N3 | Sombra, assistido e fatia limitada | Por cenário e subgrupo | 1 a 2 trimestres | Plano testado, com portões |

**Fronteira.** HB-15 gera os casos e HB-16 executa a suíte, ambas híbridas. A revisão por quem executa o processo é condição de validade do conjunto, não etapa opcional de qualidade.

### 3.5 P9 — Meça o valor gerado

**Fase F4 · camada EX3 · apuração determinística**

| Elemento | Conteúdo |
|---|---|
| Entrada | P8 encerrado; piloto executado; linha de base disponível |
| Saída | Plano de medição preenchido (Anexo C), com ao menos uma métrica de resultado apurada |
| Encerramento | Ao menos uma métrica de resultado foi apurada contra a linha de base do Passo 3; o método de apuração é determinístico e está documentado; o resultado foi reportado ao patrocinador no formato do nível |

**Atividade, em ordem:**

1. Recuperar a linha de base e sua procedência — estimada em N1, medida em N2 e N3.
2. Apurar cada métrica pelo método documentado, sem ajuste posterior de critério.
3. Comparar contra a linha de base, preservando a marca de procedência de ambos os lados.
4. Registrar o que não pôde ser apurado e por quê.
5. Reportar ao patrocinador no formato do nível.

**Corte.** Medir adoção não é medir valor. Ao menos uma métrica precisa ser de resultado do processo, e não de uso da ferramenta.

| Nível | Métricas mínimas | Comparação | Financeiro |
|---|---|---|---|
| N1 | Tempo e taxa de acerto | Contra a estimativa | Custo evitado |
| N2 | Com adoção e retrabalho | Contra a medição | Retorno realizado |
| N3 | Com nível de serviço, recuperação e viés por subgrupo | Com grupo de controle | Retorno, VPL e TIR |

**Fronteira.** HB-17 consolida os indicadores. A apuração é determinística por exigência do método: se um modelo julgasse se uma métrica foi atingida, a trava se tornaria probabilística.

### 3.6 P10 — Aprenda, recalibre e evolua

**Fase F4 · camada EX4 na decisão, EX2 no monitoramento · etapa recorrente**

| Elemento | Conteúdo |
|---|---|
| Entrada | P9 encerrado; solução em operação ou piloto concluído |
| Saída | Rotina de recalibragem instalada (Anexo D), com responsável nomeado e cadência em calendário |
| Encerramento | O responsável está nomeado — pessoa, não área — e ciente; a cadência está registrada em calendário; existe canal definido para registro de incidente; a primeira revisão tem data marcada |

**Atividade, em ordem:**

1. Nomear o responsável e obter sua ciência registrada.
2. Fixar a cadência conforme o nível e lançá-la em calendário.
3. Definir os limiares de desvio, antes do piloto e não a posteriori.
4. Definir o canal de registro de incidente e o formato da análise pós-incidente.
5. Marcar a data da primeira revisão.

**Corte.** O passo exige nome próprio como responsável nos três níveis. Sem dono, a recalibragem não acontece.

| Nível | Cadência | Dono | Monitoramento | Desvio |
|---|---|---|---|---|
| N1 | Mensal, informal | O decisor | Revisão de amostras | Percepção do usuário |
| N2 | Trimestral, com métricas | Dono do processo | Observabilidade nos dados críticos | Verificação periódica |
| N3 | Trimestral, com revisão anual de maturidade | Papel formal nomeado | Completa, com alertas | Detecção automatizada |

**Fronteira.** HB-18 monitora desvio contra limiar definido previamente. A decisão de recalibrar, expandir ou descontinuar é humana. O estado registra cadência, responsável e data da última verificação — sem esse registro, a etapa desaparece após a primeira execução.

### 3.7 Condições executáveis para o Code Plugin

| # | Tentativa | Resultado |
|---|---|---|
| M1 | Abrir P6 sem E3-E emitido | Recusa — não há solução a operacionalizar |
| M2 | Encerrar P6 com ponto de inserção descrito por área | Recusa — exige pessoa e momento |
| M3 | Agente concluir P7 ou preencher as três listas | Recusa e registro de tentativa negada |
| M4 | Emitir E4 sem termo de autonomia com as três listas | Recusa — inegociável 2 |
| M5 | Registrar caso de teste sem saída esperada | Recusa — inegociável 3 |
| M6 | Encerrar P8 com conjunto não revisado por executor | Recusa |
| M7 | Emitir E5 com métricas exclusivamente de uso | Recusa — inegociável 4 |
| M8 | Registrar responsável de P10 como nome de área | Recusa — inegociável 5 |
| M9 | Carregar P10 sem cadência declarada | Playbook não carrega |
| M10 | Alterar limiar de desvio após o início do piloto | Recusa; alteração exige nova versão com justificativa |

### 3.8 Registro no estado do caso

Ao encerrar cada passo, o estado guarda: identificação do passo, data, responsável nomeado, artefato produzido, condições de encerramento satisfeitas e, para P10, cadência e data da última verificação. Etapa recorrente atualiza a última verificação sem apagar o histórico.

## 4. Condição de aceite

O protocolo está pronto quando cada um dos cinco passos declara entrada, atividade ordenada, saída com formato definido, encerramento verificável e fronteira de delegação; quando os quatro formatos dos anexos permitem preencher os inegociáveis 2 a 5 sem inventar estrutura; quando as condições M1 a M10 podem ser convertidas em recusa do núcleo; e quando um engenheiro que não participou da construção consegue conduzir P6 a P10 sem decidir novamente o que cada passo produz.

## 5. Referências

- EMCIA-MET-01 — Documento do método, Passos 6 a 10.
- EMCIA-CAT-01 — Fronteira de delegação, HB-14 a HB-18 e AG-04.
- EMCIA-CTX-01 — Instrumento de registro da camada de contexto.
- EMCIA-ROT-01 — Roteiro de levantamento de regras não documentadas.
- EMCIA-ESP-01 — Especificação executável do Estúdio de Trabalho.
- EMCIA-TST-01 — Plano de testes da implementação.
- EMCIA-E4 — Modelo de guia operacional.
- EMCIA-E5 — Modelo de relatório de piloto.
- NIST. *AI Risk Management Framework* (2023).

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
|---|---|---|---|---|
| 0.1 | 17/09/2026 | Celso do Vale | Versão inicial: enquadramento comum, protocolo de P6 a P10, condições executáveis M1–M10 e os quatro formatos dos inegociáveis 2 a 5. | — |

---

## Anexo A — Termo de autonomia

Inegociável 2. Uma página em N1; documento de política em N2 e N3. As três listas são obrigatórias em qualquer formato.

| Seção | Conteúdo mínimo |
|---|---|
| Identificação | Solução, processo-alvo, nível, arquétipo, data, versão |
| **Faz sozinha** | Ações executadas sem aprovação prévia, uma por linha, com o limite que as delimita |
| **Exige aprovação** | Ações que dependem de autorização, com quem aprova e em que prazo |
| **Nunca faz** | Ações vedadas, incluindo a zona de contenção delimitada em P4 |
| Gatilhos de devolução | Condição que devolve a decisão ao humano e o critério que a aciona |
| Limites | Valor, volume ou alcance, quando aplicável ao nível |
| Registro de auditoria | O que é guardado, por quanto tempo e quem consulta |
| Assinatura | Nome, papel e data do responsável pela decisão |

Uma lista vazia é resposta válida e precisa estar escrita como tal. Lista ausente não é.

## Anexo B — Caso de teste com saída esperada

Inegociável 3. A saída esperada é escrita antes de qualquer execução.

| Campo | Conteúdo |
|---|---|
| Identificador | Código sequencial no conjunto |
| Origem | Regra da camada de contexto que o caso exercita |
| Entrada | Situação apresentada à solução, com os dados necessários |
| Saída esperada | Resultado correto, descrito de forma verificável |
| Critério de aprovação | O que distingue acerto de erro neste caso |
| Categoria | Comum · exceção · célula crítica |
| Revisor | Pessoa que executa o processo e revisou o caso |
| Data da revisão | — |

O conjunto precisa cobrir a célula crítica do quadro frequência × consequência. Conjunto composto apenas de casos comuns não satisfaz o passo, porque reproduz o viés do histórico.

## Anexo C — Plano de medição

Inegociável 4. Ao menos uma métrica precisa ser de resultado do processo.

| Campo | Conteúdo |
|---|---|
| Métrica | Nome e o que mede |
| Tipo | **Resultado** · uso · qualidade |
| Linha de base | Valor, data e procedência (D, I ou V) |
| Método de apuração | Fórmula ou procedimento determinístico, documentado |
| Fonte do dado | Registro de onde o valor é extraído |
| Periodicidade | — |
| Responsável pela apuração | Pessoa nomeada |
| Resultado apurado | Valor, data e procedência |

Métricas de uso podem compor o plano, mas não satisfazem sozinhas o portão de E5.

## Anexo D — Rotina de recalibragem

Inegociável 5. O responsável é pessoa nomeada; área não satisfaz.

| Campo | Conteúdo |
|---|---|
| Responsável | Nome, papel e registro de ciência |
| Cadência | Conforme o nível, lançada em calendário |
| Data da primeira revisão | — |
| Limiares de desvio | Definidos antes do piloto; alteração exige nova versão justificada |
| Monitoramento | O que é observado e por qual meio |
| Canal de incidente | Onde se registra e quem recebe |
| Análise pós-incidente | Formato previsto para o nível, com foco em causa e não em culpa |
| Última verificação | Data, atualizada a cada ciclo sem apagar o histórico |
