# Ficha de enquadramento
### Delimitação da dor, custo estimado e nível de complexidade declarado

## Controle do modelo

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-E1-01 | **Versão** | 0.1 |
| **Data** | 2026-10 | **Estado** | Aprovado |
| **Responsável** | Celso do Vale | **Aprovação** | Celso do Vale — 03/10/2026 |
| **Fase** | F0 — Enquadramento | **Passo** | Triagem |
| **Tipo** | Modelo de entregável | **Origem** | EMCIA-MET-01 |

## Identificação do entregável

A tabela seguinte é preenchida por caso e registra a versão e o aceite do entregável.

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Organização** | «razão social» | **Engajamento** | «código do caso» |
| **Fase** | F0 — Enquadramento | **Passos** | Triagem |
| **Nível apurado** | «N1, N2 ou N3 — DAD 0 · GOV 0 · CRI 0» | **Data** | «dd/mm/aaaa» |
| **Engenheiro** | «nome» | **Versão** | «0.1» |
| **Patrocinador** | «nome e cargo» | **Aceite** | «nome e data» |

* **Público:** Patrocinador e quem respondeu à triagem.
* **Extensão:** Uma página. Se passar de duas, o enquadramento não foi concluído.
* **Critério de aceite:** O patrocinador lê em dois minutos e reconhece o próprio problema descrito melhor do que ele o descreveu.

> **Procedência:** Toda afirmação deste documento traz uma das três marcas: `[D]` declarada pela organização, `[I]` inferida a partir de outras informações, `[V]` verificada em campo contra dado, documento ou leitura de volta. Afirmação sem marca não deve ser considerada.

---

## 1. A dor

| Pergunta | Detalhamento |
| :--- | :--- |
| **O quê** | «o que acontece de errado» |
| **Quem** | «quem sofre o efeito, nominalmente» |
| **Onde** | «em que etapa do processo» |
| **Quando** | «com que frequência» |
| **Por quê** | «por que isso importa para o negócio» |
| **Como** | «como o problema se manifesta na prática» |
| **Quanto** | «volume, em unidade do processo» |

---

## 2. Causa provável
«Cadeia de causa, do sintoma até a raiz. Registrar a marca de procedência em cada elo: a causa raiz declarada raramente é a causa raiz real, e a distinção entre `[D]` e `[V]` importa mais aqui do que em qualquer outro campo desta ficha.»

---

## 3. Custo estimado do problema

| Marca | Componente | Base de cálculo | Valor anual |
| :---: | :--- | :--- | :--- |
| **«[D]»** | «ex.: retrabalho» | «volume × tempo × custo/hora» | «R$» |
| **«[I]»** | «ex.: perda por atraso» | «premissa exposta» | «R$» |
| | **Total** | | **«R$»** |

*Toda premissa fica visível. Número sem base de cálculo declarada não entra na ficha.*

---

## 4. Nível de complexidade declarado

| Eixo | Soma | Leitura |
| :--- | :---: | :--- |
| **DAD — dado** | «0» | «síntese em uma linha» |
| **GOV — governança** | «0» | «síntese em uma linha» |
| **CRI — criticidade** | «0» | «síntese em uma linha» |
| **Nível apurado** | **«N_»** | *Definido pelo maior eixo, não pela média* |

> **Nível declarado:** Este resultado deriva do que a organização informou e ainda não foi verificado. A confirmação ocorre no passo 2, no passo 7 e nos passos 3 e 4, conforme o eixo. Havendo divergência, o nível é recalculado e a mudança é registrada.

---

## 5. Objetivo mensurável
«O que se pretende alcançar, em número, com prazo. Formulação verificável: quem lê precisa saber, ao final, se foi atingido ou não.»

---

## 6. Trilha recomendada e decisão solicitada
«Fases previstas, esforço estimado e o que a organização precisa disponibilizar. Registrar a decisão de prosseguimento fundamentada nesta ficha.»

O engenheiro registra decidir-prosseguimento no próprio terminal, com base na ficha preparada, antes da emissão formal de E1. Ambos os desfechos encerram F0; não prosseguir bloqueia as etapas seguintes até nova decisão que autorize prosseguir, preservando o registro anterior. A emissão permanece sujeita ao portão e à resolução de RH pendente.

| Desfecho | Decisor | Data | Motivo | Referência do registro |
| :--- | :--- | :---: | :--- | :--- |
| «prosseguir · não prosseguir» | «pessoa nomeada» | «dd/mm/aaaa» | «fundamento da decisão» | «registro/prosseguimento/decisao-NNNN.yaml» |

---

## Histórico de revisões do modelo

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| Sem versão explícita | — | Celso do Vale | Edição anterior sem controle de versão do modelo; o campo de versão existente pertencia ao entregável de cada caso | — |
| 0.1 | 2026-10 | Celso do Vale | Inclusão de tabela de metadados e histórico próprios do modelo; aprovação documental por Celso do Vale; decisão de F0 alinhada aos dois desfechos de decidir-prosseguimento | Celso do Vale — 03/10/2026 |
