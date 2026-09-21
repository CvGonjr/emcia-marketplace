# Roteiro de Levantamento de Regras Não Documentadas

*Procedimento presencial do Passo 3, com critério de encerramento e registro de autoria*

| | | | |
|---|---|---|---|
| **Código** | EMCIA-ROT-01 | **Versão** | 0.1 |
| **Data** | 17/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Sprint 2 — Implementação | **Passo** | Ação 2.1 |

## 1. Objetivo

Definir o procedimento pelo qual o engenheiro de campo levanta, registra e verifica as regras que governam o processo-alvo e não constam de sistemas, procedimentos ou normas. O roteiro torna a etapa P3b aplicável por um engenheiro que não participou da construção do método e estabelece quando ela pode ser considerada encerrada.

O documento não descreve o que fazer com as regras depois de levantadas — isso pertence ao instrumento de registro da camada de contexto (ação 2.2) e ao Passo 5. Aqui se trata de como obtê-las, como registrá-las e como saber que o levantamento terminou.

## 2. Escopo e aplicação

Aplica-se à etapa **P3b**, integrante do Passo 3 e da Fase F1, em qualquer nível de complexidade. A etapa opera em **EX4 — camada humana**, é presencial e não admite comando de agente que a conclua.

O Passo 3 desdobra-se em três etapas operacionais, e apenas a segunda é objeto deste roteiro:

| Etapa | Conteúdo | Camada |
|---|---|---|
| P3a | Preparação: lista de verificação derivada da Fase 0, recorte dos casos concretos, leitura das fontes | EX2 |
| **P3b** | **Sessão presencial de levantamento e observação** | **EX4** |
| P3d | Confronto entre regra escrita e regra praticada, placar e registro de divergência | EX3 |

Ficam fora do roteiro: a apuração da linha de base, o mapa de valor e o desenho do estado atual, que pertencem ao mesmo passo mas têm instrumentos próprios.

## 3. Conteúdo

### 3.1 Princípios do levantamento

1. **Caso concreto, não pergunta geral.** A pergunta "como você decide isso?" produz o procedimento que a pessoa acredita seguir. O caso já resolvido produz o que ela fez.
2. **A exceção é o objeto, não o desvio.** A regra geral costuma estar escrita. O que sustenta o desempenho atual é o tratamento das exceções, e é ele que não está registrado.
3. **Ausência não é contradição.** A instrução que decide o resultado é omitida pela fonte, não negada por ela. Por isso a leitura de documentos não substitui a sessão.
4. **O executor é autor, não fonte.** Toda regra registrada recebe autoria nominal e é submetida a leitura de volta. Quem opera o processo responde pelo conteúdo e pode corrigi-lo.
5. **Toda regra declara a origem do conhecimento.** Documento, ensino, experiência própria ou origem desconhecida. Sem essa coluna, a observação produz anedota e a regra não pode ser classificada depois.
6. **Regra classificada como automatizável exige segunda confirmação.** É a mitigação direta do risco de o executor omitir o que considera óbvio ou evitar formalizar o que sabe.

### 3.2 Preparação obrigatória (P3a)

A sessão não começa sem quatro itens prontos. Entrar em campo sem eles transforma a visita em exploração.

| Item | Produto | Origem |
|---|---|---|
| Lista de verificação de campo | Cada afirmação declarada na Fase 0 convertida em item a confirmar, com prioridade e método de verificação | E1 |
| Recorte de casos concretos | De cinco a oito casos reais já resolvidos, cobrindo o comum e o atípico, extraídos do histórico com apoio do executor | HB-06, HB-09 |
| Leitura das fontes escritas | Procedimentos, normas e telas de sistema que descrevem o processo-alvo | HB-07, HB-08 |
| Termo de consentimento | Autorização escrita para observação, gravação e registro de autoria | HAB-01 |

A preparação é delegável. A sessão não é.

### 3.3 Estrutura da sessão

A sessão presencial percorre seis momentos, na ordem. Nenhum é opcional; a duração de cada um é calibrada pelo nível.

**1. Abertura e posicionamento.** O engenheiro declara o objeto da sessão, o destino do que for registrado e a autoria do executor sobre o conteúdo. Declara também o limite: a automação se aplica à coleta e à conferência, não à decisão sobre exceções. Esta fala não é cortesia — é o que reduz a omissão deliberada.

**2. Reconstrução por casos concretos.** Para cada caso do recorte, o executor descreve o que fez, em ordem, sem ser perguntado sobre o procedimento. O engenheiro intervém apenas com "por que esse foi assim?" quando o tratamento diverge entre casos semelhantes.

