# Bloco inicial conduzido — evidência da decisão 045

Data: 05/10/2026. Autor: Celso do Vale. Dados, pessoas, revisões e assinaturas dos
exemplos são exclusivamente sintéticos; não representam aprovação de cliente ou
ratificação jurídica real. Nenhuma API de cliente foi chamada.

## Linha de base e regressão

Base da tarefa: `750f2c4edcf1e19a20f5c1e355736ab82f3864a7`.
Python 3.12.12, biblioteca padrão. Núcleo 0.2.46, campo 0.8.26, playbook 0.4.20.
Método aprovado metodo-v1.0 e manifesto v6 intactos, sem reempacotamento.

- [Inicial](suite-inicial-python312.txt): 986 verificações/49 módulos, sem exclusões
  e sem falhas, antes das alterações.
- [Final](suite-final-python312.txt): 1014 verificações/51 módulos; sem exclusões,
  somente A25 como falha conhecida e nenhuma falha inesperada.
- [Runner integral](reexecutar-suite.py): descobre negativos.sh e todos os módulos
  da raiz de testes. Não exclui A25; conserva saída bruta e código 1.
- [Integridade](integridade.json): 23 arquivos do pacote idênticos, hash do A25
  inalterado e versões, worktrees, árvore e ambiente conferidos.

O checkout canônico de teste é um worktree irmão na tag aprovada 08bfb16, não a
main local que contém propostas posteriores. O marketplace temporário está no
commit de base com os arquivos alterados sincronizados: por isso a saída do
runner mostra esse HEAD. Código, testes e fixtures foram comparados aos arquivos
locais antes da execução. A aprovação final da tarefa pertence à árvore entregue.

O tmpfs /tmp atingiu cota durante uma execução intermediária, causando erros 122
em fixtures e truncamento de PDF. A regressão foi repetida integralmente com
`TMPDIR=/home/netiv-dn-1/.cache/emcia-bloco-inicial-testes`, em disco local e fora
dos repositórios. Nenhuma recusa foi desativada e nenhum teste foi alterado para
aceitar erro de cota. A reescrita também suprimiu uma remissão CTX exigida em
README/INSTALACAO; ambas foram restauradas e citacoes.py foi repetido com sucesso.

## Testes negativos e controles

[item-1-antes.txt](item-1-antes.txt) registra a ausência inicial da implementação.
[item-1-depois.txt](item-1-depois.txt) registra as seis primeiras conferências de
recusa/escopo/configuração. [Item 2 antes](item-2-antes.txt) e
[depois](item-2-depois.txt) registram geração/aceitação, revogação, ratificação
prevalente e autoria; cinco novos testes levam habilitacao.py a 45 testes.
[Item 3 antes](item-3-antes.txt) e [depois](item-3-depois.txt) cobrem o checklist.
[Config ilegível antes](config-ilegivel-antes.txt) preserva a reprodução da negativa
que precisava manter saída bloqueante, sem inventar responsável.

[Guardas finais](item-4-guardas.txt) contêm 19 testes, incluindo operação sem
aprovação, entrada alterada/sem hash, chamada composta, decisão de método,
operação fora de F0, selo após P2, contrato antigo, núcleo sem instrumentos,
perfil ampliado, assinatura de ferramenta incompatível, configuração e revogação.
[Percurso](item-4-depois.txt) contém quatro testes, com MCP Tally/Drive/Calendar
simulado e operações administrativas/Git reais. O percurso chega à saída íntegra,
com cinco trechos de aprovação de conteúdo/efeito, mais perfil e aceitação iniciais.

Retomadas são verificadas durante rodada aberta, após emissão dos PDFs e antes
do selo. Retomar não muda o expediente nem cria nova versão. O percurso ratificado
termina sem pendência jurídica; o não ratificado termina com a pendência não
bloqueante. API sem retorno preservado exige conferência remota antes de repetir;
a suíte não autentica a origem nem promete execução única de APIs.

As negativas anteriores de A12/importação conservam seus contratos de caso pela
fixture byte a byte [playbook 0.4.19](../../../testes/apoio/playbook-0.4.19.json).
O contrato novo tem suas próprias negativas e controles positivos. O campo remove
somente quatro atos administrativos da lista humana, mantendo decisões de método.

## Falha conhecida A25

O teste original permanece inalterado: test_01 falha e test_02–05 passam.
A lista exata é `ato humano selar-apos-P2 ausente das seções 3.3 e 3.4`.
[Validador da exceção](../../../testes/apoio/falha_conhecida_a25.py) executa os cinco
testes e aceita somente um failure, em test_01, sem errors e com a lista exata.
O CI não usa continue-on-error; qualquer outra falha/divergência interrompe.
A decisão 045 e propostas-artefatos.md registram a revisão pendente do MAN-01.
Camadas, HBs, produtos e comandos de etapa permanecem iguais.

## Núcleo e documentos preservados

[Busca anterior](vocabulario-antes.txt) registra remissões antigas a CTX em
mensagens/comentários. [Teste anterior](vocabulario-antes-teste.txt) as detecta.
[Busca final](vocabulario-final.txt) registra comando grep e saída 1, sem ocorrências
de instrumentos, fases ou conectores. Os rótulos foram para o schema do campo;
as condições de recusa não mudaram. ctx_v.py, curadoria.py e os percursos antigos
continuam passando. Schemas legados sem rótulos conservam a recusa, com mensagem
genérica. O núcleo não contém aprovação de minuta, Tally ou nomenclatura de F0.

O pacote reference/metodo/ e manual_a25.py permanecem idênticos à base, conforme
integridade.json. Modelos HAB usados na geração continuam aprovados pelos hashes
no APR-01; nenhuma minuta posterior da main canônica foi incorporada.

## PDFs reais e situação jurídica interna

[gerar-exemplo.py](gerar-exemplo.py) usa a fixture aprovada e aceitação sintética,
executa gerar com Chrome real e confere os três PDFs por pdftotext. Arquivos em
[exemplo-sintetico](exemplo-sintetico/) incluem MD, PDF, texto extraído e registro
de versão/hash/situação jurídica. Nenhum documento contém controle, histórico
interno, aviso jurídico ou aceitação. Todos mostram Para assinatura.

Os MD do exemplo preservam as quebras de linha Markdown com dois espaços finais,
exatamente como emitidos; os hashes em emissoes.json conferem esses bytes.

Os PDFs do percurso automatizado usam renderizador sintético apenas nos testes;
origem, aprovações, assinatura testemunhada, importação, validador, guardas e selo
não são substituídos. A aprovação no chat é testemunho registrado, não autenticação.
O engenheiro assume a aceitação real; estes arquivos não a registram em seu nome.

## Reprodução

```bash
export PATH=/caminho/python3.12/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR=/diretorio/temporario/fora-de-repositorios
python3 .projectdocs/evidencias/bloco-inicial-conduzido/reexecutar-suite.py /tmp/suite.txt
```

Mantenha emcia-artefatos irmão na tag metodo-v1.0. Não faça reempacotamento para
rodar esta regressão. Aprovação, contas remotas e permissões reais não são
comprovadas pelo MCP simulado; assinatura sem perfil continua recusada.
