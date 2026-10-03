# Testes — inventário operacional

Revisão: 03/10/2026. Linha de base em Python 3.12.12: **919 verificações,
46 módulos**, sem exclusões e sem falhas. O pacote de documentação acrescenta
7 testes de citações: **1845 verificações em 48 módulos**.
As saídas integrais inicial e final e o executador estão em
`.projectdocs/evidencias/documentacao-operacional/`.

## Executar

Antes de alterar o repositório:

```bash
bash testes/negativos.sh
python3 testes/contexto.py
```

Para a suíte completa, com Python 3.12 e o binário python3 correspondente no PATH:

```bash
python3 .projectdocs/evidencias/documentacao-operacional/reexecutar-suite.py /tmp/emcia-suite.txt
```

O executador descobre negativos.sh e todos os módulos Python na raiz de testes/,
registra saídas, códigos e contagens e falha se algum módulo falhar. Os auxiliares
em testes/apoio/ não são módulos independentes. Há negativas e controles positivos;
recusa indevida também é falha. Nenhum teste usa dado real de cliente.

## Módulos e contagens

| Módulo | Verificações | Cobertura |
|---|---:|---|
| `TOTAL` | 919 | Verificações do pacote |
| `autoria_responsavel.py` | 14 | Autoria de registro atribuida pelo componente, nao informada pelo agente |
| `caminhos_a19.py` | 62 | A19: caminhos reais e aliases não escapam das zonas protegidas |
| `campo_2_6_2.py` | 38 | Verificacao operacional de P6 e P7 -- pacote 2.6.2 |
| `campo_2_6_3.py` | 57 | Verificacao operacional de P8, P9 e P10 -- pacote 2.6.3 |
| `campo_2_6_4.py` | 50 | Verificacao do catalogo de HB/AG -- pacote 2.6.4 |
| `campo_2_6_5.py` | 62 | Verificacao semantica dos inegociaveis, portoes operacionais e |
| `campo_2_6_6.py` | 43 | Verificacao integral do percurso F0-P10 -- pacote 2.6.6 |
| `campos_a10.py` | 18 | A10: campos declarados, autoria nominal e E3 por comandos reais |
| `canais.py` | 19 | Canais: negativas com evento antes dos controles positivos |
| `canais_percurso.py` | 1 | Percurso integrado de canais com ids sintéticos |
| `citacoes.py` | 7 | Seções, caminhos canônicos, auxiliares, TRI-01 e retirada dos resumos CTX |
| `consolidado.py` | 16 | Verificacao consolidada da Acao 2.5 — pacote 2.5.6 |
| `contexto.py` | 11 | Testes estruturais do pacote 2.5.1 com evidência bruta opcional |
| `ctx_v.py` | 23 | Bateria formal CTX-V01-CTX-V11 do pacote 2.5.4 |
| `curadoria.py` | 17 | Testes de curadoria, autoria e versionamento I->V do pacote 2.5.2 |
| `decisao_a12.py` | 37 | A12: origem na guarda identifica agente, independentemente do nome |
| `e5_rotina_a24.py` | 5 | A24: E5 e recorrência consultam a mesma rotina vigente do caso |
| `emissao_a9.py` | 13 | A9: emissão exige o artefato declarado pelo playbook do caso |
| `entregar.py` | 10 | Entrega: negativas antes do controle de emissão e registro humano |
| `escopo_mcp.py` | 11 | Escopo de ferramentas MCP e listagem registrada |
| `esforco.py` | 1 | Registro de esforço e cálculo |
| `formularios.py` | 5 | Redação fixa da triagem e isolamento na preparação de submissões |
| `habilidades_a18.py` | 13 | A18: rotas reais de carregamento, inclusive com sessão e selo |
| `habilitacao.py` | 19 | Travas do expediente de habilitação; dados exclusivamente sintéticos |
| `habilitacao_0d.py` | 35 | Passagem 0d: negativas primeiro, sobre componentes reais e dados sintéticos |
| `integracao.py` | 17 | Integracao P2/P3 -> CTX -> P4/P5 do pacote 2.5.5 |
| `manual_a25.py` | 5 | MAN-01 sem emenda: conformidade e quatro mutações negativas |
| `metodo_empacotado.py` | 1 | Inventário, SHA-256 e comparação ao commit canônico quando disponível |
| `negativos.sh` | 51 | Regressão das guardas, procedência e controles positivos |
| `nucleo_2_6_1.py` | 39 | Verificacao do nucleo generico de protocolos -- pacote 2.6.1 |
| `nucleo_yaml.py` | 6 | Leitor mínimo, listas e validação de objetos |
| `p3d.py` | 12 | Testes de integracao CTX <-> P3d do pacote 2.5.3 |
| `pessoa_a16.py` | 17 | Verificações do pacote pessoa_a16 |
| `playbook_2_6_0.py` | 29 | Verificacao do contrato executavel F0-P10 -- pacote 2.6.0 |
| `produtos_a14.py` | 21 | Verificações do pacote produtos_a14 |
| `receber.py` | 17 | Recebimento humano: negativas conferem a trilha e preservam fontes |
| `recorrencia_a23.py` | 12 | A23: responsável da recorrência conferido contra a fonte vigente do caso |
| `recusa_a21.py` | 2 | A21: recusa é evento; não vira asserção com procedência inventada |
| `redirecionamentos_a20.py` | 12 | A20: alvos de redirecionamento e descritores, não o caractere > |
| `restricoes.py` | 20 | RH → F, dispensa, revisões, cobertura de P2 e marcas localizadas |
| `revisao_a15.py` | 6 | Verificações do pacote revisao_a15 |
| `selo_a17.py` | 7 | A17: estado exibe o último selo confirmado pelo histórico do caso |
| `selo_p3b.py` | 5 | Selo Git confirmado depois do encerramento |
| `sessao_a8.py` | 23 | A8: sessão da etapa corrente conforme camada declarada no caso |
| `sessao_externa.py` | 6 | Referência de sessão genérica: camada, id declarado e marcador |
| `triagem_a7.py` | 24 | A7: recusas primeiro; regra de apuração declarada no playbook do caso |
| `verificacao_por_estados.py` | 7 | Verificacao por estados do caso (decisao 021, substitui 004/014-020) |
| **Total** | **1845** | **48 módulos** |

