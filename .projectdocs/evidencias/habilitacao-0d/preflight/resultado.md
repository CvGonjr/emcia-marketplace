# Passagem habilitação → caso — levantamento inicial

**Data:** 02/10/2026. **Base:** `3b38101ce1d294cb33cea261178b211cfea40964`.
**Fonte canônica consultada:** emcia-artefatos `ab09abe`.
**Estado:** interrompido antes dos pacotes A–D por divergência documentada em 039.

## Linha de base

- `bash testes/negativos.sh`: todas as travas aprovadas.
- `python3 testes/contexto.py`: 11 verificações aprovadas.
- `python3 testes/habilitacao.py`: 19 testes aprovados.

Saídas integrais nos arquivos `*-inicial.txt`. Não houve modificação de código,
fixtures, templates ou versões. A pasta preexistente `.projectdocs/figuras/`
foi preservada.

## Divergência reproduzida

`python3 .projectdocs/evidencias/habilitacao-0d/preflight/reproduzir-selo.py`
cria um repositório sintético temporário e configura um hook que recusa o
commit. A reprodução chama os componentes reais de selo, estado e playbook:

- commit recusado;
- `SeloAplicado` presente na trilha;
- nenhum selo confirmado pelo Git;
- regra atual de passagem aceita o evento.

Saída em `reproducao-selo.txt`. Reutilizar esse comportamento na nova regra
não assegura o estado inicial selado exigido em HAB-01 §3.3.4. A decisão 035
limita sua correção à exibição do selo, mantendo G7 inalterada.

Proposta para decisão: a nova exigência de evento selado deve conferir o
histórico Git, com selo confirmado posterior que inclua o evento exigido.
Não foi implementada por inferência. A regra antiga requer decisão própria
se também for modificada.

## Escopo da entrega neste levantamento

Foram preservadas a linha de base, a reprodução e a busca de vocabulário
preexistente no núcleo. A decisão 039 registra a pendência e o conflito de
código documental HAB-02. Não há implementação funcional, teste de aceite
novo, incremento de versão ou commit de pacote. README, instalação e
interfaces não anunciam funcionalidades ainda inexistentes.

As saídas finais das três suítes constam em `*-final.txt`; verificam apenas
que o levantamento documental não alterou o comportamento existente.
