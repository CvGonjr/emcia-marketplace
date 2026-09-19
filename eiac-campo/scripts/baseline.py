"""Linha de base (P3a). Unico caminho de escrita em registro/baseline/.

Uso:
  python3 baseline.py --arquivo registro/baseline/BL-001.yaml --ator "Nome"

A linha de base e artefato de medicao produzido em P3a (EMCIA-MET-01
3.4.3: "a linha de base e obrigatoria nos tres niveis, estimada em N1,
medida em N2 e N3, mas sempre registrada antes do piloto"; formato
concreto em EMCIA-E2 Parte A.3: Marca/Indicador/Valor atual/Como foi
obtido/Data). Nao e objeto CTX (CTX-01 nao define esse objeto) e "BL-nnn"
e convencao tecnica interna do Estudio para rastreabilidade, nao
terminologia do metodo -- nenhuma fonte oficial nomeia um padrao de ID
para este artefato. Este script vive em eiac-campo porque sabe o que uma
linha de base e; reaproveita as primitivas genericas do eiac-nucleo
(estrutura.validar, estado.evento, estado.autor_e_agente) sem alterar
nenhuma delas.

O nivel do caso decide o que 'apuracao' aceita: N1 admite estimativa;
N2 e N3 exigem calculo ou medicao (MET-01 3.4.3). O nucleo nao conhece
essa regra -- avancar.satisfazer_inegociavel() so exige evidencia nao
vazia; a semantica de "a linha de base deste nivel e valida" pertence
inteiramente a este script.
"""
import argparse
import pathlib
import sys

RAIZ_NUCLEO = pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estado as E  # noqa: E402
import estrutura as X  # noqa: E402
import json  # noqa: E402


APURACAO_INSUFICIENTE_FORA_DE_N1 = {"estimado"}


def _ator_pessoa_nomeada(nome):
    nome = (nome or "").strip()
    if not nome or E.autor_e_agente(nome):
        return False
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
    return nome.lower() not in genericos


def checar_autoria(dados):
    erros = []
    for campo in ("declarado_por", "registrado_por"):
        valor = dados.get(campo)
        if valor is not None and E.autor_e_agente(valor):
            erros.append(f"{campo} nao pode ser agente: '{valor}'")
    return erros


def checar_apuracao_por_nivel(candidato):
    """N1 admite estimativa; N2/N3 exigem calculo ou medicao (MET-01 3.4.3).

    O nivel gravado no proprio artefato e a fonte -- este script nao le
    registro/estado.json para nao acoplar a maquina de etapas a um
    dominio de registro que ela nao precisa conhecer; quem grava a linha
    de base declara para qual nivel ela vale.
    """
    nivel = candidato.get("nivel")
    apuracao = candidato.get("apuracao")
    if nivel and nivel != "N1" and apuracao in APURACAO_INSUFICIENTE_FORA_DE_N1:
        return [f"nivel {nivel} exige apuracao calculada ou medida; "
                f"'estimado' so e admitido em N1 (MET-01 3.4.3)"]
    return []


def gravar_baseline(destino, ator, schema_caminho="registro/baseline.schema.json"):
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, "linha_de_base")
    erros += checar_autoria(candidato)
    erros += checar_apuracao_por_nivel(candidato)

    if erros:
        E.evento("LinhaDeBaseRecusada", arquivo=str(destino), erros=erros, ator=ator)
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    E.evento("LinhaDeBaseRegistrada", arquivo=str(destino), id=candidato.get("id"),
             indicador=candidato.get("indicador"), apuracao=candidato.get("apuracao"),
             nivel=candidato.get("nivel"), ator=ator, versao=candidato.get("versao"))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True,
                     help="destino em registro/baseline/<id>.yaml")
    ap.add_argument("--ator", required=True)
    ap.add_argument("--schema", default="registro/baseline.schema.json")
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("registro/baseline/"):
        print("linha de base so grava dentro de registro/baseline/", file=sys.stderr)
        sys.exit(1)

    erro = gravar_baseline(destino, a.ator, schema_caminho=a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"linha de base gravada: {a.arquivo}")


if __name__ == "__main__":
    main()
