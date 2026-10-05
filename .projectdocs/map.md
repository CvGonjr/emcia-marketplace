# Mapa de documentação — emcia-marketplace

Retrato operacional de 05/10/2026; substitui integralmente o mapa anterior.

## Repositórios e versões

O marketplace é a ferramenta; não contém caso nem dado de cliente. O método
canônico vive em emcia-artefatos. A presença de revisão/proposta não lhe atribui
aprovação. Casos são repositórios próprios, abertos por novo-caso.sh.

| Componente | Versão | Papel |
|---|---|---|
| eiac-nucleo | 0.2.48 | Guarda, procedência, máquina de etapas, trilha e contratos genéricos |
| eiac-campo | 0.8.29 | Método, scripts de campo, comandos, habilidades e template |
| Playbook do template | 0.4.21 | 13 etapas F0–P10, camadas por N1–N3 e contratos declarados |
| Manifesto do método | 6 | 22 documentos, tag, commit, linha de base, caminhos e SHA-256 |

Origem controlada: tag `metodo-v1.0`, commit `08bfb162d762935ed35f55e0a75bc700b81d5276`.
APR-01 registra a aprovação de Celso do Vale em 03/10/2026. Só essa linha de base
aprovada entra em caso real; revisão posterior exige nova aprovação e tag.
Cada documento foi extraído do objeto Git, sem edição manual. A abertura confere
os hashes e copia documentos e manifesto para metodo/. Não há leitura do
playbook do plugin pelo caso; migração de caso existente é humana e explícita.

## Entrada e documentos do método

README.md apresenta operação e limites; INSTALACAO.md apresenta instalação,
conectores e provas locais. AGENTS.md e CLAUDE.md fixam as regras de trabalho.
O manual de aplicação é MAN-01 v1.0; A25 registra a falha conhecida da 045 contra o novo playbook.
CAN-01 declara canais por id; HAB-01 rege habilitação e vínculo de restrição;
ROT-02 substitui o identificador anterior do roteiro, preservando HAB-02 como
template do acordo de confidencialidade. Os três templates HAB são extraídos da tag e empacotados
sem alteração. A geração confere seus hashes no APR-01; um checkout externo
precisa estar na mesma tag. ESP-01, VER-01 e o fluxo auxiliar permanecem referências
históricas canônicas, fora do pacote destinado a casos reais.

O instrumento do contexto é
`eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md`.
As cópias de CTX-01-instrumento-camada-contexto.md da raiz e de reference/ foram
retiradas por decisão expressa do engenheiro: eram resumos anteriores, não
controlados pelo manifesto. A emenda da decisão 021 preserva essa decisão,
e citacoes.py confere a retirada e as remissões. O histórico Git conserva os resumos.
O README local antigo do pacote foi retirado; os procedimentos de empacotamento
ficam neste mapa e no README principal, fora dos documentos canônicos.

