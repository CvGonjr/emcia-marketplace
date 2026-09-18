# Pacote 2.5.1 — Matriz estrutural anterior à implementação

Produzida em 18/09/2026 sobre o HEAD
`5421c78edaeb074c3d14e61e6686be42431a2c56`, antes da alteração dos modelos.

Fonte principal: EMCIA-CTX-01 v0.4, seções 3.3 a 3.8 e condição de aceite.

## Contrato canônico extraído do CTX-01 v0.4

| Objeto | Campo | Obrigatório estrutural? | Tipo/formato | Significado | Restrição | Origem documental |
|---|---|---:|---|---|---|---|
| Termo | `id` | sim | string `T-NNN` | identificador estável | padrão por tipo | CTX-01 §3.3 |
| Termo | `termo` | sim | string não vazia | palavra do negócio | recorte do caso | CTX-01 §3.3 |
| Termo | `significado` | sim | string não vazia | sentido na organização | não é definição genérica | CTX-01 §3.3 |
| Termo | `nao_e` | sim | string não vazia | exclusão semântica | reduz significado vizinho | CTX-01 §3.3 |
| Termo | `sinonimos_em_uso` | sim | lista | sinônimos encontrados | pode ser vazia | CTX-01 §3.3 |
| Termo | `procedencia` | sim | `D | I | V` | estatuto documental | taxonomia única | CTX-01 §2 e §3.3 |
| Termo | `declarado_por` | sim | string não vazia | quem sustenta o conteúdo | sem regra comportamental neste pacote | CTX-01 §3.3 |
| Termo | `registrado_por` | sim | string não vazia | quem formalizou o registro | sem validação de autoria neste pacote | CTX-01 §3.3 |
| Termo | `data` | sim | data ISO | data do registro | formato estrutural | CTX-01 §3.3 |
| Termo | `premissa` / `evidencia` | condicional | string ou objeto | rastreia I ou V | I exige premissa; V exige evidência | CTX-01 §3.13, V02/V03 |
| Entidade | `id` | sim | string `E-NNN` | identificador estável | padrão por tipo | CTX-01 §3.4 |
| Entidade | `entidade` | sim | string não vazia | objeto do domínio | somente recorte necessário | CTX-01 §3.4 |
| Entidade | `atributos` | sim | lista | atributos relevantes | estrutura representável | CTX-01 §3.4 |
| Entidade | `relacoes` | sim | lista | relações com entidades | estrutura representável | CTX-01 §3.4 |
| Entidade | `onde_vive` | sim | lista de IDs `F-*` | fontes relacionadas | referência será validada no 2.5.4 | CTX-01 §3.4 |
| Entidade | `procedencia` | sim | `D | I | V` | estatuto documental | taxonomia única | CTX-01 §2 e §3.4 |
| Entidade | `declarado_por` | sim | string não vazia | quem sustenta o conteúdo | comportamento posterior | CTX-01 §3.4 |
| Entidade | `registrado_por` | sim | string não vazia | quem formalizou | comportamento posterior | CTX-01 §3.4 |
| Entidade | `data` | sim | data ISO | data do registro | formato estrutural | CTX-01 §3.4 |
| Entidade | `premissa` / `evidencia` | condicional | string ou objeto | rastreia I ou V | I exige premissa; V exige evidência | CTX-01 §3.13, V02/V03 |
| Regra | `id` | sim | string `RN-NNN` | identificador estável | contrato oficial usa `RN-*` | CTX-01 §3.5 |
| Regra | `enunciado` | sim | string não vazia | condição que governa ação/decisão | forma condicional vem do ROT-01 | CTX-01 §3.5; ROT-01 §3.4 |
| Regra | `gatilho` | sim | string não vazia | condição de acionamento | campo da ficha ROT-01 | CTX-01 §3.5/§3.8 |
| Regra | `procedencia` | sim | `D | I | V` | estatuto documental | taxonomia única | CTX-01 §3.5 |
| Regra | `autoria_conteudo` | sim | string não vazia | pessoa que enuncia/confirma | regra de pessoa será 2.5.2/2.5.4 | CTX-01 §3.5 |
| Regra | `registrado_por` | sim | string não vazia | engenheiro que formaliza | regra de pessoa será posterior | CTX-01 §3.5 |
| Regra | `data` | sim | data ISO | data do registro | formato estrutural | CTX-01 §3.5 |
| Regra | `origem_do_conhecimento` | sim | string não vazia | documento, ensino, experiência ou desconhecida | preservar saída do ROT-01 | CTX-01 §3.5/§3.8 |
| Regra | `premissa` / `evidencia` | condicional | string ou objeto | rastreia I ou V | I exige premissa; V exige evidência | CTX-01 §3.13, V02/V03 |
| Regra | `classificacao_confronto` | sim, presença | objeto | classe e referência ao P3d | sem obrigatoriedade referencial até 2.5.3 | CTX-01 §3.5 |
| Regra | `documento_de_origem` | sim, presença | string ou nulo | documento escrito associado | pode ser nulo | CTX-01 §3.5 |
| Regra | sete campos centrais | sim | escalares/listas | bloco interrogado por P4/P5 | todos estruturalmente presentes | CTX-01 §3.6 e CTX-V01 |
| Regra | `versao` / `historico` | sim, presença | inteiro/lista | estrutura de versionamento | comportamento I→V fica para 2.5.2 | CTX-01 §3.5/§3.12 |
| Fonte | `id` | sim | string `F-NNN` | identificador estável | padrão por tipo | CTX-01 §3.7 |
| Fonte | `fonte` | sim | string não vazia | nome da fonte | não inferir pelo nome | CTX-01 §3.7 |
| Fonte | `tipo` | sim | string não vazia | tipo da fonte | dimensão própria | CTX-01 §3.7 |
| Fonte | `responsavel` | sim | string não vazia | responsável pela fonte | pessoa/papel registrado | CTX-01 §3.7 |
| Fonte | `contrato.estrutura` | sim | string não vazia | forma dos dados | contrato mínimo | CTX-01 §3.7 |
| Fonte | `contrato.significado` | sim | string não vazia | o que registra de fato | não usar apenas o nome | CTX-01 §3.7 |
| Fonte | `contrato.qualidade` | sim | string não vazia | condição mínima observada | contrato mínimo | CTX-01 §3.7 |
| Fonte | `acesso` | sim | string não vazia | forma/condição de acesso | sem validação referencial neste pacote | CTX-01 §3.7 |
| Fonte | `procedencia` | sim | `D | I | V` | estatuto documental | taxonomia única | CTX-01 §3.7 |
| Fonte | `registrado_por` | sim | string não vazia | quem formalizou | comportamento posterior | CTX-01 §3.7 |
| Fonte | `data` | sim | data ISO | data do registro | formato estrutural | CTX-01 §3.7 |
| Fonte | `premissa` / `evidencia` | condicional | string ou objeto | rastreia I ou V | I exige premissa; V exige evidência | CTX-01 §3.13, V02/V03 |

