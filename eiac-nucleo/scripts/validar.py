"""Validador de procedencia documental. Unico caminho de escrita em caso/.

Uso:  python3 validar.py --arquivo caso/P2-regras.md
A autoria do registro nao vem de --autor: e sempre `responsavel` de
registro/estado.json, fixado pelo operador em novo-caso.sh, fora da sessao
do agente (nenhuma habilidade instrui a chamar validar.py diretamente, so
via comando /eiac-nucleo:gravar). Caso sem responsavel definido nao grava
nada. Le o conteudo proposto de rascunho/<mesmo-nome> e so grava se todas as
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


def valor_campo(campos_marca, nome):
    prefixo = f"{nome}:"
    for item in campos_marca:
        if item.startswith(prefixo):
            return item.split(":", 1)[1].strip() or None
    return None


def validar_linha(marca, pb, n):
    c = campos(marca)
    if not c:
        return f"linha {n}: marcacao vazia"
    proc = pb["procedencia"]
    valores = proc["valores"]
    marcas = [x for x in c if x in valores]
    if not marcas:
        return f"linha {n}: procedencia ausente. Esperado um de {valores}"
    if len(marcas) != 1:
        return f"linha {n}: informe exatamente uma procedencia; recebido {marcas}"
    procedencia = marcas[0]
    if procedencia == "I" and not any(x.startswith("premissa:") for x in c):
        return f"linha {n}: procedencia I exige premissa"
    if procedencia == "V" and not any(
        x.startswith(("observacao:", "documento:", "leitura_de_volta:")) for x in c
    ):
        return (f"linha {n}: procedencia V exige evidencia de observacao, "
                "documento ou leitura de volta")

    dimensoes = pb.get("dimensoes", {})
    tipo_fonte = valor_campo(c, "tipo_fonte")
    tipos_fonte = dimensoes.get("tipo_fonte", [])
    if tipo_fonte and tipo_fonte not in tipos_fonte:
        return f"linha {n}: tipo_fonte invalido. Esperado um de {tipos_fonte}"
    if tipo_fonte == "externa" and not any(x.startswith("http") for x in c):
        return f"linha {n}: tipo_fonte externa exige url"
    if tipo_fonte == "externa" and not any(x.startswith("limite:") for x in c):
        return f"linha {n}: tipo_fonte externa exige limite da fonte"

    doc = citado(c)
    if doc and not (pathlib.Path("fontes") / doc).exists():
        return (f"linha {n}: documento citado '{doc}' nao esta em fontes/. "
                f"Citacao que aponta para fora do caso nao e verificavel.")
    apur = valor_campo(c, "apuracao")
    apuracoes = dimensoes.get("apuracao", [])
    if apur and apur not in apuracoes:
        return f"linha {n}: apuracao invalida. Esperado um de {apuracoes}"
    if apur == "estimado" and not any(x.startswith("base:") for x in c):
        return f"linha {n}: apuracao estimado exige base"
    if apur == "medido" and not any(x.startswith("amostra:") for x in c):
        return f"linha {n}: apuracao medido exige amostra"
    if any(E.autor_e_agente(x) for x in c):
        return f"linha {n}: autor nao pode ser agente"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True)
    ap.add_argument("--autor", default=None,
                     help="ignorado para fins de autoria -- ver docstring do modulo")
    a = ap.parse_args()

    pb, erro = P.carregar()
    if erro:
        print(erro, file=sys.stderr); sys.exit(1)

    estado = E.ler()
    responsavel = (estado or {}).get("responsavel")
    if not responsavel:
        print("caso sem responsavel definido em registro/estado.json "
              "(fixado por novo-caso.sh --responsavel). Nenhuma gravacao "
              "e aceita sem isso.", file=sys.stderr)
        E.evento("AssercaoRecusada", arquivo=a.arquivo,
                 motivo="responsavel nao definido", autor_informado=a.autor)
        sys.exit(1)

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
        E.evento("AssercaoRecusada", arquivo=a.arquivo, erros=len(erros),
                 autor=responsavel, autor_informado=a.autor)
        sys.exit(1)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    E.evento("AssercaoRegistrada", arquivo=a.arquivo, assercoes=total,
             autor=responsavel, autor_informado=a.autor, documentos=docs or None)
    print(f"{total} assercoes gravadas em {a.arquivo}"
          + (f" | documentos: {', '.join(docs)}" if docs else ""))


if __name__ == "__main__":
    main()
