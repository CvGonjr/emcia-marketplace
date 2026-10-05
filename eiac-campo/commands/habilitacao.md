---
description: Conduz o expediente administrativo de habilitação anterior ao caso, prepara HAB-01 a HAB-03 e registra conferência de assinaturas externas.
---
Uso: `/eiac-campo:habilitacao <caminho-absoluto-do-expediente> [ação]`

Leia o protocolo canônico `EMCIA-HAB-01-protocolo-de-habilitacao.md`, o roteiro `auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md` e o registro `EMCIA-APR-01-registro-de-aprovacoes.md` na linha de base e no commit fixados no manifesto do método (atualmente tag `metodo-v1.0`); as cópias exatas ficam em `${CLAUDE_PLUGIN_ROOT}/reference/metodo/`. Consulte também EMCIA-CAN-01 para os canais. Modelos e templates são aprovados pelo hash do APR-01; seus metadados internos não substituem essa conferência. Documento fora da aprovação não rege caso real. A interface executável e os formatos JSON estão em `${CLAUDE_PLUGIN_ROOT}/reference/habilitacao.md`.

Consulte primeiro:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/habilitacao.py" estado --expediente "<caminho>"
```

Se não existir expediente, apresente a inicialização humana descrita na referência. Não inicialize nem escolha responsável em nome do engenheiro. O expediente precisa ficar fora de repositórios e de casos; ele não é um caso aberto e não tem as guardas de sessão do núcleo. Não escreva diretamente em seu estado ou arquivos preservados: use o script. Prepare entradas em uma pasta de trabalho separada.

Antes de consultar submissões no Tally MCP, confira que `tratamento_registrado` é verdadeiro. A exceção anterior a 0d cobre exclusivamente informações administrativas da habilitação; não leia anexos ou bases operacionais. Peça ao engenheiro uma exportação administrativa filtrada se o formulário contiver conteúdo operacional. Identificação do formulário e origem da submissão devem vir do MCP, nunca de memória. Não copie respostas para repositórios do plugin ou do método.

Use as ferramentas Tally disponíveis para consultar o formulário de habilitação pelo id informado pelo engenheiro ou retornado pelo conector. Não busque pelo nome da organização. Para esclarecimentos, prepare um formulário por expediente e rodada com perguntas revisadas pelo engenheiro; registre seu identificador e versão nas respostas. Não altere formulários anteriores. Publicação e envio ao cliente exigem instrução expressa do engenheiro; não envie mensagens por conta própria. Se não houver MCP disponível, aceite exportação manual com as mesmas referências de origem.

Sugira perguntas e campos consolidados ao engenheiro. Não decida autoridade, resolução de pendência, qualificação, revisão de conteúdo ou conferência de assinatura. Só registre essas decisões quando a pessoa nomeada as comunicar, apontando para a evidência. Não classifique procedência por modelo: respostas permanecem declarações; o expediente preserva origem e não atribui D/I/V automaticamente.

Execute as operações documentadas com `--entrada <arquivo.json>`. Para gerar documentos, indique `templates` como `${CLAUDE_PLUGIN_ROOT}/reference/metodo/`, onde estão as cópias dos três templates aprovados. Os arquivos são localizados pelo código HAB-01, HAB-02 ou HAB-03 na tabela do APR-01 do pacote; não deduza o nome pela memória nem escolha entre entradas ambíguas. Nenhuma ou mais de uma entrada para o mesmo código recusa. Se usar `auxiliares/` do checkout canônico, ele deve estar na tag declarada pelo manifesto; os hashes precisam coincidir com o APR-01 do pacote. A revisão humana da carta é obrigatória. Antes de `liberar`, apresente os PDFs finais para conferência visual e obtenha ferramenta, operador e signatários definidos pelas pessoas envolvidas.

Antes de `gerar`, o engenheiro registra `revisao-juridica` no terminal, conforme a referência: pessoa responsável pela revisão, pessoa que registra o ato, data, `resultado: "aprovado"`, hashes exatos de HAB-02 e HAB-03 e evidência importada. `ciclo` é texto opcional para identificar a revisão. O campo resultado é obrigatório e só aceita a string exata `aprovado`. Parecer condicionado ou reprovado não é registrado como revisão no expediente; aguarde ratificação sem condição sobre os hashes exatos. A tentativa inválida produz evento `Recusado`. Não declare resultado em nome do revisor nem transforme condição em aprovação.

Apresente o comando para execução humana; não atribua ao agente a revisão jurídica nem use aprovação documental como substituto. A operação não admite dispensa. O gerador considera somente revisões com resultado aprovado e recusa cobertura ausente ou divergente; registros antigos sem resultado não liberam nova geração. Confere nomes e hashes pelo APR-01. O controle e o histórico internos do modelo e os avisos jurídicos ficam preservados no template original do expediente; o MD e o PDF enviados ao cliente conservam identificação, cláusulas e estado de emissão “Para assinatura”.

A assinatura ocorre exclusivamente pelo painel escolhido pelo cliente, sem API, MCP ou webhook de assinatura. Registre os PDFs assinados e as evidências devolvidas, após conferência humana. Uma imagem de assinatura ou uma resposta “sim” não substitui esse retorno.

`concluir-0b` apenas confere a formalização. `acessos` registra a verificação humana de 0c e `preparar-0d` confere prontidão; nenhum deles abre caso, sela ou libera F0. A passagem para o caso segue o roteiro canônico e os mecanismos autorizados existentes. Preserve o expediente para importação e não escreva diretamente em `fontes/`, `registro/` ou `caso/` de um caso pelo chat.


Após a abertura, planeje e provisione os canais conforme EMCIA-CAN-01 e ROT-02 §3.6. Provisionamento MCP exige contêiner exclusivo do caso já declarado; sem ele, use a interface externa. O engenheiro define os ids pelo terminal antes de importar, ou passa a declaração completa com `--canais`. A ordem é abertura → planejar/provisionar → definir (ou `--canais`) → importar → gravar `00-habilitacao` pelo validador → selar → F0.

A importação é humana: apresente `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/importar_habilitacao.py" --expediente "<caminho>"` para execução no terminal do engenheiro, no diretório do caso, fora da sessão. Não execute essa decisão pela sessão. Depois da importação, o rascunho passa pelo validador; a selagem é um ato deliberado conforme o roteiro canônico.

Em caso aberto com o novo template, a habilidade de F0 e seu encerramento exigem importação com selo confirmado no Git. Após gravar `caso/00-habilitacao.md` pelo validador, apresente a selagem ao engenheiro. Evento `SeloAplicado` sem commit confirmado mantém a passagem bloqueada. Casos antigos seguem seu próprio playbook.

Na orientação de abertura, o engenheiro pode informar `--expediente` a `novo-caso.sh`; isso confere prontidão e identidade antes de criar o caso, mas não substitui a importação humana. O método é copiado do pacote conferido; o estado apresenta seu diagnóstico de integridade somente leitura.

Apresente as restrições RH-xx preservadas no registro. Em P2, o engenheiro vincula cada RH a fontes curadas ou registra dispensa motivada pelo ato `vincular-restricao`, conforme EMCIA-HAB-01 §3.4 e EMCIA-CTX-01 §3.7. RH pendente bloqueia materialização; E1 de caso restrito aguarda P2. Não invente relações REC → F ou destinos nem acrescente ressalva genérica. A decisão 041 completou o contrato da 039.