| Documento empacotado | Versão | Caminho no commit da tag |
|---|---|---|
| `EMCIA-APR-01-registro-de-aprovacoes.md` | 1.0 | `EMCIA-APR-01-registro-de-aprovacoes.md` |
| `EMCIA-CAM-01-protocolo-de-campo-por-passo.md` | 1.0 | `EMCIA-CAM-01-protocolo-de-campo-por-passo.md` |
| `EMCIA-CAN-01-protocolo-de-canais-externos.md` | 1.0 | `EMCIA-CAN-01-protocolo-de-canais-externos.md` |
| `EMCIA-CAT-01-fronteira-de-delegacao.md` | 1.0 | `EMCIA-CAT-01-fronteira-de-delegacao.md` |
| `EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md` | 1.0 | `EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md` |
| `EMCIA-E1-ficha-de-enquadramento.md` | 0.1 | `EMCIA-E1-ficha-de-enquadramento.md` |
| `EMCIA-E2-diagnostico-e-oportunidade.md` | 0.1 | `EMCIA-E2-diagnostico-e-oportunidade.md` |
| `EMCIA-E3-blueprint-da-solucao.md` | 0.1 | `EMCIA-E3-blueprint-da-solucao.md` |
| `EMCIA-E4-guia-operacional.md` | 0.1 | `EMCIA-E4-guia-operacional.md` |
| `EMCIA-E5-relatorio-de-piloto.md` | 0.1 | `EMCIA-E5-relatorio-de-piloto.md` |
| `EMCIA-FER-01-quadro-de-ferramentas.md` | 1.0 | `EMCIA-FER-01-quadro-de-ferramentas.md` |
| `EMCIA-GLO-01-glossario-do-metodo.md` | 1.0 | `EMCIA-GLO-01-glossario-do-metodo.md` |
| `EMCIA-HAB-01-protocolo-de-habilitacao.md` | 1.0 | `EMCIA-HAB-01-protocolo-de-habilitacao.md` |
| `EMCIA-MAN-01-manual-de-aplicacao.md` | 1.0 | `EMCIA-MAN-01-manual-de-aplicacao.md` |
| `EMCIA-MET-01-documento-do-metodo.md` | 1.0 | `EMCIA-MET-01-documento-do-metodo.md` |
| `EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md` | 1.0 | `EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md` |
| `EMCIA-ROT-02-roteiro-de-habilitacao.md` | 1.0 | `auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md` |
| `EMCIA-TRA-01-procedimentos-transversais-do-metodo.md` | 1.0 | `EMCIA-TRA-01-procedimentos-transversais-do-metodo.md` |
| `EMCIA-TRI-01-instrumento-de-triagem.md` | 1.0 | `EMCIA-TRI-01-instrumento-de-triagem.md` |
| `HAB-01-carta-de-escopo.md` | 0.2 | `auxiliares/HAB-01-carta-de-escopo.md` |
| `HAB-02-acordo-confidencialidade.md` | 0.2 | `auxiliares/HAB-02-acordo-confidencialidade.md` |
| `HAB-03-termo-de-consentimento.md` | 0.2 | `auxiliares/HAB-03-termo-de-consentimento.md` |

## Sequência de operação

Habilitação administrativa fora de repositórios → abertura → planejar/provisionar
→ definir canais (ou --canais na importação) → importar expediente → gravar
00-habilitacao pelo validador → selar → F0. Planejamento não chama API.
Provisionamento MCP exige contêiner inicial declarado e exclusivo do caso;
sem ele, o comando informa a falta. A árvore inteira e o conjunto de
compartilhamentos recebem aprovações próprias, com destinatário/id/papel;
os testemunhos não delegam decisões de método reservadas ao terminal.

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

Scripts: `aprovacao.py`, `apuracao.py`, `avancar.py`, `caminhos.py`, `canais_registro.py`, `catalogo.py`, `consultar.py`, `curar.py`, `decisao_humana.py`, `escopo_externo.py`, `esforco.py`, `estado.py`, `estrutura.py`, `fontes_registro.py`, `fronteira.py`, `guarda.py`, `integridade.py`, `pessoa.py`, `playbook.py`, `produtos.py`, `quadro.py`, `recorrencia.py`, `selar.py`, `validar.py`.

Comandos: `apurar-nivel.md`, `consultar.md`, `curar.md`, `emitir.md`, `encerrar.md`, `esforco.md`, `estado.md`, `fronteira.md`, `gravar.md`, `quadro.md`, `registrar-campo.md`, `registrar-recorrencia.md`, `registrar-sessao.md`, `satisfazer-inegociavel.md`, `selar.md`.

hooks/hooks.json registra as rotas da guarda. A guarda resolve camadas, autoria,
escrita, decisões humanas, dependências, selos e escopo MCP a partir do contrato
do caso. Verificação de selo usa autoria, nota e prefixo exato da trilha no Git,
ordenado pela posição dos eventos. Diagnóstico de integridade da referência
é somente leitura; não autentica origem. O núcleo acrescenta integridade de produto e condições genéricas de continuidade, sem interpretar o método.

### Campo

Scripts: `abrir_caso.py`, `baseline.py`, `calibragem.py`, `canais.py`, `consultar.py`, `entregar.py`, `entregaveis.py`, `formularios.py`, `governanca.py`, `habilitacao.py`, `importar_habilitacao.py`, `inegociaveis.py`, `metrica.py`, `operacional.py`, `piloto.py`, `prosseguimento.py`, `quadro.py`, `receber.py`, `registrar_listagem.py`, `restricoes.py`.

Comandos: `canais.md`, `classificar.md`, `confrontar.md`, `emitir.md`, `enquadrar.md`, `governar.md`, `habilitacao.md`, `mapear-contexto.md`, `mapear-fontes.md`, `medir-valor.md`, `medir.md`, `operacionalizar.md`, `pilotar.md`, `priorizar.md`, `recalibrar.md`.

