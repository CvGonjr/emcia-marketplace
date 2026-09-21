# Blueprint da solução
### Decisão sobre os casos e, quando couber, especificação do agente

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Organização** | «razão social» | **Engajamento** | «código do caso» |
| **Fase** | F2 — Desenho e arquitetura da solução | **Passos** | 4 e 5 |
| **Nível apurado** | «N1, N2 ou N3 — DAD 0 · GOV 0 · CRI 0» | **Data** | «dd/mm/aaaa» |
| **Engenheiro** | «nome» | **Versão** | «0.1» |
| **Patrocinador** | «nome e cargo» | **Aceite** | «nome e data» |

* **Público:** Patrocinador e gestores na Parte A; arquitetura, engenharia e fornecedores na Parte B.
* **Extensão:** Conforme o nível. A Parte A é obrigatória; a Parte B existe apenas se houver caso classificado como agente.
* **Critério de aceite:** A equipe de construção consegue iniciar o trabalho sem reabrir decisões de negócio, de autonomia ou de escopo. O que resta em aberto é apenas técnico e está listado em B6.

> **Procedência:** Toda afirmação deste documento traz uma das três marcas: `[D]` declarada pela organização, `[I]` inferida a partir de outras informações, `[V]` verificada em campo contra dado, documento ou leitura de volta. Afirmação sem marca não deve ser considerada.

### Estrutura do documento

| Parte | Conteúdo | Existe quando |
| :--- | :--- | :--- |
| **A — Decisão** | Priorização (passo 4) e classificação tecnológica (passo 5) | Sempre |
| **B — Blueprint do agente** | Fronteira de delegação, camadas, tecnologias, requisitos, avaliação, plano de construção e passagem | Apenas se o passo 5 classificar ao menos um caso como agente |

> **Nota:** O passo 5 tem autoridade para concluir que nenhum agente é necessário. Aplicar o modelo de camadas antes dessa conclusão pressuporia o agente, razão pela qual a Parte A usa a estrutura própria do método e a Parte B só se abre depois do portão.
>
> Este documento especifica; não constrói. Construção, integração e implantação permanecem fora do serviço.

---

## Parte A — Decisão

### A1. Casos candidatos e priorização

| Caso | Impacto | Viabilidade | Zona de contenção | Situação |
| :--- | :--- | :--- | :--- | :--- |
| «caso» | « » | « » | «dentro · fora» | «priorizado · adiado · descartado» |

*Todos os candidatos constam, inclusive os descartados. Registrar apenas o escolhido impede a organização de reavaliar a decisão depois.*

### A2. Classificação tecnológica

| Caso | Natureza do problema | Tecnologia adequada | Classificação |
| :--- | :--- | :--- | :--- |
| «caso» | «prever · classificar · gerar · decidir · orquestrar» | « » | «agente · isolado · habilitador» |

**A classificação define a saída de cada caso neste documento:**
* **Agente:** Parte B completa.
* **Isolado:** Automação, aprendizado de máquina ou processamento de linguagem, sem agente. Recomendação com requisitos mínimos; o ciclo encerra aqui para este caso.
* **Habilitador acoplado a caso agêntico:** Entra na Parte B como dependência, com dono e prazo.

### A3. Decisão do patrocinador

| Decisão | Responsável | Data |
| :--- | :--- | :---: |
| «seguir com «casos» · não seguir com nenhum» | «nome e cargo» | «dd/mm/aaaa» |

«Justificativa da decisão. Se a recomendação for não seguir com nenhum caso, este é o lugar de dizê-lo: é resultado legítimo do método, e não falha de aplicação. Nesse caso o documento encerra aqui, e a Parte B não se aplica.»

---

## Parte B — Blueprint do agente
*(Aplicável apenas aos casos classificados como agente em A2)*

