# Instrumento de triagem
### Nove perguntas em três eixos, com regra de pontuação e de leitura

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-TRI-01 | **Versão** | 0.1 |
| **Data** | 11/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | F0 — Enquadramento | **Passo** | Triagem |

---

## 1. Objetivo
Apurar o nível de complexidade do engajamento antes do início do percurso, de modo que a profundidade de cada um dos dez passos seja calibrada por um critério explícito e reproduzível, e não pela impressão de quem conduz.

## 2. Escopo e aplicação
Aplica-se uma única vez por engajamento, na Fase F0, após a conclusão do protocolo de habilitação. É respondido pela organização e sempre sobre o processo-alvo delimitado, nunca sobre a organização em abstrato.

Não se aplica ao levantamento de requisitos. O instrumento decide qual método aplicar, e nada além disso: seu produto é um nível, não um diagnóstico.

## 3. Conteúdo

### 3.1 Princípio e limite
Porte é atalho, não critério. Uma empresa pequena que decide sobre crédito exige método mais pesado que uma indústria de médio porte que gera texto de campanha. O que muda o método são três eixos, e é sobre eles que o instrumento pergunta.

O produto da triagem é um nível declarado, não um nível diagnosticado. Toda resposta é autodeclaração da organização, e a autodeclaração é hipótese a verificar. O rótulo “declarado” acompanha o resultado até que a verificação prevista na seção 3.7 ocorra.

### 3.2 Os três eixos

| Sigla | Eixo | Pergunta central | Passos que calibra |
| :---: | :--- | :--- | :---: |
| **DAD** | Complexidade do dado | Quantos sistemas-fonte, e o dado está integrado ou disperso? | 2, 3 e 5 |
| **GOV** | Formalidade da governança | Existem papéis, políticas e auditoria formais? | 7 e 8 |
| **CRI** | Criticidade da decisão | O erro afeta terceiros, dinheiro ou conformidade? | 7 e 8, e a autonomia |

A sigla do eixo prefixa a de cada pergunta, de modo que o identificador de um item revela o eixo a que pertence sem consulta à tabela. É por essa sigla que a ficha de enquadramento, o registro de resposta ausente e a reclassificação fazem referência aos itens.

### 3.3 As nove perguntas
Três perguntas por eixo, nove ao todo. Cada alternativa vale de um a três pontos, sem sobreposição entre elas.

#### 3.3.1 Eixo DAD — Complexidade do dado

| Sigla | Pergunta | 1 ponto | 2 pontos | 3 pontos |
| :---: | :--- | :--- | :--- | :--- |
| **DAD-1** | Quantos sistemas-fonte relevantes alimentam o processo-alvo? | Até três | De quatro a dez | Mais de dez |
| **DAD-2** | Há integração entre esses sistemas? | Nenhuma, ou por planilhas | Parcial | Repositório analítico central em uso |
| **DAD-3** | Há área ou responsável formal por dados? | Não há | Existe, de modo informal | Área constituída |

#### 3.3.2 Eixo GOV — Formalidade da governança

| Sigla | Pergunta | 1 ponto | 2 pontos | 3 pontos |
| :---: | :--- | :--- | :--- | :--- |
| **GOV-1** | As políticas de segurança e de acesso estão documentadas? | Não estão | Parcialmente | Formais e auditadas |
| **GOV-2** | Há encarregado, comitê ou responsável por proteção de dados? | Não há | A função é acumulada | Função dedicada |
| **GOV-3** | Há trilha de auditoria nos sistemas críticos? | Não há | Parcial | Completa |

#### 3.3.3 Eixo CRI — Criticidade da decisão

| Sigla | Pergunta | 1 ponto | 2 pontos | 3 pontos |
| :---: | :--- | :--- | :--- | :--- |
| **CRI-1** | O processo-alvo afeta dinheiro, crédito ou contrato? | Não afeta | Afeta indiretamente | Afeta diretamente |
| **CRI-2** | Há exigência regulatória sobre o processo? | Não há | Setorial, de baixa intensidade | Setor regulado |
| **CRI-3** | Um erro no processo é detectado com que rapidez? | De imediato | Em dias | Pode passar despercebido |

### 3.4 Regra de pontuação e de leitura
Cada eixo soma de três a nove pontos. O nível do engajamento é definido pelo **maior dos três eixos**, e não pela média.

| Maior soma entre os eixos | Nível |
| :---: | :--- |
| **3 a 4 pontos** | N1 — Ágil |
| **5 a 7 pontos** | N2 — Estruturado |
| **8 a 9 pontos** | N3 — Corporativo |

