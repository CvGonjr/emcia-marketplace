# Testes

```bash
bash testes/negativos.sh
```

Oito verificações. Sete provam que uma trava **recusa**; a quarta é controle positivo — asserção bem marcada precisa gravar, senão o validador está apenas quebrado.

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

Rodam contra uma cópia temporária do template, sem tocar em caso real.

**Falha aqui é regressão de trava, não de funcionalidade.** Não conserte o teste; conserte a trava.
