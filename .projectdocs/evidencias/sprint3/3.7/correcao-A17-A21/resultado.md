# Sprint 3 — ação 3.7 — correção A17–A21

**Data:** 28/09/2026. **Versão:** v-sprint3-poc.6.

Base de código: `v-sprint3-poc.5`, commit
`3011d886300ba911e1bc085bb4657872af02131c`. O commit anterior ao trabalho,
`08edbd3`, acrescenta a evidência da sessão 1; ela foi preservada.
Código e documentação verificados em `bcde876` (o commit seguinte só
acrescenta este pacote de evidência). Núcleo 0.2.32; campo 0.8.6.
Nenhuma regra de método nova foi introduzida no núcleo; G1 continua lendo
habilidade/delegabilidade/camada do playbook do caso. O pacote do método e
o playbook não foram alterados.

## Antes e depois

| Achado | Antes na .5 | Correção e resultado |
|---|---|---|
| A18 | Skill fora do matcher; sessão registrada liberava até habilidade não delegável | Read/Skill/Grep/Bash e UserPromptExpansion identificam o nome declarado; não delegável recusa mesmo com sessão/selo, em N1/N2/N3; TentativaNegada |
| A19 | Edit absoluto não coincidia com registro/; aliases escapavam das comparações | Contexto único normaliza absoluto/relativo/../link; protege caminho lexical e físico, inclusive alias externo para dentro; todas as áreas, escrita Bash e habilidades usam a resolução |
| A20 | Qualquer `>` associado a uma área parecia escrita | shlex distingue redirecionamento de texto; só seus alvos normalizados entram nas regras de escrita; leitura com descarte e cópia para rascunho passam; stdout/stderr/append para área protegida recusam |
| A21 | A habilidade sugeria `[tentativa-negada …]`, sem procedência aceita pelo validador | A instrução remete a TentativaNegada da guarda; não cria asserção nem inventa D/I/V para uma recusa |
| A17 | Estado mostrava o campo selo vazio mesmo após SeloAplicado | JSON e resumo derivam último selo confirmado do Git: hash completo, data e nota; tentativa de commit recusada não substitui selo; consulta não suja o caso |

### Entrada real e contrato dos hooks

Além da tabela da [sessão 1](../sessao-1/tabela-sessao.md), foram consultados
os transcripts locais do caso sintético `/tmp/emcia-demos/controle-37`.
O carregamento de hb-levantar-regras ocorreu por **Skill**, com
`{"skill":"eiac-campo:hb-levantar-regras"}`. Os parâmetros de Edit incluem
file_path absoluto, old_string, new_string e replace_all. O corpus
`testes/apoio/entradas_sessao_37.json` preserva esses parâmetros; o teste de
Edit substitui apenas a raiz temporária do caso.

[entradas-sessao-real.jsonl](entradas-sessao-real.jsonl) reúne os parâmetros
extraídos das chamadas, inclusive a restauração de P10. Os campos comuns
para exercitar a guarda (hook_event_name/permission_mode, por exemplo)
foram reconstruídos conforme o contrato oficial: **não é captura bruta do
stdin do hook**. Os testes acrescentam session_id, cwd, transcript_path e
tool_use_id de controle. Não houve nova sessão com modelo; a verificação
foi a execução determinística dessas entradas pela guarda.

Rotas verificadas: arquivo por Read absoluto/relativo/instalado, `..` e
link; leitura de conteúdo por Grep/Bash; Skill com e sem namespace;
invocação direta `/nome` por UserPromptExpansion. O matcher anterior não
alcançava Skill. A invocação direta não dispara PreToolUse, por isso tem
hook próprio. Habilidades delegáveis de camada humana conservam o uso
instrumental após sessão da própria etapa; decisões continuam no terminal.
Os dois agentes físicos do campo não declaram pré-carregamento por `skills`.

