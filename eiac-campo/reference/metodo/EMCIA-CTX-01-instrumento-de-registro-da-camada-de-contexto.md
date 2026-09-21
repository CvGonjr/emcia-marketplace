# Instrumento de Registro da Camada de Contexto

*Estrutura de termos, entidades, regras e fontes que alimenta os Passos 4 e 5*

| | | | |
|---|---|---|---|
| **Código** | EMCIA-CTX-01 | **Versão** | 0.4 |
| **Data** | 17/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | F1–F2 | **Passo** | 2 a 5 |

## 1. Objetivo

Definir a estrutura em que o conhecimento levantado nos Passos 2 e 3 é registrado, relacionado e versionado para sustentar a priorização do Passo 4 e a classificação tecnológica do Passo 5. O instrumento converte o produto do levantamento e do confronto de campo em contexto estruturado, com autoria, procedência e evidência rastreáveis.

O CTX-01 não levanta novamente o conhecimento obtido em campo. Ele recebe o que foi produzido pelos instrumentos anteriores e estabelece o contrato pelo qual esse conhecimento pode ser utilizado nas decisões posteriores do método.

## 2. Escopo e aplicação

Aplica-se ao registro de contexto do caso, alimentado por P2, P3b e P3d e consumido por P4 e P5. Opera sob a taxonomia documental de procedência **D — declarada, I — inferida e V — verificada**.

O instrumento não é uma base de conhecimento genérica, não é uma ontologia gerada automaticamente e não substitui o EMCIA-GLO-01. Registra somente o vocabulário, as entidades, as regras e as fontes necessárias ao caso priorizado. Mapeamento integral do domínio e conversão para grafo, banco semântico ou mecanismo consultável em produção permanecem fora do escopo.

A estrutura existe nos três níveis do método. O que varia entre N1, N2 e N3 é a profundidade do registro e da governança, não a presença dos quatro objetos nem das regras de procedência.

## 3. Conteúdo

### 3.1 Posição no percurso

| Origem / destino | Função no CTX-01 |
|---|---|
| **P2** | Fornece termos do negócio, entidades, fontes e definições declaradas. |
| **P3b / EMCIA-ROT-01** | Fornece regras levantadas, autoria, evidências, leitura de volta e procedência. |
| **P3d** | Fornece a classificação do confronto e o registro de divergência referenciável produzido pela ação 2.4. |
| **CTX-01** | Normaliza, relaciona, versiona e governa o contexto do caso. |
| **P4** | Usa frequência, consequência e referências de confronto/divergência na priorização. |
| **P5** | Interroga o contexto para classificar e especificar a solução. |

O CTX-01 não é um segundo roteiro de levantamento. Sua função começa quando existe material a registrar e confrontar.

### 3.2 Quatro objetos

| Objeto | O que registra | Passo de origem |
|---|---|---|
| **Termo** | Palavra do negócio, com o que significa naquela organização. | P2 |
| **Entidade** | Objeto do domínio, com atributos e relações. | P2, refinado em P3 |
| **Regra** | Condição que governa uma ação, decisão ou exceção do processo. | P2 e P3 |
| **Fonte** | Onde o dado vive e o que a fonte efetivamente representa. | P2 |

A **Regra** é o objeto central. Termos, entidades e fontes existem para torná-la interpretável, verificável e utilizável pelos passos posteriores.

### 3.3 Registro de Termo

```yaml
id: T-001
termo: guia
significado: documento de autorização emitido pelo convênio para um procedimento
nao_e: nota fiscal, nem prontuário
sinonimos_em_uso: [autorização, pedido]
procedencia: V
declarado_por: Claudia Ferreira
registrado_por: Rafael Nogueira
data: 2026-09-18
evidencia: leitura de volta da sessão de 2026-09-18
```

O campo `nao_e` reduz ambiguidade por significado vizinho. A procedência informa o estado documental do registro; `declarado_por` identifica quem sustenta o conteúdo e `registrado_por` identifica quem realizou o registro no Estúdio.

### 3.4 Registro de Entidade

```yaml
id: E-001
entidade: Guia
atributos:
  - nome: convenio
    tipo: categoria
    obrigatorio: true
  - nome: data_emissao
    tipo: data
    obrigatorio: true
relacoes:
  - com: Paciente
    cardinalidade: muitos-para-um
onde_vive: [F-002]
procedencia: D
declarado_por: Claudia Ferreira
registrado_por: Rafael Nogueira
data: 2026-09-12
```

