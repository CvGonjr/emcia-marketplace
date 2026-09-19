# Matriz consolidada — Ação 2.5 (Camada de Contexto e Dados)

Levantamento produzido antes dos testes de fechamento, cruzando o estado
real do código em `HEAD_INICIAL_2.5.6 = 96d1886580b6a638ed3deff24d5328ca5ad964d1`
com o RTE-01 oficial (v0.7) e o `resultado.md` de cada pacote. Nenhum
estado abaixo foi presumido pelo número do pacote — cada linha foi
conferida contra o código ou o teste correspondente.

| Requisito | Pacote responsável | Implementação | Teste existente | Evidência | Estado atual |
|---|---|---|---|---|---|
| Contrato D/I/V | 2.5.0 | `contexto.schema.json` (`procedencia`), `curar.py`, `validar.py` | `negativos.sh` 2.5.0-T01–T08 | `.projectdocs/evidencias/sprint2/2.5.0/` | CONFORME |
| Termo | 2.5.1 | `contexto.schema.json.objetos.termo` | `contexto.py` 2.5.1-T01/T05 | `.projectdocs/evidencias/sprint2/2.5.1/` | CONFORME |
| Entidade | 2.5.1 | `contexto.schema.json.objetos.entidade` | `contexto.py` 2.5.1-T02/T06 | idem | CONFORME |
| Regra | 2.5.1 | `contexto.schema.json.objetos.regra` | `contexto.py` 2.5.1-T03/T07/T11 | idem | CONFORME |
| Fonte | 2.5.1 | `contexto.schema.json.objetos.fonte` | `contexto.py` 2.5.1-T04/T08 | idem | CONFORME |
| `autoria_conteudo` | 2.5.2 | `curar.py:checar_autoria()` | `curadoria.py` 2.5.2-T06/T07 | `.projectdocs/evidencias/sprint2/2.5.2/` | CONFORME |
| `registrado_por` (distinto de `autoria_conteudo`) | 2.5.2 | `curar.py:checar_autoria()` | `curadoria.py` 2.5.2-T08 | idem | CONFORME |
| Premissa obrigatória para `I` | 2.5.0/2.5.1 | `contexto.schema.json.conditional_nonempty.I` | `curadoria.py` 2.5.2-T02/T03 | idem | CONFORME |
| Evidência obrigatória para `V` | 2.5.0/2.5.1 | `contexto.schema.json.conditional_nonempty.V` | `curadoria.py` 2.5.2-T04/T05 | idem | CONFORME |
| Histórico (nova versão preserva anterior) | 2.5.2 | `curar.py:checar_versao()` | `curadoria.py` 2.5.2-T09/T10/T11 | idem | CONFORME |
| `I` → `V` sem sobrescrita | 2.5.2 | `curar.py:checar_versao()` (CTX-V04) | `curadoria.py` 2.5.2-T09/T10, `ctx_v.py` V04-N/P | `.projectdocs/evidencias/sprint2/{2.5.2,2.5.4}/` | CONFORME |
| Proteção de `contexto/` | 2.5.2 | `guarda.py` G2b (CTX-V08) | `curadoria.py` 2.5.2-T12/T13, `ctx_v.py` V08-N/P | idem | CONFORME |
| `rascunho/` não é contexto curado | 2.5.2 | Ausência de leitura direta de `rascunho/` fora de `curar.py`/`validar.py` | `curadoria.py` 2.5.2-T14, `integracao.py` 2.5.5-T01/T02 | `.projectdocs/evidencias/sprint2/{2.5.2,2.5.5}/` | CONFORME |
| P3d — classificação | 2.5.3 | `contexto.schema.json.objetos.regra.enums["classificacao_confronto.classe"]` | `p3d.py` 2.5.3-T01/T02 | `.projectdocs/evidencias/sprint2/2.5.3/` | CONFORME |
| `referencia_p3d` | 2.5.3 | `curar.py:checar_confronto()` (CTX-V11) | `p3d.py` 2.5.3-T03/T04/T05, `ctx_v.py` V11-N/P | `.projectdocs/evidencias/sprint2/{2.5.3,2.5.4}/` | CONFORME |
| CTX-V01–CTX-V11 | 2.5.4 | `curar.py` (todas as onze, ver `matriz-ctx-validacoes.md` do 2.5.4) | `ctx_v.py` 22 pares + 1 multi-violação | `.projectdocs/evidencias/sprint2/2.5.4/` | 11/11 CONFORME |
| Referência a Termo | 2.5.4 | `curar.py:checar_referencias()` (CTX-V05) | `ctx_v.py` V05-N/P | idem | CONFORME |
| Referência a Entidade | 2.5.4 | `curar.py:checar_referencias()` (CTX-V06) | `ctx_v.py` V06-N/P | idem | CONFORME |
| Referência a Fonte (com contrato mínimo) | 2.5.4 | `curar.py:checar_referencias()` (CTX-V07) | `ctx_v.py` V07-N/P | idem | CONFORME |
| P2 → CTX | 2.5.5 | `hb-extrair-regras`, `extrator-documental.md` → `rascunho/` → `curar.py` | `integracao.py` 2.5.5-T01/T03 | `.projectdocs/evidencias/sprint2/2.5.5/` | IMPLEMENTADO |
| P3a → CTX (vínculo, não objeto) | 2.5.5 | `hb-medir` (orientação de `evidencia.referencia`) | Não coberto por teste automatizado — decisão de método, ver §20 deste resultado.md | `.projectdocs/evidencias/sprint2/2.5.5/matriz-integracao.md` | PARCIAL (por decisão documentada, não lacuna) |
| P3b → CTX | 2.5.2/2.5.5 | `hb-levantar-regras` → `curar.py` | `integracao.py` 2.5.5-T04 | `.projectdocs/evidencias/sprint2/2.5.5/` | IMPLEMENTADO |
| P3d → CTX | 2.5.3/2.5.5 | `hb-confrontar` → `curar.py --tipo divergencia` | `integracao.py` 2.5.5-T05/T05b | idem | IMPLEMENTADO |
| CTX → P4 | 2.5.5 | `hb-priorizar` → `quadro.py` | `integracao.py` 2.5.5-T06/T07/T08 | idem | IMPLEMENTADO |
| CTX → P5 | 2.5.5 | `hb-classificar`, `classificador-tecnologico.md` → `consultar.py` | `integracao.py` 2.5.5-T09–T12 | idem | IMPLEMENTADO |
| Eventos de recusa/operação CTX | 2.5.2–2.5.5 | `estado.evento()`, chamado por `curar.py`, `guarda.py` G2b | Todos os testes acima verificam `eventos.jsonl` | Todos os diretórios de evidência 2.5.2–2.5.5 | CONFORME |

## Nota sobre P3a

O baseline (2.5-BL20/BL21) e a instrução do próprio pacote 2.5.5 (§10)
foram explícitos: "não forçar materialização CTX de toda medição". P3a
continua fora dos quatro objetos CTX por decisão de método documentada,
não por lacuna de implementação — CTX-01 não define um objeto de medição.
Isso é revalidado neste pacote (§7 abaixo), não tratado como pendência
nova.
