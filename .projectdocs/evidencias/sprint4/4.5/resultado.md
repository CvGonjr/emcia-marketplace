# Ação 4.5 — manual de aplicação empacotado e conferido

**Base:** `master` na etiqueta `v-sprint3-poc.8` (`f39dad2`). **Fonte controlada:** `emcia-artefatos` commit `1f0c051aab4798ee0df6c86af2dcf46bae22d883` (MAN-01 0.1 e ESP-01 0.4). **Empacotado em:** 2026-10-01.

## Pacote do método

| Documento | Versão anterior → nova | SHA-256 anterior → novo |
|---|---|---|
| MAN-01 | ausente → 0.1 | — → `a8267f5b132a52e1f6731b53bbc4bb08debc8e43b1ed8fd5d755826a7ecc55dd` |
| ESP-01 | 0.3 → 0.4 | `98a19db34f636f1b250bf9aa3f4185c6e9c37df468282c5fa31e57aba82f35a3` → `36f83b92a6ef5deec4582406f7991f7e5b8b297caa0bc89cb6c205740fa7f974` |

As duas cópias coincidem byte a byte com a fonte. O manifesto passou da versão 2 à 3 e enumera 17 documentos; os outros 15 nomes e hashes permanecem iguais. A origem controlada aponta para `1f0c051`. Nenhum playbook de caso foi substituído.

## Teste de coerência manual × playbook

`testes/manual_a25.py` lê a tabela de §3.3 do MAN-01 empacotado e confere: ordem e conjunto das 13 etapas; camadas N1/N2/N3; existência, declaração de etapa e cobertura dos 12 comandos de etapa; atos de `decisoes_humanas` e cobertura por §3.3 ou §3.4, exceto `preparar-controle`; descrição dos produtos, ignorando acentos e maiúsculas; entregável presente no portão da etapa, reduzindo E3-D/E3-E a E3. A célula `—` de comando só é aceita para etapa não delegável. A tabela apresentou **zero divergências**.

Quatro verificações negativas alteram cópias da tabela em memória e confirmam a detecção de etapa removida, camada trocada, ato inexistente e comando inexistente. Resultado isolado: **5 testes aprovados**; a saída está ao fim de `saida-suite.txt`.

## Ajuste estrito de `testes/metodo_empacotado.py`

Com autorização do usuário, foi acrescentada **uma linha** à lista `DOCUMENTOS`; nenhuma outra linha desse teste nem qualquer outro teste existente foi alterado. Sem essa entrada, a comparação exata com o manifesto de 17 documentos falharia.

**Antes — 16 documentos:**

- EMCIA-GLO-01-glossario-do-metodo.md
- EMCIA-MET-01-documento-do-metodo.md
- EMCIA-CAT-01-fronteira-de-delegacao.md
- EMCIA-VER-01-plano-de-verificacao.md
- EMCIA-E2-diagnostico-e-oportunidade.md
- EMCIA-E3-blueprint-da-solucao.md
- EMCIA-CAM-01-protocolo-de-campo-por-passo.md
- EMCIA-TRA-01-procedimentos-transversais-do-metodo.md
- EMCIA-E1-ficha-de-enquadramento.md
- EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md
- EMCIA-ESP-01-especificacao-executavel-do-estudio-de-trabalho.md
- EMCIA-E5-relatorio-de-piloto.md
- EMCIA-TRI-01-instrumento-de-triagem.md
- EMCIA-E4-guia-operacional.md
- EMCIA-FER-01-quadro-de-ferramentas.md
- EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md

**Depois — 17 documentos:**

- EMCIA-GLO-01-glossario-do-metodo.md
- EMCIA-MET-01-documento-do-metodo.md
- EMCIA-CAT-01-fronteira-de-delegacao.md
- EMCIA-VER-01-plano-de-verificacao.md
- EMCIA-E2-diagnostico-e-oportunidade.md
- EMCIA-E3-blueprint-da-solucao.md
- EMCIA-CAM-01-protocolo-de-campo-por-passo.md
- EMCIA-TRA-01-procedimentos-transversais-do-metodo.md
- EMCIA-E1-ficha-de-enquadramento.md
- EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md
- EMCIA-ESP-01-especificacao-executavel-do-estudio-de-trabalho.md
- EMCIA-E5-relatorio-de-piloto.md
- EMCIA-TRI-01-instrumento-de-triagem.md
- EMCIA-E4-guia-operacional.md
- EMCIA-FER-01-quadro-de-ferramentas.md
- EMCIA-MAN-01-manual-de-aplicacao.md
- EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md

## Suíte e versões

Suíte completa: **791 verificações em 36 módulos, zero falhas**. A base anterior tinha 786 verificações em 35 módulos; `manual_a25.py` acrescentou 5. A saída integral e a execução isolada do novo módulo estão em `saida-suite.txt`. O teste `metodo_empacotado.py` confirmou os 17 hashes e a ausência de cópia no repositório do contraste.

Versões dos plugins: `eiac-campo` 0.8.8; `eiac-nucleo` 0.2.34. Não houve alteração de scripts, guarda, selo ou playbook.
