# Roteiro de habilitação — perguntas e ações do engenheiro de campo

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-ROT-02 | **Versão** | 1.0 |
| **Data** | 03/10/2026 | **Estado** | Aprovado |
| **Responsável** | Celso do Vale | **Aprovação** | Celso do Vale · 03/10/2026 |
| **Fase** | Anterior a F0 | **Passo** | 0a–0d |

---

## 1. Objetivo
Conduzir a habilitação por perguntas e ações que permitam conferir os quatro pré-requisitos e registrar o desfecho antes de F0. A habilitação não é calibrada por nível de complexidade.

## 2. Escopo e aplicação
Usar desde o primeiro contato com a organização, segundo o EMCIA-HAB-01. O comando /eiac-campo:habilitacao apoia o registro administrativo; o engenheiro inicializa o expediente fora de repositórios e da sessão do agente. A referência técnica eiac-campo/reference/habilitacao.md documenta formatos; o procedimento permanece neste roteiro e no protocolo.

O código EMCIA-ROT-02 substitui o identificador provisório EMCIA-HAB-02 do roteiro, que colidia com o template HAB-02 de confidencialidade. Os templates HAB-01/02/03 conservam seus códigos e conteúdos.

## 3. Conteúdo

### 3.1 Operação com formulário e assinatura

Use o fluxo de `EMCIA-HAB-fluxo-operacional-proposta.md`: coleta administrativa → revisão humana → rodadas de esclarecimentos → consolidação → revisão das minutas → PDFs → assinatura pelo painel escolhido pelo cliente → conferência → 0c → 0d.

A exceção administrativa aprovada está em EMCIA-HAB-01, seção 3.7. Antes de consultar respostas pelo MCP, registre as condições de tratamento e sua evidência. Não processe dados operacionais antes de 0d. Reserve o identificador do futuro caso, sem apresentá-lo como aberto.

O plugin preserva a origem dos campos e versões dos três documentos. O engenheiro confere a carta atual e o conteúdo dos PDFs antes de liberá-los. Cliente e engenheiro combinam quem opera o painel e recolhe arquivos assinados e comprovantes. Não há integração com o serviço de assinatura. Registre a conferência humana das assinaturas antes de concluir 0b.

### 3.2 Os quatro pré-requisitos

A falta de qualquer um impede o início do percurso.

| # | Pré-requisito | Pergunta de verificação |
|:-:|---|---|
| 1 | Patrocinador com autoridade sobre o processo | Quem decide sobre este processo e pode assinar as decisões dos passos 4, 7 e 9? |
| 2 | Executor liberado para sessão presencial | Quem executa o processo no dia a dia, e essa pessoa pode passar algumas horas conosco, presencialmente? |
| 3 | Autorização escrita de acesso a dado e documento | Quem autoriza por escrito o acesso aos dados e documentos do processo? |
| 4 | Processo delimitado | Qual processo, com início e fim claros, será tratado? |

---

### 3.3 Etapa 0a — Qualificação do contato

**Objetivo:** saber se existe um engajamento possível antes de formalizar qualquer coisa.

**Perguntas ao interlocutor**

1. Qual processo vocês querem tratar? Onde ele começa e onde termina?
2. Qual é o problema concreto nesse processo hoje? O que dá errado, atrasa ou custa caro?
3. Você decide sobre esse processo? Se não, quem decide?
4. Quem executa esse processo no dia a dia? Quantas pessoas?
5. Existem documentos, planilhas ou sistemas que registram esse processo?
6. Vocês estariam dispostos a dar acesso a esses dados e documentos e a liberar quem executa o processo para conversar conosco?

**Ações do engenheiro**

- [ ] Levantar informação pública sobre a organização e o setor. Guardar numa pasta **fora** do caso; esse material só entra no caso depois da 0d, com marca `I · tipo_fonte: externa`.
- [ ] Nomear um único processo candidato.
- [ ] Redigir o registro de contato qualificado: interlocutor, cargo, processo candidato, disposição de acesso.

**Passa se:** há interlocutor com autoridade e um processo delimitado.

**Não passa se:** a demanda é "usar IA na empresa", sem processo, ou o interlocutor não decide sobre o processo que descreve. Isso não é rejeição do cliente: sem processo, não há o que enquadrar.

---

### 3.4 Etapa 0b — Formalização do escopo

**Objetivo:** registrar por escrito o que o trabalho cobre, o que não cobre e como a informação circula.