### Princípios
1. **Capacidade antes de produto:** B1 descreve o que cada camada precisa fazer; produtos aparecem apenas em B2, como opções. A especificação continua válida se a organização trocar de fornecedor.
2. **Rastreabilidade:** Todo item aponta sua origem — passo, regra ou decisão — com a marca de procedência.
3. **Limite crítico é política, não instrução:** O que o agente nunca faz é especificado como bloqueio na camada de controle. Instrução ao modelo é probabilística; política no ponto de passagem é determinística.
4. **Começar pelo que a organização já tem:** A escolha tecnológica parte do inventário do passo 2, e não de uma arquitetura preferida.
5. **A fronteira é do processo, não do método:** O desenho humano-agente da própria EMCIA não se transpõe ao cliente por analogia: transpõem-se os testes e as regras, nunca o resultado.
6. **A organização decide:** Este documento recomenda com critério explícito; a escolha da tecnologia e o aceite pertencem ao patrocinador.

### B1. Fronteira de delegação e interação humano-agente
A fronteira de delegação da própria EMCIA é artefato pronto: foi decidida uma vez, no desenho do método, vale para todo engajamento e só é calibrada pelo nível. Ela descreve o trabalho da consultoria e nada além disso.

No processo do cliente não existe resposta equivalente disponível. Antes de aplicar o método não se sabe quais atividades admitem delegação, quem permanece decidindo, em que modo, nem sob quais gatilhos. É essa a pergunta que o percurso responde, e esta seção é onde a resposta fica registrada.

| Dimensão | Método interno da EMCIA | Blueprint do cliente |
| :--- | :--- | :--- |
| **Situação** | Decidido no desenho do método | Desconhecido até a aplicação |
| **Estabilidade** | Um desenho, calibrado por nível | Um desenho por processo; pode variar por ação dentro do mesmo agente |
| **Quem define** | Responsável pelo método | Engenheiro de campo com o patrocinador, sobre evidência de campo |
| **Quem julga** | Engenheiro de campo, por definição | A identificar; pode não existir ainda na organização |

#### B1.1 O que transpõe e o que não transpõe
* **Transpõe — o instrumento:** Os três testes de delegação com justificativa obrigatória por atividade; a marcação de procedência em toda saída automatizada; a regra de que nenhum agente propõe a própria autonomia; o catálogo de antipadrões, gatilhos e métricas da fronteira.
* **Não transpõe — o resultado:** Quais atividades são delegáveis, quem revisa, qual modo se aplica, quais gatilhos existem e onde a verificação ocorre. Nada disso vem da consultoria: tudo é produzido no percurso.

> *Aplicar o desenho interno por analogia repetiria o erro que o método existe para corrigir: especificar sobre o processo presumido em vez do processo praticado.*

| Pergunta desta seção | Onde a resposta é produzida |
| :--- | :--- |
| O dado que a decisão exige existe e presta? | Passo 2 — inventário e qualidade |
| Quais regras e exceções governam a decisão? | Passo 3 — levantamento em campo |
| O erro é detectável por quem recebe a saída? | Passo 3 — observação do processo praticado |
| A ação gera compromisso? Há restrição regulatória? | Passo 4 — zona de contenção |
| Quem permanece decidindo, e em que modo? | Passo 5, registrado aqui |

> **Não se presume o revisor:** A aplicação pode concluir que a revisão exigida por um modo não tem responsável disponível na organização. Nesse caso o achado é registrado como dependência em B7 e como mudança de papéis no passo 6, ou o modo é reduzido até o que a operação sustenta.

#### B1.2 Os três testes aplicados ao processo do cliente

| Teste | Pergunta no processo do cliente | Falha, e volta ao humano, quando |
| :--- | :--- | :--- |
| **Fonte** | A resposta está no que os sistemas e a camada de contexto registram? | Depende de regra não registrada ou de percepção do caso |
| **Verificabilidade** | O erro é detectável por quem recebe a saída? | O erro é plausível e passa despercebido |
| **Compromisso** | A saída é informação, ou é ação por que alguém responde? | Gera obrigação financeira, contratual ou efeito sobre terceiro |

*Regra prática herdada do método:* **o agente responde o que é; o humano responde o que fazer.**

