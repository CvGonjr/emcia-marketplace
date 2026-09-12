# eiac-nucleo

Núcleo determinístico. **Não conhece método nenhum.**

Lê `registro/playbook.json` do repositório do caso e aplica o que ele declara. O que o núcleo exige de qualquer playbook:

- toda etapa declara `camada` e `modalidade`
- todo entregável declara um `portao`
- existe uma lista de `inegociaveis`, não vazia
- existem rótulos de `procedencia`

Playbook que omita qualquer um desses não carrega, e o caso não opera.

## Scripts

| Script | Função |
|---|---|
| `guarda.py` | Hook `PreToolUse`. Três regras, `exit 2` bloqueia |
| `validar.py` | Único caminho de escrita em `caso/` |
| `avancar.py` | Encerrar etapa, registrar sessão, emitir entregável |
| `estado.py` | Lê e grava o Registro; emite eventos |
| `playbook.py` | Carrega e valida o playbook |

Nenhuma decisão passa por modelo de linguagem.

## Invariantes

| # | Invariante | Onde |
|---|---|---|
| I-1 | Toda asserção tem contexto e origem | `validar.py` |
| I-2 | Nenhuma ação executa fora da camada da etapa | `guarda.py` G1 |
| I-3 | Etapa não avança sem cumprimento | `avancar.py` |
| I-4 | Etapa dependente exige sessão registrada | `guarda.py` G3, `avancar.py` |
| I-7 | Autor é sempre pessoa nomeada | `validar.py`, `avancar.py` |
| I-9 | Inegociáveis condicionam a emissão | `avancar.py` |

## Limite honesto

A hook vive no plugin, e o plugin pode ser desinstalado. Continua sendo pedágio com rastro, não parede. A diferença em relação a configuração local é que o contorno exige desinstalar algo versionado, e isso é visível.
