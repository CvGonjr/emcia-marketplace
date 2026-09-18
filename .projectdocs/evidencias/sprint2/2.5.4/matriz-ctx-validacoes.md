# Matriz CTX-V01–CTX-V11 — pacote 2.5.4

Extração literal de EMCIA-CTX-01 v0.4, §3.13 — "Condições executáveis para
o Code Plugin". Nenhum valor abaixo foi inferido deste prompt; a coluna
"Regra oficial" reproduz o texto do documento.

| ID | Regra oficial | Objeto(s) afetado(s) | Condição de aceite | Condição de recusa | Dependência | Implementação atual | Estado inicial |
|---|---|---|---|---|---|---|---|
| CTX-V01 | Regra possui os sete campos do bloco de decisão. | Regra | Os sete campos (`determinismo`, `frequencia`, `consequencia_do_erro`, `decisor_quando_nao_cobre`, `entradas`, `excecoes_conhecidas`, `estabilidade`) presentes e, conforme aplicável, não vazios. | Falta qualquer um dos sete campos. | Nenhuma. | `contexto.schema.json` (`required`/`nonempty` da Regra), verificado por `estrutura.validar()` dentro de `curar.py`. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.1) |
| CTX-V02 | Registro I possui premissa escrita. | Termo, Entidade, Regra, Fonte | `procedencia: I` com `premissa` não vazia. | `procedencia: I` com `premissa` vazia/ausente. | Nenhuma. | `contexto.schema.json` (`conditional_nonempty.I`), verificado por `estrutura.validar()`. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.0/2.5.1) |
| CTX-V03 | Registro V possui evidência identificada. | Termo, Entidade, Regra, Fonte | `procedencia: V` com `evidencia` não vazia. | `procedencia: V` com `evidencia` vazia/ausente. | Nenhuma. | `contexto.schema.json` (`conditional_nonempty.V`), verificado por `estrutura.validar()`. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.0/2.5.1) |
| CTX-V04 | Mudança I → V cria nova versão. | Objetos com `versao`/`historico` (Regra) | Candidato com `procedencia` I→V possui `versao` maior que a versão curada anterior. | Candidato tenta gravar `procedencia` I→V mantendo a mesma `versao` (sobrescrita). | Registro anterior já curado. | `checar_versao()` em `curar.py`, mensagem prefixada `CTX-V04` quando a transição é I→V; recusa também retrocesso de versão. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.2) |
| CTX-V05 | Todo termo referenciado existe. | Regra (`entradas`) | Todo id com prefixo `T-` em `entradas` resolve para `contexto/termos/<id>.yaml` existente. | Id com prefixo `T-` em `entradas` sem arquivo correspondente. | `catalogo_referencias`/`references` no schema. | `checar_referencias()` em `curar.py` (novo neste pacote). | **AUSENTE** |
| CTX-V06 | Toda entidade referenciada existe. | Regra (`entradas`) | Todo id com prefixo `E-` em `entradas` resolve para `contexto/entidades/<id>.yaml` existente. | Id com prefixo `E-` em `entradas` sem arquivo correspondente. | `catalogo_referencias`/`references` no schema. | `checar_referencias()` em `curar.py` (novo neste pacote). | **AUSENTE** |
| CTX-V07 | Toda fonte referenciada existe e possui contrato mínimo. | Regra (`entradas`), Entidade (`onde_vive`) | Todo id com prefixo `F-` resolve para `contexto/fontes/<id>.yaml` existente **e** esse arquivo passa na validação estrutural de Fonte (`contrato.estrutura`/`significado`/`qualidade` preenchidos). | Id com prefixo `F-` sem arquivo correspondente, ou arquivo existente porém sem contrato mínimo válido. | `catalogo_referencias`/`references` no schema; reaproveita `estrutura.validar()` sobre o objeto Fonte resolvido. | `checar_referencias()` em `curar.py` (novo neste pacote). Distingue explicitamente arquivo físico em `fontes/` de objeto Fonte CTX curado — só o segundo satisfaz a referência. | **AUSENTE** |
| CTX-V08 | Escrita em `contexto/` passa pela curadoria prevista. | Todos os objetos CTX | Gravação em `contexto/` ocorre via `curar.py`. | `Write`/`Edit`/redirecionamento de shell grava diretamente em `contexto/`, sem passar por `curar.py`. | Nenhuma. | `guarda.py` G2b (hook `PreToolUse`), bloqueia com `exit 2`. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.2) |
| CTX-V09 | Autoria de conteúdo e registro são pessoas nomeadas. | Todos os objetos CTX (campos que declararem `autoria_conteudo`/`declarado_por`/`registrado_por`/`autor`) | Todos os campos de autoria presentes contêm nome de pessoa. | Qualquer campo de autoria contém identificador reconhecido como agente pela convenção lexical (`ag0*`, `agente*`, `sistema*`, tolerante a hífen/espaço/underscore). | `estado.autor_e_agente()`. | `checar_autoria()` em `curar.py`, mensagem prefixada `CTX-V09`; também verificado para `--registrado-por` da linha de comando. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.2) |
| CTX-V10 | Toda nova versão possui data, responsável e motivo da mudança. | Objetos com `versao`/`historico` (Regra) | A entrada de `historico` referente à versão anterior contém `versao`, `data` e responsável (`registrado_por` ou `confirmado_por`). | Entrada de `historico` incompleta, ou ausente quando a mudança é relevante (procedência ou classificação de confronto). | Registro anterior já curado; mudança relevante detectada. | `checar_versao()` em `curar.py`, mensagens prefixadas `CTX-V10`. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.2) |
| CTX-V11 | Toda `classificacao_confronto` possui `classe` e `referencia_p3d`; quando a classe é `divergente`, a referência resolve para registro de P3d com `documento_diz`, `observado` e `justificativa`. | Regra | `classe` pertence à taxonomia oficial (EMCIA-ROT-01 3.9); quando `classe: divergente`, `referencia_p3d` aponta para `contexto/divergencias/<id>.yaml` existente (cujo schema já exige `documento_diz`/`observado`/`justificativa`). | `classe` fora da taxonomia; `classe: divergente` sem `referencia_p3d`; `referencia_p3d` que não resolve. | Registro de divergência (`contexto/divergencias/`) curado quando aplicável. | `checar_confronto()` em `curar.py`, mensagens prefixadas `CTX-V11`; enum de `classe` em `contexto.schema.json`. | JÁ IMPLEMENTADO E CONFORME (desde 2.5.3) |

