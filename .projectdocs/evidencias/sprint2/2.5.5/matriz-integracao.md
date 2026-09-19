# Matriz de integração P2/P3 → CTX → P4/P5 — pacote 2.5.5

Levantamento feito antes de qualquer alteração, sobre o estado real do
código (`eiac-campo/skills/`, `eiac-campo/commands/`, `eiac-campo/agents/`)
em `HEAD_INICIAL_2.5.5 = 2216feef1bece5cee01e3409631945ab1dd1fb93`.

**Achado geral:** nenhuma skill, comando ou agente de P2 a P5 referenciava
`curar.py` ou `contexto/` antes deste pacote. Todos escreviam/liam
exclusivamente `caso/*.md` (asserção livre via `validar.py`). CTX existia
como estrutura validável (2.5.1–2.5.4) mas nenhuma etapa a alimentava ou
consultava de fato — confirma D-06 e 2.5-BL20/BL21 no código, não só no
baseline documental.

| Etapa | Produz | Escreve/propõe em CTX | Consome CTX | Campos | Mecanismo atual | Lacuna | Ação |
|---|---|---|---|---|---|---|---|
| **P2** | `caso/P2-regras-candidatas.md`, `caso/P2-lacunas.md` (via `hb-extrair-regras`/`extrator-documental`) | Não | Não | — | `validar.py` grava só em `caso/`. Nenhum caminho para Regra/Termo/Entidade/Fonte candidata em `rascunho/`. | AUSENTE: P2 não tem caminho para propor objetos CTX estruturados (só prosa marcada). | Adicionar à skill/agente a orientação de também escrever candidata estruturada em `rascunho/`, curada por `curar.py` com `procedencia: I` — nunca automática, nunca V. |
| **P3a** | `caso/P3a-medicao.md` (via `hb-medir`), com `amostra`/`periodo` | Não | Não | — | Medição não é um dos quatro objetos CTX (CTX-01 não define esse objeto). | PARCIAL: quando uma medição sustenta uma Regra/Fonte `V`, não havia orientação de como a `evidencia.referencia` deveria apontar para ela de forma estável. | Não criar objeto CTX para medição (CTX-01 não define). Orientar `hb-medir` a produzir um identificador estável de amostra/medição que possa ser citado em `evidencia.referencia` de Regra/Fonte quando aplicável — vínculo rastreável, não materialização obrigatória. |
| **P3b** | `caso/P3b-sessao.md` (via `hb-levantar-regras`, EX4, não delegável) | Não (implicitamente, via ROT-01 3.8) | Não | — | CTX-01 3.8 já define a correspondência de campos ROT-01→CTX-01; `curar.py` já aceita Regra com `procedencia: I`/`V` desde 2.5.2. Faltava só a skill citar o caminho. | PARCIAL: caminho técnico existe desde 2.5.2, mas não estava referenciado na skill. | Adicionar à skill a orientação explícita: após a sessão, a Regra levantada é escrita em `rascunho/` e curada por `curar.py`, preservando a procedência real (nunca promovida a V automaticamente). |
| **P3d** | Registro de confronto | Sim, desde 2.5.3 | Não (é escrita, não leitura) | `classificacao_confronto`, `referencia_p3d`, registro `divergencia` | `curar.py --tipo divergencia`, `checar_confronto()` (2.5.3), `CTX-V11` (2.5.4) | Nenhuma — já implementado e testado nos pacotes 2.5.3/2.5.4. | Formalizar o vínculo na skill `hb-confrontar` (citar o comando). |
| **P4** | `caso/P4-priorizacao.md` (via `hb-priorizar`) | Não | **Parcialmente** — `quadro.py` já lê `contexto/regras/*.yaml` e produz a grade frequência×consequência (existe desde antes deste pacote, mas a skill de P4 nunca instruía usá-lo) | `frequencia`, `consequencia_do_erro`, presença dos sete campos centrais | `quadro.py` (script já existente, não tocado neste pacote) | PARCIAL: a ferramenta existia e já era genuinamente estrutural (não reinterpreta texto), mas a skill de P4 não instruía rodá-la nem citar os IDs de Regra na priorização. | Adicionar à skill a instrução de rodar `quadro.py` antes de priorizar e registrar os IDs de Regra (`RN-*`) que sustentam a decisão. |
| **P5** | `caso/P5-classificacao.md` (via `hb-classificar`/`classificador-tecnologico`) | Não | Não — o agente só tinha `Read, Grep`, nenhuma instrução de consultar CTX estruturado | Sete campos centrais da Regra; distinção D/I/V | Nenhum | AUSENTE: nenhum mecanismo de consulta estruturada; nenhuma distinção D/I/V na decisão. | Novo `eiac-nucleo/scripts/consultar.py`, leitor genérico e somente-leitura por id, expõe `procedencia` e os sete campos centrais. Skill/agente passam a consultar por esse caminho e a preservar o estatuto documental (D/I/V) na decisão — sem exigir V globalmente, só quando a decisão específica depender de conhecimento verificado. |

## Status por seta do fluxo

| Seta | Estado inicial | Estado após 2.5.5 |
|---|---|---|
| P2 → CTX | AUSENTE | IMPLEMENTADO (caminho real via `rascunho/` → `curar.py`, procedência I) |
| P3a → CTX | PARCIAL (sem vínculo rastreável) | PARCIAL, mantido por decisão de método — vínculo via `evidencia.referencia`, não objeto novo |
| P3b → CTX | PARCIAL (caminho técnico existia, não referenciado) | IMPLEMENTADO (skill referencia o caminho já existente) |
| P3d → CTX | IMPLEMENTADO (2.5.3/2.5.4) | IMPLEMENTADO (formalizado na skill) |
| CTX → P4 | PARCIAL (`quadro.py` existia, não instruído) | IMPLEMENTADO |
| CTX → P5 | AUSENTE | IMPLEMENTADO (`consultar.py` novo + skill/agente atualizados) |

Nenhuma seta foi contabilizada como implementada sem teste negativo e
controle positivo correspondente (ver `resultado.md` §9).