Referências oficiais consultadas: [hooks](https://code.claude.com/docs/en/hooks)
e [habilidades](https://code.claude.com/docs/en/skills). CLI local: Claude
Code **2.1.283**. Validação dos dois manifests em
[validacao-plugins.txt](validacao-plugins.txt): ambos aceitos; o aviso sobre
`variante` é o campo interno já existente no núcleo, ignorado pelo runtime.
A instalação atualizada deve iniciar uma sessão nova: um hook não remove
conteúdo que a sessão da .5 já carregou.

### Caminhos e shell

As áreas registro/, caso/, contexto/, fontes/ e contexto/fontes/ têm
controles de absoluto, relativo, `..`, link externo e cwd em subdiretório,
com Edit e Bash. Há controle positivo de arquivo externo sem alias para o
caso. Um link de registro para fora continua protegido lexicalmente.
Cwd externo não perde a raiz da sessão quando CLAUDE_PROJECT_DIR a informa.

A inspeção conserva os contextos de cd, shell aninhado, subshell e pipeline;
cp/mv/tee têm alvos normalizados. A revisão capturou dois escapes de cwd
antes de corrigir a resolução, registrados em
[caminhos-a19-revisao.txt](caminhos-a19-revisao.txt). A seleção de saída
preserva a diferença entre `2>/dev/null`, `2>&1`, `&>registro/x` e `>` entre
aspas/escapado. G6k continua recusando remoção indireta de fonte por Python.

### Selo

A leitura percorre commits da trilha do próprio caso, identifica a primeira
introdução de SeloAplicado com nota/autoria correspondentes e conserva o
hash desse commit. Não confunde HEAD de um commit posterior comum com o
selo. Não regrava estado.json: o campo exibido é uma informação derivada,
e o campo bruto não se torna uma segunda fonte. Sem histórico Git
acessível, não se apresenta um hash como confirmado.

## Testes novos e totais

| Módulo | Verificações | Resultado |
|---|---:|---|
| habilidades_a18.py | 13 | verde |
| caminhos_a19.py | 62 | verde |
| redirecionamentos_a20.py | 12 | verde |
| recusa_a21.py | 2 | verde |
| selo_a17.py | 7 | verde |
| **Novas** | **96** | **0 falhas** |
| **Anteriores preservadas** | **673** | **0 falhas** |
| **Suíte completa — 33 módulos** | **769** | **0 módulos com falha** |

A suíte executa negativos.sh e todos os módulos `.py` da raiz de testes/.
[saida-suite.txt](saida-suite.txt) contém contagem por módulo, comandos,
códigos de saída e stdout/stderr integrais. Contam-se os testes unittest e
as verificações dos módulos anteriores, sem duplicar suas reexecuções
internas. Os dois módulos encapsulados esforço/método contam uma unidade
cada, conforme a convenção das evidências anteriores.

As negativas foram escritas e executadas antes das correções: registros em
[antes/](antes/), com negativos/contexto iniciais verdes nos arquivos deste
pacote. A versão final dos novos testes também foi reexecutada contra uma
cópia isolada da .5: todos os cinco módulos falham, em [base-v5/](base-v5/).
[depois/](depois/) registra os cinco módulos verdes após a correção; a
bateria integral foi repetida sobre o código commitado, em saida-suite.txt.
Nenhum teste existente foi apagado.

## Teste existente ajustado

| Teste | Ajuste | Cobertura preservada |
|---|---|---|
| verificacao_por_estados.py — T04, verificação de carregamento | Com sessão e selo posterior, agora exige saída 2 e mensagem de não delegabilidade | T04 continua exigindo encerramento humano bem-sucedido com selo; T01/T02/T03 mantêm recusas sem selo ou com selo anterior; total do módulo permanece 7 |

Os comentários do mesmo módulo e as descrições de G1 no README dos testes
foram alinhados. Nenhuma preparação de outro teste foi modificada para
contornar uma trava.

## Commits e decisões

| Achado | Commit | Decisão |
|---|---|---|
| A18 | 8d63564 | 031 |
| A19 | 0bfee21 | 032 |
| A20 | ec4ed11 | 033 |
| A21 | bdba4d5 | 034 |
| A17 | f1c9811 | 035 |
| Documentação e índice | bcde876 | README/INSTALACAO/map/testes e índice 031–035 |

[diff.patch](diff.patch) compara o código, testes e documentação da .5
com esses commits; não inclui mudanças anteriores do usuário nas evidências
3.1/3.2/3.4/3.5/3.6/3.9. [fontes-verificadas.sha256](fontes-verificadas.sha256)
registra os arquivos de implementação, playbook, testes e documentação
verificados, permitindo conferir a identidade com a versão da tag.

Reexecução a partir da raiz do repositório:

```bash
python3 .projectdocs/evidencias/sprint3/3.7/correcao-A17-A21/reexecutar-suite.py
```
