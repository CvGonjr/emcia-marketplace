# Ação 3.5 — Correção A12

## Lacuna e base

O agente podia informar --autor/--ator humano e executar uma decisão pela
sessão. A checagem lexical do nome não distinguia a origem da chamada.

Base: `v-sprint3-poc.3`, objeto anotado `3e5a93364e40185fadd8889ff4b9018d59ce1d9c`, commit `c36f1a6386e0e652362c1917ef300c7b7720a61a`.
Foram lidos CLAUDE.md, o índice e decisões 003, 019 e 022–025.
A decisão 026 já registra A10; preservado o histórico, A12 foi registrada
como **027 — Decisão humana fora da sessão do agente (A12)**. A 019 recebeu
marca de revisão: exceção de --ator substituída para decisões de método;
autoria fixa de validar/curar/selar preservada.

## Correção

Toda chamada recebida na guarda tem origem na sessão do agente. Nome
humano informado não muda essa origem. O playbook do caso declara
`decisoes_humanas`: identificador da operação, nome do script, argumento
quando aplicável e condição. O núcleo lê esses dados sem citar nomes de
scripts de método, etapas ou categorias da decisão no novo avaliador.

As condições suportadas são:

- `sempre`: a operação é humana em toda chamada correspondente;
- `arquivo`: leitura do rascunho correspondente ao caminho informado,
  com igualdade de campo ou campo preenchido;
- `camada`: camada da etapa alvo no nível apurado, comparada à lista declarada.

O contrato também declara quais estados são preparação em P6/P7. A ausência
ou invalidade da lista não desativa a guarda; recusa o playbook. Rascunho
ilegível, ausente ou fora do caso não permite decisão por falha de inspeção.
Comandos compostos condicionados por arquivo ou camada são recusados,
pois podem alterar o candidato ou mudar o contexto da etapa antes da chamada.

A recusa acontece antes da execução, com exit 2, gera `TentativaNegada` e
preserva o estado. O evento inclui operação, ação tentada, comando exato,
responsável nominal, etapa e ferramenta. A mensagem entrega o comando e
explica que o engenheiro executa no próprio terminal, fora do Claude Code.
O terminal continua aplicando as demais condições do script.

## Antes/depois de cada operação

Todas as chamadas negativas abaixo informam nome humano. “Antes” descreve a
autorização da guarda, não sucesso de uma operação com conteúdo inválido.

| Operação | Condição declarada | Antes, pela sessão | Depois, pela sessão | Execução autorizada |
|---|---|---|---|---|
| governanca.py | rascunho estado decidido | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| operacional.py | rascunho estado validado | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| calibragem.py | rascunho com decisao preenchida | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| avancar.py --apurar-nivel | sempre | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| avancar.py --registrar-sessao | sempre | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| avancar.py --registrar-campo | sempre | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| avancar.py --registrar-recorrencia | sempre | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| avancar.py --satisfazer-inegociavel | sempre | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| avancar.py --encerrar | etapa alvo em EX3 no nível apurado | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| avancar.py --encerrar | etapa alvo em EX4 no nível apurado | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| inegociaveis.py --satisfazer | sempre; wrapper chama operação humana | Permitida | NEGADO + TentativaNegada | Engenheiro no terminal |
| preparar-caso.sh | sempre; auxiliar chama operações humanas | Auxiliar não existia; guarda não reconhecia operação | NEGADO dentro do caso | Engenheiro no terminal |

Há **11 declarações**, com uma declaração de encerramento cobrindo EX3/EX4.
Os nomes e condições acima estão apenas nos dados do playbook e no campo.
A lista inclui os caminhos indiretos executáveis do pacote, evitando que o
wrapper de satisfação ou o auxiliar do caso substituam a chamada direta.

| Preparação/leitura | Depois |
|---|---|
| Governança em rascunho/proposto | PERMITIDO |
| Operacional em proposta | PERMITIDO |
| Rotina/ciclo de calibragem com recomendação, sem decisão | PERMITIDO |
| Leitura de registro e de scripts | PERMITIDO |
| Gravação pelo validador e curadoria | PERMITIDO |
| Emissão/materialização por entregaveis.py | PERMITIDO |
| Verificação de inegociável sem --satisfazer | PERMITIDO |
| Encerramento EX1/EX2 em chamada simples | PERMITIDO |

Permissão na guarda não substitui validações posteriores do script: sessão,
selo, estrutura, autoria, evidência e portões existentes continuam vigentes.

## Testes novos — negativos primeiro

Módulo: **testes/decisao_a12.py**, **37 verificações** (26 negativas e 11 positivas).

Antes de modificar o núcleo, negativos.sh teve 51 verificações e contexto.py,
11, sem falhas. Os primeiros 30 testes de A12 foram executados contra o
congelamento: **21 falhas**, mostrando as operações que a guarda permitia e
a ausência da declaração no template. Os negativos adicionais do wrapper e
do auxiliar foram executados contra o núcleo congelado: **2 falhas em 2**.
Os quatro testes das formas adicionais de shell foram escritos e executados
antes da correção dessas formas: **4 falhas em 4**. Saídas preservadas.

Após a correção, **37/37 passaram**. Cobertura:

- cada operação da lista, com nome humano, mensagem, comando, evento e estado preservado;
- camada da etapa alvo, não cache/camada de outra etapa;
- argumento em formato --opcao=valor, cadeia de comandos e shell interno;
- candidato ausente/ilegível; lista ausente e tipo de condição desconhecido;
- contrato de outro método com outro script, aplicado sem mudar o núcleo;
- rascunho proposto, proposta operacional, recomendação sem decisão e leitura;
- validador, curador, materialização/emissão e verificação sem satisfação;
- encerramento em EX2, inclusive mesma etapa em N1; texto de comando sem execução;
- execução direta de apuração no terminal e declaração do template;
- satisfação por wrapper e auxiliar automático de controle;
- mudança de contexto em comando composto, opção de interpretador com valor,
  execução por módulo e código inline referindo componente de decisão.

