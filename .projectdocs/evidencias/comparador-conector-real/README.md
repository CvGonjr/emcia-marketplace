# Revisão e commit do comparador real — decisão 046

Campo 0.8.29; núcleo 0.2.48 e playbook 0.4.21 preservados. As fixtures fornecidas
7R8Z20 têm identificação/título sintéticos e a estrutura safeHTMLSchema do conector.
Não foram feitas chamadas a contas remotas; esta revisão valida os arquivos locais.

A implementação pendente passou inicialmente em 40 testes. A revisão acrescentou
negativos para marcas malformadas, trecho extra, tipo inválido por caminho, marca
sem mapeamento e ** não pareado: cinco falhas reproduzidas em revisao-antes.txt.
Também verifica NFC/bordas, espaços internos e ausência do campo oculto nesse formato.
Um teste adicional mostrou que INPUT_DESCONHECIDO não tinha diagnóstico blocks[i];
tipo-input-antes.txt registra essa falha. A lista de tipos agora é explícita.
A bateria final tem 48 testes, sem tolerância para aproximação de texto.

## Regressões integrais

| Momento | Python | Verificações | Módulos | Falhas inesperadas |
|---|---|---:|---:|---:|
| Intermediária, antes do último diagnóstico | 3.12.12 | 1108 | 53 | 0 |
| Intermediária, antes do último diagnóstico | 3.14.4 | 1110 | 53 | 0 |
| Final | 3.12.12 | 1109 | 53 | 0 |
| Final | 3.14.4 | 1111 | 53 | 0 |

Os arquivos suite-final incluem a saída integral, HEAD e versões. O checkout
temporário possui o canônico irmão na tag metodo-v1.0, como no CI. Nenhum módulo
é excluído. A suíte bruta conserva a única falha conhecida A25, test_01, com
“ato humano selar-apos-P2 ausente das seções 3.3 e 3.4”; as quatro negativas
passam. O runner exige o diagnóstico/nome/código exatos e rejeita falha nova.
As duas verificações extras em 3.14 são as de PyYAML disponível nesse ambiente.

integridade.json registra hashes da implementação, fixtures e conjunto de figuras.
As figuras foram verificadas e o gerador foi executado numa cópia temporária,
preservando os originais (figuras-conferencia.txt). São material do PFC com versões
históricas, conforme o README próprio, sem substituir a linha de base atual.

Os resultados específicos iniciais estão em especificos-3.12/3.14.txt (47 testes
antes do último diagnóstico); o módulo final com 48 testes integra suite-final.
O método empacotado e os modelos de formulário não foram alterados.
