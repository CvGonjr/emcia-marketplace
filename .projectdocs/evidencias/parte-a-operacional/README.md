# Parte A operacional

Base: marketplace 88ac1f44faeb67d66a5b260090d41dfe61ce3c94.
Documentos canônicos locais: emcia-artefatos ab09abeaa3f6aeb21ff94242a70c2ad91c3fd911.
Python do CI: CPython 3.12.12; sem dependências novas, PyYAML opcional ausente.

- A1: argumentos intercalados e regressão descoberta no leitor mínimo.
- A2: confirmação Git de selo posterior ao encerramento; decisão 042.
- A3: vínculos e dispensas humanos; marca junto à asserção; decisão 041.

A linha de base completa está em regressao-inicial-3.12.txt; a final,
sem exclusões, em regressao-final-3.12.txt: 919 verificações, 46 módulos,
zero falhas. Os resultados intermediários e propostas aos artefatos são
preservados em cada pacote. Referência para MAN-01 v0.2: playbook **0.4.18**.

Reexecução (com python3 do 3.12 no PATH):

```bash
python3 .projectdocs/evidencias/parte-a-operacional/reexecutar-suite.py /tmp/regressao-parte-a.txt
```

O repositório contém somente ferramenta e evidência sintética. Não houve
uso de canal remoto, documento de cliente ou edição do pacote do método.
