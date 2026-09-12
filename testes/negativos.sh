#!/usr/bin/env bash
# Os sete testes negativos. Cada um prova que uma trava recusa.
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

# 3 assercao sem origem
printf -- '- [Celso · 2026-09-11] regra qualquer\n' > rascunho/t.md
python3 "$S/validar.py" --arquivo caso/t.md --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "3 assercao sem origem recusada" || falha "3 assercao sem origem ACEITA"

# 4 assercao valida grava (teste positivo de controle)
printf -- '- [inferido · premissa: teste · Celso] regra de teste\n' > rascunho/t.md
python3 "$S/validar.py" --arquivo caso/t.md --autor "Celso" >/dev/null 2>&1
[ $? -eq 0 ] && ok "4 assercao valida gravada" || falha "4 assercao valida RECUSADA"

# 5 encerrar etapa presencial sem sessao
python3 "$S/avancar.py" --encerrar P3b --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "5 encerramento sem sessao recusado" || falha "5 encerramento sem sessao ACEITO"

# 6 autor agente
python3 "$S/avancar.py" --encerrar F0 --autor "AG05" >/dev/null 2>&1
[ $? -ne 0 ] && ok "6 autor agente recusado" || falha "6 autor agente ACEITO"

# 7 emitir com portao fechado
python3 "$S/avancar.py" --emitir E2 --autor "Celso" >/dev/null 2>&1
[ $? -ne 0 ] && ok "7 emissao com portao fechado recusada" || falha "7 emissao ACEITA indevidamente"

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