#### B1.3 Classificação das atividades do processo

| Atividade do processo | Natureza | Teste que falhou | Justificativa | Procedência |
| :--- | :--- | :--- | :--- | :---: |
| « » | «automatizada · híbrida · humana» | «fonte · verificabilidade · compromisso» | « » | «[D] · [I] · [V]» |

* A coluna de justificativa é obrigatória. Sem ela a classificação é arbitrária e não pode ser discutida em revisão.
* Atividade classificada como automatizada passa por segunda rodada de confirmação com o executor.
* A classificação é confirmada por quem executa o processo, autor das regras da camada de contexto. Ele não é fonte a ser extraída: é quem revisa onde a máquina entra no próprio trabalho.
* A fronteira é desenhada sobre o processo praticado, e não sobre o documentado.

#### B1.4 Modos de delegação

| Modo | O agente faz | O humano faz | Indicado quando | Falha típica |
| :--- | :--- | :--- | :--- | :--- |
| **Sombra** | Decide em paralelo, sem efeito | Compara saídas por amostra | Antes do primeiro uso real; decisão crítica | Ninguém compara, e o registro vira log morto |
| **Sugestão** | Propõe, com evidência | Decide e executa | O teste de compromisso falhou | Proposta aceita sem leitura |
| **Aprovação prévia** | Prepara a ação completa | Autoriza antes da execução | Ação irreversível dentro de limite | Aprovação em lote, sem edição |
| **Exceção** | Age e devolve por gatilho | Trata o que foi devolvido | Regra estável e erro detectável | Gatilho largo demais, e nada é devolvido |
| **Autônomo** | Age | Revisa por amostra na calibragem | Leitura, consulta, preparo reversível | A revisão deixa de acontecer |

*O modo inicial não é o modo final.* O blueprint registra o modo de entrada, o critério para avançar e quem autoriza o avanço — progressão que coincide com a do plano de construção em B6: **sombra → assistido → autonomia autorizada**.

#### B1.5 Onde a verificação acontece

| Modo | Verificação | Momento |
| :--- | :--- | :--- |
| **Sombra** | Comparação entre a saída do agente e a decisão real | Fora da operação |
| **Sugestão** | Ocorre na própria decisão de quem executa | Antes da ação |
| **Aprovação prévia** | Item a item, sobre a ação preparada | Antes da ação |
| **Exceção** | Somente nos casos devolvidos pelo gatilho | No momento da devolução |
| **Autônomo** | Por amostra | Depois da ação, na calibragem |

> **Requisito transposto do método:** Toda saída do agente carrega procedência — declarado pelo sistema, inferido pelo agente, verificado pelo humano. Sem essa marcação não há o que verificar em nenhum dos cinco modos, e a saída vira autodeclaração com aparência de decisão. A marcação é validação de esquema, e não instrução ao modelo.

#### B1.6 O ponto de verificação

| Item | Especificação |
| :--- | :--- |
| **O que o humano vê** | «saída, evidência que a sustenta, regra da camada de contexto aplicada, procedência e grau de confiança» |
| **O que o humano faz** | «confirma, corrige ou rejeita, com justificativa obrigatória na correção» |
| **Tempo de revisão** | «estimativa, comparada ao tempo da execução manual» |
| **Destino da correção** | «registro versionado que alimenta a camada de contexto e a suíte de avaliação» |
| **Quem revisa** | «nome e cargo; nunca uma área» |

* **Critério econômico da delegação:** Se revisar custa o mesmo que executar, a delegação não gera valor: apenas desloca esforço e acrescenta risco. A comparação é registrada por atividade.

| Antipadrão | Por que é recusado |
| :--- | :--- |
| **Botão único de aprovar tudo** | Converte verificação em formalidade |
| **Aprovar sem ver a evidência** | O humano valida a forma da saída, e não o conteúdo |
| **Correção registrada apenas em conversa** | Não entra na camada de contexto, e o agente repete o mesmo erro |
| **Grau de confiança do modelo usado como trava** | Trava probabilística no lugar de determinística |
| **Agente que propõe a própria autonomia** | Regra absoluta do método, sem exceção por nível ou prazo |

