# 040 — Canais externos declarados por caso

**Data:** 02/10/2026 · **Estado:** arquitetura aprovada pelo pedido; implementação por pacotes E1–E7

## Contexto

A decisão 008 exige procedência na fronteira de contato com o cliente. A 002
fixa o playbook no caso; a 019 atribui autoria nominal; a 027 reserva decisões
ao terminal humano. A 039 estabelece a passagem administrativa e o selo de F0.
Os canais externos precisam identificar o caso sem buscas por nome nem acesso
ao espaço de outra organização.

## Decisão

O campo declara finalidades e direções no playbook. O caso declara endereços
concretos em `registro/canais.json`, com ids, proprietário, acesso, filtro e
marcador. A definição é humana, versionada, preserva versões anteriores e
produz `CanaisDefinidos`. A guarda nega o ato pela sessão, com `TentativaNegada`.
Planejamento e resolução são delegáveis. Etapas com exigência declarada recusam
carregamento e encerramento sem definição íntegra correspondente.

O núcleo lê contratos e registros genéricos. Ferramentas e convenções ficam
no campo e nos dados do caso. Scripts não chamam APIs e não recebem dependências
novas. O agente usa somente conectores disponíveis e ids declarados; prepara
coletas em `rascunho/entrada/`, preservando o manifesto de origem.

Recebimento e registro de entrega são atos humanos. Recebimento confere canal,
etapa, filtro e hash; entrega confere emissão, versão, hash e destino. Recusas
produzem `TentativaNegada`. Não há registro de aceite neste escopo.

Criação, compartilhamento, publicação, envio e convites exigem confirmação
explícita do engenheiro no chat. Cada compartilhamento apresenta destinatário,
id de destino e papel e exige confirmação própria. Confirmação não delega
os atos humanos do terminal.

## Premissas e limites de confiança

O planejamento pressupõe workspace de formulários, drive compartilhado e
calendário sob propriedade EMCIA. Canais de propriedade do cliente podem ser
declarados explicitamente; não se presume autorização nem se procura por nome.
Nomes das cinco divisões do drive são convenções de provisionamento; roteamento
é exclusivamente por id. `trabalho-interno` não admite acesso do cliente.

Os scripts verificam coerência entre manifestos trazidos pelo agente e o
contrato local; não autenticam origem, conteúdo remoto, identidade real,
permissões efetivas, recebimento pelo destinatário ou realização da sessão.
SHA-256 fixa os bytes registrados, sem provar veracidade. Como em 022, acesso
humano de escrita ao disco é a fronteira de confiança.

E7 depende de teste real dos hooks PreToolUse em uma ferramenta MCP local sintética. Sem comprovação de disparo, não se apresenta trava de escopo como implementada.

## Consequências

Casos existentes conservam seu playbook e requerem migração humana deliberada.
Não há flag de dispensa. Não se altera `reference/metodo/`; propostas canônicas
ficam nas evidências de cada pacote. A referência do pedido ao TRI-01 foi
corrigida por confirmação expressa: §3.3 para perguntas, §3.4 para pontuação.

Evidências: `.projectdocs/evidencias/canais-externos/`.
