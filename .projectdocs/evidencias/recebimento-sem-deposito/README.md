# Evidência — recebimento sem depósito obrigatório

Data: 05/10/2026 · Autor: Celso do Vale.
Base: 33f8f7dbdc9c723aa295b500ab0809a026d7ce14.
Campo 0.8.32; núcleo 0.2.48; playbook 0.4.22; pacote metodo-v1.0.

## Pedido e resultado

O engenheiro confirmou ambos: respostas e PDFs recebidos pelos conectores ou
pelos caminhos originais, sem mover para a pasta de entrada.
Tally direto permanece padrão. CSV manual aceita exportacao com o caminho
original. proximo/preparar-assinaturas recebem assinados (três caminhos) e
evidencias opcionais por HAB. Pastas/nomes diferentes são aceitos; o original
não é alterado. A sessão baixa PDFs do Drive por download_file_content/fileId
e entrega os bytes exatos em temporário externo, sem pedir exportação manual.
A API continua executada pela sessão. O script importa cópias com hash e exige
a mesma conferência humana e associação aos documentos enviados. entrada_dir
continua disponível como alternativa.

Caminhos em repositórios/casos e symlinks recusam com evento. Entrada explícita
inválida não é substituída por arquivos da pasta de entrada. Não há mudança em
núcleo, playbook, templates ou documentos do pacote; sem reempacotamento.

## Validação

Antes de editar: negativos.sh, 51 verificações, e contexto.py, 11, passaram.
Quatro verificações foram acrescentadas ao módulo simplificado; o negativo da
antiga restrição de pasta passa a cobrir repositório, conforme a mudança aprovada.
Há teste de symlink com evento, CSV no caminho original e filtro do caso,
recebimento de PDFs em três pastas com comprovantes, hashes e aprovação humana,
e recusa de conjunto ausente/divergente. O recebimento pelos caminhos passa
pelo proximo real. testes-antes.txt mostra as falhas antes da implementação.

O percurso MCP existente agora usa Tally direto e PDFs fora da entrada,
chega a F0 com três confirmações e nenhum depósito na entrada; os arquivos
representam os bytes baixados pela sessão. A leitura download_file_content sem
perfil antes do caso também é coberta. PDFs, downloads e conectores são
sintéticos; não se acessou conta real nem se autenticou assinatura.
Os registros percurso-3.12/3.14.json documentam esse percurso.

A suíte integral usa o runner existente, sem exclusões nem nova exceção, num
checkout temporário do marketplace com checkout canônico separado na tag
metodo-v1.0 (08bfb16). O checkout habitual do canônico não foi alterado.
A única exceção anterior permitida pelo runner é A25: ato selar-apos-P2 ausente
das seções 3.3/3.4; sua saída bruta e quatro negativos continuam visíveis.

| Execução | Verificações | Módulos | Resultado |
|---|---:|---:|---|
| Final Python 3.12.12 | 1158 | 55 | A25 conhecida; zero inesperadas |
| Final Python 3.14.4 | 1160 | 55 | A25 conhecida; zero inesperadas |

A linha de base anterior, no commit 33f8f7d, registrou 1154/1156 verificações
em 55 módulos, com a mesma A25 conhecida. PyYAML disponível em 3.14 explica
a diferença de duas verificações. final-3.12/3.14.txt conservam a saída integral.
A versão e os scripts foram comparados byte a byte com o checkout testado.
SHA-256 dos arquivos alterados e das evidências em integridade.json; o próprio
arquivo fica fora da lista. Espaços finais dos logs foram normalizados.
