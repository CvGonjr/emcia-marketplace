# Mapa de documentação — emcia-marketplace

Retrato operacional de 03/10/2026; substitui integralmente o mapa anterior.

## Repositórios e versões

O marketplace é a ferramenta; não contém caso nem dado de cliente. O método
canônico vive em emcia-artefatos. A presença de revisão/proposta não lhe atribui
aprovação. Casos são repositórios próprios, abertos por novo-caso.sh.

| Componente | Versão | Papel |
|---|---|---|
| eiac-nucleo | 0.2.44 | Guarda, procedência, máquina de etapas, trilha e contratos genéricos |
| eiac-campo | 0.8.22 | Método, scripts de campo, comandos, habilidades e template |
| Playbook do template | 0.4.18 | 13 etapas F0–P10, camadas por N1–N3 e contratos declarados |
| Manifesto do método | 4 | 21 documentos, origem e caminhos canônicos, SHA-256 |

Origem controlada: commit `1d6d1e8bfc1739594ea7a119257ecae28c8e5af4`.
Cada documento foi extraído do objeto Git, sem edição manual. A abertura confere
os hashes e copia documentos e manifesto para metodo/. Não há leitura do
playbook do plugin pelo caso; migração de caso existente é humana e explícita.

## Entrada e documentos do método

README.md apresenta operação e limites; INSTALACAO.md apresenta instalação,
conectores e provas locais. AGENTS.md e CLAUDE.md fixam as regras de trabalho.
O manual de aplicação é MAN-01 v0.2, conferido contra o playbook vigente.
CAN-01 declara canais por id; HAB-01 rege habilitação e vínculo de restrição;
ROT-02 substitui o identificador anterior do roteiro, preservando HAB-02 como
template do acordo de confidencialidade. Os três templates HAB ficam no checkout
canônico e não foram alterados.

O instrumento do contexto é
`eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md`.
As cópias de CTX-01-instrumento-camada-contexto.md da raiz e de reference/ foram
retiradas por decisão expressa do engenheiro: eram resumos anteriores, não
controlados pelo manifesto. A emenda da decisão 021 preserva essa decisão,
e citacoes.py confere a retirada e as remissões. O histórico Git conserva os resumos.
O README local antigo do pacote foi retirado; os procedimentos de empacotamento
ficam neste mapa e no README principal, fora dos documentos canônicos.

| Documento empacotado | Versão | Caminho no commit canônico |
|---|---|---|
| `EMCIA-CAM-01-protocolo-de-campo-por-passo.md` | 0.3 | `EMCIA-CAM-01-protocolo-de-campo-por-passo.md` |
| `EMCIA-CAN-01-protocolo-de-canais-externos.md` | 0.1 | `EMCIA-CAN-01-protocolo-de-canais-externos.md` |
| `EMCIA-CAT-01-fronteira-de-delegacao.md` | 0.4 | `EMCIA-CAT-01-fronteira-de-delegacao.md` |
| `EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md` | 0.5 | `EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md` |
| `EMCIA-E1-ficha-de-enquadramento.md` | «0.1» | `EMCIA-E1-ficha-de-enquadramento.md` |
| `EMCIA-E2-diagnostico-e-oportunidade.md` | «0.1» | `EMCIA-E2-diagnostico-e-oportunidade.md` |
| `EMCIA-E3-blueprint-da-solucao.md` | «0.1» | `EMCIA-E3-blueprint-da-solucao.md` |
| `EMCIA-E4-guia-operacional.md` | «0.1» | `EMCIA-E4-guia-operacional.md` |
| `EMCIA-E5-relatorio-de-piloto.md` | «0.1» | `EMCIA-E5-relatorio-de-piloto.md` |
| `EMCIA-ESP-01-especificacao-executavel-do-estudio-de-trabalho.md` | 0.4 | `EMCIA-ESP-01-especificacao-executavel-do-estudio-de-trabalho.md` |
| `EMCIA-FER-01-quadro-de-ferramentas.md` | 0.2 | `EMCIA-FER-01-quadro-de-ferramentas.md` |
| `EMCIA-GLO-01-glossario-do-metodo.md` | 0.3 | `EMCIA-GLO-01-glossario-do-metodo.md` |
| `EMCIA-HAB-01-protocolo-de-habilitacao.md` | 0.3 | `EMCIA-HAB-01-protocolo-de-habilitacao.md` |
| `EMCIA-HAB-fluxo-operacional-proposta.md` | 0.2 | `auxiliares/EMCIA-HAB-fluxo-operacional-proposta.md` |
| `EMCIA-MAN-01-manual-de-aplicacao.md` | 0.2 | `EMCIA-MAN-01-manual-de-aplicacao.md` |
| `EMCIA-MET-01-documento-do-metodo.md` | 0.2 | `EMCIA-MET-01-documento-do-metodo.md` |
| `EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md` | 0.1 | `EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md` |
| `EMCIA-ROT-02-roteiro-de-habilitacao.md` | 0.2 | `auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md` |
| `EMCIA-TRA-01-procedimentos-transversais-do-metodo.md` | 0.4 | `EMCIA-TRA-01-procedimentos-transversais-do-metodo.md` |
| `EMCIA-TRI-01-instrumento-de-triagem.md` | 0.2 | `EMCIA-TRI-01-instrumento-de-triagem.md` |
| `EMCIA-VER-01-plano-de-verificacao.md` | 0.2 | `EMCIA-VER-01-plano-de-verificacao.md` |

