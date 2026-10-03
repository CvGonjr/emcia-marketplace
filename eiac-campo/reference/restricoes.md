# Vínculos de restrições — decisão 041

No terminal humano, durante P2:

```bash
python3 "$EIAC_CAMPO/scripts/restricoes.py" vincular --restricao RH-01 --fontes F-001,F-002
python3 "$EIAC_CAMPO/scripts/restricoes.py" dispensar --restricao RH-02 --motivo "Nenhuma fonte do recorte usa esse item"
```

O responsável do caso é o autor fixado. A guarda da sessão recusa ambas as
operações e devolve o comando exato. `registro/restricoes.json` preserva
vigentes e histórico; cada revisão exige `--nova-versao rascunho/decisao.json`
com restricao, versao_anterior, decisor, motivo e data. Fora de P2, somente
revisão de vínculo existente após o encerramento de P2 é admitida.

Os registros materializados declaram `fontes: [F-001]` para todo o registro,
ou `fontes_por_campo: {valor_atual: [F-001]}` para uma asserção específica.
Um campo marcado `fonte: REC-000001` ou uma referência REC na lista exige
relação explícita: o objeto F curado declara `recebimentos: [REC-000001]`.
O recebimento precisa existir e seus hashes devem conferir. Nenhuma relação
é obtida por semelhança de nomes, texto livre ou interpretação do agente.

As fontes precisam estar em contexto/fontes com contrato CTX e evento de
curadoria. As marcas incluem RH, F, item negado, restrição e motivo junto
à asserção. Campos sem fonte declarada não recebem vínculo inferido.
Se houver RH pendente, qualquer materialização fica bloqueada; por isso E1
em um caso restrito só é materializado após os vínculos de P2.

O manual base permanece preservado. `manual-emenda-041.json` registra a
emenda local aprovada pela decisão 041 para a conferência do playbook
0.4.18; a proposta para o MAN-01 v0.2 está na evidência da parte A.

Demonstrações: `preparar-caso.sh <nome> <etapa> com-restricao` e
`percurso-completo.sh <nome> com-restricao`. Usam somente dados sintéticos,
curadoria e vínculo reais; não dispensam automaticamente nenhuma restrição.
