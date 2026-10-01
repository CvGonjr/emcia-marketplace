# Manual de aplicação do método
### Ordem de leitura, percurso e atos do engenheiro de campo

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-MAN-01 | **Versão** | 0.1 |
| **Data** | 01/10/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Todas | **Passo** | Todos |

---

## 1. Objetivo
Permitir que um engenheiro de campo que não participou da construção do método o aplique com o Estúdio, na ordem de uso, sabendo em cada etapa o que o agente prepara, o que só ele decide e o que encerra a etapa.

## 2. Escopo e aplicação
Aplica-se a quem conduz um caso. Pressupõe a leitura do EMCIA-MET-01. Não se aplica à manutenção do Estúdio, que segue o EMCIA-ESP-01, o EMCIA-ARQ-01 e o EMCIA-IMP-01. Substitui o Guia do Engenheiro de Campo de setembro de 2026, que descrevia a versão 0.3.0 do playbook.

## 3. Conteúdo

### 3.1 Ordem de leitura

| Momento | Documento | Para quê |
| :--- | :--- | :--- |
| Antes do primeiro caso | EMCIA-MET-01 | O percurso, os inegociáveis e as regras do método |
| Antes do primeiro caso | EMCIA-CAT-01 | O que o agente pode fazer e o que é do engenheiro |
| Antes do primeiro caso | EMCIA-TRI-01 | Como o nível do caso é apurado |
| Durante o caso | EMCIA-CAM-01 | O protocolo de cada passo em campo |
| Durante o caso | EMCIA-TRA-01 | Procedência, pendências e validações transversais |
| Durante o caso | EMCIA-ROT-01 | O levantamento presencial das regras não documentadas |
| Durante o caso | EMCIA-CTX-01 | O registro da camada de contexto |
| Durante o caso | EMCIA-E1 a EMCIA-E5 | Os modelos dos entregáveis |
| Quando surgir dúvida de termo | EMCIA-GLO-01 | Definições do método |
| Não usar como critério | EMCIA-VER-01 | Plano substituído, mantido como registro |

### 3.2 Antes do caso
1. Conduza a habilitação do engajamento pelo EMCIA-HAB-01. Ela ocorre fora do Estúdio e antecede a abertura do caso.
2. Instale o Estúdio e rode os testes negativos, conforme o INSTALACAO.md do marketplace. Não abra caso real sem que todos tenham recusado com registro.
3. Abra o caso. Ele permanece na versão do método em que foi aberto (EMCIA-MET-01 §3.7.6).

### 3.3 O percurso
Para cada etapa: o comando que o agente executa, os atos que só o engenheiro executa, o produto que o Estúdio confere para encerrá-la e o entregável que ela alimenta. Atos marcados com níveis entre parênteses só são exigidos nesses níveis.

| Etapa | Camada N1 · N2 · N3 | Comando do agente | Ato do engenheiro | Produto conferido pelo Estúdio | Entregável |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F0 | EX1 · EX1 · EX1 | `/eiac-campo:enquadrar` | `apurar-nivel` | — | E1 |
| P1 | EX2 · EX2 · EX3 | `/eiac-campo:mapear-contexto` | `encerrar-camada-humana` (N3) | — | E2 |
| P2 | EX2 · EX2 · EX3 | `/eiac-campo:mapear-fontes` | `encerrar-camada-humana` (N3) | — | E2 |
| P3a | EX2 · EX3 · EX3 | `/eiac-campo:medir` | `registrar-sessao`, `encerrar-camada-humana` (N2, N3) | Linha de base registrada | E2 |
| P3b | EX4 · EX4 · EX4 | — | `registrar-sessao`, `encerrar-camada-humana` | — | E2 |
| P3d | EX3 · EX3 · EX3 | `/eiac-campo:confrontar` | `registrar-sessao`, `encerrar-camada-humana` | — | E2 |
| P4 | EX2 · EX3 · EX3 | `/eiac-campo:priorizar` | `encerrar-camada-humana` (N2, N3) | — | E3 |
| P5 | EX3 · EX3 · EX3 | `/eiac-campo:classificar` | `registrar-campo`, `encerrar-camada-humana` | Classificação tecnológica registrada | E3 |
| P6 | EX3 · EX3 · EX3 | `/eiac-campo:operacionalizar` | `validar-operacional`, `encerrar-camada-humana` | OP validado | E4 |
| P7 | EX4 · EX4 · EX4 | `/eiac-campo:governar` | `decidir-autonomia`, `encerrar-camada-humana` | AUT decidido | E4 |
| P8 | EX3 · EX3 · EX3 | `/eiac-campo:pilotar` | `revisar-piloto`, `encerrar-camada-humana` | Conjunto revisado | E5 |
| P9 | EX3 · EX3 · EX3 | `/eiac-campo:medir-valor` | `encerrar-camada-humana` | Métrica de resultado apurada | E5 |
| P10 | EX4 · EX4 · EX4 | `/eiac-campo:recalibrar` | `definir-rotina`, `decidir-recalibragem`, `registrar-recorrencia`, `encerrar-camada-humana` | Rotina com responsável e cadência | E5 |

