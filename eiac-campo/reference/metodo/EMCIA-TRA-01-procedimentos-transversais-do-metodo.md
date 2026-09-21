# Procedimentos Transversais do Método

*Leitura de volta, confronto de divergência, procedência, débito de julgamento e pendência bloqueante*

| | | | |
|---|---|---|---|
| **Código** | EMCIA-TRA-01 | **Versão** | 0.2 |
| **Data** | 17/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | F0–F4 (transversal) | **Passo** | Todos |

## 1. Objetivo

Formalizar os cinco procedimentos que o método aplica em mais de um passo e que, até aqui, existiam como prescrição sem forma. São eles: a leitura de volta, o confronto entre regra escrita e regra praticada, a marcação de procedência, o débito de julgamento e o critério de pendência bloqueante.

Cada um resolve o mesmo tipo de problema: o método determina que algo seja feito — verificar, confrontar, marcar, responder, bloquear — sem definir como se registra o resultado. Procedimento sem registro produz declaração de conformidade, não evidência.

## 2. Escopo e aplicação

Aplica-se a todos os passos, em todos os níveis. Os procedimentos são invocados por passos específicos — o confronto em P3d, a leitura de volta em P3b e P9 —, mas suas regras não pertencem a nenhum deles e por isso ficam reunidas aqui.

Opera sob a taxonomia documental de procedência **D — declarada, I — inferida e V — verificada**.

Fica fora: o procedimento de levantamento em si, definido no EMCIA-ROT-01, e a estrutura de registro do contexto, definida no EMCIA-CTX-01.

## 3. Conteúdo

### 3.1 Os cinco procedimentos

| Procedimento | Onde é invocado | O que produz |
|---|---|---|
| Leitura de volta | P2, P3b, P4, P9 | Confirmação, correção ou recusa item a item, com data |
| Confronto e registro de divergência | P3d | Classificação de cada regra e justificativa da divergência |
| Marcação de procedência | Todo registro | Marca D, I ou V com autoria e evidência |
| Débito de julgamento | F0 a P5 | Pergunta registrada e data de liquidação |
| Pendência bloqueante | Todo encerramento de passo | Impedimento explícito, com efeito no portão |

### 3.2 Leitura de volta

**O que é.** O engenheiro lê em voz alta, para quem forneceu a informação, a lista consolidada do que registrou. A pessoa confirma, corrige ou recusa cada item.

**Por que é obrigatória.** É o instrumento de maior rendimento por tempo investido do método: produz as informações que não emergiram espontaneamente, sobretudo as de casos raros, e converte procedência D em V com evidência identificada. Adiá-la para outro dia destrói o rendimento, porque o que lhe dá força é a memória imediata do que acabou de ser dito.

**Procedimento:**

1. Consolidar a lista antes de encerrar o encontro, sem reorganizar o conteúdo.
2. Ler item a item, em voz alta, sem parafrasear o que foi registrado.
3. Registrar o desfecho de cada item: **confirmado**, **corrigido** ou **recusado**.
4. Para item corrigido, registrar a versão anterior e a corrigida, ambas datadas.
5. Registrar itens que a pessoa acrescenta durante a leitura, marcando sua origem como leitura de volta.
6. Datar e identificar quem leu e quem confirmou.

**Efeito na procedência.** Item confirmado em leitura de volta passa a V, com a sessão como evidência. Item recusado não é apagado: permanece registrado como recusado, com data. Item corrigido gera versão nova, nunca sobrescrita.

**Onde é obrigatória:** P3b, na mesma sessão; P2, ao fechar o glossário do processo; P9, na validação do resultado apurado com o patrocinador.

### 3.3 Confronto e registro de divergência

**O que é.** O procedimento de P3d: cada regra praticada é confrontada com o que os documentos, sistemas e normas determinam, e o resultado é registrado.

**Procedimento:**

1. Para cada regra levantada, localizar o dispositivo escrito correspondente, quando existir.
2. Classificar a regra em uma das cinco categorias da seção 3.4.
3. Abrir um item de confronto (Anexo A) para **toda** regra, identificado como `confronto-NNN`.
4. Quando a classe for `divergente`, preencher os três campos condicionais do item: `documento_diz`, `observado` e `justificativa`.
5. Registrar no campo `classificacao_confronto` do registro de Regra a `classe` atribuída e a `referencia_p3d` correspondente ao item.
6. Apurar o placar e o indicador da seção 3.4.

**Um item por regra, não só por divergência.** O placar exige classificar todas as regras do caso, e o registro de contexto exige que toda `classificacao_confronto` resolva para um item de P3d. O Anexo A é, portanto, o registro do confronto — a divergência é um de seus desfechos possíveis, não sua única razão de existir. Para as demais classes, os três campos condicionais permanecem vazios e a ficha guarda a classe, a evidência e a data.

**Registro da divergência.** Quando a classe é `divergente`, o item guarda o que o documento determina, o que foi observado e a justificativa apresentada por quem executa. A justificativa é o campo de maior valor: divergência sem razão declarada é desvio; divergência com razão declarada é regra de negócio não incorporada ao documento — e a distinção muda o encaminhamento.

