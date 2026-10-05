# Perfis dos conectores — emenda à decisão 045

Data: 05/10/2026. Autor: Celso do Vale. Base da tarefa:
`5fd6d03e48528db5644aff6246e493ab6ed1bfa8`.
Núcleo 0.2.47, campo 0.8.27, playbook 0.4.21.

## Fonte e calibração

A única fonte de nomes, parâmetros e tipos é o arquivo fornecido em
`~/emcia-op/ensaio/inventario-mcp.json`. Seu hash está em
[integridade.json](integridade.json). A fixture conserva integralmente a lista
de ferramentas/schemas/parâmetros; altera somente a descrição da origem para
explicitar uso sintético. Não há id de conta, credencial ou dado de cliente.

[Calibração com o arquivo real](calibracao-inventario-real.json): 11 regras
literais, 10 habilitadas. A regra de fetch_submissions recusa por ausência de
filtro estruturado pelo campo oculto do caso. Outras 36 ferramentas não têm
perfil auditado/schema disponível e ficam recusadas. O relatório mostra nomes,+motivos, parâmetros recusados e passos manuais antes da aprovação.

Drive usa query limitado ao pai, fileId com listagem prévia, create_file com
parentId e variante por contentMimeType e share_file com fileId/emailAddress/role
aprovados. Arquivo comum somente na finalidade entregas. Calendar usa calendarId.
Tally cria com workspaceId e publica com formId; não usa o workspace padrão.

O inventário tem duas lacunas relevantes: ferramentas para preparar perguntas/
campo oculto não têm schema auditável; fetch_submissions.filter só permite
datas/status, sem caso. Preparação e coleta filtrada são ações do engenheiro,
com decisão e evidência/hash registradas. A operação caminho-manual registra
essa decisão; não executa a API recusada nem autentica o ato no painel.
Publicação sem ferramenta no inventário e criação sem workspaceId também têm
caminho manual testado. Não se coleta lote amplo para filtrar depois.

create_event tem inputSchema integral não transcrito no arquivo. A lista de
parametros informa tipos simples e obrigatoriedade; esses campos são usados
literalmente. Objetos sem schema e parâmetros depreciados não são aceitos.
Não se inventam subcampos ou aliases. Essa restrição aparece no relatório.

## Regressões integrais

| Execução | Python 3.12.12 | Python 3.14.4 |
|---|---|---|
| Inicial | 1014 verificações / 51 módulos | 1016 verificações / 51 módulos |
| Final | 1054 verificações / 52 módulos | 1056 verificações / 52 módulos |
| Falhas inesperadas | 0 | 0 |
| Falha conhecida | A25 | A25 |

[Inicial 3.12](suite-inicial-python312.txt), [inicial 3.14](suite-inicial-python314.txt),
[final 3.12](suite-final-python312.txt), [final 3.14](suite-final-python314.txt).
Nenhum módulo foi excluído. A25 executa cinco testes: a primeira conferência
mantém a divergência exata `ato humano selar-apos-P2 ausente das seções 3.3 e 3.4`;
as quatro negativas passam. O teste original, helper estrito da falha conhecida
e pacote do método estão intactos. Nenhuma divergência adicional foi aceita.

A diferença de dois testes vem de nucleo_yaml.py: PyYAML está disponível no
ambiente 3.14 e ausente no 3.12. Nenhuma dependência foi acrescentada e nenhuma
diferença de resultado/recusa foi observada. Os parsers mínimo e PyYAML conservam
suas verificações. Não se atribui essa diferença à semântica da versão de Python.

As execuções usam um worktree temporário do marketplace na base com os arquivos
alterados sincronizados; por isso o HEAD dos relatórios é o commit de base.
O worktree canônico irmão está na tag aprovada metodo-v1.0/08bfb16; a main local
com propostas posteriores não foi usada nem alterada. TMPDIR fica no cache local,
fora dos repositórios. Integridade registra os hashes da árvore final testada.

## Negativas e percurso

[Antes](testes-antes.txt): 28 testes iniciais reproduzem a falta dos contratos e
a incompatibilidade do formato do inventário. [Primeira correção](testes-primeira-correcao.txt)
registra 27 aprovados e o erro de gravação da data na decisão manual, corrigido
sem afrouxar recusa. [Sessão ausente antes](sessao-ausente-antes.txt) reproduz a
passagem sem sessão ativa; [caso alheio antes](caso-alheio-antes.txt) reproduz
reutilização indevida do contexto. Ambos têm correções e negativas na suíte final.

[Perfis finais 3.12](testes-depois-python312.txt) e
[3.14](testes-depois-python314.txt): 40 testes. Contrato reprova ferramenta ou
parâmetro ausente; variantes/escopo recusam pai alheio, arquivo fora de entregas,
share_file com id não declarado, alteração de papel/destinatário, formulário
alheio, Tally sem filtro, ferramenta desconhecida, parâmetro extra, leitura sem
listagem, retorno adulterado, publicação sem conferência, sessão ausente e
contexto de outro caso. Guardas de caso verificam TentativaNegada com autor fixo.
Há controles positivos de pasta/arquivo, compartilhamento exato, agenda,
publicação conferida e leitura/download depois da listagem íntegra.

[Percurso](percurso-depois.txt): quatro testes com os nomes reais, criação de
pasta por create_file, preparação/exportação manual testemunhada e publicação
por publish_form. Cinco grupos de aprovação e três retomadas permanecem; o
checklist chega a F0 liberado. MCPs são simulados; operações locais, guardas,
validação e selo Git são reais. A simulação não comprova permissões em conta real.
O renderizador PDF do percurso é sintético, como na evidência anterior.

Os testes de escopo legado usam ferramentas-externas-v1.json byte a byte;
casos existentes conservam seu contrato. Testes específicos exercitam o template
novo. As regressões intermediárias preservadas passaram com 39 testes novos;
a final acrescenta a recusa de contexto alheio, após reprodução negativa.

## Núcleo, pacote e reprodução

[Grep](vocabulario-nucleo.txt) retorna 1, sem ocorrência de instrumentos,
etapas, nomes de conectores, ferramentas reais ou seus parâmetros no núcleo.
[Hashes do núcleo](integridade-nucleo.json) fixam os arquivos dessa conferência.
As regras ficam no campo/dados; o núcleo valida contratos genéricos. Nenhuma
decisão de camada ou procedência é atribuída ao modelo.

Os 23 arquivos de reference/metodo/ e manual_a25.py permanecem byte a byte
iguais à base. Emenda da 045 e propostas-artefatos.md registram os ajustes
documentais; não houve reempacotamento nem alteração canônica.

```bash
export PATH=/caminho/do/python/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR=/diretorio/fora-dos-repositorios
python3 .projectdocs/evidencias/perfis-conectores/reexecutar-suite.py /tmp/suite.txt
```

Use Python 3.12 ou 3.14 e seu python3 no PATH, com checkout canônico irmão na
tag metodo-v1.0. Aprovação no chat continua testemunho, não autenticação.
Nenhum serviço real foi chamado; nada foi enviado, publicado ou compartilhado.
