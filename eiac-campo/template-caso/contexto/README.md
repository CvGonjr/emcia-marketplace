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

Para validar uma instância, a partir da raiz do caso:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/estrutura.py" \
  --tipo regra --arquivo contexto/regras/RN-001.yaml
```

## Trava de curadoria

Nenhum registro entra aqui sem curadoria humana — `EX4`. A candidata nasce em `rascunho/` com `procedencia: I`; vira registro de contexto quando uma pessoa a cura, e a curadoria cria versão nova com autor, data e justificativa.

O contrato documental é `procedencia: D | I | V`. A candidata inferida nasce
com `procedencia: I` e premissa. Os campos de autoria, histórico e confronto
já fazem parte da estrutura; as regras comportamentais de curadoria,
versionamento e resolução referencial pertencem aos pacotes seguintes.

## Quadro frequência × consequência

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quadro.py"
```

Se a célula **rara × alta** estiver vazia ao fim do P3, ou a organização é excepcionalmente regular, ou o levantamento não aconteceu. Confronte as duas hipóteses antes de encerrar o passo.