P3b não tem comando, por desenho: o levantamento é presencial e não delegável, e segue o EMCIA-ROT-01. Em P10, o monitoramento opera em EX2 e a decisão em EX4. Os entregáveis são materializados com `/eiac-campo:emitir`, depois que todas as etapas do seu portão estiverem encerradas.

### 3.4 Atos transversais
Valem em qualquer etapa e são sempre do engenheiro: `registrar-sessao`, `satisfazer-inegociavel`, `satisfazer-inegociavel-campo` e `encerrar-camada-humana`. A selagem do caso também é ato do engenheiro, com autor nomeado.

### 3.5 Quando o Estúdio recusa
Uma recusa é a trava funcionando, e não um erro. Para cada recusa:
1. Leia o motivo na trilha do caso, em `registro/eventos.jsonl`. Recusa real deixa evento `TentativaNegada` com o motivo.
2. Se o motivo for uma decisão humana, peça ao agente o comando pronto e execute-o no seu próprio terminal, no diretório do caso, fora da sessão do agente. Informar o seu nome dentro da sessão do agente não basta: a trava reconhece a origem da chamada (EMCIA-CAT-01 §3.5.3).
3. Se o agente recusar sem que a trilha registre `TentativaNegada`, a recusa foi do modelo, e não da trava. Comportamento correto não é prova de verificação.
4. Consultas de ajuda também geram `TentativaNegada`. Ao contar recusas, leia o motivo de cada uma.

### 3.6 O que esta versão não faz por você
Estes pontos estão no método, mas o Estúdio ainda não os confere (EMCIA-ESP-01 §3.14). Até que confira, são tarefas do engenheiro:
1. Registrar no caso a decisão de prosseguimento em F0, a avaliação do patrocínio em P1, a verificação do dado em P2 e a decisão de prioridade em P4, também nos níveis N1 e N2.
2. Registrar o produto de F0, P1, P2, P3b, P3d e P4 antes de encerrá-las. O Estúdio confere nessas etapas o nível ou a sessão, mas não o produto.
3. Conferir de novo um inegociável já satisfeito quando o artefato ou o responsável mudar, antes de emitir.
4. Manter um único registro vigente de piloto, especificação operacional e termo de autonomia, em versões crescentes.
5. Não operar fora de um caso aberto: a guarda só confere o que ocorre dentro dele.

### 3.7 Quando algo não fizer sentido
O marketplace mantém em `decisoes/` o registro de cada decisão de construção, com contexto, decisão e consequência. Antes de propor mudança no que parecer burocracia, leia a decisão correspondente.

## 4. Condição de aceite
O manual está vigente enquanto a tabela da seção 3.3 coincidir com o playbook do Estúdio: mesmas etapas, mesmas camadas, comandos existentes e atos declarados. A coincidência é conferida por teste da suíte do marketplace; se o teste falhar, o manual está desatualizado e não deve ser usado.

## 5. Referências
EMCIA-MET-01, EMCIA-CAT-01, EMCIA-TRI-01, EMCIA-CAM-01, EMCIA-TRA-01, EMCIA-ROT-01, EMCIA-CTX-01, EMCIA-HAB-01, EMCIA-GLO-01, EMCIA-ESP-01, EMCIA-E1 a EMCIA-E5.

## 6. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| 0.1 | 01/10/2026 | Celso do Vale | Versão inicial, conferida contra o playbook 0.4.9 (ação 4.5); substitui o Guia do Engenheiro de Campo | — |
