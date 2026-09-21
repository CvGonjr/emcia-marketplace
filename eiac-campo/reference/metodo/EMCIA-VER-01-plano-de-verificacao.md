# Plano de verificação
### Duas execuções, predições registradas, indicadores e protocolo de selamento

| Metadado | Valor | Metadado | Valor |
| :--- | :--- | :--- | :--- |
| **Código** | EMCIA-VER-01 | **Versão** | 0.1 |
| **Data** | 13/09/2026 | **Estado** | Em revisão |
| **Responsável** | Celso do Vale | **Aprovação** | pendente |
| **Fase** | Não se aplica | **Passo** | Não se aplica |

---

## 1. Objetivo e alcance
Fixar, antes da execução, como o resultado do método será julgado: o que se compara, com que indicadores, sob que critérios de sucesso e de falha, e o que invalida a comparação. O plano é redigido na Sprint 1 justamente para que os critérios não possam ser ajustados depois de conhecidos os resultados.

### 1.1 O que a verificação alcança

| Dimensão | Alcance |
| :--- | :--- |
| **Organizações** | Uma. No horizonte deste relatório a aplicação ocorre em prototipação e simulação, conforme declarado no objetivo. O resultado não se generaliza a outras organizações. |
| **Trilha de complexidade** | Uma, definida pela triagem. As demais permanecem sem evidência. |
| **Extensão do percurso** | Completo, do enquadramento à calibragem, com os cinco entregáveis produzidos. |
| **Objeto verificado** | A especificação produzida e o percurso que a produz. |

### 1.2 O que permanece fora
O resultado operacional não é verificável neste desenho, porque depende de construção e implantação da solução especificada, etapas que o serviço não realiza. O que se pode afirmar ao final diz respeito à qualidade da especificação e ao esforço de produzi-la, e não ao desempenho da solução em operação.

## 2. Desenho das duas execuções
O método é executado duas vezes sobre a mesma organização, em condições deliberadamente distintas. A comparação entre as duas isola uma única variável.

| Parâmetro | Execução declarada | Execução de campo |
| :--- | :--- | :--- |
| **Insumo** | Apenas o que a organização informa por escrito ou em entrevista remota | O mesmo insumo, acrescido de observação, leitura de volta e acesso às fontes |
| **Condução** | Automatizada, sem intervenção humana nas etapas de produção | Engenheiro de campo, com apoio dos agentes catalogados |
| **Levantamento de regras não documentadas** | Ausente | Presente, com sessão presencial |
| **Momento** | Sprint 2, antes de qualquer contato de campo | Sprint 3 |
| **Saída** | Especificação declarada, selada e datada | Especificação verificada, com registro de divergência |

> **O que a comparação isola:** A execução declarada não deixa de fazer o levantamento por limitação de esforço ou de competência: ela não dispõe do meio para realizá-lo, porque a regra praticada não está no que a organização consegue declarar. É essa ausência, e não a qualidade da condução, que a comparação mede.

As duas execuções são conduzidas pela mesma pessoa, o que introduz viés de expectativa. O selamento e o registro prévio das predições existem para limitá-lo, e a limitação residual está declarada na seção 8.

## 3. Protocolo de selamento

| Aspecto | Regra |
| :--- | :--- |
| **Quando** | Ao encerrar a ação 2.9, antes de qualquer contato com a organização participante. Nenhuma etapa da Sprint 3 se inicia sem o selo registrado. |
| **O que entra** | Dossiê declarado, os cinco entregáveis da execução declarada, o registro de esforço por passo e a versão dos instrumentos utilizados. |
| **Como se fecha** | Marco datado no repositório versionado, com resumo criptográfico do conteúdo registrado no plano. O resumo é o que permite demonstrar, ao final, que nada foi alterado. |
| **Quem pode abrir** | Ninguém, até a ação 4.2. A abertura antecipada invalida a comparação e é registrada como tal. |
| **Exceção admitida** | Correção de erro material que não altere conteúdo — falha de geração de arquivo, por exemplo. Exige registro do que foi corrigido, com data, e novo resumo. |

O selo não protege contra má-fé, e não é essa sua função. Ele protege contra a reinterpretação retroativa, que é o modo como um resultado ambíguo costuma ser lido a favor da hipótese de quem o produziu.

## 4. Predições registradas
Seis predições sobre o que a comparação encontrará, registradas antes da execução de campo. Cada uma declara o resultado que a confirma e o que a refuta. Predição sem critério de refutação não é predição.