metodo_empacotado.py e esforco.py são verificações por processo e contam como
uma cada; os demais módulos declaram unittest ou imprimem verificações `ok`.
Estas contagens identificam a execução deste pacote, sem somar reexecuções.

## Contratos documentais

`metodo_empacotado.py` exige o inventário exato de 21 documentos, manifesto v4
com caminhos de origem e commit completo, hashes corretos e ausência de cópias
no contraste. Com emcia-artefatos como checkout irmão, confere bytes contra
`git show <commit>:<caminho>`; nunca compara a uma versão mutável de trabalho.
Sem esse checkout, os hashes fixados permitem conferir o pacote offline.

`manual_a25.py` exige `conferir()` vazio diretamente para o MAN-01 v0.2 e playbook
0.4.18. Não há sobreposição de emenda nem expectativa de lacunas da v0.1.
Os negativos 02–05 continuam detectando etapa removida, camada trocada,
ato humano inexistente e comando inexistente.

`citacoes.py` lê habilidades, comandos e referências fora de reference/metodo/.
Confere código/caminho e seção no pacote, incluindo os auxiliares cuja origem
é fixada em caminhos_canonicos. JSON de formulário também tem seus campos
secao_* conferidos. Inclui negativos de arquivo/seção inexistentes, o TRI-01
real (§3.3 perguntas; §3.4 pontuação), continuações de citação e a retirada das
cópias anteriores de CTX. Existência de seção não comprova correção semântica
de toda frase; o caso TRI recebe uma conferência específica.

## Fronteiras operacionais

restricoes.py e selo_p3b.py cobrem as decisões 041 e 042. habilitacao_0d.py
cobre importação, selo de F0 e cópia íntegra do método. canais.py, formularios.py,
receber.py, entregar.py, sessao_externa.py, escopo_mcp.py e canais_percurso.py
cobrem contratos locais e atos humanos da fronteira externa. Essas suítes não
autenticam conteúdo remoto nem demonstram hooks em um cliente diferente.

A prova real de runtime está em `.projectdocs/evidencias/canais-externos/pacote-E7/`:
Claude Code 2.1.283, ferramenta MCP stdio sintética, disparo real de hook e
negativa antes da chamada. Simulação de payload não substitui essa prova.
