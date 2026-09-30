# Reempacotamento do método — ação 4.3

Fonte controlada: `emcia-artefatos` commit `91053af` (inclui as sete revisões até `029d68c`). Destino: `eiac-campo/reference/metodo/` em `master` a partir de `390df37`. Data: 29/09/2026.

## Oito documentos copiados

| Documento | Versão anterior → nova | SHA-256 anterior → novo | Origem |
|---|---|---|---|
| `EMCIA-CAM-01-protocolo-de-campo-por-passo.md` | 0.1 → 0.2 | `e267faafda2091d0312241dd4f206e840bf4942058815d65e22c91623cbecd5b` → `a0771c8dac0ea024a068f82065f1a4a14caf79d39b0aca55959ab4ddccf17c4a` | `029d68c` |
| `EMCIA-CAT-01-fronteira-de-delegacao.md` | 0.2 → 0.3 | `91847fb8d23d4962e4db7ef65a817c425ac18cefebf6847b200979d9b4e9a3db` → `29f421bc592b465b61c9f00e608ae32b831c6bd76cc91f3cb9cedab71f081e39` | `029d68c` |
| `EMCIA-ESP-01-especificacao-executavel-do-estudio-de-trabalho.md` | 0.2 → 0.3 | `82d4f1db36283f264ed3b25eb8597d9f89d8eb137350b597e38e721ea2784cee` → `98a19db34f636f1b250bf9aa3f4185c6e9c37df468282c5fa31e57aba82f35a3` | `029d68c` |
| `EMCIA-GLO-01-glossario-do-metodo.md` | 0.1 → 0.2 | `36af4a2496e63c2eb1b6488de75782f7cd6f587eebad3855ecd916d687e46504` → `605dbc422e0456cc9142e2e310cd679e161341fe9ad422a7cbc2646859bde440` | `91053af` |
| `EMCIA-MET-01-documento-do-metodo.md` | 0.1 → 0.2 | `3c4dd1e127d8cd2497aab22b8fc128eb094118e2dbe470a256f5e9bee9358172` → `cf237af2d8e128073beb51af680f036c81a079ab299e69389b76352534b9eaf2` | `029d68c` |
| `EMCIA-TRA-01-procedimentos-transversais-do-metodo.md` | 0.2 → 0.3 | `0de0379d023bae35d72410ee2d16d3b616c8bc176788556472cb57f37127a649` → `f3d7ee486a462cedeeb0839cb69b7707377029bf6605ead25ca9c7bf2eca32a1` | `029d68c` |
| `EMCIA-TRI-01-instrumento-de-triagem.md` | 0.1 → 0.2 | `df679a195d14160e308c6ce65988d63241f62e0fd31f39b0fc8eacc1df406dae` → `19d8f0e564c35d07989ffe589c1db2a3ee57c496fe35cff973a94f742c7bbfdb` | `029d68c` |
| `EMCIA-VER-01-plano-de-verificacao.md` | 0.1 → 0.2 | `3961c15b9d349ad9f993404081a0a002fe59a14664aad35c472f620e82e11771` → `d038d8f3d2488259ed88c37d1e86c5de673fafa19a0f9fbc53653ac2cb65320e` | `029d68c` |

`manifesto.json`: versão 1 → 2; `origem_controlada` aponta para `91053af`; `empacotado_em` = `2026-09-29`; conjunto mantido em 16 documentos. Os oito arquivos copiados são idênticos byte a byte aos da fonte.

## Oito documentos inalterados

`cmp` confirmou identidade com a fonte; os oito hashes do manifesto foram preservados:

- `EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md`
- `EMCIA-E1-ficha-de-enquadramento.md`
- `EMCIA-E2-diagnostico-e-oportunidade.md`
- `EMCIA-E3-blueprint-da-solucao.md`
- `EMCIA-E4-guia-operacional.md`
- `EMCIA-E5-relatorio-de-piloto.md`
- `EMCIA-FER-01-quadro-de-ferramentas.md`
- `EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md`

## Conferência de referências

Busca: `rg -n -i "CAT-01|MET-01|TRI-01|TRA-01|CAM-01|ESP-01|VER-01" eiac-campo eiac-nucleo`. A tabela reúne todas as ocorrências por arquivo; números são linhas após a cópia. As citações em títulos, índices e manifesto são listadas para completar o inventário.

