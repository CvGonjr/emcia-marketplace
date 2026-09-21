#!/usr/bin/env python3
"""Contrato do pacote controlado de documentos consumido pelo eiac-campo."""
import hashlib
import json
import pathlib
import sys


RAIZ = pathlib.Path(__file__).resolve().parents[1]
PACOTE = RAIZ / "eiac-campo" / "reference" / "metodo"
CONTRASTE = RAIZ.parent / "emcia-contraste"

DOCUMENTOS = {
    "EMCIA-CAM-01-protocolo-de-campo-por-passo.md",
    "EMCIA-CAT-01-fronteira-de-delegacao.md",
    "EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md",
    "EMCIA-E1-ficha-de-enquadramento.md",
    "EMCIA-E2-diagnostico-e-oportunidade.md",
    "EMCIA-E3-blueprint-da-solucao.md",
    "EMCIA-E4-guia-operacional.md",
    "EMCIA-E5-relatorio-de-piloto.md",
    "EMCIA-ESP-01-especificacao-executavel-do-estudio-de-trabalho.md",
    "EMCIA-FER-01-quadro-de-ferramentas.md",
    "EMCIA-GLO-01-glossario-do-metodo.md",
    "EMCIA-MET-01-documento-do-metodo.md",
    "EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md",
    "EMCIA-TRA-01-procedimentos-transversais-do-metodo.md",
    "EMCIA-TRI-01-instrumento-de-triagem.md",
    "EMCIA-VER-01-plano-de-verificacao.md",
}


def falhar(mensagem):
    print(f"FALHA metodo empacotado: {mensagem}")
    sys.exit(1)


def main():
    if not PACOTE.is_dir():
        falhar(f"diretorio ausente: {PACOTE}")
    ausentes = sorted(nome for nome in DOCUMENTOS if not (PACOTE / nome).is_file())
    if ausentes:
        falhar(f"documentos ausentes: {ausentes}")

    manifesto_path = PACOTE / "manifesto.json"
    try:
        manifesto = json.loads(manifesto_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as erro:
        falhar(f"manifesto ausente ou invalido: {erro}")
    if set(manifesto.get("documentos", {})) != DOCUMENTOS:
        falhar("manifesto nao enumera exatamente o pacote operacional controlado")
    for nome, esperado in manifesto["documentos"].items():
        obtido = hashlib.sha256((PACOTE / nome).read_bytes()).hexdigest()
        if obtido != esperado:
            falhar(f"hash divergente em {nome}: {obtido} != {esperado}")

    copias_no_contraste = [
        caminho for caminho in CONTRASTE.glob("**/EMCIA-*.md")
        if ".git" not in caminho.parts
    ]
    if copias_no_contraste:
        falhar(f"documentos do metodo foram copiados para o contraste: {copias_no_contraste}")

    print(f"metodo empacotado: {len(DOCUMENTOS)} documentos, hashes validos, nenhuma copia no contraste")


if __name__ == "__main__":
    main()
