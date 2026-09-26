---
description: Conduz o expediente administrativo de habilitação anterior ao caso, prepara HAB-01 a HAB-03 e registra conferência de assinaturas externas.
---
Uso: `/eiac-campo:habilitacao <caminho-absoluto-do-expediente> [ação]`

Leia o protocolo canônico `EMCIA-HAB-01-protocolo-de-habilitacao.md`, o roteiro `auxiliares/EMCIA-HAB-02-roteiro-de-habilitacao.md` e o fluxo operacional `auxiliares/EMCIA-HAB-fluxo-operacional-proposta.md` no checkout indicado pelo engenheiro de https://github.com/CvGonjr/emcia-artefatos/. Respeite o estado de aprovação de cada documento. A interface executável e os formatos JSON estão em `${CLAUDE_PLUGIN_ROOT}/reference/habilitacao.md`.

Consulte primeiro:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/habilitacao.py" estado --expediente "<caminho>"
```

Se não existir expediente, apresente a inicialização humana descrita na referência. Não inicialize nem escolha responsável em nome do engenheiro. O expediente precisa ficar fora de repositórios e de casos; ele não é um caso aberto e não tem as guardas de sessão do núcleo. Não escreva diretamente em seu estado ou arquivos preservados: use o script. Prepare entradas em uma pasta de trabalho separada.

Antes de consultar submissões no Tally MCP, confira que `tratamento_registrado` é verdadeiro. A exceção anterior a 0d cobre exclusivamente informações administrativas da habilitação; não leia anexos ou bases operacionais. Peça ao engenheiro uma exportação administrativa filtrada se o formulário contiver conteúdo operacional. Identificação do formulário e origem da submissão devem vir do MCP, nunca de memória. Não copie respostas para repositórios do plugin ou do método.

Use as ferramentas Tally disponíveis para localizar o formulário de habilitação. Para esclarecimentos, prepare um formulário por expediente e rodada com perguntas revisadas pelo engenheiro; registre seu identificador e versão nas respostas. Não altere formulários anteriores. Publicação e envio ao cliente exigem instrução expressa do engenheiro; não envie mensagens por conta própria. Se não houver MCP disponível, aceite exportação manual com as mesmas referências de origem.

Sugira perguntas e campos consolidados ao engenheiro. Não decida autoridade, resolução de pendência, qualificação, revisão de conteúdo ou conferência de assinatura. Só registre essas decisões quando a pessoa nomeada as comunicar, apontando para a evidência. Não classifique procedência por modelo: respostas permanecem declarações; o expediente preserva origem e não atribui D/I/V automaticamente.

Execute as operações documentadas com `--entrada <arquivo.json>`. Para gerar documentos, indique `templates` como a pasta `auxiliares/` do checkout canônico. A revisão humana da carta é obrigatória: suas divergências de conteúdo não foram resolvidas por inferência. Antes de `liberar`, apresente os PDFs finais para conferência visual e obtenha ferramenta, operador e signatários definidos pelas pessoas envolvidas.

A assinatura ocorre exclusivamente pelo painel escolhido pelo cliente, sem API, MCP ou webhook de assinatura. Registre os PDFs assinados e as evidências devolvidas, após conferência humana. Uma imagem de assinatura ou uma resposta “sim” não substitui esse retorno.

`concluir-0b` apenas confere a formalização. `acessos` registra a verificação humana de 0c e `preparar-0d` confere prontidão; nenhum deles abre caso, sela ou libera F0. A passagem para o caso segue o roteiro canônico e os mecanismos autorizados existentes. Preserve o expediente para importação e não escreva diretamente em `fontes/`, `registro/` ou `caso/` de um caso pelo chat.
