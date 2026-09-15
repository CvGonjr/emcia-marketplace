# Testes

```bash
bash testes/negativos.sh
```

Dezoito verificações. Catorze provam que uma trava **recusa**; as demais são controle positivo — o que é bem formado precisa passar, senão a trava está apenas quebrada.

| # | Prova |
|---|---|
| 1 | Habilidade de camada não delegável não carrega |
| 2 | Escrita direta em `caso/` é negada |
| 2b | Redirecionamento de shell para `caso/` é negado |
| 3 | Asserção sem origem é recusada |
| 4 | Asserção bem marcada é gravada |
| 5 | Etapa presencial não encerra sem sessão registrada |
| 6 | Autor agente é recusado |
| 7 | Entregável com portão fechado não emite |
| 8 | Playbook sem itens inegociáveis não carrega |
| 14 | Nível fora dos declarados no playbook é recusado |
| 15 | Nível apurado por agente é recusado |
| 16 | Nível válido grava e emite `NivelApurado` *(controle positivo)* |
| 17 | Com o nível apurado pelo comando, F0 encerra *(controle positivo)* |

Rodam contra uma cópia temporária do template, sem tocar em caso real.

**Falha aqui é regressão de trava, não de funcionalidade.** Não conserte o teste; conserte a trava.

## Deslocamento da fronteira por nível

Cinco testes cobrem o que CAT-01 seção 3.6 estabelece: **a camada de uma etapa depende do nível do caso.**

| # | Prova |
|---|---|
| 9 | P1 em N3 é `EX3` — habilidade não carrega |
| 10 | A mesma P1 em N1 é `EX2` — carrega |
| 11 | Sem nível apurado, nenhuma etapa após F0 opera |
| 12 | F0 não encerra sem o nível |
| 13 | Playbook com camada plana, sem mapa por nível, é recusado |

O par 9 e 10 é o mais importante do conjunto: mesma etapa, mesma habilidade, resultado oposto conforme o nível. Se os dois passarem juntos, a fronteira desloca.
