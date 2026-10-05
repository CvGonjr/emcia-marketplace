# Cartão de habilitação — decisão 047, item 9

Preparação: configuração, tratamento administrativo, situação jurídica e formulários permanentes conferidos. Sem perfil antes da abertura. Resolva ausências pela referência específica; não invente ids, assinaturas ou aprovação.

Na pasta administrativa, uma chamada por avanço:

```bash
python3 <plugin>/scripts/iniciar.py proximo --entrada <entrada-local.json>
```

Entrada: habilitacao e caso. Apresente resumo, artefatos e hashes; consulte reference/habilitacao.md somente para entradas/alternativa manual.

1. Entregue o link ?caso=<caso>. Leia todas as páginas de fetch_submissions; passe o retorno ao script (iniciar.py retorno). Ele grava só o caso; zero/várias submissões exigem indicação humana. CSV: coleta: csv.
2. Redija perguntas para lacunas. Resposta colada entra em mensagem (id, pergunta, texto, respondente). Prepare campos com fonte e plano_documentos.
3. Apresente três PDFs. Primeira confirmação: aprovacao com ponto documentos, confirmado true e trecho real; cobre revisar/gerar/liberar aqueles bytes.
4. Aguarde três PDFs assinados na entrada; relatórios opcionais HAB-01-relatorio.pdf etc. Informe plano_assinaturas com nomes, papéis, datas e referência. Confira associação/evidências: segunda confirmação, ponto assinaturas.
5. Apresente matriz de 0c. Engenheiro confirma/corrige numa mensagem; acessos contém confirmado, trecho e matriz.
6. Apresente desfecho, destino, perfil calibrado e escopo. Terceira confirmação, ponto abertura: aprovar perfil, abrir/definir/importar/validar/selar até F0 liberado.

Na habilitação, Tally/Drive/Calendar leem, listam e criam rascunhos sem perfil/ids. load_form admite qualquer formId. Publicar, enviar mensagem/convite ou compartilhar exige “ok” registrado com resumo/data. “conferido” do permanente permanece.

Retome sem repetir atos. PDF sem texto/divergente usa alternativa manual. Depois da abertura, perfil/escopo são obrigatórios; Drive do caso aguarda P2. Apuração, sessões e decidir-prosseguimento continuam no terminal. F0 liberado não é encerrado.