A entidade registra apenas o recorte necessário ao caso. A existência de uma entidade no CTX-01 não significa que o domínio completo da organização tenha sido modelado.

### 3.5 Registro de Regra — objeto central

```yaml
id: RN-014
enunciado: quando o convênio X emite a autorização, a guia é enviada no mesmo dia, exceto se houver pendência documental
gatilho: recebimento_da_autorizacao

procedencia: V
autoria_conteudo: Claudia Ferreira
registrado_por: Rafael Nogueira
data: 2026-09-18
origem_do_conhecimento: experiencia_propria

evidencia:
  tipo: observacao
  referencia: sessao_P3b_2026-09-18_ficha_07

classificacao_confronto:
  classe: nao_documentada
  referencia_p3d: confronto-007
documento_de_origem: null

# bloco interrogado pelos Passos 4 e 5
determinismo: admite_julgamento
frequencia: rotineira
consequencia_do_erro: alta
decisor_quando_nao_cobre: Claudia Ferreira
entradas: [E-001, T-001]
excecoes_conhecidas:
  - convenio Y aceita 48h, e isso nao esta escrito
estabilidade: muda quando o convenio revisa contrato

versao: 2
historico:
  - versao: 1
    data: 2026-09-12
    procedencia: I
    premissa: deduzida do manual interno, sem enunciado do executor
    registrado_por: Rafael Nogueira
  - versao: 2
    data: 2026-09-18
    procedencia: V
    mudanca: corrigida na leitura de volta; prazo real e 24h, nao 72h
    confirmado_por: Claudia Ferreira
    registrado_por: Rafael Nogueira
```

`autoria_conteudo` identifica a pessoa que detém, enuncia ou confirma a regra do processo. `registrado_por` identifica o engenheiro que formalizou o registro. Um agente pode preparar rascunhos, mas nunca ocupa nenhum desses campos como autor de um registro curado.

O CTX-01 não duplica o conteúdo do confronto produzido em P3d. `classificacao_confronto` guarda a classe atribuída e `referencia_p3d` aponta para o item correspondente do instrumento da **ação 2.4**, que permanece como fonte de verdade da divergência. Quando `classe: divergente`, o registro referenciado em P3d deve conter, no mínimo, o que o documento dizia, o que foi observado e a justificativa registrada.

### 3.6 Campos interrogados pelos Passos 4 e 5

| Campo | Decisão que sustenta |
|---|---|
| `determinismo` | Distingue regra executável de situação que exige julgamento. |
| `frequencia` | Indica quanto a regra participa do processo e sustenta a priorização. |
| `consequencia_do_erro` | Informa risco, zona de contenção e limite de autonomia. |
| `decisor_quando_nao_cobre` | Identifica quem assume o julgamento quando a regra não resolve o caso. |
| `entradas` | Define quais entidades, termos e fontes a solução precisa alcançar. |
| `excecoes_conhecidas` | Expõe condições que quebram a regra geral. |
| `estabilidade` | Indica necessidade futura de revisão e recalibragem. |

Sem esses sete campos, a classificação tecnológica depende de impressão em vez de evidência estruturada.

### 3.7 Registro de Fonte

```yaml
id: F-002
fonte: planilha de controle de envios
tipo: planilha
responsavel: Claudia Ferreira
contrato:
  estrutura: uma linha por guia enviada
  significado: registra envio, nao emissao
  qualidade: preenchida ao fim do dia; lacunas em dias de pico
acesso: leitura, autorizado em 2026-09-10
procedencia: V
registrado_por: Rafael Nogueira
data: 2026-09-10
```

O campo `significado` evita que uma fonte seja interpretada apenas pelo nome. O contrato registra estrutura, significado e qualidade mínima antes de a fonte ser usada pelo caso.

### 3.8 Correspondência com o EMCIA-ROT-01

Cada regra levantada em P3b entra no CTX-01 por conversão direta, sem perder os campos produzidos na sessão.

| Ficha de regra — EMCIA-ROT-01 | Campo no CTX-01 |
|---|---|
| Enunciado condicional | `enunciado` |
| Gatilho | `gatilho` |
| Exceção conhecida | `excecoes_conhecidas` |
| Autoria | `autoria_conteudo` |
| Origem do conhecimento | `origem_do_conhecimento` |
| Frequência estimada | `frequencia` |
| Consequência do erro | `consequencia_do_erro` |
| Procedência | `procedencia` |
| Evidência | `evidencia` |
| Leitura de volta | `evidencia.referencia` e nova entrada no `historico` |

