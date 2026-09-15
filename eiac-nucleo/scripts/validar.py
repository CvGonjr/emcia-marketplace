"""Validador de procedencia. Unico caminho de escrita em caso/.

Uso:  python3 validar.py --arquivo caso/P2-regras.md --autor "Nome"
Le o conteudo proposto de rascunho/<mesmo-nome> e so grava se todas as
assercoes passarem. Nove regras, nenhuma avaliada por modelo.
"""
import argparse, hashlib, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P

LINHA = re.compile(r"^\s*-\s*\[(?P<marca>[^\]]+)\]")


def campos(marca):
    return [p.strip() for p in marca.split("·")]


def citado(c):
    """Nome do arquivo citado em 'documento: <nome> [p.N]', ou None."""
    for x in c:
        if x.startswith("documento:"):
            alvo = x.split(":", 1)[1].strip()
            # a pagina faz parte da citacao, nao do nome do arquivo
            return re.sub(r"\s+p\.\S+$", "", alvo).strip() or None
    return None


def validar_linha(marca, pb, n):
    c = campos(marca)
    if not c:
        return f"linha {n}: marcacao vazia"
    proc = pb["procedencia"]
    origem = next((x for x in c if x in proc["origem"]), None)
    if not origem:
        return f"linha {n}: origem ausente. Esperado um de {proc['origem']}"
    contexto = next((x for x in c if x in proc["contexto"]), "campo")
    if contexto != "campo":
        return f"linha {n}: contexto '{contexto}' nao entra em caso/"
    if origem == "externo" and not any(x.startswith("http") for x in c):
        return f"linha {n}: origem externo exige url"
    if origem == "externo" and not any(x.startswith("limite:") for x in c):
        return f"linha {n}: origem externo exige limite da fonte"
    if origem == "inferido" and not any(x.startswith("premissa:") for x in c):
        return f"linha {n}: origem inferido exige premissa"
    if origem == "verificado" and not any(
        x.startswith(("observacao", "documento:")) for x in c
    ):
        return f"linha {n}: verificado exige observacao ou documento interno"
    doc = citado(c)
    if doc and not (pathlib.Path("fontes") / doc).exists():
        return (f"linha {n}: documento citado '{doc}' nao esta em fontes/. "
                f"Citacao que aponta para fora do caso nao e verificavel.")
    apur = next((x for x in c if x in proc.get("apuracao", [])), None)
    if apur == "estimado" and not any(x.startswith("base:") for x in c):
        return f"linha {n}: apuracao estimado exige base"
    if apur == "medido" and not any(x.startswith("amostra:") for x in c):
        return f"linha {n}: apuracao medido exige amostra"
    if any(x.lower().startswith(("ag0", "agente", "sistema")) for x in c):
        return f"linha {n}: autor nao pode ser agente"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True)
    ap.add_argument("--autor", required=True)
    a = ap.parse_args()

    pb, erro = P.carregar()
    if erro:
        print(erro, file=sys.stderr); sys.exit(1)

    destino = pathlib.Path(a.arquivo)
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        print(f"rascunho/{destino.name} nao existe. Escreva o conteudo la primeiro.",
              file=sys.stderr)
        sys.exit(1)

    erros, total, docs = [], 0, {}
    for n, linha in enumerate(rascunho.read_text(encoding="utf-8").splitlines(), 1):
        m = LINHA.match(linha)
        if not m:
            continue
        total += 1
        e = validar_linha(m.group("marca"), pb, n)
        if e:
            erros.append(e)
            continue
        # o hash fixa qual versao do documento sustentou a assercao: trocar o
        # arquivo depois passa a ser visivel na trilha, nao silencioso
        doc = citado(campos(m.group("marca")))
        if doc and doc not in docs:
            caminho = pathlib.Path("fontes") / doc
            docs[doc] = hashlib.sha256(caminho.read_bytes()).hexdigest()[:12]

    if total == 0:
        print("nenhuma assercao marcada encontrada", file=sys.stderr); sys.exit(1)
    if erros:
        for e in erros:
            print(e, file=sys.stderr)
        E.evento("AssercaoRecusada", arquivo=a.arquivo, erros=len(erros), autor=a.autor)
        sys.exit(1)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    E.evento("AssercaoRegistrada", arquivo=a.arquivo, assercoes=total,
             autor=a.autor, documentos=docs or None)
    print(f"{total} assercoes gravadas em {a.arquivo}"
          + (f" | documentos: {', '.join(docs)}" if docs else ""))


if __name__ == "__main__":
    main()
