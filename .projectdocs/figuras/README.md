# Figuras de apoio ao PFC

Material gráfico fornecido para o relatório e seu apêndice. Os quadros e capturas
preservam os resultados e versões que exibem; não são a linha de base operacional
vigente nem substituem o método aprovado ou as evidências de regressão atuais.
Por exemplo, saida/fig49.png apresenta uma execução anterior de A25 sem falhas;
a divergência atual permanece registrada na decisão 045 e nas evidências da suíte.

- dados/fig23.json, fig45.json e fig46.json: fontes das tabelas do gerador.
- dados/apendice/: imagens e HTML de apoio fornecidos para o apêndice.
- saida/: imagens fornecidas para o relatório, incluindo capturas estáticas.
- gerar_figuras.py: regenera somente figuras que tenham JSON em dados/.
  As imagens fig47, fig48 e fig49 de saida/ não têm fonte JSON neste conjunto.

O gerador precisa de Playwright e Chromium, apenas para produzir as figuras;
essa dependência não faz parte dos plugins ou da suíte operacional. A revisão
validou todos os PNGs, os JSONs e a sintaxe do script e executou o gerador em
uma cópia temporária, preservando as imagens originais.