**3. Perseguição de exceção.** Para cada regra que emergiu, o engenheiro pergunta o que faria aquele caso não ser tratado daquela forma. A resposta "nunca acontece" é registrada como resposta, não aceita como encerramento; casos raros são justamente os invisíveis ao histórico.

**4. Observação acompanhada.** O engenheiro acompanha a execução real e preenche o registro de intervenção (Anexo B) sempre que a pessoa faz algo fora do fluxo descrito. A pergunta padrão diante de cada intervenção é "por que agora?".

**5. Arquivo pessoal.** O engenheiro solicita as anotações, planilhas e listas que o executor mantém por fora dos sistemas. Fonte identificada e não examinada é pendência aberta, e precisa ser registrada como tal.

**6. Leitura de volta.** Ao final, o engenheiro lê em voz alta a lista consolidada de regras e o executor complementa, corrige ou recusa item a item. **É obrigatória e ocorre na mesma sessão.** Produz as regras de casos raros que não ocorreram durante a observação e é o instrumento de maior rendimento por minuto investido do passo.

### 3.4 Registro da regra

Cada regra é registrada na ficha do Anexo A, com enunciado em forma condicional — *quando X, faz-se Y, exceto se Z*. Enunciado descritivo não é regra e não passa no critério de encerramento.

A procedência segue a taxonomia do método:

| Marca | Situação em P3b |
|---|---|
| **D — declarada** | O executor enunciou a regra, e ela ainda não foi observada nem confrontada com caso concreto. |
| **I — inferida** | O engenheiro deduziu a regra do padrão dos casos, sem enunciado do executor. Exige premissa escrita e não avança sem confirmação. |
| **V — verificada** | A regra foi observada em execução, confirmada em leitura de volta ou localizada em documento-fonte. Exige registro da evidência. |

A marca não é atribuída por modelo de linguagem. Uma regra inferida que passa pela leitura de volta e é confirmada pelo executor muda para V, com registro de quem confirmou e quando.

### 3.5 Calibragem por nível

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
|---|---|---|---|
| Duração | Uma sessão | Sessão e observação em dia de operação | Sessões múltiplas, com validação em comitê |
| Casos concretos | Cinco | Oito | Doze, com cobertura por tipo de exceção |
| Observação acompanhada | Recomendada | Obrigatória | Obrigatória, com amostragem por turno ou unidade |
| Executores ouvidos | Um | Um, mais confirmação de um segundo | Todos os que originam o trabalho, não apenas quem sofre o retrabalho |
| Leitura de volta | Obrigatória | Obrigatória | Obrigatória, com ata |
| Validação posterior | Não se aplica | Confirmação do dono do processo | Comitê, com registro de divergência formal |

Em nenhum nível a etapa é suprimida ou convertida em videoconferência. A modalidade remota produz concordância nominal; a presença produz decisão assumida.

### 3.6 Critério de encerramento

P3b encerra quando **todas** as condições abaixo são satisfeitas:

1. Um bloco completo de casos concretos foi percorrido sem que nenhuma regra nova emergisse.
2. Toda regra registrada tem enunciado condicional, autoria nominal e origem do conhecimento declarada.
3. A leitura de volta foi realizada, datada e registrada, com o resultado de cada item — confirmado, corrigido ou recusado.
4. Toda regra marcada como I recebeu confirmação explícita ou permanece registrada como pendente, nunca promovida por omissão.
5. Toda regra que o levantamento sugeriu como automatizável passou por segunda rodada de confirmação com o executor.
6. O arquivo pessoal foi examinado, ou sua recusa está registrada com data e motivo.
7. Cada item da lista de verificação de campo recebeu desfecho: confirmado, corrigido, refutado ou esclarecido.

O encerramento é registrado pelo engenheiro, com nome e data. Agente não encerra esta etapa.

### 3.7 Condições que impedem o encerramento

| Situação | Tratamento |
|---|---|
| Executor não liberado para sessão presencial | A etapa não ocorre; o caso retorna ao protocolo de habilitação, que exige essa liberação como pré-requisito. |
| Nenhuma regra levantada | Resultado improvável que exige verificação, não registro. Indica processo-alvo mal recortado ou sessão conduzida por pergunta geral. |
| Regras levantadas apenas em enunciado descritivo | Não satisfaz o critério 2. A sessão continua até que os enunciados assumam forma condicional. |
| Leitura de volta adiada para outra data | Não satisfaz o critério 3. A memória da sessão é o que dá rendimento ao instrumento. |
| Fonte identificada e não examinada | Pendência aberta. Pode encerrar a etapa, mas entra no E2 como limitação declarada. |

