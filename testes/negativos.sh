#!/usr/bin/env bash
# Suíte acumulada de travas e controles positivos.
# Falha aqui significa que uma trava deixou de existir.
set -u

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
S="$RAIZ/eiac-nucleo/scripts"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cp -r "$RAIZ/eiac-campo/template-caso" "$TMP/caso"
cd "$TMP/caso"
mkdir -p rascunho

falhas=0
ok()   { printf '  ok    %s\n' "$1"; }
falha(){ printf '  FALHA %s\n' "$1"; falhas=$((falhas+1)); }

echo "== testes negativos"

# 1 habilidade nao delegavel
echo '{"tool_name":"Read","tool_input":{"file_path":"skills/hb-levantar-regras/SKILL.md"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "1 habilidade EX4 negada" || falha "1 habilidade EX4 NAO foi negada"

# 2 escrita direta em caso/
echo '{"tool_name":"Write","tool_input":{"file_path":"caso/x.md"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "2 escrita direta negada" || falha "2 escrita direta NAO foi negada"

# 2b bash redirecionando
echo '{"tool_name":"Bash","tool_input":{"command":"echo oi > caso/x.md"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "2b bash para caso/ negado" || falha "2b bash para caso/ NAO foi negado"

# 3 assercao sem procedencia
printf -- '- [Celso · 2026-09-11] regra qualquer\n' > rascunho/t.md
python3 "$S/validar.py" --arquivo caso/t.md --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "3 assercao sem procedencia recusada" || falha "3 assercao sem procedencia ACEITA"

# 4 assercao valida grava (teste positivo de controle)
printf -- '- [I · premissa: teste · Celso] regra de teste\n' > rascunho/t.md
python3 "$S/validar.py" --arquivo caso/t.md --autor "Celso" >/dev/null 2>&1
[ $? -eq 0 ] && ok "4 assercao valida gravada" || falha "4 assercao valida RECUSADA"

# Pacote 2.5.0 — contrato canonico D/I/V

# T01 D valido nao exige evidencia de verificacao
printf -- '- [D · Helena · 2026-09-18] informacao declarada\n' > rascunho/procedencia.md
python3 "$S/validar.py" --arquivo caso/procedencia.md --autor "Helena" >/dev/null 2>&1
[ $? -eq 0 ] && ok "2.5.0-T01 D valido aceito" || falha "2.5.0-T01 D valido RECUSADO"

# T02 I sem premissa e recusado
printf -- '- [I · Celso] inferencia sem premissa\n' > rascunho/procedencia.md
python3 "$S/validar.py" --arquivo caso/procedencia.md --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "2.5.0-T02 I sem premissa recusado" || falha "2.5.0-T02 I sem premissa ACEITO"

# T03 I com premissa e aceito
printf -- '- [I · premissa: padrao observado nos documentos · Celso] inferencia rastreavel\n' > rascunho/procedencia.md
python3 "$S/validar.py" --arquivo caso/procedencia.md --autor "Celso" >/dev/null 2>&1
[ $? -eq 0 ] && ok "2.5.0-T03 I com premissa aceito" || falha "2.5.0-T03 I com premissa RECUSADO"

# T04 V sem evidencia e recusado
printf -- '- [V · Celso] verificacao sem evidencia\n' > rascunho/procedencia.md
python3 "$S/validar.py" --arquivo caso/procedencia.md --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "2.5.0-T04 V sem evidencia recusado" || falha "2.5.0-T04 V sem evidencia ACEITO"

# T05 V com evidencia e aceito
printf -- '- [V · observacao: sessao-2026-09-18 · Celso] verificacao rastreavel\n' > rascunho/procedencia.md
python3 "$S/validar.py" --arquivo caso/procedencia.md --autor "Celso" >/dev/null 2>&1
[ $? -eq 0 ] && ok "2.5.0-T05 V com evidencia aceito" || falha "2.5.0-T05 V com evidencia RECUSADO"

