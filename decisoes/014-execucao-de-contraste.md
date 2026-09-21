# 014 — A execução de contraste roda fora do caso de campo, antes do F0 de campo

**Data:** 21/09/2026 · **Estado:** firme · **Substitui:** [[004-janela-da-antitese]]

## Contexto

A decisão 004 fixou que a "antítese" rodaria como uma fase intermediária dentro do percurso de campo — entre o fechamento de P2 e a liberação de P3a, no mesmo repositório de caso. Duas mudanças tornaram essa janela insustentável:

1. **O nome mudou.** "Antítese" não é mais usado — o termo é `contraste`. "Antítese" não aparece em código, arquivo ou mensagem de nenhum dos dois plugins.
2. **A arquitetura mudou.** O contraste deixou de ser uma fase dentro do caso de campo e passou a ser uma **execução completa e independente do mesmo método** (`eiac-campo` + `eiac-contraste`, em vez de `eiac-campo` + `eiac-nucleo`), comparável à execução de campo, não um braço de controle interno a ela. Rodar o contraste "entre P2 e P3a" deixou de fazer sentido: o contraste percorre F0–P10 inteiro, com seu próprio plugin substituindo o núcleo, não um trecho do percurso de campo.

Manter a janela P2→P3a como está descrita em 004 misturaria as duas execuções no mesmo repositório e no mesmo caso — exatamente o que a separação de repositórios (`emcia-marketplace` vs. `emcia-contraste`) existe para evitar.

## Decisão

A execução de contraste roda:

- **Em repositório e plugin próprios** (`emcia-contraste`, plugin `eiac-contraste`), nunca dentro do repositório de um caso de campo.
- **Consumindo o mesmo `eiac-campo`** (habilidades, playbook, esquemas) do marketplace, sem cópia e sem alteração de texto — a única peça que muda é o componente que decide o que é aceito (`eiac-contraste` no lugar de `eiac-nucleo`).
- **Antes do F0 de um caso de campo**, não entre etapas dele. O contraste é um percurso F0→P10 completo e autônomo sobre o que a organização declara por escrito, sem contato humano de confirmação — não uma fase intermediária do caso de campo.
- **O caso de campo nunca carrega dado da execução de contraste.** Não há importação, referência ou merge entre os dois. A comparação entre as duas execuções (Quadro de Contraste) é externa a ambas — lê os dois braços, não escreve em nenhum, como já valia em 004.

Isolamento em código: o núcleo (`eiac-nucleo`) recusa operar se `eiac-contraste` estiver habilitado no mesmo caso, ou se houver qualquer registro com `execucao: contraste` no repositório do caso — trava adicionada nesta mesma frente de trabalho (ver Fase 5, teste de isolamento).

## Consequência

- Não existe mais "janela" no percurso de campo reservada ao contraste — P2, P3a e todas as demais etapas de campo seguem seu curso normal, sem depender de uma execução de contraste ter ocorrido antes.
- O contraste não tem "segunda tentativa" pelo mesmo motivo de 004 (a segunda já saberia o que a primeira produziu), mas essa é agora uma propriedade do processo de pesquisa, não uma trava dentro do percurso de um caso.
- A decisão 004 fica marcada como **substituída**. Seu conteúdo histórico permanece no arquivo para registro, mas não rege mais o comportamento do sistema.
