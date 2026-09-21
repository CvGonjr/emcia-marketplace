# Fase 0 — Estabilizar o emcia-marketplace (pré-condição para o contraste)

Pré-condição da pesquisa de contraste (`emcia-contraste`), executada antes de
qualquer trabalho no novo repositório. HEAD ao final: `6f4bb2f` + esta série
de correções.

Data: 21/09/2026

---

## 1. Reprodução em clone limpo

A afirmação inicial ("`testes/campo_2_6_2.py` aborta procurando `AUT-001.yaml`;
`testes/campo_2_6_5.py` tem 6 falhas") **não se reproduziu com o ambiente
Python padrão** (sem PyYAML instalado) — 447/447 verificações passam. Só se
reproduziu instalando PyYAML e ativando o venv (`source venv/bin/activate`,
não apenas chamando o binário do venv diretamente — `subprocess.run(["python3",
...])` dentro dos próprios testes resolve `python3` pelo `PATH`, então um venv
não ativado não afeta os subprocessos que os testes disparam).

Com PyYAML ativo, os dois sintomas reproduziram exatamente como descrito:

- `campo_2_6_2.py`: `FileNotFoundError` em `AUT-001.yaml` (aborta antes do fim).
- `campo_2_6_5.py`: 6 falhas (T04, T30, T31, T46, T57, T60 + regressão em
  2.6.2-T15).

## 2. Causa raiz

`eiac-nucleo/scripts/estrutura.py::carregar_yaml` e
`eiac-nucleo/scripts/quadro.py::ler_yaml` usam PyYAML quando presente e um
parser próprio quando ausente (decisão de projeto: nenhuma dependência externa
obrigatória). Os dois caminhos **não produziam o mesmo tipo de dado para o
mesmo texto**:

- Uma data bare (`data_validacao: 2026-09-19`) vira `datetime.date` com
  `yaml.safe_load` e `str` no parser próprio.
- (Achado adicional, mesmo mecanismo: `quadro.ler_yaml` também devolvia
  `versao: '2'` como `str` sem PyYAML e `int` com PyYAML — sem consumidor
  afetado hoje, corrigido por ser a mesma classe de defeito.)

`eiac-campo/scripts/operacional.py::checar_validacao` (linha 87) chama
`.strip()` direto em `data_validacao`, assumindo `str`. Com PyYAML instalado,
isso quebra com `AttributeError: 'datetime.date' object has no attribute
'strip'` — a especificação operacional de P6 nunca chega a `validado`, P7
recusa em cascata ("`operacional_ref` aponta para especificação em estado
'proposta', não 'validado'"), e o inegociável 2 (termo de autonomia) nunca é
satisfeito. `campo_2_6_2.py` aborta mais cedo porque um dos cenários de teste
lê `AUT-001.yaml` esperando que ele já exista, e o P7 anterior nunca chegou lá.

**Comportamento de trava dependente de dependência opcional instalada** — o
mesmo caso de teste passa ou falha conforme o ambiente, sem nenhuma mudança de
código ou de caso.

## 3. Correção

Sem afrouxar nenhuma trava — o próprio parser sem PyYAML já devolvia o
comportamento correto (`str`); a correção foi tornar o caminho com PyYAML
consistente com ele, não o contrário.

- `estrutura.py` e `quadro.py`: `yaml.safe_load` substituído por
  `yaml.load(texto, Loader=_LoaderSemTimestamp)`, onde `_LoaderSemTimestamp` é
  uma subclasse de `yaml.SafeLoader` com o resolvedor implícito de
  `tag:yaml.org,2002:timestamp` removido. **Continua um `SafeLoader`** — nenhum
  construtor novo foi adicionado, então continua incapaz de instanciar objetos
  Python arbitrários (verificado manualmente: uma tag
  `!!python/object/apply:os.system` continua recusada com
  `ConstructorError`, igual a `safe_load`).
- `quadro.py`, parser próprio: passou a coagir escalares inteiros
  (`re.fullmatch(r"-?\d+", v)`) para paridade com o que PyYAML já fazia,
  fechando o segundo achado.

## 4. Teste negativo (item 1b)

Novo arquivo `testes/nucleo_yaml.py`: carrega a mesma fixture pelos dois
caminhos (PyYAML real, quando instalado; e um segundo carregamento do módulo
com `mod.yaml = None`, forçando o caminho sem dependência) e exige dicionário
idêntico, campo a campo — inclusive o tipo do campo de data. Inclui também um
controle positivo que chama `operacional.checar_validacao` diretamente sobre o
resultado de `carregar_yaml`, reproduzindo o ponto exato de quebra original.

Rodado antes da correção (branch com o loader antigo): a comparação
`com-PyYAML != sem-PyYAML` falha, confirmando que o teste pega o defeito.
Depois da correção: 0 falhas nos dois ambientes.

## 5. Suíte completa nas duas condições (item 1c)

| Suíte | Sem PyYAML | Com PyYAML |
|---|---|---|
| `negativos.sh` (33 + 8 G6) | ok | ok |
| `contexto.py` (11) | ok | ok |
| `campo_2_6_2.py` (38) | ok | ok |
| `campo_2_6_3.py` (57) | ok | ok |
| `campo_2_6_4.py` (50) | ok | ok |
| `campo_2_6_5.py` (62) | ok | ok |
| `campo_2_6_6.py` (43) | ok | ok |
| `curadoria.py` (17) | ok | ok |
| `p3d.py` (12) | ok | ok |
| `ctx_v.py` (23) | ok | ok |
| `integracao.py` (17) | ok | ok |
| `consolidado.py` (16) | ok | ok |
| `playbook_2_6_0.py` (29) | ok | ok |
| `nucleo_2_6_1.py` (39) | ok | ok |
| `nucleo_yaml.py` (novo) | 5, 0 falhas | 7, 0 falhas |

Saída completa em `suite-sem-pyyaml.txt` e `suite-com-pyyaml.txt`. Sem CI
configurado neste repositório para incluir as duas condições na matriz —
registrado como pendência de infraestrutura, não deste pacote.

## 6. Pendências removidas do playbook (item 2)

As duas entradas de `pendencias` no `playbook.json` do template referiam-se a:

1. HB de P6–P10 ainda não implementadas — confirmado que as 18 HB existem no
   catálogo (`eiac-campo/reference/habilidades.json`, `2.6.4-T01–T06`).
2. Motor do núcleo sem interpretação semântica de E3-E/recorrência/
   inegociáveis — confirmado implementado e testado (`2.6.5-T01–T12`,
   `2.6.0-T17`, `2.6.1-T15/T16`).

Ambas removidas. `versao` do playbook: `0.4.0` → `0.4.1`.

## 7. Decisão 006 atualizada (item 3)

Estado mudou de "⚠️ EM CONFLITO COM DOCUMENTO CONTROLADO" para "resolvida —
D/I/V, conforme documento controlado". A dimensão "Contexto" (campo · antitese
· conversa · livre) da proposta original foi descartada — o problema que ela
tentava resolver (identificar qual execução produziu a asserção) passou a ser
resolvido pelo campo `execucao` (`campo`/`contraste`) previsto para o
contraste, não por mais uma dimensão de procedência. `apuração`
(medido/calculado/estimado) — a única parte que sobreviveu da proposta — já
está implementada e testada, sem mudança de código nesta fase.

## 8. Decisão 014 registrada, 004 substituída (item 4)

`decisoes/014-execucao-de-contraste.md`: a execução de contraste roda fora do
caso de campo, em repositório e plugin próprios (`emcia-contraste` /
`eiac-contraste`), antes do F0 de um caso de campo — nunca como fase
intermediária dele. O caso de campo nunca carrega dado da execução de
contraste. `decisoes/004-janela-da-antitese.md` marcada como substituída
(estado editado; corpo original preservado, conforme convenção do
`decisoes/README.md`).

## 9. G6 — fontes/ protegida contra escrita de agente (item 5)

`fontes/README.md` já declarava "só leitura", mas nada impedia a escrita antes
da citação — só o SHA-256 gravado por `validar.py` detectava alteração
**depois** dela. Nova regra G6 em `guarda.py`: nega Write, Edit e Bash
(redirecionamento, `mv`, `cp`, `rm`) sobre qualquer caminho com segmento
`fontes/` na árvore do caso — cobre a raiz (`fontes/`, o gap real) e
`contexto/fontes/` (já coberta também por G2b, mantida como defesa em
profundidade). Cada recusa emite evento, como as demais regras da guarda.
Leitura permanece permitida (controle positivo G6h).

Teste negativo escrito antes da implementação (`testes/negativos.sh`, blocos
G6a–G6h): G6a–e falhavam antes da mudança em `guarda.py` (nenhuma trava
existia), G6f/g/h já passavam (cobertos por G2b/infra de eventos
pré-existente). Depois da implementação, os 8 passam.

`eiac-nucleo` versão: `0.2.16` → `0.2.17` (mudança em scripts do núcleo:
`estrutura.py`, `quadro.py`, `guarda.py`).

## 10. Arquivos alterados

```
decisoes/004-janela-da-antitese.md               (estado marcado substituída)
decisoes/006-procedencia-tres-dimensoes.md       (estado resolvida, D/I/V)
decisoes/014-execucao-de-contraste.md            (novo)
decisoes/README.md                               (tabela atualizada)
eiac-campo/template-caso/registro/playbook.json  (pendencias removidas, versao 0.4.1)
eiac-nucleo/.claude-plugin/plugin.json           (versao 0.2.17)
eiac-nucleo/scripts/estrutura.py                 (loader YAML deterministico)
eiac-nucleo/scripts/quadro.py                    (loader YAML deterministico + coercao int)
eiac-nucleo/scripts/guarda.py                    (regra G6)
testes/negativos.sh                              (8 verificacoes G6)
testes/nucleo_yaml.py                            (novo, 5-7 verificacoes)
```

## 11. Critério de pronto da Fase 0

- [x] Sintoma reproduzido em condição real (PyYAML instalado), não apenas
      hipotetizado.
- [x] Causa raiz identificada e corrigida sem afrouxar trava nenhuma.
- [x] Teste negativo cobre o defeito, escrito e confirmado falhando antes da
      correção.
- [x] Suíte inteira verde nas duas condições de ambiente.
- [x] Pendências resolvidas removidas do playbook.
- [x] Decisão 006 atualizada; decisão 014 registrada; decisão 004 marcada
      substituída.
- [x] G6 implementada com teste negativo primeiro.
- [x] Versões de plugin (`eiac-nucleo`) e de playbook incrementadas.

Fase 0 concluída. Aguardando revisão antes de iniciar a Fase 1 (inventário da
interface núcleo↔campo), conforme instrução do pedido original.
