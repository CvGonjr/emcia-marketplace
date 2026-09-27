#!/usr/bin/env bash
# Execute dentro do caso, no terminal. Apenas simula a chamada à guarda.
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo 'uso: como-agente.sh "<comando>" (dentro do caso)' >&2
  exit 1
fi
raiz_demo="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
python3 - "$raiz_demo" "$1" <<'PY'
import json, pathlib, subprocess, sys
raiz, comando = pathlib.Path(sys.argv[1]), sys.argv[2]
r = subprocess.run([sys.executable, str(raiz / 'eiac-nucleo/scripts/guarda.py')],
                   input=json.dumps({'tool_name': 'Bash', 'tool_input': {'command': comando}}),
                   text=True, capture_output=True)
if r.returncode == 0:
    print('PERMITIDO | a guarda permite esta chamada; o comando não foi executado.')
elif r.returncode == 2:
    print('NEGADO | '+r.stderr.strip())
else:
    print('ERRO | '+(r.stderr.strip() or r.stdout.strip()), file=sys.stderr)
    sys.exit(r.returncode)
PY
