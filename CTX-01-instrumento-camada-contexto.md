# CTX-01 — Instrumento da Camada de Contexto

**Documento controlado · EMCIA**
**Ação:** 2.2 — Construir o instrumento de registro de regras verificadas da camada de contexto
**Entregável:** estrutura de glossário, entidades e regras verificadas que alimenta o passo 5
**Camada:** `CA4`
**Versão:** 1.0 · setembro de 2026

> **Nota de compatibilidade:** o contrato de procedência deste documento foi
> normalizado para `D | I | V`. A migração integral dos quatro objetos para o
> EMCIA-CTX-01 v0.4 pertence ao pacote 2.5.1.

---

## 1. O que este instrumento é

A estrutura em que o conhecimento levantado em campo é registrado, de modo que o passo 5 possa classificá-lo.

## 2. O que ele não é

**Não é base de conhecimento.** Base de conhecimento existe para ser consultada. Esta estrutura existe para ser **interrogada por um critério de decisão** — o do passo 5, que pergunta se o caso é de agente. Todo campo aqui existe porque alguma pergunta do passo 5 depende dele. Campo que nenhuma pergunta usa não entra.

**Não é ontologia gerada.** Nenhum registro entra sem curadoria humana. Geração automática de ontologia produz artefato plausível e errado — o pior resultado possível.

**Não é o glossário do método.** Aquele é `GLO-01`, vocabulário de quem aplica. Este é o vocabulário da organização atendida, levantado no passo 2.

---

## 3. Quatro objetos

| Objeto | O que registra | Passo de origem |
|---|---|---|
| **Termo** | Palavra do negócio da organização, com o que significa ali | P2 |
| **Entidade** | Objeto do domínio, com atributos e relações | P2, refinado em P3 |
| **Regra** | O que determina o comportamento do processo | P2 e P3 |
| **Fonte** | Onde o dado vive, com contrato | P2 |

A **Regra** é o objeto central. Os outros três existem para que ela seja interpretável.

---

## 4. Registro de Termo

```yaml
id: T-001
termo: guia
significado: documento de autorização emitido pelo convênio para um procedimento
nao_e: nota fiscal, nem prontuário
sinonimos_em_uso: [autorização, pedido]
procedencia: D
```

O campo `nao_e` faz o mesmo trabalho que faz no glossário do método: a ambiguidade raramente vem de ausência de definição, e sim de significado vizinho.

---

## 5. Registro de Entidade

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
```

---

## 6. Registro de Regra — o objeto central

```yaml
id: R-014
enunciado: guias do convênio X são enviadas no mesmo dia da emissão

# procedência documental
procedencia: V
evidencia:
  tipo: observacao
  referencia: sessão presencial de 2026-09-18
data: 2026-09-18
autor: Rafael Nogueira

# estatuto — escrita, praticada, ou as duas
estatuto: praticada
documento_de_origem: null
divergencia:
  documento_diz: fila única por ordem de chegada
  observado: três convênios saem no mesmo dia
  justificativa: convênio glosa se o envio passar de 24h
  registrada_em: P3d

# o que o passo 5 interroga
determinismo: admite_julgamento
frequencia: rotineira
consequencia_do_erro: alta
decisor_quando_nao_cobre: Cláudia Ferreira
entradas: [E-001, T-001]
excecoes_conhecidas:
  - convênio Y aceita 48h, mas não está escrito
estabilidade: muda quando o convênio revisa contrato

# governança
versao: 2
historico:
  - versao: 1
    data: 2026-09-12
    procedencia: I
    premissa: deduzida do manual interno
    mudanca: registrada a partir do manual interno
    autor: Rafael Nogueira
  - versao: 2
    data: 2026-09-18
    procedencia: V
    mudanca: corrigida na leitura de volta; prazo real é 24h, não 72h
    autor: Rafael Nogueira
```

### 6.1 Por que cada campo do bloco central existe

| Campo | Pergunta do passo 5 que ele responde |
|---|---|
| `determinismo` | Se é determinística e escrita, é automação, não agente |
| `frequencia` | Regra rara não sustenta caso, mas pode inviabilizá-lo |
| `consequencia_do_erro` | Define zona de contenção e nível de autonomia |
| `decisor_quando_nao_cobre` | Se existe um nome, há julgamento humano no fluxo |
| `entradas` | Define o que a solução precisa alcançar |
| `excecoes_conhecidas` | Exceção não documentada é o que quebra piloto |
| `estabilidade` | Regra instável exige recalibragem mais frequente |

Sem esses sete campos, o passo 5 classifica por impressão.

---

## 7. Registro de Fonte

```yaml
id: F-002
fonte: planilha de controle de envios
tipo: planilha
responsavel: Cláudia Ferreira
contrato:
  estrutura: uma linha por guia enviada
  significado: registra envio, não emissão
  qualidade: preenchida ao fim do dia; lacunas em dias de pico