#### B1.7 Gatilhos de devolução ao humano

| Gatilho | Detecção |
| :--- | :--- |
| **Valor acima do limite** | Determinística, no ponto de passagem |
| **Ação classificada como irreversível** | Determinística, pela matriz de autonomia |
| **Caso sem regra correspondente na camada de contexto** | Determinística, por ausência de correspondência |
| **Conflito entre regras da camada de contexto** | Determinística, pela política de decisão |
| **Dado-fonte desatualizado além do exigido** | Determinística, por carimbo de tempo |
| **Caso fora da distribuição conhecida** | Estatística, sobre o histórico |
| **Baixa confiança na saída** | Sinal do modelo, nunca usado sozinho para liberar ação |

* Silêncio não libera ação. Sem resposta no prazo, o caso permanece parado e escala para o suplente nomeado.
* O gatilho aponta para uma pessoa nomeada. Encaminhamento para área equivale a não haver encaminhamento.
* Gatilho determinístico tem precedência. Sinal do modelo pode acrescentar devolução, nunca dispensá-la.

#### B1.8 Do humano para o agente
* **Acionamento:** «como o humano inicia, interrompe ou desliga o agente, e quem pode fazê-lo»
* **Contexto faltante:** «como fornece a informação que o agente não alcançou, e onde ela fica registrada»
* **Correção de regra:** «como uma correção recorrente vira regra nova, com autor, data e justificativa»
* **Recurso:** «como alguém afetado pela decisão pede revisão humana»

> *Correção que não chega à camada de contexto versionada não é aprendizado: é retrabalho recorrente.*

#### B1.9 Medição da fronteira

| Métrica | O que indica |
| :--- | :--- |
| **Taxa de devolução ao humano** | Se a fronteira está no lugar certo |
| **Taxa de correção na verificação** | Qualidade real da saída |
| **Taxa de aprovação sem edição** | Próxima de 100% significa agente perfeito ou ninguém revisando. Investigar sempre |
| **Tempo de revisão por caso** | Sustentação do critério econômico |
| **Devoluções sem regra correspondente** | Lacunas da camada de contexto a preencher na calibragem |

#### B1.10 Calibragem da fronteira por nível

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **Modo de entrada** | Sugestão ou aprovação prévia | Sombra e depois assistido | Sombra prolongada |
| **Verificação** | Por amostra, pelo dono do processo | Item a item nas ações de escrita | Item a item, com trilha auditável |
| **Registro da correção** | Planilha versionada | Registro estruturado na camada de contexto | Camada versionada, com donos e auditoria |
| **Revisão da fronteira** | Mensal, informal | Trimestral | Trimestral, com comitê |

---

### B2. Especificação por camada

| Camada | Pergunta central | Origem no percurso |
| :--- | :--- | :--- |
| **CA1 · Controle** | O que o agente pode fazer, com qual identidade, sob qual vigilância? | Passo 4 (zona de contenção) e passo 7 (termo de autonomia) |
| **CA2 · Agente** | Como raciocina, como é orquestrado, o que acessa na tarefa? | Passos 4 (arquétipo) e 5 |
| **CA3 · Protocolos** | Por onde alcança sistemas, dados e outros agentes? | Passos 2 (inventário) e 5 |
| **CA4 · Contexto** | Quais regras, termos e entidades governam a decisão? | Passo 3 (levantamento) para o passo 5 (montagem) |
| **CA5 · Dados** | Quais fontes sustentam a decisão e em que condição estão? | Passo 2 (inventário e qualidade) |

#### CA1 · Camada de controle
* **Identidade:** «identidade própria do agente ou atuação em nome do usuário; papéis e permissões por ferramenta; menor privilégio»
* **Cofre:** «credenciais utilizadas; classificação da informação acessada; mascaramento exigido»
* **Ambientes:** «desenvolvimento, homologação e produção; isolamento de execução; limite de recursos»
* **Ponto de passagem:** «modelos e ferramentas permitidos; políticas de bloqueio e de aprovação; limite de chamadas; teto de gasto»
* **Observabilidade:** «o que se registra — entrada, ferramenta acionada, saída, aprovação humana; retenção; quem acessa a trilha»

