# Camada de contexto — CA4

Estrutura definida em `CTX-01`. Quatro objetos, um arquivo por registro.

```
contexto/
├── termos/      T-001.yaml   glossário do processo (P2)
├── entidades/   E-001.yaml   objetos do domínio (P2, refinado em P3)
├── regras/      RN-001.yaml  o objeto central (P2 e P3)
└── fontes/      F-001.yaml   contratos de dados (P2)
```

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
com `procedencia: I` e premissa. A resolução referencial entre objetos
(Regra → Entidade, Regra → Fonte etc.) e a semântica completa de
`classificacao_confronto`/`referencia_p3d` pertencem aos pacotes seguintes.

## Quadro frequência × consequência

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quadro.py"
```

Se a célula **rara × alta** estiver vazia ao fim do P3, ou a organização é excepcionalmente regular, ou o levantamento não aconteceu. Confronte as duas hipóteses antes de encerrar o passo.
