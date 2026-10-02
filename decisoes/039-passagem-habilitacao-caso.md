# 039 — Passagem da habilitação ao caso

**Data:** 02/10/2026 · **Estado:** decisão aprovada; implementação por pacotes

## Contexto

A solicitação prevê importação humana do expediente, pré-condição declarativa
de evento selado para F0, cópia conferida do método e restrições nos entregáveis.
A decisão 022 estabelece o expediente separado; a 021 estabelece comparação
por ordem de eventos para o selo posterior. A decisão 035 confirma o selo
exibido pelo histórico Git e declara expressamente que não altera a máquina
de etapas nem G7.

O protocolo canônico EMCIA-HAB-01 v0.2, §3.3.4, exige estado inicial selado.
O roteiro canônico exige gravar o desfecho e selar antes de F0. O checkout
consultado de emcia-artefatos está no commit `ab09abe`.

Foi reproduzida uma divergência: `selar.py` registra `SeloAplicado` antes do
commit; quando o commit falha, o evento permanece. `estado.ultimo_selo()`
corretamente devolve ausência de selo confirmado, enquanto
`playbook.selo_apos_etapa()` aceita esse mesmo evento para autorizar passagem.
Reutilizar somente esse padrão na nova pré-condição permitiria passagem sem
estado efetivamente selado. A reprodução usa exclusivamente dados sintéticos.

## Decisão

A implementação foi inicialmente interrompida para registrar a divergência.
Em seguida o usuário aprovou expressamente a confirmação pelo histórico Git
para a nova trava e autorizou prosseguir com os pacotes A–D.

**Decisão aprovada:** a nova exigência `exige_evento_selado` deve conferir
um selo confirmado no histórico Git, posterior ao evento exigido, incluindo
esse evento no conteúdo versionado. Evento deixado por commit recusado não
satisfaz essa exigência. A ordem da trilha continua sendo o ordenador, sem
comparação por timestamps. A regra anterior `exige_selo_apos` permanece com
o alcance registrado em 021 e 035 até decisão específica sobre sua mudança.

Sem histórico Git acessível, a nova trava recusa com TentativaNegada e motivo.
`selar.py` permanece inalterado. A confirmação é genérica, sem vocabulário do
método. A derivação do selo exibido em 035 é reutilizada.

**Achado próprio em P3b:** `exige_selo_apos` tem a mesma falha de aceitar
evento deixado por commit recusado. Por decisão expressa, permanece inalterado
neste pacote; migrá-lo para confirmação pelo Git exige pacote posterior e
decisão específica. Esta decisão não altera a regra anterior de 021.

O conflito de códigos entre o roteiro `EMCIA-HAB-02` e o template
`HAB-02-acordo-confidencialidade.md` permanece registrado. Nenhum documento
é renomeado nem sua correspondência é resolvida por inferência.

## Consequência

Pacote A: importação pelo terminal humano, declarada em `decisoes_humanas`.
Originais pertinentes entram em diretório por importação; nenhuma resposta
bruta ou documento operacional é copiado. A matriz exportada é conferida
contra o hash da entrada já preservada no expediente. O rascunho segue o
validador; não há escrita direta em caso/. Recusas produzem TentativaNegada.
Reimportação exige decisão que cite a importação anterior, antes de encerrar
qualquer etapa; mantém histórico e arquivos. Não implementa retomada durante
o percurso. O responsável fixado é autor de todos os eventos da importação.

O ato anterior ao percurso tem `escopo: antes_do_percurso`. A conferência do
manual §3.3/3.4 continua verificando os atos do percurso; o novo ato pertence
a §3.2, cuja atualização é proposta na evidência, sem editar o pacote controlado.

Há também referências preexistentes ao método no núcleo, incluindo `F0` em
`avancar.py`, `guarda.py` e `estado.py`. O critério literal de ausência de
termos no núcleo exigirá tratar essas referências; a busca foi preservada
na evidência. Isso não foi corrigido neste levantamento.

Evidências: `.projectdocs/evidencias/habilitacao-0d/`.

### Pacote B

O campo declara `exige_evento_selado` em F0; o núcleo verifica o último evento
exigido e um selo confirmado no Git que contém o prefixo exato da trilha,
com nota e autor correspondentes. Guarda de carregamento e encerramento
recusam com TentativaNegada, incluindo indisponibilidade do Git. A apresentação
do selo reutiliza a mesma derivação de histórico. `selar.py` não mudou;
a regra antiga `exige_selo_apos` mantém o comportamento anterior.

As fixtures de percurso e as duas demonstrações passaram a importar expediente
sintético, validar o desfecho e selar, sem sinalizador de dispensa. O percurso
completo congela o HEAD commitado em worktree separado, em vez da antiga tag.
As demais condições negativas continuam sendo verificadas.

Os identificadores antes fixados no núcleo para a etapa inicial passam a vir
da primeira etapa do playbook. Exemplos e comentários foram generalizados.
**Limite do grep literal:** permanece a referência histórica F0/E1 no exemplo
da docstring de `selar.py`, pois a decisão expressa exige não alterar esse arquivo.
Não é usada em nenhuma regra e nenhum vocabulário administrativo entrou no núcleo.
A exceção textual é informada na evidência, sem alegar resultado vazio no grep.