**Desfecho de cada item da lista de verificação de campo.** Toda afirmação declarada na Fase 0 e convertida em item a verificar recebe um de quatro desfechos, e nenhum item fica sem desfecho:

| Desfecho | Significado |
|---|---|
| Confirmado | A verificação encontrou o que fora declarado |
| Corrigido | A verificação encontrou algo diferente, e a correção foi aceita |
| Refutado | A verificação contradisse o declarado |
| Esclarecido | O declarado era ambíguo; a verificação fixou o sentido |

### 3.4 Placar de confronto

Cada regra do caso recebe exatamente uma classificação:

| Categoria | Definição |
|---|---|
| **Alinhada** | Escrita e praticada conforme o escrito |
| **Divergente** | Escrita, mas praticada de modo diferente |
| **Não documentada** | Praticada e não escrita em lugar algum |
| **Órfã** | Escrita e não praticada |
| **Escrita-mas-inacessível** | Escrita, porém quem executa não conhece ou não alcança o documento |

**Denominador.** As regras efetivamente praticadas são as alinhadas, divergentes e não documentadas. Órfãs e escritas-mas-inacessíveis são contadas à parte, porque descrevem o estado da documentação e não o do processo.

**Indicador de conhecimento não documentado:**

```
(divergentes + não documentadas) ÷ (alinhadas + divergentes + não documentadas)
```

O indicador mede quanto do que sustenta o processo não pode ser obtido por leitura. É o produto defensável do Passo 3 e insumo direto da comparação prevista no plano de verificação.

**Leitura das categorias residuais.** Proporção alta de escritas-mas-inacessíveis indica problema de distribuição documental, não de conhecimento tácito, e admite solução diferente. Proporção alta de órfãs indica documentação desatualizada. Nenhuma das duas entra no indicador, e confundi-las com regra não documentada infla o resultado.

### 3.5 Marcação de procedência

**Regra geral.** Toda informação registrada no percurso recebe uma marca. A marca não é atribuída por modelo de linguagem e acompanha a informação até o entregável.

| Marca | Quando se aplica | Exige |
|---|---|---|
| **D — declarada** | A organização informou | Autor nomeado e data |
| **I — inferida** | Pessoa ou ferramenta deduziu de outras informações | Premissa escrita |
| **V — verificada** | Confirmada por observação, documento-fonte ou leitura de volta | Evidência identificada e responsável |

**Transições admitidas.** D → V por verificação; I → V por confirmação; I → descartada quando refutada. **Nenhuma transição ocorre por edição do registro:** toda mudança de marca cria versão nova e preserva a anterior. Hipótese confirmada não se torna evidência retroativamente.

**Restrição de uso.** Informação marcada I não sustenta decisão conclusiva. Pode orientar a investigação, compor hipótese e figurar no dossiê como tal, mas não fundamenta a classificação tecnológica do Passo 5 nem o cálculo de um número apresentado como resultado.

**Procedência em número.** Todo valor quantitativo apresentado carrega a marca da sua origem. Estimativa apresentada sem marca assume aparência de medição, e é a forma mais comum de inflar a credibilidade de um diagnóstico sem afirmar nada falso.

### 3.6 Débito de julgamento

**O que é.** Quando uma pergunta relevante não pode ser respondida no momento em que surge, ela é registrada como débito, com o passo de origem e o prazo de liquidação. O percurso segue.

**Por que existe.** Sem registro, a pergunta é respondida por omissão: o método avança, logo a resposta terá sido sim. Foi o que ocorreu na simulação com a pergunta sobre a adequação da IA à estratégia — e a resposta implícita contradisse o que o Passo 4 concluiu depois, por outro instrumento e tarde demais.

**Procedimento:**

1. Registrar a pergunta na forma em que surgiu, sem reformular para torná-la respondível.
2. Registrar o passo de origem, a data e quem a levantou.
3. Definir o passo em que deve ser liquidada.
4. No encerramento do passo definido, registrar a resposta e sua procedência, ou reclassificar o débito como pendência bloqueante.

**Efeito.** Débito não liquidado até o passo definido bloqueia o encerramento daquele passo. Débito respondido por omissão não existe: ausência de registro de resposta é débito em aberto.

### 3.7 Pendência bloqueante

**O que é.** Critério que distingue pendência que pode conviver com o avanço da que impede o encerramento. Sem ele, "passo não fechado" é observação sem consequência.

**Uma pendência é bloqueante quando satisfaz qualquer das condições:**

| # | Condição |
|---|---|
| B1 | Sua resposta pode alterar materialmente um número já apresentado ao patrocinador |
| B2 | Recai sobre a linha de base de uma métrica declarada como objetivo |
| B3 | Impede a verificação de um item inegociável |
| B4 | Deixa sem fonte identificada uma regra classificada como de alta consequência |
| B5 | Corresponde a débito de julgamento vencido |