**Matriz de autonomia por ação:**

| Ação ou ferramenta | Efeito | Reversível | Nível | Aprovador | Política |
| :--- | :--- | :---: | :--- | :--- | :--- |
| «consultar pedido» | Leitura | — | Age sozinho | — | Permitir |
| «emitir documento» | Escrita em sistema de registro | Não | Age com aprovação | «nome e cargo» | Exigir aprovação |
| «exceder limite de valor» | Financeiro | Não | Nunca | — | Bloquear |

> **Regra de conversão:** O que o termo de autonomia classifica como “nunca faz” vira bloqueio; o que classifica como “exige aprovação” vira ponto de parada com aprovador nomeado.

#### CA2 · Camada do agente
* **Fronteira no fluxo:** «arquétipo; onde o agente entra no processo, o que decide, onde a pessoa permanece; gatilhos de devolução ao humano»
* **Modelo:** «requisitos, e não o nome do modelo: tipo de raciocínio, tamanho de contexto, latência, custo por tarefa, residência do dado, uso do dado pelo provedor. Registrar ao menos duas alternativas aceitáveis»
* **Padrão de execução:** «fluxo fixo com etapas de modelo ou planejamento livre; agente único ou múltiplos; memória de sessão e de longo prazo; pontos de parada para aprovação; tratamento de erro»
* **Conhecimento externo:** «o que é recuperado, de qual fonte, com que frequência de atualização»
* **Ferramentas:** «por ferramenta: finalidade, entradas, saídas, efeito, erros previstos e nível de autonomia, herdado da CA1»
* **Habilidades:** «capacidades modulares reutilizáveis, com critério de verificação»

#### CA3 · Camada de protocolos

| Sistema | Tipo | Protocolo | Operação | Autenticação e contrato | Dono | Existe hoje? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| « » | «registro · analítico · interação · documentos» | « » | «leitura · escrita» | « » | «nome» | «sim [V] · não» |

#### CA4 · Camada de contexto

| Componente | O que especificar | Origem |
| :--- | :--- | :--- |
| **Glossário** | «termo, definição, dono, fonte» | Passos 2 e 5 |
| **Entidades e relações** | «modelo do domínio» | Passo 5 |
| **Regras verificadas** | «regra, condição, exceção, autor, leitura de volta, procedência, caso de teste vinculado» | Passos 3 e 5 |
| **Contexto operacional** | «exceções, sazonalidade, prioridades não escritas» | Passo 3 |
| **Política de decisão** | «como as regras se combinam quando conflitam» | Passo 5 |

* **Ciclo de observação e aprendizado:** «qual rastro da observabilidade vira evidência; quem revisa essa evidência; o que pode mudar sem aprovação — métricas e exemplos — e o que não pode — regras e política de decisão.»
* Nenhuma regra inferida entra sem validação humana expressa.
* Forma por nível: N1 documento versionado · N2 glossário, catálogo e contratos de dados · N3 camada semântica versionada, com donos nomeados.

#### CA5 · Camada de dados

| Fonte | Tipo | Dono | Qualidade | Classificação | Acesso | Atualização exigida |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| « » | «registro · analítico · interação · documentos» | «nome» | «achado do passo 2» | «sensibilidade» | « » | « » |

---

### B3. Tecnologias e integração
* **Inventário do ecossistema atual:** «O que a organização já opera, a partir do passo 2 e das perguntas DAD-1 e DAD-2 da triagem, com procedência.»

**Postura de arquitetura:**

