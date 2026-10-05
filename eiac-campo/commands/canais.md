---
description: Planeja canais por ids e conduz provisionamento aprovado, preservando o escopo e a definição versionada.
---
Uso: `/eiac-campo:canais [planejar|definir|resolver]`

Leia `reference/canais.md`, o CAN-01, ROT-02 e MAN-01 do pacote aprovado e a decisão
045. O fluxo completo é `/eiac-campo:iniciar`; não edite o método empacotado.

Planejamento é leitura. Apresente a árvore inteira junto da decisão de abrir e
obtenha sua aprovação; execute MCP somente com perfil de assinatura conferido,
id declarado e aprovação registrada. Outra aprovação cobre o conjunto de
compartilhamentos, listando destinatário, pasta/id e papel. Trabalho-interno não
é compartilhado com cliente. Não envie link, publique ou compartilhe sem aprovação.

Prepare a declaração pelos ids retornados e execute o ato local pelo wrapper
aprovado `iniciar.py executar`; `canais.py definir` no terminal é alternativa.
A ordem é abertura → planejar/provisionar → definir ou --canais → importar →
validar 00-habilitacao → selar → F0 liberado. Listagem e recebimento no bloco
podem ser executados pela sessão aprovada; fora de F0 use o terminal.

Ferramenta sem perfil fica recusada. Não amplie expressões nem busque clientes
pelo nome. Preserve manifestos, retornos e hashes; leitura por id exige listagem
íntegra do contêiner declarado. Caso antigo conserva o contrato anterior.
Aprovação e retorno são testemunhos locais, não autenticação remota.
