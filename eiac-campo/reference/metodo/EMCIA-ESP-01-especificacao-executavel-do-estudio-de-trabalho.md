# Especificação Executável do Estúdio de Trabalho

*Contrato de playbook, estado, D/I/V, portões e invariantes para F0–P10*

| | | | |
|---|---|---|---|
| **Código** | EMCIA-ESP-01 | **Versão** | 0.2 |
| **Data** | 17/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Sprint 1 — Planejamento | **Passo** | Ação 1.9 |

## 1. Objetivo

Definir os contratos executáveis que o Code Plugin precisa respeitar para instrumentar o método completo, de F0 a P10. O documento traduz as decisões metodológicas em estruturas verificáveis de playbook, estado, procedência D/I/V, camadas de execução, agentes, habilidades, transições, escrita, portões, recorrência e eventos, sem prescrever linguagem de programação ou biblioteca de orquestração.

## 2. Escopo e aplicação

Aplica-se ao `eiac-nucleo`, ao `eiac-campo` e ao repositório de cada caso. Serve de contrato entre os artefatos metodológicos da Sprint 1 e o código da Sprint 2.

A procedência desta versão permanece **D — declarada, I — inferida e V — verificada**. O Code Plugin não incorpora uma taxonomia alternativa enquanto o método não a aprovar. P6 a P10 fazem parte do contrato executável, ainda que a PoC não valide a solução do cliente em operação real.

## 3. Conteúdo

### 3.1 Objetos mínimos do domínio

| Objeto | Responsabilidade |
|---|---|
| Caso | Unidade isolada de engajamento e estado. |
| Playbook | Declara F0–P10, camadas por nível, modalidades, HB, AG, portões, cadências e inegociáveis. |
| Etapa | Unidade de avanço; treze etapas operacionais no percurso completo. |
| Nível | N1, N2 ou N3; governa profundidade e fronteira. |
| Camada de execução | EX1, EX2, EX3 ou EX4. Nenhum agente opera em EX3/EX4. |
| Habilidade HB | Procedimento delegável ou híbrido com insumo, saída e critério de verificação. |
| Agente AG | Agrupa habilidades compatíveis com sua camada. |
| Asserção | Informação registrada com autoria humana e marca D, I ou V. |
| Entregável | Artefato condicionado por portão. |
| Evento | Registro append-only de transição, gravação, recusa ou selamento. |

### 3.2 Invariantes de carga do playbook

Um playbook é inválido se faltar qualquer condição abaixo:

1. toda etapa declara camada por nível e modalidade;
2. todo entregável declara portão;
3. existe lista não vazia de itens inegociáveis;
4. a taxonomia de procedência válida é D/I/V;
5. toda etapa recorrente declara cadência;
6. todo agente declara critério de verificação para as habilidades que executa;
7. etapa humana não expõe comando que a conclua por agente.

### 3.3 Cobertura obrigatória

O playbook completo contém: **F0, P1, P2, P3a, P3b, P3d, P4, P5, P6, P7, P8, P9 e P10**. Nenhuma fase pode ser omitida na versão da PoC.

| Fase | Etapas | Entregável/portão |
|---|---|---|
| F0 | F0 | E1 |
| F1 | P1, P2, P3a, P3b, P3d | E2 |
| F2 | P4, P5 | E3-D / E3-E |
| F3 | P6, P7 | E4 |
| F4 | P8, P9, P10 | E5 |

### 3.4 Catálogo de agentes e habilidades

| Agente | Camada | Habilidades |
|---|---|---|
| AG-01 — Enquadramento | EX1 | HB-01 a HB-05 |
| AG-02 — Análise documental | EX2 | HB-06 a HB-10, HB-13 |
| AG-03 — Especificação | EX2 | HB-11, HB-12, HB-14 |
| AG-04 — Avaliação | EX2 | HB-15 a HB-18 |

Os códigos HB e AG são obrigatórios na implementação. Nenhuma skill de produção existe sem código, insumo, saída e critério de verificação rastreáveis ao EMCIA-CAT-01.

### 3.5 Restrições humanas fixas

**P3b — levantamento de regras não documentadas.** Presencial, EX4 e sem comando de conclusão por agente. O Code Plugin pode registrar a sessão, organizar rascunhos e receber o produto verificado.

**P7 — definição de autonomia.** O agente pode produzir a minuta HB-14, mas não decide as três listas nem os limites. O fechamento exige decisão humana registrada; tentativa de decisão por agente é recusada.

**P10 — recalibragem.** É recorrente. O agente pode monitorar desvio por HB-18, mas a decisão de recalibrar, expandir ou descontinuar é humana. O estado registra cadência, responsável e última verificação.

### 3.6 Procedência D/I/V e escrita

| Marca | Significado | Regra mínima |
|---|---|---|
| D — declarada | Informação fornecida pela organização. | Autor e data registrados; permanece D até verificação. |
| I — inferida | Dedução de pessoa ou ferramenta a partir de outras informações. | Premissa explícita; não avança para diagnóstico sem confirmação. |
| V — verificada | Confirmada por observação, documento-fonte ou leitura de volta. | Evidência e responsável identificados. |

Regras de escrita:

- escrita direta em `caso/` e `registro/` é recusada;
- toda asserção tem autor pessoa nomeada; agente não é autor;
- toda asserção tem D, I ou V;
- informação I exige premissa;
- V exige registro da evidência que sustentou a verificação;
- recusa sempre emite evento; falha silenciosa é defeito.

### 3.7 Estado e transições

