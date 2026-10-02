#!/usr/bin/env bash
# Bootstrap humano; executar antes de abrir a sessão do agente.
# ./novo-caso.sh <nome> --responsavel "Nome Sobrenome" [base] [--expediente <caminho>]
# Identidade, expediente e pacote do método são conferidos pelo campo.
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$RAIZ/eiac-campo/scripts/abrir_caso.py" "$@"
