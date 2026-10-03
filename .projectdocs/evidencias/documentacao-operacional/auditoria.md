# Auditoria documental — 03/10/2026

Referência: código no HEAD de partida d5924c0 e commit canônico 1d6d1e8.
A auditoria utiliza os scripts existentes; não modifica sua execução.

| Texto | Fonte executável e resultado |
|---|---|
| README/INSTALACAO: abertura, destino, identidade e cópia SHA-256 | novo-caso.sh e abrir_caso.py: parse_intermixed_args, pacote antes de criar, expediente opcional, importação separada; commit inicial pode falhar |
| Habilitação administrativa: 17 operações e entradas | habilitacao.py: iniciar/estado/tratamento/receber/pendencia/resolver/reabrir/consolidar/revisar/gerar/liberar/assinatura/ocorrencia/concluir-0b/acessos/preparar-0d/nao-prosseguir; consulta de estado sem entrada; gerar usa templates intactos e navegador |
| Importação e ordem de canais | importar_habilitacao.py: definição prévia ou --canais; migra origem e valida versão; mesmo caso e responsável; reimportação só antes de encerrar etapas |
| Planejamento/definição/resolução | canais.py: planejar somente leitura; definir --entrada e versão sequencial; resolver alvo/direção; ids conforme ferramenta, proprietário, filtro e marcador |
| Coleta | receber.py: arquivo/manifesto em rascunho/entrada, datas com fuso, coleta >= modificação, decisão --nova-versao, REC/hash preservados |
| Publicação registrada | entregar.py: --entrada em rascunho, versão/hash/emissão/arquivo/destino e destinatário nominal, data ISO; sem aceite |
| Listagem e MCP | registrar_listagem.py e escopo_externo.py: ferramenta/argumentos/contêiner/lista/data, registro humano, hash, ids limitados; confirmação no chat não é autenticada pelo script |
| Restrição | restricoes.py: vincular/dispensar, --restricao, --fontes ou --motivo, revisão --nova-versao; vínculo inicial em P2 aberta, posterior só revisão de vínculo existente após P2 encerrada |
| F0 e P3b | playbook e confirmação de selo do Git em 039/042: importação selada e selo posterior ao último encerramento de P2; evento sem commit não satisfaz |
| Sessões externas | avançar e playbook: referência opcional no template, canal e marcador coerentes quando presente |
| Estado | estado.py: etapa/camada, selo e diagnóstico da referência; não foi atribuída exibição de canais inexistente |
| Fontes | importação e receber.py são os caminhos de preservação de bytes; validador/curador recebem rascunhos e não escrevem fontes |

MAN-01 v0.1 continua recuperável no commit canônico 968281c. MAN-01 v0.2 é
conferido diretamente com lista vazia, sem sobreposição local. A comparação
canônica cobre também HAB-01 e os auxiliares, necessários para resolver as
citações sem acesso à rede. O README local antigo do pacote foi retirado,
preservando dentro de metodo/ somente bytes canônicos e manifesto.

Os textos originais das decisões não foram reescritos. O grep histórico mostra
os dois registros canônicos da renomeação e o contexto antigo da decisão 039;
nenhum é remissão operacional ao roteiro retirado. As emendas explicam a
retirada CTX e a atualização do manual. Não houve divergência de seção cujo
destino precisasse ser escolhido por semelhança de título.

Limites mantidos: assinatura integrada, aceite, gravação/transcrição fora do
escopo; identidade/origem remota não autenticadas; hash fixa bytes; runtime E7
apenas Claude Code 2.1.283, MCP stdio sintético. Pendências 020 e carta mantidas.

A suíte final passou com 926 verificações em 47 módulos em Python 3.12.12.
Nenhuma exclusão, nenhum dado real de cliente, nenhuma alteração no núcleo ou
nos scripts de campo. Um commit por item; nenhum push.