## Sequência de operação

Habilitação administrativa fora de repositórios → abertura → planejar/provisionar
→ definir canais (ou --canais na importação) → importar expediente → gravar
00-habilitacao pelo validador → selar → F0. Planejamento não chama API.
Provisionamento MCP exige contêiner inicial declarado e exclusivo do caso;
sem ele, use a interface externa. Confirmação no chat é própria de cada efeito
externo e compartilhamento; não delega decisões humanas do terminal.

fontes/ recebe bytes apenas por importar_habilitacao.py e receber.py.
A importação copia PDFs assinados, evidências e matriz; recebimento copia coleta
preparada com manifesto de origem. O curador grava termos, entidades, regras,
fontes e confrontos em contexto/. Toda asserção tem D/I/V, autoria nominal e
origem; recebimento não promove declaração a V.

P2 exige cobertura dos RH importados por vínculo a fontes curadas ou dispensa
motivada. Fora de P2 só cabe revisão de vínculo existente após P2 encerrada.
A relação REC → F é explícita. Cada valor afetado recebe a marca de RH junto
ao próprio ponto; RH pendente bloqueia materialização e posterga E1 até P2.
O selo de F0 cobre a importação. P3b exige selo após o último encerramento de P2.
Ambos exigem confirmação no Git; eventos de commit recusado não liberam a trava.

## Inventário dos plugins

### Núcleo

Scripts: `apuracao.py`, `avancar.py`, `caminhos.py`, `canais_registro.py`, `catalogo.py`, `consultar.py`, `curar.py`, `decisao_humana.py`, `escopo_externo.py`, `esforco.py`, `estado.py`, `estrutura.py`, `fontes_registro.py`, `fronteira.py`, `guarda.py`, `integridade.py`, `pessoa.py`, `playbook.py`, `produtos.py`, `quadro.py`, `recorrencia.py`, `selar.py`, `validar.py`.

Comandos: `apurar-nivel.md`, `consultar.md`, `curar.md`, `emitir.md`, `encerrar.md`, `esforco.md`, `estado.md`, `fronteira.md`, `gravar.md`, `quadro.md`, `registrar-campo.md`, `registrar-recorrencia.md`, `registrar-sessao.md`, `satisfazer-inegociavel.md`, `selar.md`.

hooks/hooks.json registra as rotas da guarda. A guarda resolve camadas, autoria,
escrita, decisões humanas, dependências, selos e escopo MCP a partir do contrato
do caso. Verificação de selo usa autoria, nota e prefixo exato da trilha no Git,
ordenado pela posição dos eventos. Diagnóstico de integridade da referência
é somente leitura; não autentica origem. Nenhum arquivo do núcleo mudou neste pacote.

### Campo

Scripts: `abrir_caso.py`, `baseline.py`, `calibragem.py`, `canais.py`, `consultar.py`, `entregar.py`, `entregaveis.py`, `formularios.py`, `governanca.py`, `habilitacao.py`, `importar_habilitacao.py`, `inegociaveis.py`, `metrica.py`, `operacional.py`, `piloto.py`, `quadro.py`, `receber.py`, `registrar_listagem.py`, `restricoes.py`.

