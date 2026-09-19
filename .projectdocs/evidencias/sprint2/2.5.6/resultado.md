# Pacote 2.5.6 — Verificação consolidada da Camada de Contexto e Dados

## 1. Identificação

- **Ação:** 2.5 — Contexto e Dados
- **Pacote:** 2.5.6 (verificação, não implementação)
- **Data/hora:** 18/09/2026, execução única de verificação
- **Branch:** `master`
- **HEAD inicial:** `96d1886580b6a638ed3deff24d5328ca5ad964d1`
- **HEAD final:** ver `git-show.txt`

## 2. Documentos consultados

EMCIA-MET-01, EMCIA-CTX-01 v0.4, EMCIA-ROT-01, EMCIA-TRA-01,
EMCIA-TST-01, EMCIA-VER-01, EMCIA-ESP-01, EMCIA-E2, EMCIA-E3 — nenhuma
divergência documental nova encontrada além das já registradas nos
pacotes anteriores. RTE-01 oficial (v0.7) usado como fonte de
recuperação de baseline, defeitos e commits.

## 3. Estado dos pacotes anteriores

| Pacote | Estado registrado (RTE-01) | Estado revalidado neste pacote |
|---|---|---|
| 2.5.0 | CONFORME | CONFORME — `negativos.sh` 2.5.0-T01–T08 continuam PASS; C01 reexercita D/I/V sobre objeto novo |
| 2.5.1 | CONFORME | CONFORME — `contexto.py` continua 11/11 PASS; C02 reexercita os quatro objetos sobre caso novo |
| 2.5.2 | CONFORME | CONFORME — `curadoria.py` continua 17/17 PASS; C03/C04/C05/C06 reexercitam autoria, curadoria, bloqueio e versionamento |
| 2.5.3 | CONFORME | CONFORME — `p3d.py` continua 12/12 PASS; C07 reexercita a integração P3d sem duplicação |
| 2.5.4 | CONFORME (11/11 CTX-V) | CONFORME — `ctx_v.py` continua 23/23 PASS; C08 reexecuta 8 das 11 CTX-V sobre objetos novos, C09 reexercita as três de referência |
| 2.5.5 | CONFORME | CONFORME — `integracao.py` continua 17/17 PASS; C10–C14 reexercitam P2→CTX, P3→CTX, CTX→P4, CTX→P5 e não reinterpretação |

Todos os commits registrados no RTE-01 (`acf35f9`, `9217925`, `c9df31f`,
`323d153`, `e3d0bea`, `8420451`) foram confirmados presentes em
`git log` na ordem correta, sem reescrita de histórico.

## 4. Baseline S2-BL

Baseline preservado, não alterado por este pacote (26 testes, 26 PASS, 0
FAIL, no HEAD `9a54017411c20cf54ab3a28fa488678c945a34b1`). Ver §7 do
RTE-01 e a tabela comparativa em §21 deste documento.

## 5. Matriz consolidada

Ver `matriz-consolidada.md` — 28 linhas cobrindo D/I/V, os quatro
objetos, autoria, premissa/evidência, histórico, I→V, proteção de
`contexto/`, `rascunho/`, P3d, `referencia_p3d`, CTX-V01–V11, as três
referências, e as seis setas de integração P2/P3→CTX→P4/P5. Nenhuma
linha foi marcada CONFORME apenas pelo número do pacote — cada uma foi
conferida contra código ou teste.

## 6. Caso de controle

`CTX-TEST-2.5.6-001` — ver `caso-controle.md`. Caso novo, construído do
zero em `testes/consolidado.py`, sem reaproveitar estado residual de
nenhum teste anterior. Percorre P2→CTX→P3(b,d)→CTX→P4→P5 com uma Regra
central (`RN-100`) atravessando D → tentativa de sobrescrita recusada →
V(v2) → V(v3, divergente, referenciando P3d), além de quatro Termos com
D/I/V variados, uma Entidade, uma Fonte, oito Regras para reexecução das
CTX-V, e duas Divergências P3d.

## 7. D/I/V