## Schema atual × CTX-01 v0.4

| Objeto | Campo atual | Campo CTX-01 | Estado | Ação |
|---|---|---|---|---|
| Termo | `id`, `termo`, `significado`, `nao_e`, `sinonimos_em_uso`, `procedencia`, `data` | mesmos | CONFORME | manter |
| Termo | `autor` | `declarado_por`, `registrado_por` | MIGRAR | separar estruturalmente |
| Termo | `fonte` | `premissa` / `evidencia` condicionais | MIGRAR | substituir campo ambíguo |
| Entidade | `id`, `entidade`, `atributos`, `relacoes`, `onde_vive`, `procedencia`, `data` | mesmos | CONFORME | manter |
| Entidade | `autor` | `declarado_por`, `registrado_por` | MIGRAR | separar estruturalmente |
| Entidade | `fonte` | `premissa` / `evidencia` condicionais | MIGRAR | substituir campo ambíguo |
| Regra | `id: R-*` | `id: RN-*` | RENOMEAR | alinhar prefixo e nome do modelo |
| Regra | `enunciado`, sete campos centrais, `documento_de_origem`, `versao`, `historico` | mesmos conceitos | CONFORME | preservar e ajustar metadados internos |
| Regra | ausente | `gatilho`, `autoria_conteudo`, `registrado_por`, `origem_do_conhecimento` | ADICIONAR | materializar contrato oficial |
| Regra | `autor` | `autoria_conteudo`, `registrado_por` | MIGRAR | separar papéis sem impor comportamento |
| Regra | `estatuto` | sem campo correspondente | REMOVER | CTX-01 v0.4 não o utiliza |
| Regra | `divergencia` embutida | `classificacao_confronto` com referência | MIGRAR | remover duplicação; sem validar referência ainda |
| Regra | `premissa`, `evidencia` | mesmos | PARCIAL | alinhar forma e manter condição D/I/V |
| Regra | `historico[].autor` | `historico[].registrado_por` | RENOMEAR | alinhar vocabulário; comportamento posterior |
| Fonte | `id`, `fonte`, `tipo`, `responsavel`, `contrato`, `acesso`, `procedencia`, `data` | mesmos | CONFORME | manter |
| Fonte | `autor` | `registrado_por` | RENOMEAR | alinhar rastreabilidade |
| Fonte | `evidencia` escalar | `premissa` / `evidencia` condicionais | PARCIAL | permitir estrutura condicional |

## Instâncias encontradas

Busca em `/home/netiv-ai/Projetos`: quatro arquivos encontrados, todos modelos
do template deste repositório. Nenhuma instância real de caso foi localizada.
Logo, este pacote não executa migração de dados nem reescreve casos existentes.