| Postura | Descrição | Indicada quando | Risco principal |
| :--- | :--- | :--- | :--- |
| **Nativa** | Plataforma de agentes do provedor que já sustenta os dados | Ecossistema consolidado, equipe capacitada, governança instalada | Dependência do provedor |
| **Híbrida** | Dados e governança no ecossistema atual; agentes em outro provedor ou estrutura aberta | Dados consolidados, oferta de agentes do provedor imatura para o caso | Duas superfícies de governança |
| **Portável** | Estruturas abertas e protocolos padrão, sobre infraestrutura própria | Baixa dependência de plataforma ou exigência explícita de portabilidade | Mais construção e operação próprias |

**Matriz de aderência:**

| Critério | Pergunta | Peso | Avaliação |
| :--- | :--- | :---: | :---: |
| **Aderência ao ecossistema** | Reaproveita o que a organização já opera? | « » | « » |
| **Residência do dado** | O dado permanece onde precisa permanecer? | « » | « » |
| **Governança reaproveitada** | Identidade, auditoria e classificação já instaladas cobrem o agente? | « » | « » |
| **Maturidade do serviço** | O componente está em disponibilidade geral ou em prévia? | « » | « » |
| **Competência da equipe** | Quem vai operar sabe operar? | « » | « » |
| **Custo total** | Licença, consumo por tarefa e operação | « » | « » |
| **Portabilidade** | Quanto custa sair? | « » | « » |

* **Mapa de integração:** «Agente ao centro, sistemas da organização ao redor, cada ligação com protocolo e operação. N1 lista · N2 diagrama · N3 diagrama de contexto e de contêineres.»

**Registro de decisão de arquitetura:**
* **Contexto:** «o que motivou a decisão»
* **Opções:** «ao menos duas»
* **Critérios:** «da matriz de aderência»
* **Recomendação:** «com justificativa»
* **Decisão:** «o que foi escolhido»
* **Decisor e data:** «nome, cargo, data»

---

### B4. Requisitos de arquitetura

| ID | Categoria | Requisito | Origem | Verificação |
| :---: | :--- | :--- | :--- | :--- |
| **«R1»** | «funcional · desempenho · contingência · segurança · custo · auditoria · qualidade» | « » | «passo» | «como se verifica» |

---

### B5. Avaliação e riscos

#### Especificação de avaliação
* Toda regra crítica da CA4 tem ao menos um caso de teste com saída esperada.
* Casos de baixa frequência e alta consequência têm caso próprio: são invisíveis tanto à leitura de documentos quanto à análise do histórico.
* O conjunto cobre quatro tipos: regra geral, exceção, situação fora de escopo que deve ser recusada e tentativa de violar limite que deve ser bloqueada.
* Métricas: acerto nos casos, taxa de devolução ao humano, divergência em revisão e custo por tarefa.
* Critério de aprovação datado antes do início do piloto.
* Quantidade por nível: N1 de 15 a 30 · N2 de 50 a 100 · N3 por cenário e por subgrupo.

#### Riscos próprios de agentes

| Risco | Exemplo | Controle | Camada |
| :--- | :--- | :--- | :---: |
| **Injeção de instrução** | Documento lido contém ordem dirigida ao agente | Separar dado de instrução; política no ponto de passagem | CA1 · CA2 |
| **Permissão excessiva** | Ferramenta com escrita além do necessário | Menor privilégio por ferramenta | CA1 · CA3 |
| **Ação irreversível sem aprovação** | Emissão, pagamento, envio | Matriz de autonomia convertida em política | CA1 |
| **Exposição de dado pessoal** | A saída revela dado identificável | Classificação e mascaramento | CA1 · CA5 |
| **Regra desatualizada** | Mudança de norma não refletida | Versão e dono na CA4; gatilho de revisão | CA4 |
| **Custo descontrolado** | Laço de chamadas | Teto de gasto e limite de chamadas | CA1 |
| **Queda de desempenho** | Acerto cai após mudança no dado | Execução periódica dos casos de teste | CA1 · CA4 |

---

### B6. Plano de construção
*Plano indicativo para quem constrói. Não constitui compromisso do serviço.*