O avaliador não executa shell nem decide por modelo. A inspeção é dirigida às
invocações e condições declaradas; não é autenticação do sistema operacional
nem um sandbox para todo programa arbitrário. O disco e o terminal do
engenheiro permanecem a fronteira de confiança do projeto. Foram testadas
as formas de chamada registradas acima; não se afirma contenção universal
de código ofuscado ou de executáveis arbitrários fora desse contrato.

## Todos os testes existentes ajustados

| Arquivo/teste | Antes | Ajuste |
|---|---|---|
| campo_2_6_2.py — 2.6.2-T19 | Chamada Bash de governança aceita sem rascunho correspondente | Prepara AUT-002 proposto e testa somente a preparação permitida, conforme solicitado |
| nucleo_2_6_1.py — 2.6.1-T22 | Apuração por Bash da sessão era aceita | Agora exige exit 2 e mensagem de terminal humano, com o mesmo nome humano informado |

Nenhum teste existente apagado. Os demais testes que chamam scripts diretamente
continuam simulando o terminal do engenheiro, e suas expectativas permanecem.
Contagens dos dois módulos ajustados preservadas: 38 e 39, respectivamente.

## Comandos, habilidades e demonstrações

Atualizados os comandos do núcleo de apuração, sessão, campos, recorrência,
inegociáveis e encerramento; comandos do campo operacionalizar, governar e
recalibrar; habilidades correspondentes, incluindo medir/pilotar/medir-valor
quanto à satisfação de inegociáveis. O comando emitir esclarece que o agente
verifica/materializa, mas entrega a satisfação ao engenheiro. README e
INSTALACAO descrevem o fluxo e mantêm os testes de sessão/selo no terminal.
Os comandos entregues usam o caminho absoluto real do plugin, sem depender
de variável disponível apenas à sessão.

Auxiliares em `.projectdocs/demos/`:

- `como-agente.sh "<comando>"`: envia Bash à guarda, imprime PERMITIDO/NEGADO
  com motivo e não executa a operação;
- `preparar-caso.sh <nome> <ate-etapa>`: executado no terminal, abre caso
  sintético com responsável Celso do Vale, apura N2 por DAD 5/GOV 3/CRI 6,
  mantém etapa alvo corrente, registra as sessões exigidas (inclusive a alvo),
  selo após P2, classificação de P5 e candidatos/registros OP-001 e AUT-001
  conforme o percurso. AUT-001 fica proposto; OP-001 está validado ao chegar
  a P7. Base padrão /tmp/emcia-demos, configurável por EMCIA_DEMO_BASE.

Demonstração real preservada em demonstracao-terminal.txt: P7 corrente com
sessão, nível N2 e classificação agente. AUT proposto é permitido; o mesmo
comando com AUT decidido é NEGADO pela guarda, mas é executado diretamente
no terminal com sucesso e registra o termo decidido. demonstracao.txt guarda
também leitura permitida e sessões/operacional negados. Todos os dados são
sintéticos. Não houve aplicação em campo.

## Suíte completa

| Módulo | Verificações | Falhas |
|---|---:|---:|
| negativos.sh | 51 | 0 |
| autoria_responsavel.py | 14 | 0 |
| campo_2_6_2.py | 38 | 0 |
| campo_2_6_3.py | 57 | 0 |
| campo_2_6_4.py | 50 | 0 |
| campo_2_6_5.py | 62 | 0 |
| campo_2_6_6.py | 43 | 0 |
| campos_a10.py | 18 | 0 |
| consolidado.py | 16 | 0 |
| contexto.py | 11 | 0 |
| ctx_v.py | 23 | 0 |
| curadoria.py | 17 | 0 |
| decisao_a12.py | 37 | 0 |
| emissao_a9.py | 13 | 0 |
| esforco.py | 1 | 0 |
| habilitacao.py | 19 | 0 |
| integracao.py | 17 | 0 |
| metodo_empacotado.py | 1 | 0 |
| nucleo_2_6_1.py | 39 | 0 |
| nucleo_yaml.py | 7 | 0 |
| p3d.py | 12 | 0 |
| playbook_2_6_0.py | 29 | 0 |
| sessao_a8.py | 23 | 0 |
| triagem_a7.py | 24 | 0 |
| verificacao_por_estados.py | 7 | 0 |
| **Total (25 módulos)** | **629** | **0** |

Comparação: **592 anteriores + 37 A12 = 629**. suite.txt contém todos os
comandos, a saída integral e as contagens. Conferidos códigos de saída e
mensagens de falha, inclusive módulos que podem devolver zero ao imprimir
falha. Nenhuma expectativa foi relaxada para fazer uma recusa passar.

## Entrega e versões

- fix(A12): `e295542`.
- docs: `065cc3b` (decisão 027 e revisão da 019).
- docs(evidence): este pacote, em commit separado.
- diff.patch: diferença exata de v-sprint3-poc.3 até correção e documentação.
- Tag anotada da entrega: v-sprint3-poc.4, sobre o pacote completo.

Núcleo **0.2.26**, campo **0.8.4**, playbook **0.4.7**. Casos existentes
atualizam explicitamente sua lista; não há fallback ao playbook do plugin.
Nenhum sinalizador desativa a guarda; nenhuma dependência nova. Tags
anteriores preservadas.

Edições anteriores em 3.1/suite-congelamento.txt, 3.2/testes-f0.txt, e os novos
arquivos locais 3.4/testes-f2.txt e 3.9/ ficaram fora destes commits.