Comandos: `canais.md`, `classificar.md`, `confrontar.md`, `emitir.md`, `enquadrar.md`, `governar.md`, `habilitacao.md`, `mapear-contexto.md`, `mapear-fontes.md`, `medir-valor.md`, `medir.md`, `operacionalizar.md`, `pilotar.md`, `priorizar.md`, `recalibrar.md`.

Habilidades: 18 arquivos SKILL.md.
Agentes físicos: `classificador-tecnologico.md`, `extrator-documental.md`.
O catálogo declara 18 HB e quatro AG lógicos. HB-04/05/06/13 não têm habilidade
física própria; correspondência CAT/catálogo/playbook permanece pendente na 020.
Habilidade não delegável não carrega mesmo com sessão e selo; nas camadas humanas,
o apoio permitido segue as condições declaradas. As habilidades remetem ao método.

reference/ conserva interfaces de habilitação/canais, formulários, procedência,
gates e catálogos. reference/metodo/ contém somente documentos extraídos e o
manifesto. template-caso/ contém instruções, playbook, estado, schemas e modelos
CTX. O bootstrap fixa responsável, reserva destino, copia e confere os bytes,
registra CasoAberto e tenta o commit inicial. Não importa expediente automaticamente.

## Decisões 001–042

O índice em decisoes/README.md registra estados, substituições e emendas.
As decisões originais continuam preservadas; a 038 recebeu nota sobre MAN-01
operacional sem emenda local, e a 021 recebeu a retirada dos resumos CTX.

| # | Decisão | Estado |
|---|---|---|
| 001 | Dois plugins: núcleo e playbook | firme |
| 002 | O playbook vive no caso, não no plugin | firme |
| 003 | Chat não tem autoridade de escrita | firme |
| 004 | A antítese roda entre P2 e P3a | substituída por 021 |
| 005 | Camada resolvida por nível | firme |
| 006 | Procedência em três dimensões | resolvida — D/I/V, conforme CAT-01 |
| 007 | Um repositório Git por caso | firme |
| 008 | O cliente nunca fala com um agente | firme |
| 009 | Habilidades remetem ao método, não o reproduzem | firme |
| 010 | Três zonas de escrita | proposta |
| 011 | Testes negativos antes do caminho feliz | firme |
| 012 | E3 dividido; termo de autonomia no E4 | firme (pendência de correspondência superada por 013) |
| 013 | E4 = P6/P7, E5 = P8/P9/P10, fixado por EMCIA-CAM-01/ESP-01 | firme |
| 014 | Execução de contraste roda fora do caso de campo, em repositório e plugin próprios, antes do F0 | substituída por 021 |
| 015 | Isolamento, esforço comparável e cálculo compartilhado | parcialmente superada por 018 (checagem por plugin habilitado); a parte de execução de contraste substituída por 021 |
| 016 | O contraste substitui a identidade de runtime do núcleo | substituída por 021 |
| 017 | O campo empacota o método; o contraste registra ambiguidades como pendências | substituída por 021 |
| 018 | Isolamento verificado no selo por carimbo de componente, não por nome de plugin | substituída por 021 (aparato de isolamento mantido no código, não removido, mas não rege mais um fluxo ativo) |
| 019 | Autoria de registro é atribuída pelo componente, nunca informada pelo agente | firme quanto à autoria; exceção de --ator para decisões substituída por 027; parte de contraste substituída por 021 |
| 020 | Pendência única de correspondência entre CAT-01, catálogo e playbook | pendente de decisão de método (menção à execução de contraste substituída por 021; pendência de cruzamento continua aberta) |
| 021 | Retirada da execução de contraste; verificação por estados do caso | firme; emendas 042 (selo Git) e retirada dos resumos CTX |
| 022 | Expediente administrativo de habilitação anterior ao caso; assinatura pelo painel escolhido pelo cliente | firme quanto ao escopo aprovado |
| 023 | Regra de leitura da triagem declarada e conferida (A7) | firme |
| 024 | Sessão exigida no encerramento das camadas EX3 e EX4 (A8) | firme |
| 025 | Emissão exige artefato declarado no playbook (A9) | firme quanto à correção solicitada |
| 026 | Campos da etapa declarados e registrados pelo núcleo (A10) | firme quanto à correção solicitada |
| 027 | Decisão humana fora da sessão do agente (A12) | firme; ampliada por 029 e checagem nominal por 030 |
| 028 | Produto próprio exigido no encerramento (A14) | firme |
| 029 | Revisão humana do piloto declarada na guarda (A15) | firme |
| 030 | Pessoa nomeada sem termos coletivos (A16) | firme |
| 031 | Habilidade não delegável bloqueada nas rotas de carregamento (A18) | firme; substitui a exceção de sessão para habilidades não delegáveis |
| 032 | Caminhos normalizados relativos à raiz do caso (A19) | firme |
| 033 | Redirecionamento inspecionado pelo alvo de escrita (A20) | firme |
| 034 | Recusa de habilidade registrada como evento (A21) | firme |
| 035 | Selo exibido pelo histórico confirmado do caso (A17) | firme |
| 036 | Responsável da recorrência conferido com a fonte vigente (A23) | firme |
| 037 | E5 usa a rotina de calibragem vigente (A24) | firme |
| 038 | Manual de aplicação conferido contra o playbook (ação 4.5) | firme; emenda MAN-01 v0.2 operacional, sem sobreposição local |
| 039 | Passagem da habilitação ao caso; novo selo confirmado pelo Git | aprovada; A–D entregues; restrições completadas por 041 e selo de P3b por 042; roteiro renomeado para ROT-02 no canônico |
| 040 | Canais externos por caso, origem com hash e atos humanos na fronteira | aprovada; E1–E7 concluídos; limites locais e runtime testado registrados |
| 041 | Restrição vinculada a fonte curada, com marca no ponto do entregável | aprovada; completa o pacote D da 039 |
| 042 | Selo confirmado no Git para a exigência após encerramento | aprovada; emenda 021 e completa a correção reservada em 039 |


