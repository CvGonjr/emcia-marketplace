# emcia — marketplace de plugins

O método é conferido pelo manifesto SHA-256 antes de abrir cada caso. Comece pelo
[MAN-01 v0.2](eiac-campo/reference/metodo/EMCIA-MAN-01-manual-de-aplicacao.md),
conferido contra o playbook 0.4.18. O pacote foi extraído, sem edição manual, do
commit canônico `1d6d1e8bfc1739594ea7a119257ecae28c8e5af4` de
[emcia-artefatos](https://github.com/CvGonjr/emcia-artefatos).
O manifesto v4 identifica origem, data, caminhos canônicos e hashes dos 21
documentos, incluindo CAN-01, HAB-01, ROT-02 e o fluxo auxiliar. Empacotar uma
revisão não altera seu estado nem lhe atribui aprovação.

Este repositório é a ferramenta. Casos e dados de clientes vivem em repositórios
próprios; não entram no marketplace.

| Plugin | Versão | Papel |
|---|---|---|
| eiac-nucleo | 0.2.44 | Guarda, procedência, etapas e trilha; aplica o contrato do caso |
| eiac-campo | 0.8.22 | Método, habilidades, comandos, scripts e template de caso |

O núcleo lê `registro/playbook.json` do caso. Atualizar o plugin não substitui
esse arquivo nem migra casos em andamento. Camadas EX1–EX4 e procedência D/I/V
são resolvidas deterministicamente; autoria vem do responsável nomeado.

## Instalação

No Claude Code:

```text
/plugin marketplace add CvGonjr/emcia-marketplace
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

Requisitos: Python 3.12 ou superior no PATH, Git e Claude Code. Para gerar PDFs
HAB, instale Google Chrome ou Chromium. Configure os conectores de Tally, Google
Drive e Google Calendar no Claude Code e confira seus ids, ferramentas e
argumentos. A demonstração real de hooks MCP da evidência E7 usou Claude Code
2.1.283, com ferramenta stdio sintética. Veja [INSTALACAO.md](INSTALACAO.md).

## Da habilitação a F0

A ordem operacional é:

**habilitação → abertura (`novo-caso.sh`) → planejar e provisionar canais →
definir canais (`canais.py definir`, ou na importação com `--canais`) → importar
expediente → gravar `00-habilitacao` pelo validador → selar → F0.**

1. No terminal do engenheiro, inicialize o expediente fora de repositórios e
   casos. O comando `/eiac-campo:habilitacao` prepara a coleta administrativa e
   registra decisões comunicadas por pessoas. Tratamento administrativo deve
   ser registrado antes de consultar submissões pelo MCP. HAB-01/02/03 continuam
   sendo os três templates e os códigos dos PDFs da formalização.
2. Conclua formalização e acessos, confira `preparar-0d` e abra o caso com o
   identificador reservado e o mesmo responsável. A abertura confere todos os
   hashes, copia os documentos e o manifesto para `metodo/` e prepara o Git.
   `--expediente` é opcional na abertura; quando informado, confere prontidão e
   identidade, sem executar a importação.
3. Em caso aberto, `/eiac-campo:canais` usa `canais.py planejar` para propor a
   estrutura. Provisionamento pelo MCP exige um contêiner previamente declarado,
   exclusivo do caso, com regra compatível. Sem ele, provisione pela interface
   externa. Cada criação, publicação, envio, convite e compartilhamento exige
   confirmação explícita no chat; cada compartilhamento apresenta destinatário,
   endereço, id e papel e recebe sua própria confirmação.
4. O engenheiro define a declaração de ids pelo terminal, antes da importação.
   Alternativamente, passa a declaração completa com `--canais` ao importador.
   Na migração, o importador preserva os ids dos formulários e a origem do
   expediente. Não busca por nome nem inventa workspace ausente.
5. O engenheiro importa o expediente. Só os três PDFs assinados, suas evidências
   e a matriz administrativa entram em `fontes/habilitacao/`; o importador prepara
   `rascunho/00-habilitacao.md`. Respostas brutas não são copiadas para o caso.
6. Grave pelo validador e sele deliberadamente. F0 exige o evento de importação
   coberto por selo confirmado no histórico Git. Evento `SeloAplicado` deixado por
   commit recusado mantém F0 bloqueado.

Exemplos de chamadas, com caminhos e identidade preenchidos pelo engenheiro:

```bash
python3 eiac-campo/scripts/habilitacao.py iniciar --expediente /base/habilitacoes/HAB-0001 --id HAB-0001 --caso caso-0001 --responsavel "Nome Sobrenome"
./novo-caso.sh caso-0001 /base/casos --responsavel "Nome Sobrenome" --expediente /base/habilitacoes/HAB-0001
cd /base/casos/caso-0001
python3 /checkout/emcia-marketplace/eiac-campo/scripts/canais.py planejar
python3 /checkout/emcia-marketplace/eiac-campo/scripts/canais.py definir --entrada rascunho/canais.json
python3 /checkout/emcia-marketplace/eiac-campo/scripts/importar_habilitacao.py --expediente /base/habilitacoes/HAB-0001
python3 /checkout/emcia-marketplace/eiac-nucleo/scripts/validar.py --arquivo caso/00-habilitacao.md
python3 /checkout/emcia-marketplace/eiac-nucleo/scripts/selar.py --nota "habilitação importada e conferida"
```

A declaração de canais é preparada e conferida antes de executar os exemplos;
`planejar` não cria recursos nem grava ids. Destino padrão da abertura é
`~/casos/<nome>`; a base opcional não pode estar dentro de repositório. O caso
não nasce com remote. Configure a identidade Git para os commits.

Procedimentos: [HAB-01](eiac-campo/reference/metodo/EMCIA-HAB-01-protocolo-de-habilitacao.md),
[CAN-01](eiac-campo/reference/metodo/EMCIA-CAN-01-protocolo-de-canais-externos.md) e
[ROT-02](eiac-campo/reference/metodo/EMCIA-ROT-02-roteiro-de-habilitacao.md).
O caminho canônico do roteiro é `auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md`.
Interfaces e entradas: [habilitação](eiac-campo/reference/habilitacao.md) e
[canais](eiac-campo/reference/canais.md).

## Percurso e atos humanos

O template declara 13 etapas. A camada depende de N1/N2/N3; a tabela mostra N2.
A tabela completa, com atos e produtos, é MAN-01 §3.3.

| Etapa | Comando do campo | Camada N2 |
|---|---|---|
| F0 | enquadrar | EX1 |
| P1 | mapear-contexto | EX2 |
| P2 | mapear-fontes | EX2 |
| P3a | medir | EX3 |
| P3b | Sem comando delegável | EX4 |
| P3d | confrontar | EX3 |
| P4 | priorizar | EX3 |
| P5 | classificar | EX3 |
| P6 | operacionalizar | EX3 |
| P7 | governar, para preparar a minuta | EX4 |
| P8 | pilotar | EX3 |
| P9 | medir-valor | EX3 |
| P10 | recalibrar, para preparar recomendação | EX4 |

Use `/eiac-nucleo:estado` e `/eiac-nucleo:fronteira` na raiz do caso.
Habilidade não delegável não carrega pela sessão, mesmo com sessão humana e
selo. Camadas humanas exigem sessão da própria etapa para encerrar. Os produtos
exigidos são conferidos no encerramento conforme o playbook.

Definir canais, importar expediente, registrar listagem, receber material,
registrar entrega e vincular ou dispensar restrição são atos humanos no
terminal. Também são humanos apuração do nível, sessão, campos, recorrência,
inegociáveis, decisões dos registros e encerramento em EX3/EX4. O agente prepara
os argumentos e entrega o comando com caminho absoluto. Confirmação no chat
não autoriza executar esses atos pela sessão; a guarda recusa com evento.

Em P2, o engenheiro usa `restricoes.py vincular --restricao RH-xx --fontes F-xxx`
ou `dispensar --restricao RH-xx --motivo <motivo>`; o ato declarado chama-se
`vincular-restricao`. Cada RH importado precisa estar vinculado a fonte curada
ou dispensado com motivo para encerrar P2. Revisões preservam histórico e exigem
`--nova-versao` com decisão explícita; fora de P2 só cabe revisar vínculo existente
após P2 encerrada. Sem RH, a coleção vazia satisfaz a cobertura.

## Materiais, canais e emissão

Coletas são preparadas em `rascunho/entrada/`. O engenheiro registra listagem
prévia limitada a contêiner declarado e executa `receber.py --arquivo <arquivo>
--manifesto <json>`. O recebimento preserva bytes, hash e origem em
`registro/recebimentos.json`, com id REC. `fontes/` só recebe material pela
importação administrativa e por `receber.py`; não há cópia direta pelo agente.

A curadoria produz fontes F em `contexto/` a partir de rascunhos. Relações REC → F
são explícitas. Consulte o instrumento canônico
[EMCIA-CTX-01](eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md).
As duas cópias antigas foram retiradas por decisão humana registrada na emenda
à decisão 021. Declaração recebida não se torna V automaticamente.

`/eiac-campo:emitir` materializa os registros; o núcleo confere portões, arquivo,
versão e hash para a emissão. RH pendente bloqueia a materialização de E1–E5
antes da escrita. Em caso restrito, E1 fica pendente até resolver RH em P2.
Cada asserção afetada recebe RH, F, item negado, restrição e motivo no próprio
ponto; não existe ressalva genérica que substitua esse vínculo.

| Entregável | Portão |
|---|---|
| E1 | F0 |
| E2 | P1, P2, P3a, P3b, P3d |
| E3-D / E3-E | P4 / P5; E3-E segue a condição tecnológica declarada |
| E4 | P6, P7 |
| E5 | P8, P9, P10 |

Inegociáveis e condições específicas continuam exigidos; veja
[gates.md](eiac-campo/reference/gates.md). Após publicação confirmada no canal
`entregas`, o engenheiro executa `entregar.py --entrada <json>`; confere versão,
hash, emissão, arquivo e destino declarado. O registro não constitui aceite.

Sessões podem ter referência Calendar, canal e marcador `[caso/etapa]`.
No template a referência externa é opcional; o caso pode exigi-la por camada.
Quando informada, ela sempre precisa corresponder ao canal e ao marcador.

## Selos e guardas

F0 exige importação selada; P3b exige selo após o último encerramento de P2.
Ambos exigem confirmação no histórico Git, com nota, autoria e prefixo exato
da trilha. A ordem é a posição dos eventos, sem comparação de timestamps.
Git inacessível ou commit de selo recusado mantém a trava fechada. Um commit
comum não confirma tentativa recusada. `estado` exibe o último selo confirmado.

O estado declarado selado ao fim de P2 é confrontado com o levantamento de
P3b/P3d no mesmo caso. A execução independente de contraste foi retirada
pela decisão 021. O aparato residual de isolamento permanece no código.

A guarda protege escrita em `caso/`, `contexto/`, `registro/` e `fontes/`, normaliza
caminhos e inspeciona redirecionamentos. Os hooks MCP leem as regras de
`registro/ferramentas-externas.json`: ids declarados, contêineres exclusivos e
listagem registrada limitam leitura; provisionamento tem regra própria; escrita
de material só vai a `entregas`. Ferramenta não declarada ou chamada incompatível
recusa. Ajuste nomes e argumentos ao conector instalado, pelo terminal.

## Verificação e atualização

```bash
bash testes/negativos.sh
python3 testes/contexto.py
python3 testes/metodo_empacotado.py
python3 testes/manual_a25.py
python3 testes/citacoes.py
```

A suíte completa usa Python 3.12; módulos e contagens estão em
[testes/README.md](testes/README.md). Negativa inesperadamente permitida é regressão
de trava. As evidências deste pacote estão em
[documentacao-operacional](.projectdocs/evidencias/documentacao-operacional/).
Demonstrações sintéticas: `.projectdocs/demos/preparar-caso.sh`,
`como-agente.sh` e `percurso-completo.sh`; este último congela o HEAD commitado.

Atualize os plugins pelo marketplace e reinicie a sessão. Migração de caso exige
decisão humana e atualização explícita do seu contrato. Versão do plugin, versão
do playbook e versão do manifesto são registradas separadamente. Mudança em
scripts do núcleo exige incremento da versão do núcleo; nesta revisão apenas
campo e documentação foram alterados.
