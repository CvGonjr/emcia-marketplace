#!/usr/bin/env bash
# Cria o repositorio de um caso a partir do template do playbook.
#
#   ./novo-caso.sh medic-plus --responsavel "Nome Sobrenome"
#   ./novo-caso.sh medic-plus --responsavel "Nome Sobrenome" ~/trabalho/clientes
#
# Destino padrao: ~/casos/<nome>
#
# --responsavel e obrigatorio: e a pessoa cuja autoria valida validar.py,
# curar.py e selar.py gravam daqui em diante -- fixada aqui, fora da sessao
# do agente, precisamente para que nenhum comando do plugin possa definir
# ou trocar quem e o responsavel do caso.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$RAIZ/eiac-campo/template-caso"

nome=""
base="$HOME/casos"
responsavel=""

uso() {
  echo "uso: $(basename "$0") <nome-do-caso> --responsavel \"Nome Sobrenome\" [diretorio-base]" >&2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --responsavel) responsavel="${2:-}"; shift 2 ;;
    -h|--help) uso; exit 0 ;;
    *)
      if [ -z "$nome" ]; then nome="$1";
      else base="$1"; fi
      shift ;;
  esac
done

if [ -z "$nome" ] || [ -z "$responsavel" ]; then
  uso
  exit 1
fi

case "$nome" in
  */*|.*|"") echo "nome invalido: use apenas o nome do caso, sem barras" >&2; exit 1 ;;
esac

python3 - "$responsavel" <<'PY'
import re, sys
nome = (sys.argv[1] or "").strip()
if not nome:
    sys.exit("responsavel vazio: informe pessoa nomeada")
if re.search(r"[<>]", nome):
    sys.exit(f"responsavel invalido (placeholder nao preenchido): '{nome}'")
chave = re.sub(r"[\s\-_]", "", nome.lower())
if chave.startswith(("ag0", "agente", "sistema")):
    sys.exit(f"responsavel nao pode ser codigo de agente: '{nome}'")
genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
if nome.lower() in genericos:
    sys.exit(f"responsavel precisa ser pessoa nomeada, nao coletivo generico: '{nome}'")
PY

destino="$base/$nome"

[ -d "$TEMPLATE" ] || { echo "template nao encontrado em $TEMPLATE" >&2; exit 1; }
[ -e "$destino" ] && { echo "ja existe: $destino" >&2; exit 1; }

# um repositorio por caso: o destino nao pode nascer dentro de outro
if git -C "$base" rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "erro: $base esta dentro de um repositorio git." >&2
  echo "Um repositorio por caso. Escolha um diretorio base fora de qualquer repo." >&2
  exit 1
fi

mkdir -p "$base"
cp -r "$TEMPLATE" "$destino"
cd "$destino"

# nome do caso e responsavel no registro; CLAUDE.md so recebe o nome
python3 - "$nome" "$responsavel" "$RAIZ" <<'PY'
import json, pathlib, sys
nome, responsavel, raiz = sys.argv[1], sys.argv[2], sys.argv[3]

sys.path.insert(0, str(pathlib.Path(raiz) / "eiac-nucleo" / "scripts"))
import estado as E

p = pathlib.Path("registro/estado.json")
d = json.loads(p.read_text(encoding="utf-8"))
d["caso"] = nome
d["responsavel"] = responsavel
p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")

E.evento("CasoAberto", caso=nome, responsavel=responsavel)

c = pathlib.Path("CLAUDE.md")
c.write_text(c.read_text(encoding="utf-8").replace("ALTERE-ME", nome), encoding="utf-8")
PY

mkdir -p metodo rascunho caso fontes
touch metodo/.gitkeep rascunho/.gitkeep caso/.gitkeep

git init -q
git add -A

commit_ok=1
if ! git config user.email >/dev/null 2>&1 && ! git config --global user.email >/dev/null 2>&1; then
  commit_ok=0
elif ! git commit -qm "abertura do caso $nome" 2>/dev/null; then
  commit_ok=0
fi

cat <<FIM

caso "$nome" criado em $destino

Falta uma coisa antes de comecar:

  copie os documentos do metodo para $destino/metodo/
  documento do metodo, glossario, catalogo de delegacao, quadro de
  ferramentas, instrumento de triagem, modelos E1-E5, plano de
  verificacao, CTX-01

Os artefatos da organizacao vao para $destino/fontes/ — leia o README
de la antes de commitar documento de cliente.

Depois:

  cd "$destino" && claude

E confirme com  /eiac-nucleo:estado

FIM

if [ "$commit_ok" -eq 0 ]; then
  cat <<'AVISO'
ATENCAO: o commit inicial nao foi feito. Configure a identidade do git e
commite — a trilha do caso depende do historico:

  git config --global user.name "Seu Nome"
  git config --global user.email "voce@exemplo.com"
  git commit -m "abertura do caso"

AVISO
fi