**Perguntas para fechar a formalização**

1. Quem tem competência para assinar a carta de escopo e o acordo de confidencialidade?
2. Vocês autorizam a gravação das sessões de levantamento?
3. Vocês autorizam que documentos e dados do processo sejam processados por um modelo de IA de terceiro? Qual provedor e qual localização de processamento são aceitáveis?
4. Há dado pessoal ou sensível no processo? Que regra de anonimização precisa ser seguida?
5. Está claro que o serviço entrega diagnóstico e especificação, e não implanta, não integra sistemas e não opera a solução?

**Ações do engenheiro**

- [ ] Emitir a carta de escopo com o processo-alvo, as fases F0 a F4, os cinco entregáveis e o limite do serviço.
- [ ] Firmar o acordo de confidencialidade.
- [ ] Obter o termo de consentimento para gravação das sessões e uso do dado, incluindo o provedor de modelo que será usado.

**Passa se:** os três documentos estão assinados por quem tem competência.

**Não passa se:** a organização exige implantação, ou recusa a gravação das sessões. Sem gravação, não há como demonstrar quem disse cada regra.

---

### 3.5 Etapa 0c — Concessão de acesso

**Objetivo:** transformar a autorização escrita em acesso efetivo.

**Perguntas ao patrocinador**

1. Quem será o patrocinador nomeado do trabalho, com nome e cargo?
2. Quem será o executor que participará da sessão presencial? Em que data?
3. A que dados, sistemas e documentos teremos acesso? Leitura direta ou amostra exportada?
4. De que período é a amostra? Ela representa o processo normal ou um período atípico?
5. O que **não** poderá ser acessado, e por quê?

**Ações do engenheiro**

- [ ] Registrar o nome do patrocinador e do executor.
- [ ] Reservar a data da sessão presencial do passo 3. Este é o ponto mais frágil do cronograma.
- [ ] Receber a documentação do processo. **Não processar nada no Claude Code antes da 0d.**
- [ ] Montar a matriz de acessos:

| Item | Concedido | Negado | Restrição aplicada | Motivo |
|---|---|---|---|---|
| | | | | |

**Passa se:** patrocinador e executor nomeados, data reservada e ao menos uma fonte acessível.

**Não passa se:** nenhum acesso a dado é concedido, ou o executor não é liberado para a sessão presencial.

Registre o que foi negado com o mesmo cuidado que o concedido. É isso que permite separar, no final, uma lacuna do diagnóstico de uma falha do método.

---

### 3.6 Etapa 0d — Abertura do caso

**Objetivo:** preparar o ambiente antes de processar dados operacionais do cliente. Informações administrativas anteriores seguem HAB-01 §3.7.

**Checklist na ordem das operações:**

- [ ] Conferir a prontidão do expediente: 0a qualificada, revisão vigente, 0b formalizada com os três documentos assinados e evidências conferidas, 0c com acesso efetivo e sem pendência impeditiva. Conferir o identificador reservado e o responsável nomeado.
- [ ] **Abrir** o caso com novo-caso.sh. abrir_caso.py confere e copia o pacote do método e seu manifesto antes da abertura, confere os hashes da cópia e cria o repositório por caso. A opção --expediente confere prontidão e identidade, sem importar.
- [ ] **Planejar e provisionar** os canais no caso aberto, com /eiac-campo:canais ou canais.py planejar, conforme CAN-01. Conferir ids, propriedade e acessos; confirmar no chat cada criação e cada compartilhamento. Para provisionar pelo MCP, declarar primeiro contêiner exclusivo do caso; se faltar id ou regra compatível, usar a interface externa.
- [ ] **Definir** os endereços por ids com canais.py definir no próprio terminal, antes da importação, ou preparar a declaração humana completa para fornecê-la por --canais junto da importação. Nenhum endereço é deduzido de nome de pasta.
- [ ] **Importar** obrigatoriamente o expediente por importar_habilitacao.py, no terminal humano e fora da sessão do agente. O componente conserva PDFs assinados, evidências e matriz, origem e hashes, o desfecho e os RH-xx; conserva também os ids dos formulários e seu vínculo com o expediente.
- [ ] **Gravar 00-habilitacao**: conferir o rascunho gerado e gravar caso/00-habilitacao.md por validar.py. Não editar diretamente a versão de caso nem colocar documentos operacionais em fontes; esses documentos passam pelo recebimento humano após coleta preparada.
- [ ] **Selar** por selar.py. Conferir em /eiac-nucleo:estado e no histórico Git que o commit confirmou um selo posterior à importação e contém o evento HabilitacaoImportada e o prefixo correspondente da trilha. O diagnóstico do método copiado é de integridade, não de autenticação da origem do manifesto.
- [ ] **Iniciar F0** somente após importação e selo confirmados, procedência ativa e canais exigidos íntegros. Um evento SeloAplicado sem commit confirmado, um commit recusado ou Git inacessível mantém F0 bloqueado.

