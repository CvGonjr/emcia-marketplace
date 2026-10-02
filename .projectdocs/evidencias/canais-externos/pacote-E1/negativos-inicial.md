# Verificação antes dos scripts

Os testes de canais, recebimento e entrega foram escritos antes dos scripts.
A primeira execução de canais encontrou ausência também do contrato de canais
na fixture. Declarado o contrato, a execução inicial de 15 testes terminou com
14 falhas: canais.py ainda não existia, e as operações não produziam evento.
A recusa de definição pela sessão já passou pela declaração humana na guarda.
Isso não é resultado final: a implementação fechou as recusas com evento.
As saídas anteriores à implementação de receber.py e entregar.py ficam nos
respectivos `negativos-inicial.txt`. Falhas finais não foram dispensadas.