Três campos são acrescentados na curadoria: `determinismo`, `decisor_quando_nao_cobre` e `estabilidade`. Eles constituem julgamento do engenheiro sobre a regra e exigem autoria nominal do registro.

### 3.9 Calibragem por nível

| Dimensão | N1 — Ágil | N2 — Estruturado | N3 — Corporativo |
|---|---|---|---|
| **Termos** | Glossário mínimo do caso. | Catálogo estruturado. | Glossário governado do recorte. |
| **Entidades** | Apenas as usadas no caso. | Atributos e relações explícitas. | Modelo semântico formal do recorte. |
| **Regras** | Arquivo estruturado e versionado. | Catálogo versionado com relações. | Catálogo governado, com responsáveis e aprovação. |
| **Fontes** | Origem, significado e acesso. | Contrato de fonte. | Contrato, responsável e regras de governança. |
| **Versionamento** | Git + autoria. | Git + autoria + justificativa. | Git + autoria + justificativa + aprovação definida. |

N1 não exige ontologia, knowledge graph ou plataforma adicional. A profundidade aumenta com o nível, mas o contrato mínimo de procedência, autoria e rastreabilidade permanece.

### 3.10 Quadro frequência × consequência

O instrumento produz o cruzamento entre frequência e consequência do erro para as regras do caso:

| | Consequência baixa / média | Consequência alta |
|---|---|---|
| **Rotineira** | Regra recorrente. | Regra central para o caso. |
| **Rara** | Regra de baixa exposição. | **Zona crítica.** |

A **zona crítica** reúne regras de baixa frequência e alta consequência que podem estar sub-representadas em documentos e no histórico operacional. Se essa região permanecer vazia após o P3, o engenheiro deve confrontar duas hipóteses: ausência real desse tipo de regra ou insuficiência do levantamento. O instrumento não decide automaticamente entre elas.

O mesmo quadro pode ser utilizado na verificação para comparar o que a representação declarada alcançou com o que o campo posteriormente revelou.

### 3.11 Trava de curadoria

| Momento | Camada | Saída |
|---|---|---|
| Extrair candidata de fonte registrada | EX2 | Regra candidata D ou I, com referência. |
| Confrontar escrita × praticada | EX3 | Classificação e referência ao registro de confronto/divergência de P3d. |
| **Curar e decidir sobre conflito** | **EX4** | Registro aceito, com autoria e versão. |

Nenhuma regra inferida entra como evidência consolidada da camada de contexto sem decisão humana registrada. O Code Plugin pode detectar ausência de campos, duplicidades, referências quebradas e inconsistências; não decide que uma regra é verdadeira.

Na prática, a candidata nasce em `rascunho/`. Somente após curadoria humana pode ser registrada em `contexto/` como versão válida.

### 3.12 Versionamento e regra de não conversão

Toda alteração cria uma nova versão e preserva a anterior no `historico`, com data, responsável e justificativa.

**Confirmação não converte o registro original.** Uma regra I confirmada em campo ganha nova versão com `procedencia: V` e evidência própria. A versão anterior permanece. Assim, hipótese confirmada não se torna evidência retroativamente e a comparação entre representação declarada e campo permanece auditável.

O repositório registra as alterações, mas o commit não substitui os campos de autoria, data e justificativa do próprio registro.

### 3.13 Condições executáveis para o Code Plugin

O CTX-01 define regras que o núcleo pode verificar deterministicamente. Os identificadores abaixo são estáveis e devem ser referenciados pelo EMCIA-TST-01.