`D` válida aceita; `I` sem premissa recusada, `I` com premissa aceita;
`V` sem evidência recusada, `V` com evidência aceita; valor fora do
contrato (`X`) recusado. **Resultado consolidado: D/I/V funcional e
inequívoco** (C01, PASS).

## 8. Quatro objetos

Termo, Entidade, Regra e Fonte válidos aceitos no mesmo caso; Termo
estruturalmente inválido (sem `significado`) recusado. Schemas atuais
(`contexto.schema.json` v0.2.0) correspondem ao CTX-01 v0.4 — confirmado
pela aceitação dos quatro objetos com todos os campos do documento (C02,
PASS).

## 9. Curadoria e autoria

`autoria_conteudo` ≠ `registrado_por` aceito; agente como
`autoria_conteudo` recusado (C03). Conteúdo em `rascunho/` isolado não é
contexto; curado pelo caminho autorizado, materializa objeto (C04).
Escrita direta em `contexto/` negada (`exit 2`); escrita pelo curador
aceita (C05).

## 10. Histórico I→V

Sobrescrita de versão sem histórico recusada; nova versão com histórico
da anterior aceita; versão anterior permanece recuperável dentro do
registro atual (C06). Confirmado sobre o mesmo objeto que já vinha de
C02 (`RN-100`, `D`, versão 1) — não um objeto artificialmente pré-criado
só para este teste, e sim a continuação real do percurso do caso de
controle.

## 11. P3d

Registro de divergência curado e referenciado pela Regra via
`classificacao_confronto.referencia_p3d`, sem duplicar `documento_diz`,
`observado` ou `justificativa` no objeto Regra (C07, confirmado por
inspeção literal do conteúdo do arquivo curado).

## 12. CTX-V01–CTX-V11

Reexecutadas neste pacote, não apenas herdadas do 2.5.4: oito cenários
de violação (CTX-V01, V02, V03, V05, V06, V07, V09, V11) construídos
sobre objetos novos do caso de controle, todos recusados (C08). As três
restantes (V04, V08, V10) demonstradas nos testes C05/C06/C07 do mesmo
caso.

**Resultado: 11 / 11 conformes**, com negativo e positivo comprovados
para cada uma — soma da bateria formal do 2.5.4 (`ctx_v.py`, 22
pares) com a reexecução parcial deste pacote (C08/C09).

## 13. Verificação referencial

Referência válida a Termo, Entidade e Fonte aceita no mesmo teste;
referência a cada tipo inexistente recusada isoladamente (C09) — Termo
inexistente, Entidade inexistente e Fonte inexistente cada um produz
recusa `CTX-Vxx` específica, não uma mensagem genérica.

## 14. Integração P2/P3 → CTX

**P2:** candidato de Termo escrito em `rascunho/T-200.yaml`
(`procedencia: I`, premissa citando "manual, página 7"); confirmado que
não é contexto até curadoria explícita; curado com sucesso (C10).

**P3b:** Regra levantada com `procedencia: I`, referenciando Termo
existente (C11, primeira metade).

**P3d:** confronto atualiza a mesma Regra para `V`, versão 2, com
`referencia_p3d` resolvendo para registro de divergência curado,
histórico da versão 1 preservado (C11, segunda metade).

## 15. Integração CTX → P4/P5

**P4:** `quadro.py` executado sobre `contexto/regras/` do caso de
controle (contendo `RN-100` e as demais Regras curadas ao longo dos
testes), `exit 0` (C12).

**P5:** `consultar.py --id RN-100` retorna exatamente os sete campos
centrais do CTX-01 §3.6 e `procedencia: V` como dado estruturado (C13).

## 16. Não reinterpretação

Reverificado sobre o mesmo mecanismo do 2.5.5: `quadro.py` lê
`r.get("frequencia")`/`r.get("consequencia_do_erro")` diretamente do
dicionário resultante do parse YAML — confirmado por inspeção do
código-fonte, não por alegação — e nenhuma chamada a modelo de
linguagem existe em `quadro.py` ou `consultar.py`. Adicionalmente,
`consultar.py --campo frequencia` retorna o valor literal curado
(`rotineira`), não uma súmula gerada (C14).

