# Sprint 3 — Pacote 3.1 — congelamento da versão

## 1. Identificação

HEAD inicial: `74aa886f19a9e86601183fbd88897f7a8fe6d518`
Data: 23/09/2026
Escopo: (1) trava do selo do estado declarado — P3b exige selo posterior
ao encerramento de P2; (2) regra documental do material público da etapa
0a; (3) documentação desatualizada (INSTALACAO.md, README.md, gates.md,
CTX-01 §184, `.projectdocs/map.md`).

## 2. Premissa reconciliada antes de implementar

O prompt original assumia que "a execução de contraste foi retirada do
projeto" e que a verificação por estados já era o modelo vigente. O
repositório, no HEAD inicial, mostrava o oposto: decisões 014–020
(21–22/09/2026, todas "firme") estabeleciam que a execução de contraste
era um plugin/repositório completamente separado (`emcia-contraste`),
com travas de isolamento em `eiac-nucleo` desenhadas para impedir que
dado de contraste entrasse num caso de campo.

Antes de tocar em código, essa divergência foi levada ao usuário. A
resposta confirmou o objetivo do prompt (retirar a execução de contraste,
adotar verificação por estados do caso) e definiu explicitamente:

1. A comparação declarado × verificado é interna ao caso de campo, entre
   o estado selado ao fim de P2 e o estado após P3b/P3d — conceito novo,
   não reaproveita vocabulário nem código do contraste.
2. Criar a decisão 021, marcando 004 e 014–020 como substituídas por ela
   (019 só na parte específica de execução de contraste — a regra geral
   de autoria por responsável permanece firme).
3. O aparato de isolamento núcleo × contraste em `guarda.py`/`selar.py`
   permanece no código nesta rodada — não conflita com a trava nova —,
   listado aqui como candidato a remoção em decisão futura.
4. Numeração 021 no lugar do 014 que o prompt original citava.
5. Ao final, além da tag, `git push` para `origin/master`.

## 3. Pendência 1 — trava do selo do estado declarado

### 3.1 Mecanismo

`eiac-campo/template-caso/registro/playbook.json` (v0.4.1 → v0.4.2):
P3b ganhou `"exige_selo_apos": "P2"`, campo genérico — o núcleo não sabe
o que "P2" ou "P3b" significam.

`eiac-nucleo/scripts/estado.py`: nova função `eventos()`, lê
`registro/eventos.jsonl` inteiro (linha ilegível é pulada, não
interrompe a leitura).

`eiac-nucleo/scripts/playbook.py`: nova função `selo_apos_etapa(pb,
etapa_id, trilha)`. Lê `exige_selo_apos` da etapa, localiza a última
posição de `EtapaEncerrada` para a etapa referenciada e verifica se
existe `SeloAplicado` em posição posterior na trilha. **"Posterior" é
definido por posição na lista de eventos, não por timestamp** — achado
descrito na seção 6.

`eiac-nucleo/scripts/guarda.py`: nova regra **G7**, aplicada no mesmo
loop que já detecta a habilidade de uma etapa pelo `alvo` (arquivo lido).
Bloqueia a abertura (carregamento da skill) com evento `TentativaNegada`.

`eiac-nucleo/scripts/avancar.py::encerrar()`: mesma checagem, bloqueia o
fechamento com `RecusaMaquina` (convenção já existente do script — a
trava de abertura usa `TentativaNegada` porque vive em `guarda.py`, a de
fechamento usa o padrão de `avancar.py`, ambas com mensagem nomeando
exatamente qual selo falta).

### 3.2 Testes — negativos primeiro

`testes/verificacao_por_estados.py` (novo, 7 verificações):

| Teste | Cenário | Resultado esperado |
|---|---|---|
| T01 | P3b sem selo algum após P2 | Recusa na abertura (guarda, `TentativaNegada`) |
| T02 | P3b sem selo algum após P2 | Recusa no fechamento (avancar, `RecusaMaquina`) |
| T03 | Selo aplicado **antes** do encerramento de P2 | Recusa (selo existe, mas não é posterior) |
| T04 | Selo aplicado **depois** do encerramento de P2 | Abre e encerra normalmente (controle positivo) |
| T05 | Etapa sem `exige_selo_apos` (P1) | Não afetada |
| T06 | Busca por "antitese"/"contraste" em `playbook.py` | Ausente — mecanismo genérico |