| ID | Condição verificável | Comportamento esperado |
|---|---|---|
| **CTX-V01** | Regra possui os sete campos do bloco de decisão. | Recusar gravação se faltar campo obrigatório. |
| **CTX-V02** | Registro I possui premissa escrita. | Recusar inferência sem premissa. |
| **CTX-V03** | Registro V possui evidência identificada. | Recusar verificação sem evidência. |
| **CTX-V04** | Mudança I → V cria nova versão. | Recusar sobrescrita da versão inferida. |
| **CTX-V05** | Todo termo referenciado existe. | Recusar referência quebrada. |
| **CTX-V06** | Toda entidade referenciada existe. | Recusar referência quebrada. |
| **CTX-V07** | Toda fonte referenciada existe e possui contrato mínimo. | Recusar fonte ausente ou sem contrato. |
| **CTX-V08** | Escrita em `contexto/` passa pela curadoria prevista. | Recusar escrita direta que burle a etapa humana. |
| **CTX-V09** | Autoria de conteúdo e registro são pessoas nomeadas. | Recusar identificador de agente como autor de registro curado. |
| **CTX-V10** | Toda nova versão possui data, responsável e motivo da mudança. | Recusar alteração sem trilha mínima. |
| **CTX-V11** | Toda `classificacao_confronto` possui `classe` e `referencia_p3d`; quando a classe é `divergente`, a referência resolve para registro de P3d com `documento_diz`, `observado` e `justificativa`. | Recusar classificação órfã ou divergência sem registro justificável em P3d. |

### 3.14 Saídas e uso posterior

Ao final do registro de contexto de um caso existem: glossário do processo, catálogo de entidades, catálogo de fontes, catálogo de regras, quadro frequência × consequência e lista de pendências de contexto.

| Produto | Uso posterior |
|---|---|
| Termos | E2 e referência do E3. |
| Entidades | E2 e especificação da solução. |
| Regras | E2, P4, P5 e E3. |
| Fontes | Inventário e contratos de dados. |
| Quadro frequência × consequência | P4 e E2. |
| Pendências | Limitações e dependências registradas no E3. |

## 4. Condição de aceite

O CTX-01 está pronto para uso quando um engenheiro consegue receber as saídas de P2, P3b e P3d e registrar termos, entidades, regras e fontes sem decidir novamente quais campos compõem o instrumento; quando a correspondência com o EMCIA-ROT-01 preserva autoria, procedência e evidência; e quando as validações CTX-V01 a CTX-V11 possuem condição verificável suficiente para implementação no Code Plugin.

O registro de contexto de um caso está completo quando: todo termo, entidade e fonte referenciados existem; toda regra contém os sete campos de decisão; toda regra V possui evidência; toda regra I possui premissa e permanece fora de decisão conclusiva até confirmação; toda classificação de confronto aponta para o item correspondente de P3d e, quando `classe: divergente`, a referência resolve para registro com o que o documento dizia, o que foi observado e a justificativa; fontes possuem contrato mínimo; o quadro frequência × consequência foi produzido; e as pendências foram explicitamente registradas.

## 5. Limites declarados

**Não cobre o domínio inteiro.** O CTX-01 registra o recorte necessário ao caso priorizado, não toda a organização.

**Não é uma camada de execução da solução do cliente.** É uma estrutura de registro validável pelo Code Plugin. Sua conversão para grafo, banco semântico ou mecanismo consultável em produção é trabalho de implantação e permanece fora do escopo do método.

**Depende do levantamento.** Sem P3b, o instrumento registra principalmente conhecimento declarado e escrito. Ele não compensa a ausência da verificação de campo; apenas torna essa limitação visível.

## 6. Referências

- EMCIA-MET-01 — Documento do método, Passos 2, 3, 4 e 5.
- EMCIA-ROT-01 — Roteiro de levantamento de regras não documentadas.
- EMCIA-CAT-01 — Fronteira de delegação e catálogo de agentes e habilidades.
- EMCIA-ESP-01 — Especificação executável do Estúdio de Trabalho.
- EMCIA-TST-01 — Plano de testes da implementação.
- EMCIA-GLO-01 — Glossário do método.
- EMCIA-VER-01 — Plano de verificação do método.
- *Data Governance*, John Ladley (2019).

## 7. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
|---|---|---|---|---|
| 0.1 | 15/09/2026 | Celso do Vale | Versão embrionária: quatro objetos, bloco central da regra e quadro frequência × consequência. | — |
| 0.2 | 17/09/2026 | Celso do Vale | Procedência convertida para D/I/V; correspondência com o ROT-01; condições executáveis e terminologia alinhadas ao plano de verificação. | — |
| 0.3 | 17/09/2026 | Celso do Vale | Separação entre autoria do conteúdo e registro; calibragem N1–N3; revisão da zona crítica; condições CTX-V01–V10; escopo e metadados alinhados ao template oficial. | — |
| 0.4 | 17/09/2026 | Celso do Vale | Divergência retirada do registro de Regra como conteúdo duplicado; `classificacao_confronto` passa a referenciar o item de P3d/Ação 2.4; adicionada validação CTX-V11 e ajustada a condição de aceite. | — |