## 17. Eventos

Cenário com quatro violações simultâneas de tipos diferentes (D/I/V,
agente como autor, escrita direta, referência inválida) produziu, na
trilha, tanto `CuradoriaRecusada` quanto `TentativaNegada` — os dois
tipos de evento cobrindo os dois mecanismos de recusa do sistema
(curadoria e guarda) (C15). O evento de recusa por agente-como-autor
demonstrou também a política acumulativa: a mesma recusa carregou
`CTX-V09` (autoria) e `CTX-V06`/`CTX-V07` (referências quebradas) juntos
— ver `eventos.jsonl`.

## 18. Testes consolidados

| ID | Cenário | Resultado |
|---|---|---|
| 2.5.6-C01 | D/I/V integrados | PASS |
| 2.5.6-C02 | Quatro objetos CTX | PASS |
| 2.5.6-C03 | Autoria × registrado_por | PASS |
| 2.5.6-C04 | Curadoria rascunho → contexto | PASS |
| 2.5.6-C05 | Bloqueio de escrita direta | PASS |
| 2.5.6-C06 | I→V com histórico | PASS |
| 2.5.6-C07 | Integração P3d | PASS |
| 2.5.6-C08 | CTX-V01–V11 (reexecução) | PASS |
| 2.5.6-C09 | Referências Termo/Entidade/Fonte | PASS |
| 2.5.6-C10 | P2 → CTX | PASS |
| 2.5.6-C11 | P3 → CTX | PASS |
| 2.5.6-C12 | CTX → P4 | PASS |
| 2.5.6-C13 | CTX → P5 | PASS |
| 2.5.6-C14 | Não reinterpretação | PASS |
| 2.5.6-C15 | Eventos | PASS |
| 2.5.6-C16 | Percurso integrado da camada | PASS |

**16/16 PASS.** Evidência bruta individual em `teste-2.5.6-Cxx.txt`.

## 19. Regressão

- **Baseline S2-BL** (histórico, imutável): 26 testes / 26 PASS / 0 FAIL.
- **Início do 2.5.6:** 113 total / 113 PASS / 0 FAIL / 0 SKIP (ver `teste-regressao-inicial.txt`).
- **2.5.6 (novos):** 16 total / 16 PASS / 0 FAIL.
- **Final do 2.5.6:** 129 total / 129 PASS / 0 FAIL / 0 SKIP (ver `teste-regressao-final.txt`).

Nenhuma regressão entre pacotes. Todos os seis pacotes anteriores
permanecem válidos.

## 20. Defeitos encontrados

**Nenhum defeito em código de produção** (`eiac-nucleo/`, `eiac-campo/`)
foi encontrado durante esta verificação. Não há `D-2.5.6-XX` a abrir.

Durante a construção de `testes/consolidado.py`, dois problemas foram
encontrados e corrigidos **nas próprias fixtures do teste novo**, antes
da execução registrada como evidência:

1. C06 originalmente tentava curar `RN-100` como um objeto "recém-nascido"
   em `I`, versão 1 — mas `RN-100` já tinha sido curado em `D`, versão 1,
   por C02 (o mesmo caso de controle, executado em sequência). A tentativa
   colidia com o próprio `curar.py`, corretamente, porque não era uma
   transição válida (`D`→`I` sem versão nova). Corrigido para o teste
   continuar do estado real do objeto (`D`→`V`), que é o comportamento
   verdadeiro do percurso integrado, não um cenário artificial.
2. Um erro de indexação (`depois[len(antes):]` em vez de `depois[antes:]`,
   onde `antes` já era um inteiro) quebrava C15 com `TypeError`. Corrigido.

Nenhum dos dois é defeito do sistema verificado — são erros de teste,
corrigidos antes de qualquer evidência ser gerada.

## 21. Correções e retestes

Não aplicável a código de produção (nenhuma correção funcional foi
necessária). As duas correções de fixture (§20) foram aplicadas e o
arquivo `testes/consolidado.py` foi reexecutado até produzir 16/16 PASS
antes da geração da evidência final.

## 22. Indicadores finais