# T06 valores fora de D/I/V nao sao procedencia
invalidas_recusadas=1
for valor in X campo externo; do
  printf -- '- [%s · Celso] procedencia invalida\n' "$valor" > rascunho/procedencia.md
  if python3 "$S/validar.py" --arquivo caso/procedencia.md --autor "Celso" >/dev/null 2>&1; then
    invalidas_recusadas=0
  fi
done
[ "$invalidas_recusadas" -eq 1 ] \
  && ok "2.5.0-T06 X/campo/externo recusados como procedencia" \
  || falha "2.5.0-T06 procedencia fora de D/I/V ACEITA"

# T07 apuracao coexiste em campo distinto da procedencia
printf -- '- [V · observacao: amostra-controlada · apuracao: medido · amostra: 10 casos · periodo: set/2026 · Celso] numero verificado\n' > rascunho/procedencia.md
python3 "$S/validar.py" --arquivo caso/procedencia.md --autor "Celso" >/dev/null 2>&1
[ $? -eq 0 ] && ok "2.5.0-T07 V coexiste com apuracao separada" || falha "2.5.0-T07 dimensao separada RECUSADA"

# 5 encerrar etapa presencial sem sessao
python3 "$S/avancar.py" --encerrar P3b --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "5 encerramento sem sessao recusado" || falha "5 encerramento sem sessao ACEITO"

# 6 autor agente
python3 "$S/avancar.py" --encerrar F0 --autor "AG05" >/dev/null 2>&1
[ $? -ne 0 ] && ok "6 autor agente recusado" || falha "6 autor agente ACEITO"

# 7 emitir com portao fechado
python3 "$S/avancar.py" --emitir E2 --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "7 emissao com portao fechado recusada" || falha "7 emissao ACEITA indevidamente"


# 9 camada desloca com o nivel (CAT-01 3.6)
python3 -c "
import json, pathlib
p = pathlib.Path('registro/estado.json'); d = json.loads(p.read_text())
d['nivel'] = 'N3'; d['etapa_atual'] = 'P1'; p.write_text(json.dumps(d))"
echo '{"tool_name":"Read","tool_input":{"file_path":"skills/hb-mapear-contexto/SKILL.md"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "9 P1 em N3 negada (EX3)" || falha "9 P1 em N3 NAO foi negada"

# 10 a mesma etapa em N1 passa
python3 -c "
import json, pathlib
p = pathlib.Path('registro/estado.json'); d = json.loads(p.read_text())
d['nivel'] = 'N1'; p.write_text(json.dumps(d))"
echo '{"tool_name":"Read","tool_input":{"file_path":"skills/hb-mapear-contexto/SKILL.md"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 0 ] && ok "10 P1 em N1 permitida (EX2)" || falha "10 P1 em N1 NEGADA indevidamente"

# 11 sem nivel apurado, etapa apos F0 e negada
python3 -c "
import json, pathlib
p = pathlib.Path('registro/estado.json'); d = json.loads(p.read_text())
d['nivel'] = None; p.write_text(json.dumps(d))"
echo '{"tool_name":"Read","tool_input":{"file_path":"metodo/x.md"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "11 etapa sem nivel apurado negada" || falha "11 etapa sem nivel ACEITA"

# 12 F0 nao encerra sem nivel
python3 -c "
import json, pathlib
p = pathlib.Path('registro/estado.json'); d = json.loads(p.read_text())
d['etapa_atual'] = 'F0'; d['nivel'] = None; p.write_text(json.dumps(d))"
python3 "$S/avancar.py" --encerrar F0 --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "12 F0 sem nivel nao encerra" || falha "12 F0 encerrou sem nivel"

# 13 playbook com camada plana e recusado
cp registro/playbook.json /tmp/pb-bom.json
python3 -c "
import json, pathlib
p = pathlib.Path('registro/playbook.json'); d = json.loads(p.read_text())
d['etapas'][1]['camada'] = 'EX2'; p.write_text(json.dumps(d))"
python3 "$S/playbook.py" >/dev/null 2>&1
[ $? -ne 0 ] && ok "13 camada plana recusada" || falha "13 camada plana ACEITA"
cp /tmp/pb-bom.json registro/playbook.json