## Suítes e evidências

A linha de base em Python 3.12.12 passou com 919 verificações em 46 módulos.
A revisão acrescenta citacoes.py: 1845 verificações em 48 módulos.
O inventário completo e o executador estão em testes/README.md e
.projectdocs/evidencias/documentacao-operacional/. Registre códigos, saídas e
contagens; falha de teste impede commit. Antes de alterações, rode negativos.sh
e contexto.py; para pacote específico, rode seus módulos e a regressão completa.

metodo_empacotado.py confere inventário, caminhos de origem e hashes; com checkout
canônico irmão, compara bytes ao objeto do commit. manual_a25.py exige conferir()
vazio para o manual empacotado, sem emenda, mantendo quatro negativos.
citacoes.py confere seções, instrumentos JSON, auxiliares e o TRI-01 real.
restricoes.py e selo_p3b.py cobrem as decisões 041 e 042; habilitacao_0d.py cobre
passagem e selo de F0. Os módulos de canais cobrem a fronteira externa.

Evidências anteriores: sprint2/, sprint3/, habilitacao-0d/, canais-externos/ e
parte-a-operacional/. A prova real E7 usou Claude Code 2.1.283 e MCP stdio
sintético. Os demos em .projectdocs/demos/ preparam controles sintéticos;
percurso-completo.sh usa o HEAD commitado congelado, incluindo decisões humanas
fictícias. Simulação não é prova de execução de hook em outro cliente.

## Limites e pendências

Scripts conferem coerência local, contratos e hashes, sem autenticar origem
remota, identidade, acesso ou recebimento efetivo. SHA-256 fixa bytes, não
veracidade. Acesso humano de escrita ao disco é a fronteira de confiança.
Hooks MCP foram demonstrados no runtime testado; a guarda não comprova a
confirmação no chat. Não há assinatura eletrônica integrada, aceite de entregáveis,
gravação ou transcrição de sessões no escopo aprovado.

Permanecem a revisão humana da carta, a pendência 020 e o aparato residual de
isolamento da execução de contraste retirada. ESP-01 conserva o recorte histórico
da prova de conceito; os limites operacionais estão em MAN-01 §3.6. Contrato RH,
selo confirmado de P3b e colisão do código do roteiro já foram resolvidos.
