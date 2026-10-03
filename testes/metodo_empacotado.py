#!/usr/bin/env python3
"""Contrato do pacote controlado de documentos consumido pelo eiac-campo."""
import hashlib
import json
import pathlib
import sys
import re
import subprocess


RAIZ = pathlib.Path(__file__).resolve().parents[1]
PACOTE = RAIZ / "eiac-campo" / "reference" / "metodo"
CONTRASTE = RAIZ.parent / "emcia-contraste"

DOCUMENTOS = {
    'EMCIA-ROT-02-roteiro-de-habilitacao.md',
    'EMCIA-HAB-fluxo-operacional-proposta.md',
    'EMCIA-HAB-01-protocolo-de-habilitacao.md',
    'EMCIA-CAN-01-protocolo-de-canais-externos.md',
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
    "EMCIA-MAN-01-manual-de-aplicacao.md",
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
    if {p.name for p in PACOTE.iterdir()} != DOCUMENTOS | {'manifesto.json'}:
        falhar('arquivos fora do manifesto')
    caminhos = manifesto.get('caminhos_canonicos', {})
    if set(caminhos) != DOCUMENTOS:
        falhar('caminhos canônicos não enumeram exatamente o pacote')
    origem = re.search(r'commit ([0-9a-f]{40})$', manifesto.get('origem_controlada', ''))
    if origem is None:
        falhar('origem controlada deve fixar commit completo')
    canonico = RAIZ.parent / 'emcia-artefatos'
    for nome, esperado in manifesto["documentos"].items():
        caminho = pathlib.PurePosixPath(caminhos[nome])
        if caminho.is_absolute() or '..' in caminho.parts or caminho.name != nome:
            falhar(f'caminho canônico inválido: {nome}')
        if (PACOTE / nome).is_symlink():
            falhar(f'symlink no pacote: {nome}')
        data = (PACOTE / nome).read_bytes()
        obtido = hashlib.sha256(data).hexdigest()
        if obtido != esperado:
            falhar(f"hash divergente em {nome}: {obtido} != {esperado}")

        # Quando o checkout canônico está disponível, confere o objeto Git,
        # nunca o arquivo mutável do working tree. O pacote funciona offline.
        if canonico.is_dir():
            try:
                original = subprocess.check_output(
                    ['git', 'show', f'{origem[1]}:{caminhos[nome]}'], cwd=canonico,
                    stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as erro:
                falhar(f'objeto canônico indisponível: {nome}: {erro.stderr.decode()}')
            if data != original:
                falhar(f'bytes diferentes do commit canônico: {nome}')

    copias_no_contraste = [
        caminho for caminho in CONTRASTE.glob("**/EMCIA-*.md")
        if ".git" not in caminho.parts
    ]
    if copias_no_contraste:
        falhar(f"documentos do metodo foram copiados para o contraste: {copias_no_contraste}")

    print(f"origem controlada: {origem[1]}; comparação Git: {canonico.is_dir()}")
    print(f"metodo empacotado: {len(DOCUMENTOS)} documentos, hashes validos, nenhuma copia no contraste")


if __name__ == "__main__":
    main()