**Efeito.** Pendência bloqueante impede o encerramento do passo e a emissão do entregável da fase. Pendência não bloqueante permite o avanço e entra no entregável como limitação declarada, com o passo de origem e o efeito conhecido.

**Registro.** Toda pendência é registrada com origem, condição de bloqueio aplicável — ou sua ausência —, responsável pela resolução e efeito sobre o resultado.

### 3.8 Condições executáveis para o Code Plugin

| ID | Condição verificável | Comportamento esperado |
|---|---|---|
| **TRA-V01** | Toda regra classificada possui item de confronto referenciado por `referencia_p3d` | Recusar classificação órfã |
| **TRA-V02** | Item de classe `divergente` possui `documento_diz`, `observado`, `justificativa` e data | Recusar item de divergência incompleto |
| **TRA-V03** | Todo item da lista de verificação de campo possui desfecho | Recusar encerramento de P3d com item sem desfecho |
| **TRA-V04** | Cada regra possui exatamente uma classificação do placar | Recusar regra sem classificação ou com duas |
| **TRA-V05** | Registro marcado I não figura como fundamento de decisão de P5 | Recusar uso conclusivo de inferência |
| **TRA-V06** | Mudança de marca cria versão nova | Recusar sobrescrita de procedência |
| **TRA-V07** | Item de leitura de volta possui desfecho e data | Recusar registro de leitura sem desfecho |
| **TRA-V08** | Débito vencido impede encerramento do passo de liquidação | Recusar encerramento com débito em aberto |
| **TRA-V09** | Pendência bloqueante impede emissão do entregável da fase | Recusar emissão |
| **TRA-V10** | Pendência não bloqueante consta do entregável como limitação | Recusar emissão que omita pendência registrada |

## 4. Condição de aceite

O artefato está pronto quando os cinco procedimentos possuem passo a passo aplicável e formato de registro definido; quando o placar tem cinco categorias mutuamente exclusivas e denominador explícito; quando as transições de procedência estão fixadas e nenhuma ocorre por edição; quando existe critério objetivo que distingue pendência bloqueante de não bloqueante; e quando as validações TRA-V01 a TRA-V10 podem ser convertidas em recusa determinística do núcleo.

## 5. Referências

- EMCIA-MET-01 — Documento do método, seção 3.7.
- EMCIA-ROT-01 — Roteiro de levantamento de regras não documentadas.
- EMCIA-CTX-01 — Instrumento de registro da camada de contexto.
- EMCIA-CAM-01 — Protocolo de campo por passo, P6 a P10.
- EMCIA-VER-01 — Plano de verificação do método.
- EMCIA-TST-01 — Plano de testes da implementação.
- EMCIA-GLO-01 — Glossário do método.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
|---|---|---|---|---|
| 0.1 | 17/09/2026 | Celso do Vale | Versão inicial: leitura de volta, confronto e placar, procedência, débito de julgamento, pendência bloqueante e validações TRA-V01–V10. | — |
| 0.2 | 17/09/2026 | Celso do Vale | Item de confronto passa a ser aberto para toda regra, não apenas para divergências; nomes de campo alinhados ao EMCIA-CTX-01 0.4; identificador padronizado como `confronto-NNN`; TRA-V01 e TRA-V02 ajustadas. | — |

---

## Anexo A — Item de confronto

Aberto em P3d para toda regra do caso. É a fonte de verdade do confronto; o registro de contexto guarda apenas a classe e a referência a este item.

| Campo | Conteúdo | Obrigatório |
|---|---|---|
| `id` | `confronto-NNN`, sequencial no caso | Sempre |
| `regra` | Identificador da regra no registro de contexto | Sempre |
| `classe` | alinhada · divergente · nao_documentada · orfa · escrita_inacessivel | Sempre |
| `evidencia` | Sessão, caso observado, amostra ou documento que sustentou a classificação | Sempre |
| `fonte_documental` | Onde o dispositivo escrito está, com data da versão | Quando a regra é escrita |
| `documento_diz` | Transcrição ou referência ao que o dispositivo determina | Quando `classe: divergente` |
| `observado` | Descrição do que é praticado | Quando `classe: divergente` |
| `justificativa` | Razão declarada por quem executa | Quando `classe: divergente` |
| `justificado_por` | Pessoa nomeada | Quando `classe: divergente` |
| `encaminhamento` | incorporar_ao_documento · corrigir_a_pratica · manter_e_registrar · pendente | Quando `classe: divergente` ou `orfa` |
| `registrado_por` | Engenheiro que formalizou o item | Sempre |
| `data` | — | Sempre |

## Anexo B — Registro de débito de julgamento

| Campo | Conteúdo |
|---|---|
| Identificador | Código sequencial no caso |
| Pergunta | Na forma em que surgiu |
| Passo de origem | — |
| Levantada por | Pessoa nomeada |
| Data de origem | — |
| Passo de liquidação | Onde precisa ser respondida |
| Resposta | Preenchida na liquidação |
| Procedência da resposta | D, I ou V |
| Data de liquidação | — |
| Desfecho | Liquidado · reclassificado como pendência bloqueante |
