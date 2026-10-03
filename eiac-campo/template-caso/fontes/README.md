# Fontes — material preservado do caso

Esta área só recebe arquivos pela importação humana da habilitação
(`importar_habilitacao.py`) e pelo recebimento humano (`receber.py`).
O agente prepara coletas em `rascunho/entrada/`; não copia nem altera arquivos
em `fontes/`. O validador e o curador também não escrevem nesta área.

A importação preserva três PDFs assinados, suas evidências e a matriz em
`fontes/habilitacao/importacao-NNN-AAAA-MM-DD/`. O recebimento conserva bytes,
hash e origem em caminho sequencial por finalidade e data, com id REC;
as asserções podem citá-lo com `fonte: REC-NNNNNN`. Relações com fontes F
curadas são explícitas. Nova versão requer decisão e mantém a anterior.

Hash preserva bytes; não autentica origem remota nem transforma declaração
em verificação. Documento citado não é substituído silenciosamente.

Material cuja preservação não foi autorizada permanece ausente; registre seu
contrato, acesso e limites em `contexto/fontes/` pela curadoria. Restrições RH
são vinculadas a fontes curadas ou dispensadas com motivo pelo engenheiro em P2.
O procedimento está no EMCIA-CTX-01 copiado em `metodo/`.

O caso não nasce com remote. A publicação de seu histórico é uma decisão do
engenheiro com a organização. Material público de 0a não é importado
automaticamente; eventual uso posterior conserva URL, premissa e limite.