> **Por que o maior e não a média:** A média dissolve o eixo alto isolado, que é justamente o que impõe risco. Uma organização informal que decide sobre crédito pontua baixo em dado e governança e alto em criticidade; pela média seria N1, e o método leve aplicado ali produziria autonomia excessiva sobre decisão consequente.

As três somas ficam registradas na ficha de enquadramento ao lado do nível, identificadas por sigla, no formato `DAD 5 · GOV 3 · CRI 8`. Elas não rebaixam nenhum passo — o nível apurado governa o percurso inteiro —, mas indicam em que passos a exigência do nível é mais crítica, conforme a correspondência da seção 3.2.

A apuração é determinística e ocorre fora de qualquer modelo de linguagem. Um terceiro que receba as nove respostas precisa chegar ao mesmo nível.

### 3.5 Resposta ausente ou incerta
“Não sei” é resposta legítima e frequente, sobretudo no eixo GOV, cujas perguntas exigem conhecimento que o interlocutor do processo raramente tem. O tratamento é o seguinte:

| Situação | Tratamento |
| :--- | :--- |
| **O respondente não sabe** | O item pontua no valor que impõe o método mais pesado, é marcado para verificação obrigatória e a ausência de resposta fica registrada como tal. |
| **O respondente hesita entre dois valores** | Registra-se o maior dos dois, com a hesitação anotada. |
| **A pergunta não se aplica ao processo-alvo** | Pontua o valor mais baixo, com justificativa escrita. Se três ou mais itens forem inaplicáveis, o processo-alvo provavelmente está mal delimitado. |

O critério é assimétrico de propósito. Aplicar o método pesado ao cliente errado custa esforço; aplicar o leve custa risco. Na dúvida, o instrumento erra para o lado que custa esforço.

### 3.6 Registro obrigatório
Cada item registra quatro elementos, e o instrumento não se conclui sem os quatro:

| Elemento | Por que é exigido |
| :--- | :--- |
| **A pontuação atribuída** | É o que produz o nível. |
| **A resposta literal do respondente** | A interpretação pode estar errada; o literal permite reabrir a apuração sem repetir a entrevista. |
| **Quem respondeu cada item** | O instrumento admite mais de um respondente, e o eixo B costuma exigir alguém distinto de quem responde o eixo A. |
| **A marca de procedência** | Toda resposta entra como declarada, e só muda de marca quando a verificação da seção 3.7 ocorrer. |

### 3.7 Verificação posterior
A triagem não verifica nada — ela declara. A confirmação de cada eixo ocorre mais adiante no percurso, no passo em que o acesso necessário já existe.

| Eixo | Verificado no | Como |
| :---: | :---: | :--- |
| **DAD** | Passo 2 | Inventário de fontes com acesso efetivo e inspeção da qualidade dos campos críticos |
| **GOV** | Passo 7 | Exame das políticas existentes e da trilha de auditoria dos sistemas envolvidos |
| **CRI** | Passos 3 e 4 | Mapeamento do fluxo atual, que revela o efeito real do erro, e aplicação da zona de contenção |

> **Ponto cego conhecido:** Organizações superestimam a própria maturidade de dados nas três perguntas do eixo DAD. É o trecho do instrumento com maior taxa de erro na autodeclaração, e a razão pela qual esse eixo é o primeiro a ser verificado.

### 3.8 Reclassificação
Quando a verificação contradiz o declarado, o nível é recalculado com as respostas corrigidas e a mudança é registrada com data, item alterado e origem da correção. A ficha de enquadramento passa a exibir os dois valores: o nível declarado na triagem e o nível verificado.

A reclassificação alcança apenas os passos ainda não encerrados. Passo já encerrado sob o nível anterior permanece válido, e a divergência entre a profundidade aplicada e a profundidade que o novo nível exigiria fica registrada como restrição — o mesmo tratamento dado ao acesso negado no protocolo de habilitação.

## 4. Condição de aceite
Este artefato está pronto quando:
1. As nove perguntas têm sigla estável e as três alternativas pontuadas sem sobreposição entre elas;
2. A regra de leitura permite que um terceiro reproduza o nível a partir das respostas;
3. O tratamento de resposta ausente está definido;
4. Cada eixo tem declarado o passo em que será verificado.

## 5. Referências
* **AI Maturity Model**, Gartner
* **Data Management Maturity Model**, CMMI Institute
* **AI Risk Management Framework**, NIST (2023)
* **Artefatos relacionados:** EMCIA-MET-01, EMCIA-HAB-01, EMCIA-FER-01 (ADM-04), EMCIA-E1.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| **0.1** | 11/09/2026 | Celso do Vale | Versão inicial: nove perguntas com sigla por eixo, regra de leitura, tratamento de resposta ausente, registro obrigatório, verificação posterior e reclassificação | — |