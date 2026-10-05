# Evidência — habilitação simplificada (047)

**Data:** 05/10/2026 · **Autor:** Celso do Vale · **Origem:** pedido do engenheiro.
Campo 0.8.30, playbook 0.4.22, núcleo 0.2.48. Pacote metodo-v1.0 intacto.

## Regressão

| Execução | Python 3.12.12 | Python 3.14.4 | Resultado |
|---|---:|---:|---|
| Inicial, HEAD 70702c6 | 1109 / 53 módulos | 1111 / 53 módulos | Somente A25 conhecida |
| Integral, base 028e92a + rascunho item 8 | 1140 / 54 módulos | 1142 / 54 módulos | Somente A25 conhecida; zero inesperadas |
| Específicos após recusa de campos extras | 31 | 31 | Todos passam |

Logs integrais em inicial-3.12.txt, inicial-3.14.txt, final-3.12.txt e
final-3.14.txt. Nenhum módulo excluído. O checkout temporário canônico aponta
à tag metodo-v1.0, 08bfb162d762935ed35f55e0a75bc700b81d5276; templates desse
checkout também conferidos contra o APR-01. O checkout habitual com minutas
posteriores não foi alterado. Uma tentativa final iniciada no diretório habitual
foi interrompida antes de concluir; os logs finais são das árvores isoladas.

A25 permanece inalterado, com saída 1 somente em test_01, quatro negativas
passando e a divergência exata `ato humano selar-apos-P2 ausente das seções 3.3
e 3.4`. O runner confirma lista, teste e código; não tolera outra falha. As duas
verificações adicionais em 3.14 decorrem de PyYAML disponível nesse ambiente.

Depois da regressão integral, a revisão da coleta encontrou que campos extras
ignorados poderiam ser preservados pelo evento da entrada. O negativo em
entrada-extra-antes.txt reproduziu a falha. Coleta/mensagem agora recusam campos
extras antes da persistência. Os 31 específicos finais foram executados nas duas
versões após essa alteração; arquivos especificos-finais-3.12.txt/3.14.txt.
A seleção entre múltiplas submissões também passou a mostrar somente ids do
caso (até dez), sem expor respostas ou ids de outro caso; negativo em
selecao-antes.txt e específicos finais nas duas versões. As demais verificações
integrais não foram repetidas, pois não mudaram.

Os arquivos item-N-antes/depois documentam cada incremento; importações/rotas
inexistentes também foram vistas falhando antes da implementação. Não substituem
os negativos que reproduzem as travas e os logs finais. A validação de autoria
recebe explicitamente o playbook na declaração nova, em vez de depender do cwd;
o commit do item 7 foi emendado depois da correção e verificações verdes.

## Percurso e custo

| Medida | Anterior (045, fixture no commit 70702c6) | Simplificado (047) |
|---|---:|---:|
| Grupos de aprovação por caso | 5 | 3 |
| Conferência de formulário por caso | 1 | 0 (preparação permanente reutilizada) |
| Chamadas públicas de script modeladas | 93 | 7 |
| Depósitos na pasta de entrada | Arquivos apontados individualmente | 2 |
| Formulários de esclarecimento | Caminho com rodada Tally | Mensagem manual, uma rodada |
| Drive antes de F0 | Raiz e cinco pastas | Nenhum |

percurso-antes.json provém de medir-percurso-anterior.py executado na árvore
70702c6. Conta aprovar, operar, retomar e retorno; exclui perfil/aceitação
reutilizáveis. Não conta hooks, helpers internos ou APIs. A fixture antiga testa
uma rodada com fonte recebida; a instrumentação não mede criação de formulário
da rodada nem latência real. São chamadas públicas modeladas, não medições de
sessão Claude ou tokens. A configuração inicial, calibração, situação jurídica
e conferência dos permanentes são preparação reutilizável, fora do percurso.

percurso-depois.json é produzido por test_80: sete chamadas proximo até F0
liberado, duas entregas de arquivos e três confirmações com literal ok. O CSV
contém CASO, OUTRO-A e OUTRO-B. Todo arquivo do expediente é verificado contra
SEGREDO-OUTRO; somente a linha CASO e seu hash entram, com hash do original sem
copiá-lo. Há uma mensagem M1, três PDFs separados, nomes/datas/evidências,
restrição RH importada, canais Tally/calendário, validação, selo Git e checklist.
Retomada conserva bytes do expediente, sem repetir operação/aprovação.

Test_81 usa P2 aberta como fixture depois de F0 liberado: canal documentos ausente
bloqueia; uma confirmação aprova seis criações e quatro compartilhamentos. Os
hooks conferem as chamadas e retornos sintéticos. A definição final libera a
exigência de canal; raiz e trabalho-interno permanecem privados. O teste não
executa decisões de método pela sessão nem simula encerramento humano real.

Os negativos cobrem ausência/duas submissões, permanentes não conferidos ou contrato
alterado, relatório adulterado/nova leitura, pasta indevida, mensagem vazia,
tratamento ausente, ausência de cada aprovação, PDF divergente, bytes alterados,
matriz não confirmada, pasta antes de P2, comando composto e saída sem outro caso.

## Cartão e limites

cartao-conferencia.txt registra geração real por Chrome com sandbox padrão,
uma página A4 e extração de texto pelo Poppler/pdftotext. O cartão é o único
material carregado pelo comando normal; referência extensa só em preparação,
lacuna de interface ou alternativa manual. Cada avanço tem resumo curto.

O percurso substitui navegador/extrator e MCP por fixtures sintéticas; assinaturas
não são autenticadas e nenhuma conta remota foi acessada. A conferência real do
cartão verifica as dependências de renderização/extração, sem cliente. Retorno
perdido de API exige conferir objeto por id antes de repetir. Dados operacionais
continuam posteriores à abertura e sujeitos à procedência. Decisões de método
continuam no terminal. Propostas canônicas em propostas-artefatos.md, sem edição
do pacote ou dos templates aprovados. SHA-256 em integridade.json fixa o código,
as evidências e a referência aprovados nesta verificação, sem hash autorreferente.