| # | Predição | Confirma se | Refuta se |
| :-: | :--- | :--- | :--- |
| **P1** | A execução declarada não produzirá nenhuma regra não documentada com autoria nominal | Contagem igual a zero na declarada e superior a zero no campo | A declarada produz regra com autoria verificável |
| **P2** | A divergência entre as execuções estará nas definições operacionais, e não nos números declarados | A maioria dos números declarados é confirmada e ao menos uma definição é refutada | A divergência se concentra em números, e as definições coincidem |
| **P3** | A execução declarada recomendará agente para ao menos um caso que a execução de campo reclassifica como não agêntico | Ao menos um caso muda de classificação na Matriz Problema→Tecnologia | As duas execuções classificam todos os casos de modo idêntico |
| **P4** | A camada de contexto da execução declarada conterá regras plausíveis sem autoria identificável | Regras presentes na declarada sem autor, ausentes ou corrigidas no campo | Toda regra da declarada tem autoria e sobrevive à verificação |
| **P5** | A execução declarada encerrará todos os passos sem registrar pendência bloqueante | Nenhuma pendência bloqueante na declarada e ao menos uma no campo | A declarada registra pendência bloqueante por conta própria |
| **P6** | A diferença de esforço entre as execuções se concentrará no passo 3 | O passo 3 responde pela maior parcela da diferença de horas | A diferença se distribui uniformemente entre os passos |

> **Nota:** P4 é a predição de maior consequência prática. Uma camada de contexto plausível e errada é mais perigosa que uma incompleta, porque não se apresenta como incompleta a quem a revisa.
>
> Predição e indicador cumprem papéis distintos: a predição declara antecipadamente o que se espera encontrar; o indicador apura o que se encontrou. P1 e P3 antecipam, respectivamente, o comportamento de CRC e de MCT.

## 5. Indicadores
Os cinco primeiros derivam diretamente do critério mensurável do objetivo declarado na seção 3.1 do relatório, e são os que julgam se o objetivo foi atingido. Os três complementares medem o funcionamento do próprio método e existem porque os critérios de encerramento e o registro de pendências são contribuição desta sprint, sem os quais não haveria como afirmar que um passo foi cumprido.

A apuração é determinística e documentada, de modo que um terceiro com os mesmos registros chegue aos mesmos valores.

### 5.1 Indicadores do objetivo

| Sigla | Indicador e fórmula | Fonte do dado | Sucesso declarado | Limiar de falha |
| :---: | :--- | :--- | :--- | :--- |
| **ENT** | **Cobertura de entregáveis:** Entregáveis concluídos e revisados com o responsável pelo processo, sobre cinco | Registro de aceite de cada entregável | 100% | Qualquer entregável sem revisão registrada |
| **CRC** | **Conhecimento recuperado em campo:** Regras registradas em campo e ausentes da execução declarada, sobre o total registrado em campo | Registro de regras, com autoria e origem | ≥ 25% | < 25% |
| **MCT** | **Mudança de classificação tecnológica:** Casos priorizados cuja classificação difere entre as duas execuções | Matriz Problema→Tecnologia das duas execuções | Toda mudança registrada, com justificativa | Classificações não comparáveis por diferença de casos priorizados |
| **RIV** | **Regra inferida sem validação:** Regras inferidas incorporadas ao blueprint sem validação humana expressa, sobre o total de regras do blueprint | Camada de contexto, com marca de procedência | 0% | Qualquer valor acima de zero |
| **ESF** | **Distribuição de esforço:** Horas do engenheiro de campo entre atividades delegáveis e não delegáveis, em cada execução | Registro de esforço, cruzado com o catálogo de delegação | Sem limiar: sustenta a leitura de custo e de tempo | Registro incompleto em qualquer execução |

> *Nota:* MCT não tem limiar numérico porque o objetivo pede registro, e não quantidade. A direção esperada da mudança está declarada na predição P3; o indicador apura o que de fato ocorreu.

### 5.2 Indicadores complementares

| Sigla | Indicador e fórmula | Fonte do dado | Sucesso declarado | Limiar de falha |
| :---: | :--- | :--- | :--- | :--- |
| **CE** | **Cobertura de encerramento:** Passos encerrados com o critério integralmente satisfeito, sobre dez | Registro de estado do caso | Campo ≥ 0,90 | Campo < 0,70 |
| **TDIV** | **Taxa de divergência:** Itens corrigidos ou refutados sobre o total de itens verificados | Registro de divergência entre declarado e observado | ≥ 15% | 0%, ver observação abaixo |
| **PEND** | **Pendências bloqueantes:** Pendências classificadas como bloqueantes, abertas no encerramento de cada fase | Registro de pendências | Toda bloqueante impede o avanço da fase | Fase encerrada com bloqueante em aberto |

> **Sobre o limiar de falha da TDIV:** Divergência igual a zero não é bom resultado. Significa que a verificação não encontrou nada, o que ou indica que a declaração da organização era integralmente exata, ou que a verificação foi rasa. As duas leituras precisam ser distinguidas na apuração, e a segunda é a mais provável.
>
> CRC e TDIV medem coisas distintas e não devem ser somados. CRC compara o que cada execução produziu; TDIV compara o que a organização declarou com o que a verificação observou, dentro da execução de campo.

## 6. Critérios de falha da verificação
Falha da verificação e refutação da hipótese são coisas distintas. A primeira invalida a comparação e nada permite concluir; a segunda é resultado legítimo e deve ser relatado como tal. Confundi-las converteria qualquer problema de execução em evidência contrária, ou o contrário.