**Passa se:** o caso está aberto com método conferido, canais definidos antes ou junto da importação, expediente importado, 00-habilitacao gravado pelo validador e selo confirmado no histórico Git.

**Falha técnica:** a operação recusa com motivo e registro de negativa; corrigir a causa e repetir. Antes de existir caso, a abertura emite diagnóstico estruturado e preserva diário se a base já existir fora de repositório, sem criar caso apenas para registrar a negativa. Identidade inválida não autoriza inventar autor humano.

**Nota sobre restrições:** o RH importado de 0c é vinculado pelo engenheiro a fonte F curada, ou dispensado com motivo, durante P2 e pelo terminal humano. P2 não encerra com RH pendente. E1 de caso restrito aguarda essa resolução para materializar; a marca aparece junto a cada asserção que cita fonte restrita, conforme HAB-01 §3.4 e CTX-01 §3.7. Nenhum vínculo é inferido do texto da matriz.

---

### 3.7 Desfecho

| Desfecho | Quando | O que acontece |
|---|---|---|
| **Prosseguir** | Os quatro pré-requisitos estão satisfeitos e nenhum acesso essencial foi negado | F0 começa |
| **Prosseguir com restrição** | Os pré-requisitos estão satisfeitos, mas há acesso negado | O percurso segue, e a restrição aparece em cada entregável, no item afetado |
| **Não prosseguir** | Falta ao menos um pré-requisito | O trabalho não começa. A organização recebe o registro do que precisa mudar |

A restrição nunca vira ressalva genérica no fim do relatório. Ela acompanha o item que ficou sem verificação.

O rascunho de 00-habilitacao é gerado pelo importador e passa pelo validador; não exige cópia manual de um modelo. RH vinculado acompanha as asserções afetadas; dispensa motivada não concede acesso nem verifica conteúdo negado.

---

### 3.8 Durante o percurso: perda de pré-requisito

Se o patrocinador sair, o executor for realocado ou um acesso for revogado:

1. Suspenda o percurso e registre a data e a causa no diário de campo.
2. Volte à etapa 0c e substitua o pré-requisito perdido.
3. Só retome depois da substituição registrada.

Retomar sem substituir produz entregável sem autoridade. Um termo de autonomia assinado por um patrocinador que saiu não vincula ninguém.

## 4. Condição de aceite
O roteiro está pronto quando o engenheiro consegue aplicar as perguntas de 0a–0c, conferir os pré-requisitos e executar o checklist de 0d na ordem declarada, distinguindo confirmação no chat de ato humano no terminal. F0 exige importação e selo confirmado; o encerramento de P2 exige resolução de todos os RH importados.

## 5. Referências
EMCIA-HAB-01, EMCIA-CAN-01, EMCIA-MAN-01, EMCIA-CTX-01 §3.7 e EMCIA-TRA-01; auxiliares/EMCIA-HAB-fluxo-operacional-proposta.md. Referência operacional: emcia-marketplace, decisões 039–043 e playbook 0.4.19. Templates HAB-01/02/03 permanecem próprios da formalização.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.2 | 2026-10 | Celso do Vale | Revisão da edição anterior sem versão explícita; renomeação de EMCIA-HAB-02 para EMCIA-ROT-02 devido ao conflito com o template HAB-02; checklist de 0d conforme decisões 039–042, sem cópia manual do método ou escrita direta em fontes, e vínculo RH em P2 | pendente |
| 0.3 | 2026-10 | Celso do Vale | Aprovação documental por Celso do Vale; referência operacional atualizada para o playbook 0.4.19 | Celso do Vale — 03/10/2026 |
| 1.0 | 03/10/2026 | Celso do Vale | Primeira linha de base aprovada (metodo-v1.0), sem alteração de conteúdo em relação à v0.3 | Celso do Vale |