### 3.8 Fronteira de delegação na etapa

| Momento | O que o Estúdio pode fazer | O que permanece humano |
|---|---|---|
| Antes | Preparar a lista de verificação, montar o recorte de casos, ler as fontes, propor perguntas | Selecionar quem participa e decidir o recorte final |
| Durante | Registrar a sessão, transcrever, consultar a base curada em tempo real quando solicitado | Conduzir, observar, perguntar, ler de volta |
| Depois | Organizar rascunhos, agrupar enunciados, sinalizar contradições | Aceitar cada regra, atribuir procedência, encerrar a etapa |

O arranjo do momento "durante" é copilotado: o humano conduz e o componente automatizado responde, sem produzir saída não supervisionada. Rascunho produzido por agente não é evidência aceita e permanece fora de `caso/` até decisão registrada.

### 3.9 Saída da etapa

P3b entrega ao P3d:

- conjunto de regras registradas, com autoria, procedência e origem do conhecimento;
- registro de intervenção preenchido durante a observação;
- resultado da leitura de volta, item a item;
- lista de verificação de campo com desfecho por item;
- pendências abertas, com motivo.

O P3d converte esse conjunto no placar de confronto entre regra escrita e regra praticada, classificando cada regra em **alinhada, divergente, não documentada, órfã ou escrita-mas-inacessível**, e apura o percentual de conhecimento praticado sem registro formal. Esse indicador é o produto defensável do Passo 3 e insumo direto do plano de verificação.

## 4. Condição de aceite

O roteiro está pronto quando um engenheiro que não participou de sua construção consegue conduzir a sessão sem decidir novamente o que investigar; quando cada regra levantada carrega enunciado condicional, autoria nominal, origem do conhecimento e procedência; quando existe critério objetivo que distingue etapa encerrada de etapa interrompida; e quando a fronteira entre o que o Estúdio prepara e o que o engenheiro conduz está declarada momento a momento.

## 5. Referências

- EMCIA-MET-01 — Documento do método, Passo 3.
- EMCIA-CAT-01 — Fronteira de delegação e catálogo de agentes e habilidades.
- EMCIA-HAB-01 — Protocolo de habilitação, pré-requisito de liberação do executor.
- EMCIA-GLO-01 — Glossário do método.
- EMCIA-VER-01 — Plano de verificação do método.
- EMCIA-E2 — Modelo de diagnóstico e oportunidade.
- Polanyi, M. *The Tacit Dimension* (1966).
- Nonaka, I.; Takeuchi, H. *The Knowledge-Creating Company* (1995).
- Relatório de avaliação da simulação — instrumentos emergentes 4.1 a 4.4, setembro de 2026.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
|---|---|---|---|---|
| 0.1 | 17/09/2026 | Celso do Vale | Versão inicial: princípios, estrutura da sessão em seis momentos, calibragem por nível, critério de encerramento e fronteira de delegação. | — |

---

## Anexo A — Ficha de regra

| Campo | Conteúdo |
|---|---|
| Identificador | Código sequencial dentro do caso |
| Enunciado | Forma condicional: quando X, faz-se Y, exceto se Z |
| Gatilho | O que faz a regra ser acionada |
| Exceção conhecida | Situação em que a regra não se aplica |
| Autoria | Pessoa nomeada que enunciou ou confirmou |
| Origem do conhecimento | Documento · ensino · experiência própria · desconhecida |
| Frequência estimada | Diária · semanal · mensal · rara |
| Consequência do erro | Baixa · média · alta |
| Procedência | D · I · V |
| Evidência | Caso observado, documento-fonte ou registro da leitura de volta |
| Leitura de volta | Data e resultado: confirmado · corrigido · recusado |
| Segunda confirmação | Exigida quando sugerida como automatizável — data e resultado |

## Anexo B — Registro de intervenção da observação

| Campo | Conteúdo |
|---|---|
| Caso observado | Identificação do item em tratamento |
| Etapa do fluxo | Onde a intervenção ocorreu |
| O que foi feito fora do fluxo descrito | Descrição literal da ação |
| Resposta a "por que agora?" | Transcrição da justificativa |
| Origem declarada do conhecimento | Documento · ensino · experiência · desconhecida |
| Regra derivada | Identificador da ficha correspondente, quando houver |