acesso: leitura, autorizado em 2026-09-10
procedencia: V
```

O campo `significado` é o que evita o erro mais caro da camada de dados: tratar uma fonte pelo nome em vez de pelo que ela de fato registra.

---

## 8. O quadro que o instrumento produz

Cruzamento de `frequencia` por `consequencia_do_erro`, para todas as regras do caso:

| | Consequência baixa | Consequência alta |
|---|---|---|
| **Rotineira** | Candidata a automação | Núcleo do caso |
| **Rara** | Ignorável | **Célula crítica** |

A célula crítica é o achado empírico do método: regras de baixa frequência e alta consequência não estão nos documentos nem no histórico, que é dominado pelos casos comuns.

**Consequência de uso:** se a célula crítica estiver vazia ao fim do P3, ou a organização é excepcionalmente regular, ou o levantamento não aconteceu. As duas hipóteses precisam ser confrontadas antes de encerrar o passo — e a segunda é a mais provável.

O mesmo quadro serve ao Quadro de Contraste: **a previsão é que o braço da antítese produza a célula crítica vazia.**

---

## 9. A trava de curadoria

O ciclo de referência das arquiteturas de contexto é observar → refletir → aprender, sem humano em nenhum ponto. Aqui ele é interrompido por desenho:

| Etapa | Executor | Saída |
|---|---|---|
| Observar — extrair regras de documentos | Agente · `EX2` | Regra candidata, com fonte e trecho |
| Refletir — confrontar escrita × praticada | Copilotado · `EX3` | Placar classificado |
| **Aprender — curar e decidir sobre conflito** | **Humano · `EX4`** | Regra consolidada, com autor e data |

**Nenhuma regra entra na camada de contexto sem passar pela terceira linha.**

Na prática: a candidata nasce em `rascunho/`, com `procedencia: I` e premissa. Só vira registro de contexto quando uma pessoa a curou, e a curadoria exige mudança de versão com autor, data e justificativa.

---

## 10. Versionamento

Toda alteração cria versão nova e preserva a anterior no `historico`, com o que mudou e por quê.

**Confirmação não converte o registro original.** Uma regra `I` confirmada em campo ganha versão nova com `procedencia: V` e evidência própria. A versão anterior permanece. Hipótese confirmada não vira evidência retroativamente.

O arquivo por registro é versionado em Git, e o commit é a data.

---

## 11. O que alimenta cada entregável

| Objeto | E2 | E3 |
|---|---|---|
| Termo | Parte B, glossário do processo | Referenciado |
| Entidade | Registrada | Especificação da solução |
| Regra | Corpo do dossiê | Zona de contenção e gatilhos |
| Fonte | Inventário | Contratos de dados |

O quadro da seção 8 entra no E2 e é o que sustenta a priorização do passo 4.

---

## 12. Critério de encerramento do instrumento

O registro de contexto de um caso está completo quando:

1. Todo termo usado nas regras existe no glossário do processo
2. Toda regra tem os sete campos do bloco central preenchidos
3. Toda regra `V` tem evidência de observação, documento-fonte ou leitura de volta
4. Toda divergência tem justificativa e etapa de registro
5. Toda fonte tem contrato com os três campos
6. O quadro frequência × consequência foi produzido e a célula crítica foi confrontada

---

## 13. Limites declarados

**Não cobre o domínio inteiro.** Registra o que o caso priorizado exige, não a organização toda. Mapeamento completo de domínio é projeto próprio.

**Não é executável.** É estrutura de registro, não grafo consultável em tempo de execução. A conversão para grafo, se o cliente a quiser, é trabalho de implantação — fora do método.

**Depende do levantamento.** Se o P3b não acontecer, este instrumento registra apenas regra escrita, e o quadro da seção 8 fica com metade das células vazias. O instrumento não compensa a ausência do passo; apenas a torna visível.

---

*Documento controlado. Alterações exigem registro do que mudou e da data.*