Todos os seis pares/controles passam. Os quatro primeiros formam os dois
pares negativo/positivo exigidos pelo prompt (sem selo / com selo
posterior; selo anterior / selo posterior).

### 3.3 Regressão causada e corrigida

A trava nova quebrou quatro suítes pré-existentes que constroem
percursos F0→P3b (ou além) sem selar após P2 — comportamento que nunca
foi exigido antes desta pendência:

- `testes/nucleo_2_6_1.py`: 8 falhas (T04, T07, T11–T14, T17, T20c)
- `testes/campo_2_6_3.py`: 1 falha (regressão de suíte completa)
- `testes/campo_2_6_5.py`: 18 falhas
- `testes/campo_2_6_6.py`: 4 falhas

Corrigido adicionando setup de repositório git + `responsavel` a
`preparar_caso()` (onde faltava) e uma função `selar()` a cada um dos
quatro arquivos, chamada logo após o encerramento de P2 nos percursos
que alcançam P3b — via o helper compartilhado `percorrer_ate()` nos três
arquivos que o têm (`nucleo_2_6_1.py`, `campo_2_6_3.py`,
`campo_2_6_5.py`, generalizado para não assumir que a etapa exigente é a
próxima imediata da referenciada — P3a se intercala entre P2 e P3b), e
inline nos dois pontos de `campo_2_6_6.py` que constroem o percurso à
mão.

Nenhuma dessas correções alterou o que cada teste verifica — só a
sequência de comandos que produz o estado necessário para verificá-lo.

## 4. Pendência 2 — material público da etapa 0a