| Transição | Pré-condição | Resultado |
|---|---|---|
| Abrir caso | playbook válido | Caso em F0; versão do playbook congelada. |
| Encerrar F0 | triagem válida e nível apurado | Nível passa a governar as etapas seguintes. |
| Registrar sessão | atividade humana realizada e responsável nomeado | Dependências humanas podem ser satisfeitas. |
| Encerrar etapa | critério + dependências atendidos | Estado avança. |
| Autorizar entregável | portão + inegociáveis satisfeitos | Documento pode ser gerado. |
| Registrar recorrência | etapa recorrente com cadência, responsável e data | Estado atualiza última verificação sem apagar histórico. |
| Selar braço declarado | percurso declarado encerrado antes do campo | Conteúdo fica imutável para comparação. |

### 3.8 Portões de entregáveis

| Entregável | Portão mínimo | Regra especial |
|---|---|---|
| E1 — Ficha de enquadramento | F0 encerrada | Nível registrado. |
| E2 — Diagnóstico e oportunidade | P1, P2, P3a, P3b e P3d encerrados | Linha de base registrada; regras com autoria e D/I/V. |
| E3-D — Decisão | P4 e P5 encerrados | Existe sempre. |
| E3-E — Especificação | P5 classificou ao menos um caso como agente | Não emite quando nenhum caso é agêntico. |
| E4 — Guia operacional | P6 e P7 encerrados | Termo de autonomia é inegociável 2. |
| E5 — Relatório de piloto | P8, P9 e P10 especificados/encerrados conforme PoC | Exige inegociáveis 3, 4 e 5. |

### 3.9 Cinco inegociáveis como condição de máquina

| # | Regra executável |
|---:|---|
| 1 | E2 não fecha sem linha de base registrada antes do piloto. |
| 2 | E4 não emite sem termo de autonomia com faz sozinho / exige aprovação / nunca faz. |
| 3 | E5 não emite sem casos de teste com saída esperada. |
| 4 | E5 não emite se não houver ao menos uma métrica de resultado. |
| 5 | E5 não emite sem pessoa nomeada responsável pela recalibragem. |

### 3.10 Guardas mínimas

| ID | Regra | O que impede |
|---|---|---|
| G1 | Skill de camada humana não carrega para agente. | Automação de EX3/EX4. |
| G2 | Escrita direta em `caso/` e `registro/` é negada. | Bypass do validador e da procedência. |
| G3 | Etapa dependente de sessão exige sessão registrada. | Confronto ou decisão humana fictícios. |
| G4 | Nenhuma etapa após F0 opera sem nível. | Fronteira indefinida. |
| G5 | Etapa recorrente exige cadência. | P10 invisível após primeira execução. |
| G6 | Agente exige critério de verificação. | Skill que produz saída sem regra de conferência. |

### 3.11 Eventos mínimos

`CasoAberto`, `AssercaoGravada`, `AssercaoRecusada`, `TentativaNegada`, `SessaoRegistrada`, `EtapaEncerrada`, `EntregavelAutorizado`, `DocumentoGerado`, `RecorrenciaRegistrada` e `CasoSelado`.

### 3.12 Testes do percurso completo

Os testes existentes são preservados. A ampliação F0–P10 adiciona, no mínimo:

| # | Prova | Esperado |
|---:|---|---|
| 14 | Emitir E4 sem termo de autonomia | Recusa e estado inalterado. |
| 15 | Caso de teste sem saída esperada | Não satisfaz P8/E5. |
| 16 | E5 com métricas apenas de uso | Recusa. |
| 17 | Responsável pela recalibragem = nome de área | Recusa. |
| 18 | Agente tenta concluir P7 | Recusa + `TentativaNegada`. |
| 19 | P10 sem cadência | Playbook não carrega. |
| 20 | Agente sem critério de verificação | Playbook não carrega. |

### 3.13 Comportamento conservador

Ausência ou ambiguidade nunca resolve para o modo mais permissivo. Sem nível, nenhuma etapa pós-F0 opera; sem procedência, não se grava; sem sessão humana, não se encerra; sem inegociável, não se emite; sem cadência, P10 não carrega; sem critério de verificação, agente não carrega.

## 4. Condição de aceite

Este artefato está pronto quando um implementador consegue derivar schemas, validadores, guardas, estado e testes para as treze etapas F0–P10 sem inventar regra metodológica; quando os quatro agentes e as dezoito habilidades possuem códigos oficiais; quando P3b, P7 e P10 preservam a responsabilidade humana; quando D/I/V é a única taxonomia documental de procedência desta versão; e quando os cinco inegociáveis condicionam de fato os portões E2, E4 e E5.

## 5. Referências

- EMCIA-ARQ-01 — Arquitetura do Estúdio de Trabalho.
- EMCIA-IMP-01 — Plano de implementação do Estúdio de Trabalho.
- EMCIA-MET-01 — Documento do método.
- EMCIA-CAT-01 — Fronteira de delegação e catálogo de agentes e habilidades.
- EMCIA-TRI-01 — Instrumento de triagem.
- EMCIA-VER-01 — Plano de verificação.
- EMCIA-GLO-01 — Glossário do método.
- Plano — do percurso parcial ao percurso completo (documento interno, setembro de 2026).

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
|---|---|---|---|---|
| 0.1 | 17/09/2026 | Celso do Vale | Contratos iniciais do Estúdio. | — |
| 0.2 | 17/09/2026 | Celso do Vale | Contrato ampliado para F0–P10; D/I/V fixado; portões E4/E5, recorrência e testes 14–20 adicionados. | — |