| Condição | Efeito |
| :--- | :--- |
| Informação obtida em campo entra na execução declarada antes do selo | Comparação invalidada. A execução declarada deixa de ser cega. |
| Selo não registrado, sem data ou sem resumo do conteúdo | Comparação invalidada. Não há como demonstrar que a declarada precede o campo. |
| O executor do processo não é liberado para a sessão presencial | Comparação invalidada quanto a H5. O passo 3 não ocorreu, e sua ausência não é evidência sobre seu valor. |
| Acesso negado a fonte crítica impede a verificação do eixo de dados | Comparação parcialmente invalidada. Os itens afetados são excluídos da apuração e listados. |
| O percurso de campo é interrompido antes do passo 5 | Comparação invalidada quanto aos entregáveis não produzidos. O que foi produzido permanece comparável. |
| Registro de esforço incompleto em qualquer execução | ESF não apurável. A leitura de custo e tempo de H4 fica sem base. |
| Regra sem marca de procedência na camada de contexto | RIV não apurável. Sem a marca não há como distinguir regra inferida de regra verificada. |

## 7. Vínculo com as hipóteses

| H | Enunciado, em síntese | Como é verificada | Indicadores |
| :-: | :--- | :--- | :---: |
| **H4** | Combinar automação na coleta com validação humana reduz custo e tempo sem comprometer a confiabilidade | Comparação entre as duas execuções: esforço de um lado, cobertura e divergência do outro | ESF, ENT, CE, TDIV |
| **H5** | Método apoiado apenas no declarado produz especificação incorreta; é preciso etapa de levantamento das regras não documentadas | Condição interna de H4. Verificada pelo que a execução de campo produz e a declarada não alcança | CRC, RIV, e as predições P1 e P4 |
| **H1** | Partir do problema, e não da tecnologia disponível, leva a decisão mais acertada | Validação secundária, restrita à avaliação técnica: casos reclassificados após a verificação | MCT, e a predição P3 |

> *Nota:* H2 e H3 não são verificadas. Cumprem função analítica: delimitam os polos entre os quais a solução se posiciona, e seu descarte é o que legitima a escolha de H4.

## 8. Limitações declaradas

### 8.1 Alcance
Uma organização e uma trilha de complexidade. As demais trilhas permanecem sem evidência empírica, e o resultado não autoriza afirmação sobre elas.

### 8.2 Independência entre as execuções
As duas execuções são conduzidas pela mesma pessoa, que conhece as predições registradas. O selamento impede a alteração retroativa da execução declarada, mas não elimina o viés de expectativa na condução da execução de campo. Um desenho com dois engenheiros independentes seria superior e não é viável no prazo do projeto.

### 8.3 Alcance temporal
Os passos 8 a 10 produzem a especificação do piloto, da medição e da calibragem, e não sua execução em operação. A verificação alcança o que o método especifica, e não o que a solução especificada produziria se construída.

### 8.4 O resultado que enfraquece a hipótese
**Declarado antecipadamente:** Se a execução declarada produzir especificação equivalente à de campo — mesmas regras, mesma classificação tecnológica, mesmas pendências —, H5 sai enfraquecida, e o registro dirá isso. O desenho de verificação foi construído para que esse resultado seja possível; um desenho em que a hipótese não pudesse falhar não verificaria coisa alguma.

### 8.5 Dependência de terceiros
Modelo, orquestração e repositório são serviços de mercado sujeitos a mudança de preço, disponibilidade e termos de uso. Alteração relevante durante a execução é registrada com data, porque afeta a comparabilidade do esforço entre as duas execuções.

## 9. Condição de aceite
Este artefato está pronto quando:
1. As duas execuções estão descritas com a variável isolada explicitada;
2. O protocolo de selamento define momento, conteúdo, fechamento e exceção;
3. Cada predição declara o que a confirma e o que a refuta;
4. Cada métrica do critério mensurável do objetivo tem indicador correspondente, com fórmula, fonte, valor de sucesso e limiar de falha;
5. Os critérios que invalidam a comparação estão separados dos que refutam a hipótese.

## 10. Referências
* **The Tacit Dimension**, Polanyi (1966)
* **The Knowledge-Creating Company**, Nonaka e Takeuchi (1995)
* **AI Risk Management Framework**, NIST (2023)
* **Artefatos relacionados:** EMCIA-MET-01, EMCIA-CAT-01, EMCIA-TRI-01, modelos E1 a E5.

## 11. Histórico de revisões

| Versão | Data | Autor | Descrição da alteração | Aprovação |
| :---: | :---: | :--- | :--- | :---: |
| **0.1** | 13/09/2026 | Celso do Vale | Versão inicial: desenho das duas execuções, protocolo de selamento, seis predições, cinco indicadores do objetivo e três complementares, critérios de falha e limitações | — |