| Indicador | Resultado |
|---|---|
| Procedência D/I/V | **CONFORME** |
| Objetos CTX | **4 / 4** conformes |
| CTX-V | **11 / 11** conformes |
| Curadoria protegida | **SIM** |
| I→V versionado | **SIM** |
| P3d rastreável | **SIM** |
| P2/P3 → CTX | **IMPLEMENTADO** |
| CTX → P4 | **IMPLEMENTADO** |
| CTX → P5 | **IMPLEMENTADO** |
| Eventos de recusa | **CONFORME** |

## 23. Comparação S2-BL → final da Ação 2.5

| Indicador | S2-BL | Final Ação 2.5 |
|---|---|---|
| D/I/V | divergente (procedência multidimensional) | conforme, contrato único D/I/V |
| Objetos CTX conformes | 0/4 plenamente alinhados ao CTX-01 | 4/4 |
| `autoria_conteudo` × `registrado_por` | ausente | conforme, distinção imposta (CTX-V09) |
| Histórico I→V imposto | parcial | conforme, versão nova obrigatória (CTX-V04/V10) |
| `referencia_p3d` | ausente | conforme, resolvível e verificada (CTX-V11) |
| CTX-V | 0/11 | 11/11 |
| P2/P3 → CTX | parcial | implementado |
| CTX → P4/P5 | parcial | implementado |
| Eventos CTX | ausente | conforme (`CuradoriaRecusada`, `ObjetoContextoCurado`, `TentativaNegada`) |

## 24. Evidências

`.projectdocs/evidencias/sprint2/2.5.6/`: `resultado.md`,
`matriz-consolidada.md`, `caso-controle.md`, `estado-final-caso.json`,
16 arquivos `teste-2.5.6-Cxx.txt`, `teste-regressao-inicial.txt`,
`teste-regressao-final.txt`, `eventos.jsonl`, `diff.patch`,
`git-show.txt`.

## 25. Commit(s)

Um único commit — pacote de verificação, sem correção funcional
necessária:

- `fc5fd2f` — `test(context): verify Sprint 2 context and data layer`

## 26. Situação D-01–D-06

| ID | Síntese | Pacote que tratou | Estado |
|---|---|---|---|
| D-01 | Procedência multidimensional antiga | 2.5.0 | **RESOLVIDO** |
| D-02 | Quatro objetos CTX no schema anterior | 2.5.1 | **RESOLVIDO** |
| D-03 | Curadoria e versionamento não impostos pelo código | 2.5.2 | **RESOLVIDO** |
| D-04 | P3d sem `referencia_p3d` | 2.5.3 | **RESOLVIDO** |
| D-05 | CTX-V01–V11 ausentes | 2.5.4 | **RESOLVIDO** |
| D-06 | P2/P3 não alimentam e P4/P5 não consomem CTX de forma executável | 2.5.5 | **RESOLVIDO** |

Todos os seis defeitos do baseline relativos à Ação 2.5 estão resolvidos
e revalidados neste pacote. Nenhum foi apagado do RTE-01 — cada um
mantém sua entrada histórica, com a resolução registrada como evidência
adicional (conforme §3.11 do RTE-01).

## 27. Estado final da Ação 2.5

**CONFORME.**

Todos os 19 critérios de saída da Ação 2.5 (§42 da instrução do pacote)
foram demonstrados por evidência, não presumidos: D/I/V vigente; quatro
objetos operantes; curadoria separando candidato de contexto consolidado;
autoria humana imposta; premissa obrigatória para `I`; evidência
obrigatória para `V`; histórico preservado em `I`→`V`; escrita direta
bloqueada com caminho positivo real; P3d rastreável; CTX-V01–CTX-V11
conformes (11/11); referências a Termo/Entidade/Fonte verificadas; P2/P3
alimentam CTX; P4 consome quando previsto; P5 consome preservando D/I/V;
contexto curado não é reinferido arbitrariamente; recusas auditáveis;
suíte sem regressão inexplicada (129/129); caso controlado demonstra o
percurso integrado com um objeto rastreável do início ao fim.

Nenhum item da Ação 2.6 foi antecipado.