Habilidades: 18 arquivos SKILL.md.
Agentes físicos: `classificador-tecnologico.md`, `extrator-documental.md`.
O catálogo declara 21 HB e quatro AG lógicos, reproduzindo CAT-01 v0.5 Anexos A e C. Toda HB está ligada à habilidade de uma etapa; P3b permanece sem HB/AG. A decisão 043 supera a regra provisória da 020.
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
| 020 | Pendência única de correspondência entre CAT-01, catálogo e playbook | superada por 043; regra provisória preservada como histórico |
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
| 043 | Correspondência CAT-01, catálogo e playbook; decisão de prosseguimento em F0 | firme por instrução do engenheiro; supera 020 e registra D5 e MAN-01 v0.4 |
| 044 | Linha de base aprovada metodo-v1.0; separação do modelo e emissão; revisão jurídica | obrigatoriedade de ratificação parcialmente superada por 045 |
| 045 | Bloco inicial conduzido com aprovação nominal e aceitação revogável | firme por instrução do engenheiro |

## Suítes e evidências

A linha de base inicial em Python 3.12.12 passou com 958 verificações em 49 módulos.
A geração acrescenta dez testes e a conferência do pacote passa de um controle
por processo a oito testes, incluindo negativas de APR-01, tag e templates.
As contagens finais constam da evidência linha-de-base-v1 e de testes/README.md.
O inventário completo e o executador atual estão em testes/README.md e
.projectdocs/evidencias/bloco-inicial-conduzido/. Registre códigos, saídas e
contagens; falha inesperada impede commit; a exceção A25 exige divergência exata. Antes de alterações, rode negativos.sh
e contexto.py; para pacote específico, rode seus módulos e a regressão completa.

metodo_empacotado.py confere inventário, caminhos de origem e hashes; com checkout
canônico irmão, resolve a tag, compara bytes aos objetos do commit e confere
os templates do checkout pelos hashes do APR-01. habilitacao.py resolve os nomes
pelos códigos no APR-01, recusando ausência ou ambiguidade; exige revisão
jurídica com resultado aprovado para os hashes ou aceitação nominal ativa; retira
controle, histórico e avisos internos, preservando cláusulas e identificação.
A evidência contém PDFs reais sintéticos antes/depois e extrações pdftotext.
Resultado obrigatório, registros legados sem liberação e os dois nomes de
HAB-03 são cobertos em .projectdocs/evidencias/revisao-juridica-resultado/:
linha de base de 975 verificações e regressão de 986, em 49 módulos, Python 3.12.
manual_a25.py permanece inalterado e acusa a divergência da decisão 045;
somente test_01 é falha conhecida, mantendo quatro negativos aprovados.
citacoes.py confere seções, instrumentos JSON, auxiliares e o TRI-01 real.
restricoes.py e selo_p3b.py cobrem as decisões 041 e 042; habilitacao_0d.py cobre
passagem e selo de F0. Os módulos de canais cobrem a fronteira externa.

Evidências anteriores: sprint2/, sprint3/, habilitacao-0d/, canais-externos/ e
parte-a-operacional/. A prova real E7 usou Claude Code 2.1.283 e MCP stdio
sintético. Os demos em .projectdocs/demos/ preparam controles sintéticos;
percurso-completo.sh usa o HEAD commitado congelado, incluindo decisões humanas
fictícias. Simulação não é prova de execução de hook em outro cliente.

## Limites vigentes

Scripts conferem coerência local, contratos e hashes, sem autenticar origem
remota, identidade, acesso ou recebimento efetivo. SHA-256 fixa bytes, não
veracidade. Acesso humano de escrita ao disco é a fronteira de confiança.
Hooks MCP foram demonstrados no runtime testado; a guarda não comprova a
confirmação no chat. Não há assinatura eletrônica integrada, aceite de entregáveis,
gravação ou transcrição de sessões no escopo aprovado.

A revisão humana da carta integra a habilitação normal. A correspondência 020 foi
resolvida pela 043. Permanece o aparato residual de isolamento da execução de contraste retirada. ESP-01 conserva o recorte histórico
da prova de conceito; os limites operacionais estão em MAN-01 §3.6. Contrato RH,
selo confirmado de P3b e colisão do código do roteiro já foram resolvidos.

