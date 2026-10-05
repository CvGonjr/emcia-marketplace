# Evidência — decisão 047, item 9

Data: 05/10/2026 · Autor: Celso do Vale · Base: 93bc1a143a2fd8668fc7afeb4c56637dfbec40c6.
Campo 0.8.31, núcleo 0.2.48 e playbook 0.4.22. Núcleo/playbook/pacote sem alterações.

## Escopo e percurso

Habilitação usa Tally/Drive/Calendar sem perfil/escopo por id. O hook registra
leituras/rascunhos sem aprovação; efeitos externos exigem testemunho com ok,
resumo, data, autor e argumentos. Publicação conserva conferência vigente.
load_form admite ids não declarados; conferir-formulario executa sem aprovação
própria. Perfil/escopo apresentados entram na terceira confirmação e no caso.
A existência do caso encerra a autorização administrativa, independentemente
do cwd ou de flag. O núcleo conserva o contrato de F0–P10.

percurso.json registra três confirmações administrativas, um depósito de PDFs,
sete avanços proximo e um registro de retorno da coleta. Conectores são sintéticos;
o script não chama APIs nem envia mensagens. Nenhuma conta real foi acessada.
A preparação permanente lê/compare sem perfil e sem aprovação própria; a confirmação
conferido e declaração do modelo continuam atos humanos reutilizáveis.

A coleta aceita somente uma submissão cujo caso é oculto e igual ao reservado.
O retorno original fica só em temporário administrativo, removido na recusa ou
sucesso. Fonte contém CSV projetado daquela submissão e hashes, sem preservar
lote em mcp-retornos/eventos/expediente. Seleção/nome/fonte são metadados locais
que podem chegar depois da leitura; argumentos da API precisam coincidir com
uma chamada administrativa registrada. Nenhum metadado local vira filtro de API.
CSV continua alternativa e seu percurso anterior segue coberto.

## Testes e ajustes

negativos-antes.txt registra a execução antes da implementação: 43 testes,
pois a primeira versão do módulo importava também os 31 da fixture anterior.
O módulo definitivo importa a fixture como módulo e contém 14 verificações,
sem duplicar as anteriores. Inclui recusas por efeito sem ok, outro caso,
seleção de id alheio, caso visível e paginação incompleta; seleção humana válida;
leitura/rascunho sem perfil/ids; chamada fora do perfil após abrir pelo hook real.

O adaptador contempla questions/id/title/type e responses/questionId/answer
conforme [a referência pública Tally](https://developers.tally.so/api-reference/endpoint/forms/submissions/list),
além da projeção do conector com labels/campo oculto. Fixtures desse formato são
sintéticas. Todas as páginas precisam ser conferíveis, desde a primeira até
hasMore false; páginas intermediárias ou formato desconhecido não viram fonte.
Os hashes do retorno são dos bytes JSON recebidos pelo script, sem autenticação
remota. O filtro é determinístico; o modelo não decide camada, procedência ou ids.

As negativas de ids da conferência e dos perfis passam a operar em caso aberto;
suas expectativas foram conservadas. A primeira regressão integral, guardada em
intermediaria-3.12/3.14.txt, expôs quatro verificações do percurso manual que ainda
usavam a fronteira anterior: criação sem aprovação antes do caso; coleta recusada
antes do caso; perfil ainda não instalado no caso na abertura. O caminho manual
foi corrigido para incluir hash do perfil na aprovação e instalá-lo ao abrir.
O negativo de efeito usa compartilhamento; o de perfil executa no caso aberto.
Ambos continuam recusando. Não foi tolerada essa regressão no runner.

especificos-3.12/3.14.txt registram os 14 novos testes, com metadados locais
fornecidos depois da leitura. percurso-manual-3.12/3.14.txt registram os quatro
verificadores do caminho manual após a correção. A integral final confere ambos.
cartao-conferencia.txt registra Chrome real com sandbox padrão, uma página A4,
SHA do cartão e texto extraído por Poppler. PDFs e retornos do percurso usam
fixtures, sem autenticar assinatura ou conta remota.

## Regressão

As verificações obrigatórias negativos.sh (51) e contexto.py (11) passaram antes
de editar. As integrais usam o mesmo runner sem excluir módulos, em checkout
temporário; o canônico temporário aponta à tag metodo-v1.0 (08bfb16). O checkout
habitual de emcia-artefatos não foi alterado. Saída original do manual_a25 fica
visível: somente test_01, a divergência exata selar-apos-P2 ausente das seções
3.3 e 3.4; quatro negativas passam. A exceção é anterior, já autorizada na 047.
Nenhuma exceção nova foi incluída; PyYAML disponível em 3.14 acrescenta dois checks.

| Execução | Python 3.12.12 | Python 3.14.4 | Resultado |
|---|---:|---:|---|
| Inicial (93bc1a1) | 1140 / 54 módulos | 1142 / 54 módulos | A25 conhecida; zero inesperadas |
| Final (rascunho item 9) | 1154 / 55 módulos | 1156 / 55 módulos | A25 conhecida; zero inesperadas |

final-3.12/3.14.txt são as execuções integrais finais, sem módulos excluídos.
SHA-256 do código, documentação, testes, pacote e evidências em integridade.json;
o próprio arquivo fica fora da lista. Núcleo sem alterações e sem vocabulário
do método/conectores, conferido em nucleo-conferencia.txt.

Somente espaços finais do log negativos-antes.txt foram normalizados para git diff --check; SHA-256 da captura original: 4df038e819b252872d1a511ec2031bf5affa6091673dff508eddf295d03c7704.