# 14 nivel fora do playbook e recusado
python3 -c "
import json, pathlib
p = pathlib.Path('registro/estado.json'); d = json.loads(p.read_text())
d['etapa_atual'] = 'F0'; d['nivel'] = None; p.write_text(json.dumps(d))"
python3 "$S/avancar.py" --apurar-nivel N9 --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "14 nivel fora do playbook recusado" || falha "14 nivel invalido ACEITO"

# 15 apuracao de nivel por agente e recusada
python3 "$S/avancar.py" --apurar-nivel N2 --autor "AG05" >/dev/null 2>&1
[ $? -ne 0 ] && ok "15 nivel apurado por agente recusado" || falha "15 nivel por agente ACEITO"

# 16 apuracao valida grava e deixa rastro (controle positivo)
python3 "$S/avancar.py" --apurar-nivel N2 --autor "Celso" --eixos "DAD 4, GOV 5, CRI 7" >/dev/null 2>&1
gravou=$?
grep -q '"evento": "NivelApurado"' registro/eventos.jsonl 2>/dev/null
rastro=$?
[ $gravou -eq 0 ] && [ $rastro -eq 0 ] \
  && ok "16 nivel apurado grava com evento" || falha "16 nivel apurado SEM gravar ou SEM evento"

# 17 com o nivel apurado pelo comando, F0 encerra
python3 "$S/avancar.py" --encerrar F0 --autor "Celso" >/dev/null 2>&1
[ $? -eq 0 ] && ok "17 F0 encerra apos nivel apurado" || falha "17 F0 NAO encerrou com nivel apurado"

# 18 selo por agente e recusado, e pelo motivo certo
# (so o exit code nao serve: aqui varias travas recusam, e o teste passaria
#  mesmo com a recusa de autor-agente removida)
saida="$(python3 "$S/selar.py" --autor "AG05" --nota "teste" 2>&1)"
[ $? -ne 0 ] && echo "$saida" | grep -q "pessoa nomeada" \
  && ok "18 selo por agente recusado" || falha "18 selo por agente ACEITO ou recusado por outro motivo"

# 19 selo fora de repositorio git e recusado, e pelo motivo certo
saida="$(python3 "$S/selar.py" --autor "Celso" --nota "teste" 2>&1)"
[ $? -ne 0 ] && echo "$saida" | grep -q "repositorio git" \
  && ok "19 selo sem repositorio recusado" || falha "19 selo sem repositorio ACEITO ou recusado por outro motivo"

# 20 selo valido commita com o autor nomeado e deixa rastro (controle positivo)
git init -q . 2>/dev/null
git config user.name "Identidade Da Maquina"
git config user.email "maquina@exemplo.com"
python3 "$S/selar.py" --autor "Celso do Vale" --nota "teste de selo" >/dev/null 2>&1
selou=$?
grep -q '"evento": "SeloAplicado"' registro/eventos.jsonl 2>/dev/null
rastro=$?
[ "$(git log -1 --format=%an 2>/dev/null)" = "Celso do Vale" ]
assinatura=$?
[ $selou -eq 0 ] && [ $rastro -eq 0 ] && [ $assinatura -eq 0 ] \
  && ok "20 selo commita com autor nomeado e evento" \
  || falha "20 selo NAO commitou, NAO deixou evento ou assinou com a maquina"

# 21 selar duas vezes seguidas recusa: nada a selar, e pelo motivo certo
saida="$(python3 "$S/selar.py" --autor "Celso do Vale" --nota "de novo" 2>&1)"
[ $? -ne 0 ] && echo "$saida" | grep -q "nada a selar" \
  && ok "21 selo sem mudanca recusado" || falha "21 selo vazio ACEITO ou recusado por outro motivo"