| Arquivo | Linhas | Resultado |
|---|---|---|
| `eiac-campo/reference/agentes.json` | 4 | **Válida após correção**: Anexo A do CAT-01 v0.3 permite preparação; nenhum agente decide ou encerra EX3/EX4. |
| `eiac-campo/reference/gates.md` | 50, 51 | **Corrigida conforme decisão**: a correspondência E4/E5 é mantida nas revisões CAM-01 v0.2 e ESP-01 v0.3. |
| `eiac-campo/reference/habilidades.json` | 4, 5 (referências); 26 (HB-02) | **Válida após correção**: saída de HB-02 inclui o registro pelo engenheiro, como no CAT-01 v0.3. |
| `eiac-campo/reference/metodo/EMCIA-CAM-01-protocolo-de-campo-por-passo.md` | 7, 212, 213, 216 | Válida: citação no documento canônico copiado; seções e conteúdo correspondem à fonte `029d68c`. |
| `eiac-campo/reference/metodo/EMCIA-CAT-01-fronteira-de-delegacao.md` | 4, 175 | Válida: citação no documento canônico copiado; seções e conteúdo correspondem à fonte `029d68c`. |
| `eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md` | 288, 290, 291, 294 | Válida como lista de documentos relacionados; a menção ao VER-01 designa o arquivo histórico, sem aplicar seu plano. |
| `eiac-campo/reference/metodo/EMCIA-ESP-01-especificacao-executavel-do-estudio-de-trabalho.md` | 7, 72, 82, 179, 180, 181, 182, 193, 194, 195, 196 | Válida: citação no documento canônico copiado; seções e conteúdo correspondem à fonte `029d68c`. |
| `eiac-campo/reference/metodo/EMCIA-FER-01-quadro-de-ferramentas.md` | 169 | Válida: lista genérica de artefatos relacionados. |
| `eiac-campo/reference/metodo/EMCIA-GLO-01-glossario-do-metodo.md` | 34, 35, 36, 38, 39, 40, 41, 42, 47, 61, 66, 72, 73, 74, 75, 76, 77, 78, 79, 80, 90, 94, 95, 96, 97, 98, 99, 100, 102, 103, 133, 149, 158, 159, 162, 169, 178, 179, 182, 183, 184, 185, 186, 191, 192, 193, 194 | **Válida após revisão 0.2**: §3.6 marca como históricos os quatro termos da verificação por duas execuções; “Indicador” permanece vigente. |
| `eiac-campo/reference/metodo/EMCIA-MET-01-documento-do-metodo.md` | 4, 60, 74, 264 | Válida: citação no documento canônico copiado; seções e conteúdo correspondem à fonte `029d68c`. |
| `eiac-campo/reference/metodo/EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md` | 151, 152, 155 | Válida como lista de documentos relacionados; a menção ao VER-01 designa o arquivo histórico, sem aplicar seu plano. |
| `eiac-campo/reference/metodo/EMCIA-TRA-01-procedimentos-transversais-do-metodo.md` | 7, 172, 180, 183, 184 | Válida: citação no documento canônico copiado; seções e conteúdo correspondem à fonte `029d68c`. |
| `eiac-campo/reference/metodo/EMCIA-TRI-01-instrumento-de-triagem.md` | 6, 130 | Válida: citação no documento canônico copiado; seções e conteúdo correspondem à fonte `029d68c`. |
| `eiac-campo/reference/metodo/EMCIA-VER-01-plano-de-verificacao.md` | 6, 13, 154, 161 | Válida: citação no documento canônico copiado; seções e conteúdo correspondem à fonte `029d68c`. |
| `eiac-campo/reference/metodo/manifesto.json` | 6, 7, 14, 17, 19, 20, 21 | Válida: nomes dos oito documentos e hashes atualizados. |
| `eiac-campo/scripts/baseline.py` | 6, 19, 53, 64 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/scripts/calibragem.py` | 11, 19, 20, 71, 154, 155, 170 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/scripts/governanca.py` | 177 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/scripts/inegociaveis.py` | 60 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/scripts/metrica.py` | 9, 48, 118 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/scripts/operacional.py` | 123 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/scripts/piloto.py` | 12, 143 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-classificar/SKILL.md` | 31 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-enquadrar/SKILL.md` | 13 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-governar/SKILL.md` | 19 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-medir/SKILL.md` | 15 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-medir-valor/SKILL.md` | 12, 17, 23, 33 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-operacionalizar/SKILL.md` | 11, 18 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-pilotar/SKILL.md` | 12, 17 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/skills/hb-recalibrar/SKILL.md` | 15, 19, 22 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/contexto/README.md` | 76 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/registro/autonomia.schema.json` | 4 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/registro/baseline.schema.json` | 4 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/registro/calibragem.schema.json` | 4 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/registro/metricas.schema.json` | 4 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/registro/operacional.schema.json` | 4 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/registro/piloto.schema.json` | 4 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-campo/template-caso/registro/playbook.json` | 4, 298 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-nucleo/commands/apurar-nivel.md` | 13, 27 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-nucleo/commands/fronteira.md` | 6 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-nucleo/scripts/avancar.py` | 67, 146 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-nucleo/scripts/catalogo.py` | 24 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-nucleo/scripts/fronteira.py` | 7 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-nucleo/scripts/guarda.py` | 224 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |
| `eiac-nucleo/scripts/playbook.py` | 47, 193 | Válida: seção/conteúdo citado preservado na revisão; sem menção incompatível a EX3/EX4 ou ao VER-01 vigente. |

