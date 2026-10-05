# Cartão de habilitação — decisão 047

Preparação reutilizável: configuração, perfil MCP aprovado, tratamento administrativo, situação jurídica e formulários permanentes conferidos. Resolva ausências pela referência específica. Não invente ids, assinaturas ou aprovação.

Uma chamada por avanço, na pasta administrativa:

```bash
python3 <plugin>/scripts/iniciar.py proximo --entrada <entrada-local.json>
```

Entrada: habilitacao e caso. Apresente resumo, próximo passo e artefatos; preserve hashes e trecho real. Consulte reference/habilitacao.md somente para entradas/alternativa manual.

1. Entregue o link permanente ?caso=<caso>; engenheiro envia ao cliente.
2. Aguarde CSV em ~/emcia-op/entrada/. Script filtra antes de gravar; zero/várias submissões exigem indicação humana.
3. Redija perguntas para lacunas. Resposta colada entra em mensagem (id, pergunta, texto, respondente). Prepare campos com fonte e plano_documentos (qualificação, signatários, competência, painel).
4. Apresente três PDFs. Primeira confirmação: aprovacao com ponto documentos, confirmado true e trecho real. Cobre revisar/gerar/liberar aqueles bytes.
5. Aguarde três PDFs assinados na entrada; relatórios opcionais HAB-01-relatorio.pdf etc. Informe plano_assinaturas (nomes, papéis, datas reais, referência). Confira associação/evidências: segunda confirmação, ponto assinaturas.
6. Apresente matriz de 0c. Engenheiro confirma/corrige numa mensagem; acessos contém confirmado, trecho e matriz completa.
7. Apresente desfecho/destino. Terceira confirmação, ponto abertura: declarar Tally/calendário, abrir/importar/validar/selar até F0 liberado.

“ok” ou outro trecho aprovado vale; silêncio não. Retome pelo mesmo comando sem repetir atos. Alteração exige nova conferência. PDF sem texto ou divergente usa alternativa manual com conferência humana.

Drive aguarda P2: passo P2 apresenta criação/compartilhamento por ids, com aprovação posterior. Execute MCPs na pasta administrativa. Raiz/trabalho-interno são privados. Apuração, sessões, decidir-prosseguimento e demais decisões de método continuam no terminal; F0 liberado não é encerrado.