## Síntese

| Estado inicial (ao abrir o 2.5.4) | Quantidade |
|---|---:|
| JÁ IMPLEMENTADO E CONFORME (formalizado neste pacote com código CTX-Vxx nas mensagens/eventos, sem reescrever lógica) | 8 (V01, V02, V03, V04, V08, V09, V10, V11) |
| AUSENTE (implementado neste pacote) | 3 (V05, V06, V07) |

Nenhuma CTX-V foi contabilizada apenas por constar no documento — todas as
onze têm teste negativo e controle positivo executados e persistidos (ver
`CTX-Vxx-negativo.txt`/`CTX-Vxx-positivo.txt` neste diretório).

## Resultado dos testes

| CTX-V | Regra oficial (resumo) | Negativo | Positivo | Resultado |
|---|---|---|---|---|
| CTX-V01 | Sete campos do bloco de decisão | PASS | PASS | CONFORME |
| CTX-V02 | I exige premissa | PASS | PASS | CONFORME |
| CTX-V03 | V exige evidência | PASS | PASS | CONFORME |
| CTX-V04 | I→V cria nova versão | PASS | PASS | CONFORME |
| CTX-V05 | Termo referenciado existe | PASS | PASS | CONFORME |
| CTX-V06 | Entidade referenciada existe | PASS | PASS | CONFORME |
| CTX-V07 | Fonte referenciada existe e tem contrato mínimo | PASS | PASS | CONFORME |
| CTX-V08 | Escrita em `contexto/` passa pela curadoria | PASS | PASS | CONFORME |
| CTX-V09 | Autoria é pessoa nomeada | PASS | PASS | CONFORME |
| CTX-V10 | Nova versão tem data/responsável/motivo | PASS | PASS | CONFORME |
| CTX-V11 | Classificação de confronto completa e resolvível | PASS | PASS | CONFORME |

**11/11 CONFORME.**

## Decisão sobre ordem de validação (§21 da instrução do pacote)

`curar.py` já acumulava erros de múltiplas verificações antes deste pacote
(schema, autoria, confronto, versão); este pacote manteve essa política ao
adicionar `checar_referencias()` — todas as violações de um mesmo objeto
são coletadas na mesma lista `erros` e reportadas juntas, não apenas a
primeira encontrada. O teste `2.5.4-multi` demonstra isso com `I` sem
premissa e Fonte inexistente no mesmo objeto: a recusa contém as duas
causas. Não há dependência da ordem de iteração de arquivos ou diretórios
— cada checagem opera sobre os dados já carregados do candidato, na ordem
fixa em que `curar()` as chama (`estrutura.validar` → `checar_autoria` →
`checar_confronto` → `checar_referencias` → `checar_versao`).
