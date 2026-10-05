# 046 — Comparador de formulário no formato real do conector Tally

**Data:** 05/10/2026 · **Estado:** firme por instrução do engenheiro

## Contexto

A conferência automática de formulário (045) foi escrita para o formato da API Tally,
com o texto da pergunta em `payload.html`. O conector MCP `mcp__tally__load_form`
devolve o texto em `payload.safeHTMLSchema`, sem `html`. Com isso, uma leitura real
do formulário 7R8Z20 era recusada como "formato de retorno não conferível", e a
publicação ficava bloqueada mesmo com o formulário correto.

## Decisão

Adapta-se o comparador ao formato real devolvido por `mcp__tally__load_form`, com as regras abaixo.

1. **Fonte do formato:** somente o retorno real capturado. A fixture de teste deriva
   desse retorno, trocando apenas ids e títulos. Capturas de modelos entram quando fornecidas.
2. **Texto da pergunta:** usa `payload.html` quando existe; senão, `payload.safeHTMLSchema`,
   concatenando os trechos de texto na ordem. Se os dois existirem e o texto divergir, recusa.
3. **Normalização**, aplicada igualmente ao contrato e ao retorno, e nada além disso:
   Unicode NFC; espaço não separável convertido em espaço comum; espaços nas bordas
   removidos; marcação de formatação ignorada na comparação (o `**` do contrato e as
   marcas do schema), com registro no relatório de onde havia formatação. Diferença de
   pontuação, acento, palavra, ordem ou espaço interno continua sendo divergência.
4. **Opções e campos ocultos:** lidos no formato devolvido pelo conector, com mapeamento
   explícito e testado. O campo oculto precisa existir com o nome exato `caso`.
5. **Estrutura não reconhecida** (bloco de tipo desconhecido, campo ausente, safeHTMLSchema
   fora do formato): recusa, com o caminho do item no relatório (`blocks[i]`). Nada é
   aceito por presunção.
6. **Testes negativos antes da implementação:** palavra trocada; acento removido; ordem
   trocada; pergunta a mais; pergunta a menos; campo oculto ausente ou com outro nome;
   html e safeHTMLSchema divergentes; bloco de tipo desconhecido; formId não declarado.
   Positivos: formulário idêntico com espaço não separável e negrito.
7. **Conferência humana permanece.** O relatório do comparador é a evidência; o engenheiro
   confirma com "conferido". O caminho manual com PDF continua como alternativa.

## Consequência

- Os testes negativos foram escritos e vistos falhando antes da implementação; depois da
  implementação, a suíte de `conferencia_formulario.py` passa (48 testes na revisão).
- A normalização é a única tolerância: nenhuma pergunta é aproximada por semelhança.
- Um formulário montado com prefixo de id nas perguntas (por exemplo `HAB-0a-1 · …`)
  diverge do modelo e não é publicável sem correção do texto no painel.
- As fixtures fornecidas do formulário 7R8Z20 preservam o formato capturado, com ids
  de contexto e título sintéticos, sem respostas de cliente. A fixture idêntica retira
  os prefixos e exercita NBSP/negrito; não se afirma captura de outro formulário.
- Versão do `eiac-campo`: 0.8.29. README, instalação e mapa passam a citar essa versão.
- Não substitui a decisão 045 nem altera a aprovação humana; apenas corrige o formato lido.

## Conferência antes do commit

A revisão encontrou trechos com elementos extras, marcas malformadas ou sem
mapeamento aceitos silenciosamente. Cinco novos negativos reproduziram as
lacunas antes da correção. O leitor agora exige um trecho de texto com marcas
opcionais no formato capturado; marca não reconhecida recusa. Tipo inválido
também indica blocks[i]. O teste adicional de INPUT_DESCONHECIDO mostrou
que o prefixo INPUT_ aceitava um tipo sem mapeamento; a lista de tipos passa
a ser explícita, com recusa por blocks[i]. Marcador ** não pareado não é retirado como formatação.
A mesma normalização restrita continua aplicada aos dois lados da comparação.

Os 48 testes incluem os negativos da revisão e os controles NFC/bordas, espaços
internos e campo oculto ausente no formato real. A regressão integral em 3.12/3.14
e os hashes estão em .projectdocs/evidencias/comparador-conector-real/. Permanece
a falha conhecida A25 da 045, sem nova divergência ou alteração do pacote canônico.
