# eiac-nucleo

Núcleo determinístico. **Não conhece método nenhum.**

Lê `registro/playbook.json` do repositório do caso e aplica o que ele declara. O que o núcleo exige de qualquer playbook:

- toda etapa declara `camada` e `modalidade`
- todo entregável declara um `portao`
- existe uma lista de `inegociaveis`, não vazia
- existe um contrato não vazio de valores e rótulos de `procedencia`

Playbook que omita qualquer um desses não carrega, e o caso não opera.

## Scripts

| Script | Função |
|---|---|
| `guarda.py` | Hook `PreToolUse`. Três regras, `exit 2` bloqueia |
| `validar.py` | Único caminho de escrita em `caso/` |
| `estrutura.py` | Valida objetos estruturados contra schema declarado no caso |
| `curar.py` | Único caminho de escrita em `contexto/`; impõe versionamento sem sobrescrita |
| `avancar.py` | Apurar nível, encerrar etapa, registrar sessão, emitir entregável |
| `estado.py` | Lê e grava o Registro; emite eventos |
| `playbook.py` | Carrega e valida o playbook |
| `selar.py` | Único caminho de commit no repositório do caso |
| `fronteira.py` | Imprime o que é preparável e o que exige pessoa, para o nível do caso |

Nenhuma decisão passa por modelo de linguagem.

`estrutura.py` não conhece os objetos do EMCIA. Tipos, campos obrigatórios,
formatos e valores de procedência são lidos do schema congelado no caso.

## Documento citado

Uma asserção que cita `documento: <nome>` só grava se o arquivo estiver em `fontes/`, e o hash do que foi lido entra no evento. Citação que aponta para fora do repositório não é verificável, e trocar um documento já citado passa a aparecer na trilha em vez de mudar a base da asserção em silêncio.

## Invariantes

| # | Invariante | Onde |
|---|---|---|
| I-1 | Toda asserção tem procedência documental declarada pelo playbook | `validar.py` |
| I-2 | Nenhuma ação executa fora da camada da etapa | `guarda.py` G1 |
| I-3 | Etapa não avança sem cumprimento | `avancar.py` |
| I-4 | Etapa dependente exige sessão registrada | `guarda.py` G3, `avancar.py` |
| I-7 | Autor é sempre pessoa nomeada | `validar.py`, `avancar.py` |
| I-9 | Inegociáveis condicionam a emissão | `avancar.py` |
| I-10 | O nível entra pelo comando, com autor e evento | `avancar.py` |
| I-11 | O selo sai com o autor nomeado, não com a identidade da máquina | `selar.py` |
| I-12 | A fronteira humana é anunciada antes de ser aplicada | `estado.py`, `fronteira.py` |
| I-13 | Documento citado existe em `fontes/` e tem o hash na trilha | `validar.py` |
| I-14 | Nenhuma escrita direta em `contexto/`; só o curador grava | `guarda.py` G2b, `curar.py` |
| I-15 | Mudança de procedência ou de classificação de confronto em `contexto/` só entra como versão nova, com histórico | `curar.py` |
| I-16 | Classe de confronto que exige vínculo com P3d (`divergente`) só cura com `referencia_p3d` resolvível | `curar.py` |
| I-17 | Toda referência declarada em `references` do schema do caso resolve para um objeto curado existente | `curar.py` |

`autor_e_agente`, em `estado.py`, centraliza a convenção lexical usada por
`validar.py`, `avancar.py`, `selar.py` e `curar.py` para recusar identificador
de agente como autor humano. É uma convenção de nome, não identidade tipada
de ator — limitação assumida enquanto o núcleo não tiver um contrato de
papel/ator mais rico.

## Resolução de referências (I-17)

`curar.py` lê dois blocos declarativos do schema do caso: `catalogo_referencias`
(prefixo do id → tipo e diretório do objeto) e `references`, por tipo de objeto
(campo → prefixos aceitos). O núcleo não sabe o que é Termo, Entidade ou Fonte
— só que um id com um certo prefixo precisa existir em certo diretório, e que
resolver contra um objeto do tipo declarado como `"fonte"` também exige que
esse objeto passe pela própria validação estrutural do schema (contrato
mínimo). O mesmo mecanismo serve qualquer schema que declare esses blocos;
não há `if tipo == "regra"` nem `if campo == "entradas"` no núcleo.

As onze condições verificáveis do EMCIA-CTX-01 3.13 (CTX-V01–CTX-V11) estão
todas formalizadas em `curar.py` — a maioria via `estrutura.py` (schema
genérico), as demais em checagens próprias (autoria, versionamento,
confronto P3d, resolução de referência). Nenhuma delas hard-codeia
vocabulário do EMCIA fora dos dados declarados pelo schema do caso.

## Limite honesto

A hook vive no plugin, e o plugin pode ser desinstalado. Continua sendo pedágio com rastro, não parede. A diferença em relação a configuração local é que o contorno exige desinstalar algo versionado, e isso é visível.

## Camada resolvida por nível

A camada de uma etapa **não é fixa**. Em N1 a preparação automatizada vai até o passo 4; em N3, apenas F0. A mesma etapa pode ser `EX2` em um caso e `EX3` em outro.

Por isso o playbook declara `camada` como mapa por nível, e o carregador recusa camada plana:

```json
"camada": { "N1": "EX2", "N2": "EX2", "N3": "EX3" }
```

O nível entra por `--apurar-nivel`, com autor nomeado e evento `NivelApurado` na trilha. Reapuração registra o valor anterior. **Editar `registro/estado.json` à mão grava o nível sem autor e sem rastro — não faça.**

**Sem nível apurado, aplica-se a camada mais restritiva declarada.** Não se assume o nível mais permissivo enquanto a triagem não apurou — e nenhuma etapa após F0 opera até o nível existir.
