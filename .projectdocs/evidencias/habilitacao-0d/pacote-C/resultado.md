# Pacote C — abertura com método conferido

Campo 0.8.11; núcleo 0.2.36; playbook 0.4.12. Abertura delegada ao script
abrir_caso.py do campo. Hashes e, quando indicado, expediente, são conferidos
antes de criar o caso. Método copiado de snapshot em memória, manifesto
preservado e hashes da cópia novamente conferidos. Pacote controlado intacto.

Negativas antes da implementação: manifesto adulterado, identidade reservada
divergente e acessos ausentes. Verificam negativa estruturada, diário na base
existente e ausência do destino. Positivos: expediente sintético → novo-caso →
importação → gravação validada → selo → carga de F0; cada hash é conferido.
Outro controle adultera a cópia e comprova diagnóstico somente leitura, sem
alterar estado/trilha nem bloquear apuração. Saídas nos arquivos de regressão.

Antes de existir caso, TentativaNegada é emitido no stderr; base existente
fora de repositório também recebe diário. Base/caso não são criados apenas
para diagnóstico. Sem identidade humana legítima não se inventa autoria.

A origem fica fixada pelo manifesto do pacote; não há download de HEAD remoto.
A conferência do caso compara com o manifesto copiado, não autentica o
manifesto. Material público de 0a permanece fora do caso. selar.py inalterado.
