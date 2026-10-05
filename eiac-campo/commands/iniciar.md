---
description: Conduz habilitação por conectores, três confirmações e abertura com perfil aprovado.
---
Uso: `/eiac-campo:iniciar [id-da-habilitacao] [id-do-caso]`

Carregue somente `reference/cartao-habilitacao.md` no percurso normal.
Use `scripts/iniciar.py proximo --entrada <json-local>` por avanço e apresente
resumo, próximo passo, artefatos e hashes. Consulte a referência específica
somente para preparação, entradas, recusa ou alternativa manual.

Antes da abertura, Tally, Google Drive e Google Calendar funcionam sem perfil
nem escopo por id. Leia, liste, crie rascunhos e compare sem aprovação por chamada.
Não calibre na preparação. Publicação, envio de mensagem/convite e compartilhamento
exigem “ok” simples: registre chamada, resumo, trecho e data com iniciar.py aprovar.
O hook confere essa autorização. Nenhum efeito externo é autorizado por silêncio.

Leia todas as páginas de fetch_submissions; entregue o retorno ao script pelo
iniciar.py retorno. O script filtra pelo campo oculto caso antes de gravar a fonte.
Não selecione por semelhança, não transcreva o lote na conversa nem o copie para
o expediente. Zero ou várias submissões exigem indicação do engenheiro.
A exportação CSV é alternativa: coleta: csv. Esclarecimentos e matriz usam mensagem;
os três PDFs assinados são depositados em ~/emcia-op/entrada/.

Na terceira confirmação, apresente perfil/inventário/hash e escopo de canais junto
da abertura. O inventário fornecido é a fonte dos nomes/parâmetros para esse perfil.
A partir da existência do caso, perfil e escopo valem de F0 a P10; opere no contexto
do caso. Retornos administrativos não dão acesso a ids dentro do caso.

A decisão 047, item 9, emenda a 045. APR-01 rege os três templates separados;
o pacote não é editado. Pastas/canais Drive do caso continuam em P2. Decisões de
método permanecem no terminal. Confira objeto remoto antes de repetir API cujo
retorno foi interrompido; o script não executa APIs nem autentica retornos.
