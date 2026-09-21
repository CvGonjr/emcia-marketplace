# Evidência — pacote operacional do método para o contraste

**Data:** 21/09/2026

## Problema resolvido

As habilidades do campo remetem a `metodo/`, enquanto T2 autoriza somente
`insumo/` e a árvore consumida de `eiac-campo`. A execução estrutural passava,
mas uma sessão real não possuía acesso autorizado aos documentos controlados.

## Implementação

- 16 documentos operacionais oficiais empacotados em
  `eiac-campo/reference/metodo/`.
- `manifesto.json` fixa o SHA-256 de cada documento e a origem controlada.
- Nenhum documento foi copiado para `emcia-contraste`.
- `eiac-campo` elevado de 0.7.1 para 0.7.2.
- Decisão 017 registra fonte única, vínculo de runtime e tratamento de
  ambiguidades como I pendente.
- `AGENTS.md` e o resumo final já existente da Ação 2.6 passam a ser rastreados,
  deixando o repositório apto ao requisito de limpeza do selo.

## Verificação

- `python3 testes/metodo_empacotado.py`: 16 documentos, hashes válidos e nenhuma
  cópia no contraste.
- Suítes Python do marketplace: todas verdes; `campo_2_6_5.py` reexecutado
  isoladamente com 62 verificações e zero falhas.
- `bash testes/negativos.sh`: verde.
- Manifests de `eiac-campo` e `eiac-nucleo`: válidos.
- `git diff -- eiac-campo/skills`: vazio.
