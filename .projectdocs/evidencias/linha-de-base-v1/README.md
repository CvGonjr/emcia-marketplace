# Linha de base metodo-v1.0 — evidência operacional

Data: 04/10/2026. Aprovação documental: Celso do Vale, em 03/10/2026,
conforme APR-01 canônico. A revisão jurídica dos exemplos é exclusivamente
sintética; esta evidência não constitui revisão jurídica para cliente real.

## Origem e pacote

Tag anotada publicada: metodo-v1.0, objeto Git
`e0cb22ba5d80d009e402f2693aa18171f794b18f`, resolvida para
`08bfb162d762935ed35f55e0a75bc700b81d5276` em emcia-artefatos.
[publicacao-tag-confirmada.txt](publicacao-tag-confirmada.txt) registra a consulta
bem-sucedida. [publicacao-tag.txt](publicacao-tag.txt) conserva o diagnóstico
anterior à publicação, sem descrever o estado vigente.

O pacote contém os 21 arquivos aprovados pelo APR-01 e o próprio registro:
22 documentos extraídos dos objetos Git da tag, sem edição manual. Inclui os
três templates HAB. ESP-01, VER-01 e fluxo auxiliar, excluídos pelo APR-01,
ficam fora do pacote que a abertura copia para casos reais. A origem foi obtida
por clone limpo da tag publicada. [tag-bytes-hashes.json](tag-bytes-hashes.json)
confere todos os bytes, hashes do manifesto e os 21 hashes do APR-01.
O nome operacional do manifesto permanece manifesto.json; a versão passa a 6,
com tag, commit e linha_de_base. Campo 0.8.24; núcleo 0.2.45 e playbook 0.4.19.
Nenhum arquivo canônico ou script do núcleo foi alterado.

## Testes primeiro e regressão

- Linha de base: Python 3.12.12, **958 verificações em 49 módulos**, sem exclusões
  ou falhas, no HEAD d9551a90b5ee3cec5006bbbfcbdebca4cbfe0f35. Saída integral:
  [suite-inicial-python312.txt](suite-inicial-python312.txt).
- Os testes com cópias exatas dos templates da tag foram escritos antes da
  correção. A execução anterior teve 28 testes, uma falha e 13 erros esperados:
  não existia revisao-juridica e gerar iniciou PDF sem essa pré-condição.
  [habilitacao-antes-correcao.txt](habilitacao-antes-correcao.txt).
- Habilitação corrigida: **29 testes**, incluindo revisão ausente, cobertura
  parcial, hash errado, pessoa inválida, data inválida, evidência adulterada,
  marcas ausentes, remoção multilinha, preservação de histórico e recusa sem
  publicar versões parciais após falha no PDF.
  [habilitacao-depois-correcao.txt](habilitacao-depois-correcao.txt).
- Pacote: **8 testes**, incluindo APR-01 com hash divergente mesmo após atualizar
  o manifesto, tag para outro commit, template adulterado no checkout, manifesto
  divergente, origem inválida, fixtures idênticos e controle offline.
  [metodo_empacotado-final.txt](metodo_empacotado-final.txt).
- A25: **5 testes**, incluindo os quatro negativos; conformidade direta do manual.
  [manual_a25-final.txt](manual_a25-final.txt).
- Catálogo: **11 testes**; citações: **8 testes**.
  [catalogo_cat01-final.txt](catalogo_cat01-final.txt), [citacoes-final.txt](citacoes-final.txt).
- Regressão final: Python 3.12.12, **975 verificações em 49 módulos**, sem exclusões
  ou falhas. Executada sobre todas as alterações de código, pacote e testes,
  antes dos seis commits por item; o HEAD do relatório é a origem anterior,
  e o diff de implementação está em [alteracoes.patch](alteracoes.patch).
  [suite-final-python312.txt](suite-final-python312.txt).

O novo executador conserva a descoberta completa de negativos.sh e módulos
Python, registra códigos e saídas e não admite exclusões. Ele conta o novo
unittest do pacote como oito testes; o executador histórico o contava como
um processo. Essa diferença não exclui nem repete módulos na contagem.

```bash
PATH=/home/netiv-dn-1/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin:$PATH \
  PYTHONDONTWRITEBYTECODE=1 python3 \
  .projectdocs/evidencias/linha-de-base-v1/reexecutar-suite.py /tmp/emcia-suite-v1.txt
```

## Exemplo sintético antes e depois

Os arquivos em exemplo-sintetico/ foram gerados com Chrome real e examinados
com pdftotext. HAB-02-antes.md/.pdf/.txt mostram o defeito anterior: controle,
aprovação e histórico do modelo, aviso jurídico e ausência de Para assinatura.
HAB-01-depois, HAB-02-depois e HAB-03-depois, em MD, PDF e texto extraído,
preservam identificação, cláusulas e controle de assinatura e trazem Para assinatura,
sem controle interno, histórico do modelo ou aviso jurídico.

hashes-e-revisao-sintetica.json registra hashes dos templates originais, Markdown,
PDF e a revisão sintética importada. revisao-juridica-sintetica.json conserva
uma cópia da evidência sintética cujo hash aparece nesse registro; os caminhos
arquivos/ são os do expediente temporário usado na demonstração, já encerrado.
Nenhum desses documentos foi enviado a cliente. Para reproduzir, com Chrome,
pdftotext e o objeto Git do HEAD inicial disponíveis:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .projectdocs/evidencias/linha-de-base-v1/demonstrar-geracao.py
```

## Documentação e decisão

A decisão 044 registra aprovação, nova linha de base após alteração documental,
separação entre controle do modelo e emissão e revisão jurídica como pré-condição.
README, INSTALACAO, mapa, referências e índice de testes descrevem a aprovação
vigente. As decisões 026, 038 e 043 recebem nota que situa seus estados anteriores
como históricos, sem reescrever a decisão original. O retrato de auditoria de
18/09/2026 é marcado histórico. Menções à aprovação pendente nos históricos
canônicos e nas evidências de versões anteriores permanecem fatos datados e não
afirmam pendência da linha de base atual. Casos existentes conservam seu contrato.

## Commits por item

- Item 0: 9b6cad78bfda32c31e31c336a119d605a71f9033 — geração, revisão jurídica, testes e campo 0.8.24.
- Item 1: 8795ba4e36d8a7bcaafdb14e81a3b0675286d6ab — pacote aprovado extraído da tag.
- Item 2: c8fae95a1842811178865b81904c943411a8dd8b — teste do pacote, citações e obtenção da tag no CI.
- Item 3: 96ea3dca42e349c0e8363e1426f223f942d736ed — comando e referência da habilitação.
- Item 4: 28dee7a06797aa35bcda70fc640f65f27f5f74a3 — documentação operacional, mapa e índices.
- Item 5: este commit — decisão 044, notas de atualização de estado e evidência integral.

As quebras de linha Markdown de dois espaços nos templates e nos exemplos
emitidos foram preservadas; não se normalizam bytes aprovados para satisfazer
uma checagem de espaço final. A inspeção do diff desconsidera somente esse
aviso de formatação; os hashes do pacote e dos fixtures foram conferidos.
