---
description: Conduz habilitação por conectores, três confirmações e abertura com perfil aprovado.
---
Uso: `/eiac-campo:iniciar [id-da-habilitacao] [id-do-caso]`

Carregue somente `reference/cartao-habilitacao.md` no percurso normal.
Use `scripts/iniciar.py proximo --entrada <json-local>` por avanço e apresente
resumo, próximo passo, artefatos e hashes. Consulte a referência específica
somente para preparação, entradas, recusa ou alternativa manual.

No início da coleta, apresente o nome operacional, id e link de `formulario`
retornado por `proximo`. Use o permanente conferido na configuração; não peça
escolha por título no Tally nem crie uma cópia por cliente. O nome operacional
não é uma leitura atual do título remoto. Sem permanente válido, conduza a
conferência contra `reference/formularios/habilitacao.json` e aguarde “conferido”.

Antes da abertura, Tally, Google Drive e Google Calendar funcionam sem perfil
nem escopo por id. Leia, liste, crie rascunhos e compare sem aprovação por chamada.
Não calibre na preparação. Publicação, envio de mensagem/convite e compartilhamento
exigem “ok” simples: registre chamada, resumo, trecho e data com iniciar.py aprovar.
O hook confere essa autorização. Nenhum efeito externo é autorizado por silêncio.

Leia todas as páginas de fetch_submissions; entregue o retorno ao script pelo
iniciar.py retorno, usando a chamada apresentada por proximo. O script filtra
pelo campo oculto caso e gera o CSV automaticamente no expediente. Apresente
o caminho csv retornado e siga com proximo para os esclarecimentos e documentos.
Não peça exportação, download ou depósito de CSV ao engenheiro no fluxo padrão.
Se faltar o nome do respondente, peça apenas a identificação nominal e informe
respondente na chamada local, sem enviá-lo como parâmetro da API.
Não selecione por semelhança, não transcreva o lote na conversa nem o copie para
o expediente. Zero ou várias submissões exigem indicação do engenheiro; mantenha
a coleta pelo conector e não troque para CSV manual por causa dessa recusa.
A exportação CSV é alternativa escolhida pelo engenheiro ou quando o conector
estiver indisponível: coleta: csv, com exportacao indicando o caminho
original. Esclarecimentos e matriz usam mensagem. Receba os três PDFs assinados
pelos caminhos originais ou pelo Drive, sem exigir exportação/movimentação do
engenheiro para ~/emcia-op/entrada/. Essa pasta permanece alternativa.

Para arquivos do Drive, peça o link/id quando faltar; execute
mcp__claude_ai_Google_Drive__download_file_content com fileId pelo fluxo MCP
administrativo. Salve os bytes exatos do retorno em temporário externo aos
repositórios e ao caso; não reconstrua nem converta PDF assinado. A sessão prepara
assinados (três caminhos) e evidencias (mapa opcional por código HAB) para proximo,
inclusive quando os arquivos vierem de pastas distintas. O script associa por
conteúdo, importa e calcula hashes. Remova temporários criados pela sessão após
o recebimento bem-sucedido; preserve arquivos originais do engenheiro.
Não peça CSV, download manual nem JSON preparado pelo engenheiro quando o
conector estiver disponível. A sessão prepara as entradas técnicas.

Na terceira confirmação, apresente perfil/inventário/hash e escopo de canais junto
da abertura. O inventário fornecido é a fonte dos nomes/parâmetros para esse perfil.
A partir da existência do caso, perfil e escopo valem de F0 a P10; opere no contexto
do caso. Retornos administrativos não dão acesso a ids dentro do caso.

A decisão 047, item 9, emenda a 045. APR-01 rege os três templates separados;
o pacote não é editado. Pastas/canais Drive do caso continuam em P2. Decisões de
método permanecem no terminal. Confira objeto remoto antes de repetir API cujo
retorno foi interrompido; o script não executa APIs nem autentica retornos.