## Correspondência e prosseguimento — decisão 043

CAT-01 v1.0 Anexo C é a fonte da relação etapa → HBs → AG. HB-09 está em P3d,
com o estado declarado selado em P2 como entrada e candidatos para P4 como saída;
as quatro frentes pertencem a P1 e são instrumento distinto. A camada das HBs
é de preparação, limitada pela camada de encerramento da etapa em cada nível.

O engenheiro executa prosseguimento.py --entrada rascunho/prosseguimento.json
no terminal. O registro exige pessoa, data, desfecho, motivo e ficha E1 preparada.
Ambos os desfechos encerram F0; não prosseguir bloqueia as etapas seguintes até
nova decisão que preserva a anterior. Produtos e continuidade vêm do contrato
copiado no caso; casos anteriores não são migrados automaticamente. Evidência:
.projectdocs/evidencias/correspondencia-cat01/.


## Bloco inicial conduzido — decisão 045

/iniciar verifica ambiente, reutiliza ~/.emcia/config.json, calibra perfis conhecidos
pela assinatura real e conduz 0a–0d até F0 liberado. Testemunhos de aprovação
vinculam operações, entradas e hashes; não autenticam o chat. Cinco aprovações
cobrem envio/rodadas, carta, PDFs, abertura com árvore e compartilhamentos.
Perfil e aceitação sem ratificação são confirmações iniciais; aceitação é revogável.
Revisão aprovada para o hash prevalece. A situação jurídica fica no expediente,
nunca na emissão ao cliente; pendência não bloqueia o checklist de saída.

iniciar.py, guarda_inicial.py, saida_inicial.py e o contrato operacoes_sessao
instrumentam essa autorização. Decisões de método e selo após P2 continuam
humanos. Rótulos antigos de curadoria ficam no schema do campo; o núcleo lê dados.
Casos existentes conservam seu playbook; há fixture íntegra de 0.4.19 nos testes.
Pacote/manifesto metodo-v1.0 permanecem idênticos. Propostas de HAB-01, ROT-02,
CAN-01, CAT-01 e MAN-01 estão em propostas-artefatos.md, sem aprovação presumida.

Evidência: .projectdocs/evidencias/bloco-inicial-conduzido/. Linha de base 986/49
em Python 3.12.12. Regressão final 1014 verificações/51 módulos, com somente A25
como falha conhecida. O runner e o CI conferem a divergência exata e as quatro
negativas de A25; não excluem o teste nem toleram outra falha.

## Perfis reais dos conectores

reference/perfis-conectores.json contém contratos auditados pelo inventário fornecido.
Calibração literal, variantes de criação, parâmetros extras recusados, listagem/hash,
aprovação dos valores de compartilhamento e caminhos manuais registrados. Tally sem
filtro de caso fica manual; schemas incompletos não são aproximados. Emenda da 045,
propostas canônicas preservadas e pacote sem alterações. perfis_conectores.py: 40 testes.
Regressão integral: 1054/52 em 3.12 e 1056/52 em 3.14.4; somente a A25 conhecida.
Evidência: .projectdocs/evidencias/perfis-conectores/.

## Conferência automática de formulário

Campo 0.8.28 e núcleo 0.2.48: load_form por formId corrente; retorno bruto com
hash, comparação determinística em scripts/conferencia_formulario.py e relatório
MD. iniciar.py conduz conferir-formulario e confirmar-formulario com literal
conferido; publicação exige a última conferência vigente. PDF permanece alternativa.
Ciclo sem textos fixos não é inferido. conferencia_formulario.py: 29 testes;
perfis_conectores.py: 47. Regressão integral: 1090/53 em 3.12 e 1092/53 em 3.14,
somente A25 conhecida. Evidência: .projectdocs/evidencias/conferencia-formulario/.

## Comparador no formato real do conector (046)

Campo 0.8.29 lê payload.html ou safeHTMLSchema, com normalização restrita NFC,
NBSP, bordas e formatação. Marcas/estrutura não reconhecidas são recusadas por
blocks[i]. Prefixo de id nas perguntas continua divergindo. Bateria: 48 testes;
regressão integral 1109/53 em 3.12 e 1111/53 em 3.14, somente A25 conhecida.
Evidência: .projectdocs/evidencias/comparador-conector-real/.
