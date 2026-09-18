# Camada de contexto — CA4

Estrutura definida em `CTX-01`. Quatro objetos, um arquivo por registro.

```
contexto/
├── termos/         T-001.yaml    glossário do processo (P2)
├── entidades/      E-001.yaml    objetos do domínio (P2, refinado em P3)
├── regras/         RN-001.yaml   o objeto central (P2 e P3)
├── fontes/         F-001.yaml    contratos de dados (P2)
└── divergencias/   DIV-001.yaml  registro de confronto P3d (não é um dos quatro objetos CTX)
```

`divergencias/` não é um quinto objeto do CTX-01 — é o registro estruturado do confronto produzido em **P3d**, que `classificacao_confronto.referencia_p3d` da Regra aponta para localizar. Guarda `documento_diz`, `observado`, `justificativa` e `autor`; a Regra não duplica esse detalhe, só a classificação e a referência.

Os modelos seguem o EMCIA-CTX-01 v0.4. O contrato estrutural executável está
em `registro/contexto.schema.json`; ele declara campos obrigatórios, tipos,
padrões de identificador e as condições mínimas de procedência.

Para validar uma instância sem gravar nada, a partir da raiz do caso:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/estrutura.py" \
  --tipo regra --arquivo contexto/regras/RN-001.yaml
```

## Trava de curadoria

`contexto/` não aceita escrita direta — a guarda bloqueia `Write`/`Edit`/redirecionamento de shell para dentro do diretório, do mesmo modo que já bloqueia `caso/`. O único caminho de gravação é o curador:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curar.py" \
  --tipo regra --arquivo contexto/regras/RN-001.yaml --registrado-por "Nome da pessoa"
```

O candidato precisa estar em `rascunho/<mesmo-nome>`. O curador valida a estrutura pelo schema, confere que `autoria_conteudo`, `declarado_por` e `registrado_por` são pessoa nomeada (nunca agente) e só grava se passar.

Quando já existe um registro curado com o mesmo id e a mudança altera a `procedencia` — por exemplo `I` → `V` — o candidato precisa trazer `versao` incrementada e uma entrada de `historico` que preserve a versão anterior (versão, data e responsável). Sobrescrever a versão existente sem esse histórico é recusado; a versão anterior permanece legível dentro do registro atualizado.

O contrato documental é `procedencia: D | I | V`. A candidata inferida nasce
com `procedencia: I` e premissa.

## Resolução de referências

A Regra referencia Termo, Entidade e Fonte em `entradas` (`T-*`, `E-*`,
`F-*`); a Entidade referencia Fonte em `onde_vive` (`F-*`). Toda referência
precisa resolver para um objeto já curado no diretório correspondente —
`T-999` que não existe em `contexto/termos/` é recusado, e o mesmo vale
para Entidade e Fonte. Um arquivo físico em `fontes/` **não** é o mesmo que
um objeto Fonte CTX curado em `contexto/fontes/`: só o segundo satisfaz a
referência, e precisa ter passado pelo próprio contrato mínimo (`contrato.estrutura`,
`contrato.significado`, `contrato.qualidade`).

Essa é a bateria formal **CTX-V01–CTX-V11** do EMCIA-CTX-01 3.13, implementada
em `curar.py`. A matriz completa (regra oficial, implementação, negativo e
positivo) está em `.projectdocs/evidencias/sprint2/2.5.4/matriz-ctx-validacoes.md`.

## Confronto P3d

A taxonomia oficial de classificação é a do EMCIA-ROT-01 3.9: `alinhada`,
`divergente`, `nao_documentada`, `orfa`, `escrita_inacessivel`. Qualquer
outro valor em `classificacao_confronto.classe` é recusado.

Só a classe `divergente` exige `referencia_p3d` preenchida e resolvível —
é a única para a qual o CTX-01 3.5 descreve o conteúdo mínimo que o
registro referenciado precisa ter. A referência precisa apontar para um
`contexto/divergencias/<id>.yaml` já curado:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curar.py" \
  --tipo divergencia --arquivo contexto/divergencias/DIV-001.yaml \
  --registrado-por "Nome da pessoa" --schema registro/p3d.schema.json
```

O `autor` do registro de confronto precisa ser pessoa nomeada — P3d é `EX3`
(EMCIA-CAT-01), o Estúdio prepara e organiza, mas não confirma o confronto
por conta própria. Mudar `classificacao_confronto` numa Regra já curada é
mudança relevante do mesmo jeito que mudar `procedencia`: exige versão nova
com histórico que preserve a versão anterior.

## Quadro frequência × consequência

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quadro.py"
```

Se a célula **rara × alta** estiver vazia ao fim do P3, ou a organização é excepcionalmente regular, ou o levantamento não aconteceu. Confronte as duas hipóteses antes de encerrar o passo.