# 22 a fronteira anunciada acompanha o nivel
# P3a e EX2 em N1 (delegavel) e EX3 em N2 (humana). Se o aviso nao mudar com
# o nivel, ele esta decorado em vez de resolvido pelo playbook.
python3 -c "
import json, pathlib
p = pathlib.Path('registro/estado.json'); d = json.loads(p.read_text())
d['etapa_atual'] = 'P2'; d['nivel'] = 'N2'; p.write_text(json.dumps(d))"
n2="$(python3 "$S/fronteira.py" 2>&1)"
python3 -c "
import json, pathlib
p = pathlib.Path('registro/estado.json'); d = json.loads(p.read_text())
d['nivel'] = 'N1'; p.write_text(json.dumps(d))"
n1="$(python3 "$S/fronteira.py" 2>&1)"
echo "$n2" | grep -q "A partir de P3a" && echo "$n1" | grep -qv "A partir de P3a" \
  && ok "22 fronteira acompanha o nivel" \
  || falha "22 fronteira NAO muda com o nivel"

# 23 etapa nao delegavel aparece como tal, em qualquer nivel
echo "$n2" | grep -q "P3b .*nao delegavel" && echo "$n1" | grep -q "P3b .*nao delegavel" \
  && ok "23 P3b marcada nao delegavel nos dois niveis" \
  || falha "23 P3b NAO marcada como nao delegavel"

# 24 documento citado que nao esta em fontes/ e recusado
mkdir -p fontes
printf -- '- [V · documento: ausente.xlsx p.2 · 2026-09-15 · Celso] regra\n' > rascunho/d.md
saida="$(python3 "$S/validar.py" --arquivo caso/d.md --autor "Celso" 2>&1)"
[ $? -ne 0 ] && echo "$saida" | grep -q "nao esta em fontes/" \
  && ok "24 documento citado ausente recusado" \
  || falha "24 documento ausente ACEITO ou recusado por outro motivo"

# 25 com o documento presente, grava e registra o hash (controle positivo)
echo "conteudo" > fontes/ausente.xlsx
python3 "$S/validar.py" --arquivo caso/d.md --autor "Celso" >/dev/null 2>&1
gravou=$?
grep -q '"documentos": {"ausente.xlsx"' registro/eventos.jsonl 2>/dev/null
rastro=$?
[ $gravou -eq 0 ] && [ $rastro -eq 0 ] \
  && ok "25 documento presente grava com hash na trilha" \
  || falha "25 documento presente NAO gravou ou NAO registrou hash"

# G6 — fontes/ e so leitura: escrita, edicao ou remocao por agente e negada
# fontes/README.md ja declara "so leitura", mas antes de G6 nada impedia a
# escrita — so o SHA-256 do validar.py detectava alteracao depois da
# citacao. G6 nega antes, com evento, tanto por Write/Edit quanto por Bash.

# G6a Write em fontes/ e negado
echo '{"tool_name":"Write","tool_input":{"file_path":"fontes/novo.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6a Write em fontes/ negado" || falha "G6a Write em fontes/ NAO foi negado"

# G6b Edit em fontes/ e negado
echo '{"tool_name":"Edit","tool_input":{"file_path":"fontes/ausente.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6b Edit em fontes/ negado" || falha "G6b Edit em fontes/ NAO foi negado"

# G6c Bash escrevendo em fontes/ (redirecionamento) e negado
echo '{"tool_name":"Bash","tool_input":{"command":"echo oi > fontes/novo.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6c bash redirecionando para fontes/ negado" || falha "G6c bash para fontes/ NAO foi negado"

# G6d Bash removendo arquivo de fontes/ e negado
echo '{"tool_name":"Bash","tool_input":{"command":"rm fontes/ausente.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6d bash removendo de fontes/ negado" || falha "G6d bash rm em fontes/ NAO foi negado"

# G6e Bash movendo/copiando por cima de arquivo em fontes/ e negado
echo '{"tool_name":"Bash","tool_input":{"command":"mv rascunho/x.xlsx fontes/ausente.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6e bash mv para fontes/ negado" || falha "G6e bash mv para fontes/ NAO foi negado"

# G6f escrita em contexto/fontes/ (fonte curada) tambem e negada por caminho direto
echo '{"tool_name":"Write","tool_input":{"file_path":"contexto/fontes/F-100.yaml"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6f Write em contexto/fontes/ negado" || falha "G6f Write em contexto/fontes/ NAO foi negado"