| Onda | Conteúdo | Portão de saída |
| :---: | :--- | :--- |
| **0 · Fundação** | Acessos (CA5); identidade, cofre e observabilidade (CA1); ambientes | Leitura funcionando, com trilha |
| **1 · Contexto** | CA4 carregada e versionada; casos de teste executáveis | O conjunto de teste roda |
| **2 · Sombra** | CA2 e CA3 em leitura; o agente sugere e não age | Acerto igual ou acima do critério |
| **3 · Assistido** | Escrita com aprovação humana | Critério do piloto, definido no E5 |
| **4 · Autonomia autorizada** | Ações classificadas como “age sozinho” liberadas conforme o termo | Aprovação do patrocinador ou do comitê |

* **Ordem obrigatória:** Controle e dados antes do agente; contexto antes do comportamento; autonomia por último.
* «Cronograma com dependências e caminho crítico; esforço por papel; estimativa de custo de construção e de operação mensal. Duração de referência: N1 semanas · N2 meses · N3 trimestres.»

---

### B7. Pacote de passagem
* **Decisões fechadas:** «registros de decisão e aceites; não devem ser reabertas»
* **Premissas:** «com procedência»
* **Perguntas técnicas abertas:** «com responsável e prazo»
* **Dependências:** «habilitadores acoplados, acessos pendentes»
* **Critério de aceite da construção:** «vinculado aos casos de teste de B5 e ao critério do piloto do E5»
* **Contatos:** «dono do processo · executor, autor das regras da CA4 · responsável pela calibragem»

---

### Anexo — Referência por camada e ecossistema
*(Verificado em 10/09/2026)*

| Camada | Databricks | Microsoft | Google Cloud | AWS | Portável |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CA1 Controle** | Unity Catalog; Unity AI Gateway (prévia) | Entra Agent ID (prévia); Purview; rastreamento do Foundry | Agent Identity, Registry e Gateway | AgentCore Identity; AgentCore Gateway com políticas Cedar; Guardrails | OpenTelemetry; motor de políticas; cofre próprio |
| **CA2 Agente** | Agent Bricks; MLflow; Model Serving | Foundry Agent Service; Microsoft Agent Framework | ADK; Agent Runtime; Memory Bank; Model Garden | AgentCore Runtime e Memory; modelos do Bedrock | LangGraph; CrewAI; interface direta de modelos |
| **CA3 Protocolos** | MCP Catalog | Conectores e ferramentas MCP do Foundry | MCP; A2A | AgentCore Gateway, expondo interfaces como ferramentas MCP | MCP; A2A; REST |
| **CA4 Contexto** | Genie Ontology; metadados do Unity Catalog | Modelos semânticos do Fabric; catálogo do Purview | Dataplex | Glue Data Catalog; Bedrock Knowledge Bases | Repositório versionado e grafo |
| **CA5 Dados** | Lakehouse (Delta Lake); Lakebase | Fabric e OneLake | BigQuery; Cloud Storage | S3; Redshift | Bases da própria organização |

#### Calibragem da Parte B por nível

| Subentregável | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
| :--- | :--- | :--- | :--- |
| **B1 Fronteira** | Classificação e modo por atividade | Com gatilhos e ponto de verificação | Com trilha auditável e revisão em comitê |
| **B2 Camadas** | Uma página por camada | Completo | Completo, com diagrama por camada |
| **B3 Tecnologias** | Postura e lista do existente | Matriz de aderência e mapa de integração | Matriz ponderada, diagrama de contêineres e registros formais de decisão |
| **B4 Requisitos** | Lista curta, com critério de verificação | Por categoria, com identificador | Rastreáveis, com aprovação de segurança e do DPO |
| **B5 Avaliação e riscos** | 15 a 30 casos; tabela de riscos | 50 a 100 casos; lista de verificação | Por cenário e subgrupo; modelo formal de risco |
| **B6 Plano** | Marcos em semanas | Cronograma por onda | Cronograma, custo por caso e portões em comitê |
| **B7 Passagem** | Uma página | Completo | Completo, com aceite da equipe de construção |