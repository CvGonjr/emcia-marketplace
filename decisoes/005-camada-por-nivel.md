# 005 — Camada resolvida por nível

**Data:** setembro de 2026 · **Estado:** firme
**Referência:** EMCIA-CAT-01 seção 3.6

## Contexto

A camada de uma etapa não é fixa. O alcance da preparação automatizada vai até o passo 4 em N1, até o passo 2 em N2, e apenas F0 em N3. O núcleo aplicava camada plana e, com isso, um caso N3 rodava com a fronteira de N2 — justamente onde a consequência do erro é alta e regulada.

## Decisão

O playbook declara `camada` como mapa por nível:

```json
"camada": { "N1": "EX2", "N2": "EX2", "N3": "EX3" }
```

O carregador recusa camada plana. Sem nível apurado, aplica-se **a mais restritiva declarada** — não se assume o nível mais permissivo enquanto a triagem não apurou. Nenhuma etapa após F0 opera sem nível, e F0 não encerra sem ele.

## Consequência

Ruptura deliberada: caso aberto com playbook antigo não carrega. Um caso rodando com fronteira que ignora o nível é pior que um caso travado.

Testes 9 e 10 da suíte provam o par: mesma etapa, mesma habilidade, resultado oposto conforme o nível.