Regra documental adicionada em `README.md` ("Material público da etapa
0a") e `INSTALACAO.md` (passo 5): o levantamento público sobre a
organização e o setor (etapa 0a de EMCIA-HAB-01, anterior a F0) não
entra no caso automaticamente — é coletado fora do repositório e só é
gravado depois da abertura (etapa 0d), com marca `I · tipo_fonte:
externa`, URL e limite da fonte explícitos, no formato já definido por
`eiac-campo/reference/procedencia.md`. Nenhum código foi criado — é
regra de processo, não trava.

## 5. Pendência 3 — documentação desatualizada

- `README.md`: reescrito. Percurso de 13 etapas (era de 8, com P3b "sem
  comando"), procedência no formato D/I/V de `procedencia.md` (era
  descrição solta), portões E1–E5 fixados (era "pendência aberta,
  `portao_pendente: true`"), repositório público
  `CvGonjr/emcia-marketplace`, seção nova "Verificação por estados do
  caso", seção nova "Material público da etapa 0a", removida menção a
  "P6 a P10 não têm habilidade".
- `INSTALACAO.md`: reescrito. Clone do repositório público em vez de
  descompactar zip, `novo-caso.sh --responsavel` (obrigatório desde a
  decisão 019, o guia antigo não mencionava), oito testes negativos (era
  sete — acrescido o teste do selo de P3b), tabela "O que ainda não
  existe" atualizada (a antiga listava "habilidades de P6-P10 ausentes"
  e "geração de documento ausente", ambos resolvidos há duas sprints).
- `eiac-campo/reference/gates.md`: linha "Quadro de Contraste | Sprint 4
  | Anexo do relatório" → "Quadro de Confronto (declarado × verificado)
  | P2 (selo) → P3b/P3d | Anexo do relatório".
- `CTX-01-instrumento-camada-contexto.md` (raiz e
  `eiac-campo/reference/`, mantidas idênticas): linha 184 — "a previsão
  é que o braço da antítese produza a célula crítica vazia" → "a
  previsão é que a célula crítica esteja vazia no estado declarado
  selado", com a explicação de que isso ocorre ao fim de P2, antes do
  levantamento presencial de P3b.
- `.projectdocs/map.md`: reescrito por completo. O arquivo anterior
  retratava o estado do repositório em 12/09/2026 (6 commits, 8 etapas,
  13 skills) — defasado em duas Ações inteiras (2.5 e 2.6) e 15 decisões
  (007–021). Nova versão reflete playbook v0.4.2, 13 etapas, 18 HB, 21
  decisões, a verificação por estados do caso e a situação real do
  aparato de isolamento núcleo × contraste (mantido, candidato a
  remoção).

## 6. Defeito encontrado e corrigido durante a implementação

`playbook.py::selo_apos_etapa()` comparava inicialmente por `data`
(timestamp ISO com precisão de segundo). Em qualquer percurso rápido —
inclusive o próprio teste automatizado — vários eventos caem no mesmo
segundo, e `SeloAplicado` não era reconhecido como posterior a
`EtapaEncerrada` de P2 mesmo quando vinha depois na trilha real. Achado
durante a primeira execução de `testes/verificacao_por_estados.py::T04`
(controle positivo), antes de qualquer commit. Corrigido comparando
**posição na lista de eventos** em vez de timestamp — a trilha é
sequencial por construção (uma linha por `estado.evento()`, nunca
reordenada), então a posição é um ordenador confiável onde o timestamp
não é.

Nenhum outro defeito de produção pré-existente foi encontrado.

## 7. Regressão

Inicial (HEAD `74aa886`, antes de qualquer mudança): **484 verificações,
0 falhas** (`teste-regressao-inicial.txt`).

Final (após as três pendências): **491 verificações, 0 falhas**
(`teste-regressao-final.txt`) — os 7 testes novos de
`verificacao_por_estados.py`, nenhuma mudança de contagem nas demais
suítes (as quatro que quebraram foram corrigidas para o mesmo número de
verificações que tinham antes).

## 8. Commits

Três commits separados, por pendência:

1. `feat(nucleo+campo): require case seal after P2 to open/close P3b` —
   pendência 1 (trava + testes + correções de regressão nas 4 suítes
   afetadas).
2. `docs: document 0a public material rule` — pendência 2.
3. `docs: rewrite stale docs after removing contraste execution` —
   pendência 3.
4. `docs(evidence): register sprint3 package 3.2` — este diretório de
   evidência.

Hashes reais em `git-show.txt`.

## 9. Tag

`v-sprint3-freeze`, criada após o commit de evidência, aponta para o
HEAD que o engenheiro deve instalar. Hash em `git-show.txt`.

## 10. Push

`git push origin master` executado após a tag, por instrução explícita
do usuário — o GitHub estava atrás do repositório local e o engenheiro
instala a partir de lá.

## 11. Situação das decisões tocadas

| Decisão | Estado final |
|---|---|
| 004 | substituída por 021 |
| 014 | substituída por 021 |
| 015 | parcialmente superada por 018 (inalterado); parte de execução de contraste substituída por 021 |
| 016 | substituída por 021 |
| 017 | substituída por 021 |
| 018 | substituída por 021 (aparato de isolamento mantido no código, não removido) |
| 019 | firme (regra geral de autoria); parte de execução de contraste substituída por 021 |
| 020 | pendente de decisão de método (inalterado quanto ao cruzamento CAT-01); menção à execução de contraste substituída por 021 |
| **021** | **firme (nova)** |

## 12. Itens explicitamente não resolvidos nesta rodada

- Remoção do aparato de isolamento núcleo × contraste em
  `guarda.py`/`selar.py` — mantido por instrução explícita, listado como
  candidato a decisão futura.
- Pendência 020 (cruzamento CAT-01 Anexo A × catálogo × playbook) —
  continua aberta, não é objeto deste pacote.
- Repositórios irmãos `emcia-contraste`/`emcia` (diretórios de trabalho
  adicionais desta sessão) — não foram tocados; nenhuma referência deste
  pacote presume sua existência ou remoção.

## 13. Estado final

**CONFORME** quanto ao escopo das três pendências descritas no prompt.
Working tree limpa, suíte completa verde, decisões e documentação
reconciliadas com o código.
