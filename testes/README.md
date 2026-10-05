# Testes — inventário operacional

Revisão: 04/10/2026. Linha de base antes das alterações em Python 3.12.12:
**958 verificações em 49 módulos**, sem exclusões e sem falhas. A geração
com templates aprovados acrescenta dez testes; o pacote passa de uma
verificação por processo a oito testes. Suíte final: **975 verificações em
49 módulos**. Saídas integrais, executador e exemplos sintéticos estão em
`.projectdocs/evidencias/linha-de-base-v1/`.

## Executar

Antes de alterar o repositório:

```bash
bash testes/negativos.sh
python3 testes/contexto.py
```

Para a suíte completa, com Python 3.12 e o binário python3 correspondente no PATH:

```bash
python3 .projectdocs/evidencias/linha-de-base-v1/reexecutar-suite.py /tmp/emcia-suite.txt
```

O executador descobre negativos.sh e todos os módulos Python na raiz de testes/,
registra saídas, códigos e contagens e falha se algum módulo falhar. Os auxiliares
em testes/apoio/ não são módulos independentes. Há negativas e controles positivos;
recusa indevida também é falha. Nenhum teste usa dado real de cliente.

## Módulos e contagens

| Módulo | Verificações | Cobertura |
|---|---:|---|
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
| `catalogo_cat01.py` | 11 | Reprodução literal do CAT-01, correspondência de etapas, AG e camadas; negativas de cada regra |
| `citacoes.py` | 8 | Seções, caminhos canônicos, auxiliares, TRI-01, retirada dos resumos CTX e instrumentos distintos de P1/P3d |
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
| `habilitacao.py` | 29 | Travas do expediente, hashes aprovados, revisão jurídica exata, separação do modelo e emissão; dados sintéticos |
| `habilitacao_0d.py` | 35 | Passagem 0d: negativas primeiro, sobre componentes reais e dados sintéticos |
| `integracao.py` | 17 | Integracao P2/P3 -> CTX -> P4/P5 do pacote 2.5.5 |
| `manual_a25.py` | 5 | MAN-01 sem emenda: conformidade e quatro mutações negativas |
| `metodo_empacotado.py` | 8 | Inventário aprovado, APR-01, tag → commit, bytes canônicos e templates do checkout; negativas de cada contrato |
| `negativos.sh` | 51 | Regressão das guardas, procedência e controles positivos |
| `nucleo_2_6_1.py` | 39 | Verificacao do nucleo generico de protocolos -- pacote 2.6.1 |
| `nucleo_yaml.py` | 6 | Leitor mínimo, listas e validação de objetos |
| `p3d.py` | 12 | Testes de integracao CTX <-> P3d do pacote 2.5.3 |
| `pessoa_a16.py` | 17 | Verificações do pacote pessoa_a16 |
| `playbook_2_6_0.py` | 29 | Verificacao do contrato executavel F0-P10 -- pacote 2.6.0 |
| `produtos_a14.py` | 21 | Verificações do pacote produtos_a14 |
| `prosseguimento.py` | 20 | Ato humano, registro íntegro, histórico, dois desfechos, bloqueio, E1 e compatibilidade de casos anteriores |
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
| **Total** | **975** | **49 módulos** |

esforco.py é uma verificação por processo e conta como uma; os demais módulos
declaram unittest ou imprimem verificações `ok`.
Estas contagens identificam a execução deste pacote, sem somar reexecuções.

## Contratos documentais

`metodo_empacotado.py` exige 22 documentos, manifesto v6, tag, commit completo,
linha_de_base e caminhos canônicos. Os 21 arquivos além do APR-01 precisam estar
aprovados pelo hash do registro. Com o checkout irmão canônico, resolve a tag
para o commit, compara bytes via git show e confere os três templates HAB no
checkout pelos hashes do APR-01; o CI obtém esse checkout da tag publicada.
Sem checkout, o controle offline confere manifesto e registro de aprovação.
As negativas alteram hash no APR-01 com manifesto coerente, destino da tag,
bytes do template, hash do manifesto e origem/linha de base. Fixtures HAB e APR-01
em testes/apoio/templates-hab-v1 são cópias exatas da tag, conferidas pelo pacote.
ESP-01, VER-01 e fluxo auxiliar ficam fora do inventário aprovado.

`manual_a25.py` exige `conferir()` vazio diretamente para o MAN-01 v1.0 e playbook
0.4.19. O produto de F0 é "Decisão de prosseguimento registrada", conforme
correção aprovada antes do commit canônico. Não há sobreposição de emenda.
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

## Geração da habilitação aprovada

Os templates de teste são os três originais da tag, copiados para diretórios
temporários sem modificar os fixtures. A revisão jurídica é exclusivamente
sintética, registrada pelas operações reais com pessoa nomeada, data, hashes e
evidência importada. Há negativas sem revisão, cobertura parcial, hash diferente,
evidência adulterada e marcas ausentes. O controle positivo compara todo o
conteúdo contratual e a identificação, verifica remoção do controle e histórico
internos e do aviso jurídico e confere o estado “Para assinatura”. Somente o
renderizador de PDF é substituído nas fixtures de integração; nenhuma trava
é dispensada. A demonstração separada gera PDFs reais com Chrome e usa pdftotext.
