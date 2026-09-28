# 032 — Caminhos normalizados relativos à raiz do caso (A19)

**Data:** 28/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

Edit recebeu um absoluto para `registro/estado.json`; o prefixo relativo
não coincidiu, e a escrita foi liberada sem evento. Read/Write/Edit recebem
caminhos absolutos do Claude Code, conforme seu contrato de hooks.

## Decisão

A guarda localiza o caso pela raiz de projeto informada pelo runtime,
pelo cwd do hook ou pelo diretório de execução, procurando o registro nos
ancestrais. O playbook continua sendo exclusivamente o do caso.

Um único contexto de caminhos resolve absoluto, relativo ao cwd da
ferramenta, `~`, `..` e links simbólicos. Todas as comparações de áreas usam
representações relativas à raiz física do caso. Preserva também a forma
lexical: um link de registro para fora não libera a escrita; um alias
externo para dentro continua protegido. Caminho não resolvível é recusado.

A mesma normalização serve às áreas caso/contexto/registro/fontes e à
identificação de habilidades. Alvos e argumentos de Bash são segmentados
com shlex; cd, subshell, pipeline e shell aninhado preservam seu contexto.
Literais de código inline são inspecionados sem executar esse código.
NotebookEdit também passa pela proteção de escrita. Recusas produzem evento.

## Consequência e verificação

`testes/caminhos_a19.py` cobre as cinco áreas, cinco formas de caminho,
Edit/Bash, cp/mv/tee, raiz mantida com cwd externo, fontes, leitura e
rascunho. Inclui os parâmetros de Edit da sessão controle-37, substituindo
somente a raiz temporária. Arquivos externos sem alias para o caso não são
classificados como registro do caso só pelo nome de uma pasta.

Referência: [entrada PreToolUse](https://code.claude.com/docs/en/hooks#pretooluse-input).
