# Camada de contexto — CA4

Estrutura definida em `CTX-01`. Quatro objetos, um arquivo por registro.

```
contexto/
├── termos/      T-001.yaml   glossário do processo (P2)
├── entidades/   E-001.yaml   objetos do domínio (P2, refinado em P3)
├── regras/      R-001.yaml   o objeto central (P2 e P3)
└── fontes/      F-001.yaml   contratos de dados (P2)
```

## Trava de curadoria

Nenhum registro entra aqui sem curadoria humana — `EX4`. A candidata nasce em `rascunho/` com `origem: inferido`; vira registro de contexto quando uma pessoa a cura, e a curadoria cria versão nova com autor, data e justificativa.

## Quadro frequência × consequência

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quadro.py"
```

Se a célula **rara × alta** estiver vazia ao fim do P3, ou a organização é excepcionalmente regular, ou o levantamento não aconteceu. Confronte as duas hipóteses antes de encerrar o passo.