# G6g evento de recusa e registrado (controle positivo da trilha)
grep -q '"motivo": ".*fontes/' registro/eventos.jsonl 2>/dev/null
[ $? -eq 0 ] && ok "G6g tentativa negada em fontes/ gera evento" || falha "G6g tentativa negada em fontes/ SEM evento"

# G6h leitura em fontes/ continua permitida (controle positivo)
echo '{"tool_name":"Read","tool_input":{"file_path":"fontes/ausente.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 0 ] && ok "G6h leitura em fontes/ permanece permitida" || falha "G6h leitura em fontes/ foi negada indevidamente"

# G6i-k: contornos que nao usam os verbos literais da primeira implementacao.
echo '{"tool_name":"Bash","tool_input":{"command":"cd fontes && rm ausente.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6i cd seguido de rm em fontes/ negado" || falha "G6i cd+rm em fontes/ NAO foi negado"

echo '{"tool_name":"Bash","tool_input":{"command":"sed -i s/conteudo/alterado/ fontes/ausente.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6j sed -i em fontes/ negado" || falha "G6j sed -i em fontes/ NAO foi negado"

echo '{"tool_name":"Bash","tool_input":{"command":"python3 -c \"from pathlib import Path; Path('fontes/ausente.xlsx').unlink()\""}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "G6k remocao indireta por Python negada" || falha "G6k remocao indireta por Python NAO foi negada"

# G6l: o par positivo de Bash continua permitindo leitura simples.
echo '{"tool_name":"Bash","tool_input":{"command":"cat fontes/ausente.xlsx"}}' \
  | python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 0 ] && ok "G6l leitura simples por Bash permanece permitida" || falha "G6l leitura por Bash foi negada indevidamente"

# Isolamento núcleo x contraste. O núcleo não pode operar no mesmo caso,
# seja pelo plugin habilitado, seja por marcador durável já presente.
mkdir -p .claude
printf '%s\n' '{"enabledPlugins":{"eiac-contraste@pesquisa":true}}' > .claude/settings.json
echo '{"tool_name":"Read","tool_input":{"file_path":"caso/F0.md"}}' \
  | CLAUDE_CONFIG_DIR="$TMP/config-sem-plugins" python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "ISO1 núcleo recusa caso com eiac-contraste habilitado" \
  || falha "ISO1 núcleo operou com eiac-contraste habilitado"
rm .claude/settings.json

cp registro/estado.json registro/estado-campo.json
python3 -c "import json; p='registro/estado.json'; d=json.load(open(p)); d['execucao']='contraste'; open(p,'w').write(json.dumps(d))"
echo '{"tool_name":"Read","tool_input":{"file_path":"caso/F0.md"}}' \
  | CLAUDE_CONFIG_DIR="$TMP/config-sem-plugins" python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 2 ] && ok "ISO2 núcleo recusa registro de execução de contraste" \
  || falha "ISO2 núcleo operou sobre registro de contraste"
mv registro/estado-campo.json registro/estado.json

echo '{"tool_name":"Read","tool_input":{"file_path":"caso/F0.md"}}' \
  | CLAUDE_CONFIG_DIR="$TMP/config-sem-plugins" python3 "$S/guarda.py" >/dev/null 2>&1
[ $? -eq 0 ] && ok "ISO-controle núcleo opera em caso de campo isolado" \
  || falha "ISO-controle caso de campo isolado foi recusado"

# 8 playbook incompleto nao carrega
python3 - <<'PY'
import json, pathlib
p = pathlib.Path("registro/playbook.json")
d = json.loads(p.read_text())
d.pop("inegociaveis")
p.write_text(json.dumps(d))
PY
python3 "$S/playbook.py" >/dev/null 2>&1
[ $? -ne 0 ] && ok "8 playbook incompleto recusado" || falha "8 playbook incompleto ACEITO"

echo
if [ "$falhas" -eq 0 ]; then
  echo "todas as travas recusam como devem"
  exit 0
else
  echo "$falhas trava(s) deixaram de recusar"
  exit 1
fi