### Decisão sobre as quatro referências

As quatro ocorrências foram corrigidas como texto de referência, sem mudar código, testes ou playbook.

| Ocorrência | Antes | Depois |
|---|---|---|
| `reference/agentes.json:referencia` | “nenhum agente opera em EX3 ou EX4” | “nenhum agente decide ou encerra etapa em EX3 ou EX4” |
| `reference/habilidades.json:HB-02.saida` | “Nivel N1, N2 ou N3” | “Nivel N1, N2 ou N3, registrado pelo engenheiro” |
| `reference/gates.md:Correspondência entregável × passo` | “foi fixada por EMCIA-CAM-01/EMCIA-ESP-01 v0.2 (17/09/2026), coincidindo com o relatório” | “foi fixada por EMCIA-CAM-01/EMCIA-ESP-01 v0.2 (17/09/2026) e mantida nas versões seguintes (CAM-01 v0.2 e ESP-01 v0.3, de 29/09/2026), coincidindo com o relatório” |
| `reference/metodo/EMCIA-GLO-01...:§3.6` | Termos da verificação por duas execuções sem ressalva de vigência. | Nota: execução declarada, execução de campo, selamento e predição registrada são históricos; indicador permanece vigente. |

### Pontos de sentido alterado

- **CAT-01 §3.3:** o levantamento das regras não documentadas agora é EX4. `hb-levantar-regras` e a etapa P3b do playbook já declaram EX4; as citações a CAT-01 §3.6, §3.4.5, §3.5.1 e Anexo A foram conferidas. A frase em `reference/agentes.json` foi alinhada ao novo alcance da fronteira.
- **VER-01:** versão 0.2 está marcada “Substituído”; seções 1 a 10 ficaram como registro histórico e não definem o critério vigente. O GLO-01 v0.2 marca os quatro termos do plano antigo como históricos e mantém “Indicador” vigente.
- **Outras seções conferidas:** TRI-01 §3.4; MET-01 §§3.4.3, 3.4.6, 3.4.8–3.4.10; TRA-01 §3.5; CAM-01 §§3.2–3.6, 3.8 e Anexos A–D; ESP-01 §3.10/G6. Todas existem e preservam as afirmações citadas nos comandos, scripts e habilidades.

## Suíte e versões

- Suíte completa: **786 verificações em 35 módulos; 0 falhas**. A saída integral está em `saida-suite.txt`; `metodo_empacotado.py` passou com os 16 hashes.
- Plugins: `eiac-nucleo` **0.2.34**; `eiac-campo` **0.8.8**.

## Estado da entrega

As quatro referências receberam a correção decidida. O pacote reúne oito documentos revisados e oito inalterados, com a suíte reconferida sem falhas.
