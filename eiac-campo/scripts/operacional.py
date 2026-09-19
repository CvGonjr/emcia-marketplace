"""Especificacao operacional (P6). Unico caminho de escrita em registro/operacional/.

Uso:
  python3 operacional.py --arquivo registro/operacional/OP-001.yaml --ator "Nome"

Produto do P6: especificacao de como a solucao entra no fluxo de
trabalho -- nao e deployment, nao e objeto CTX, nao e o termo de
autonomia de P7. Vive em eiac-campo porque sabe o que uma especificacao
operacional e; reaproveita as mesmas primitivas genericas do eiac-nucleo
usadas por curar.py e governanca.py (estrutura.validar, estado.evento,
estado.autor_e_agente), sem tocar em nenhuma delas.

Estados: proposta -> validado. Agente pode propor; so ator humano
nomeado pode validar. Validacao nao e a decisao de autonomia de P7 --
e a confirmacao de que o desenho operacional em si (onde a solucao
entra, quem recebe a saida) esta correto, distinta e anterior a ela.
"""
import argparse
import pathlib
import sys

RAIZ_NUCLEO = pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estado as E  # noqa: E402
import estrutura as X  # noqa: E402
import json  # noqa: E402


ESTADOS = ("proposta", "validado")


def checar_autoria(dados):
    erros = []
    for campo in ("declarado_por", "registrado_por", "validado_por"):
        valor = dados.get(campo)
        if valor is None:
            continue
        if E.autor_e_agente(valor):
            erros.append(f"{campo} nao pode ser agente: '{valor}'")
    return erros


def checar_transicao_estado(anterior, candidato):
    """proposta -> validado, nunca ao contrario; versao cresce a cada
    mudanca de estado (mesmo principio das demais versoes deste pacote).
    """
    estado_novo = candidato.get("estado")
    if estado_novo not in ESTADOS:
        return [f"estado '{estado_novo}' invalido, esperado um de {ESTADOS}"]

    if anterior is None:
        if estado_novo != "proposta":
            return [f"especificacao nova deve nascer em estado 'proposta', recebido '{estado_novo}'"]
        versao = candidato.get("versao")
        if versao not in (1, "1"):
            return [f"especificacao nova deve nascer na versao 1, recebido {versao!r}"]
        return []

    estado_antes = anterior.get("estado")
    idx_antes = ESTADOS.index(estado_antes) if estado_antes in ESTADOS else -1
    idx_depois = ESTADOS.index(estado_novo)

    erros = []
    if idx_depois < idx_antes:
        erros.append(f"estado nao pode retroceder: '{estado_antes}' -> '{estado_novo}'")
    elif idx_depois > idx_antes:
        try:
            cresceu = int(candidato.get("versao")) > int(anterior.get("versao"))
        except (TypeError, ValueError):
            cresceu = False
        if not cresceu:
            erros.append(
                f"mudanca de estado '{estado_antes}' -> '{estado_novo}' exige nova versao "
                f"(recebido {anterior.get('versao')!r} -> {candidato.get('versao')!r})"
            )
    return erros


def checar_validacao(candidato):
    """Estado 'validado' exige validado_por preenchido -- especificacao
    nao vira validada so porque o campo 'estado' foi trocado.
    """
    if candidato.get("estado") != "validado":
        return []
    if not (candidato.get("validado_por") or "").strip():
        return ["estado 'validado' exige validado_por preenchido"]
    if not (candidato.get("data_validacao") or "").strip():
        return ["estado 'validado' exige data_validacao preenchida"]
    return []


def _ator_pessoa_nomeada(nome):
    nome = (nome or "").strip()
    if not nome or E.autor_e_agente(nome):
        return False
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
    return nome.lower() not in genericos


def gravar_especificacao(destino, ator, schema_caminho="registro/operacional.schema.json"):
    """Le o rascunho correspondente, valida e grava se tudo passar.

    Propor (estado 'proposta') e permitido a qualquer ator, inclusive
    agente -- e a preparacao (item 12 do pacote: ler E3/CTX, estruturar,
    apontar inconsistencias). Validar (estado 'validado') exige pessoa
    humana nomeada -- fluxo sugerido nao vira fluxo aprovado sozinho.
    """
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, "especificacao_operacional")
    erros += checar_autoria(candidato)
    erros += checar_validacao(candidato)

    if candidato.get("estado") == "validado":
        if E.autor_e_agente(ator):
            erros.append(
                "agente nao pode validar a especificacao operacional: o estado "
                "'validado' exige ator humano nomeado (CAT-01 3.5.1, mesmo "
                "principio aplicado ao termo de autonomia de P7)."
            )
        elif not _ator_pessoa_nomeada(ator):
            erros.append(
                f"validacao exige pessoa nomeada; '{ator}' nao satisfaz "
                f"(agente, vazio ou coletivo generico nao substitui pessoa)."
            )

    anterior = None
    if destino.exists():
        try:
            anterior = X.carregar_yaml(destino.read_text(encoding="utf-8"))
        except (X.ErroYaml, ValueError) as erro:
            return f"registro existente esta ilegivel: {erro}"
    erros += checar_transicao_estado(anterior, candidato)

    if erros:
        E.evento(
            "EspecificacaoOperacionalRecusada", arquivo=str(destino), erros=erros,
            ator=ator, estado_tentado=candidato.get("estado"),
        )
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    evento_tipo = "EspecificacaoOperacionalValidada" if candidato.get("estado") == "validado" \
        else "EspecificacaoOperacionalRegistrada"
    E.evento(
        evento_tipo, arquivo=str(destino), id=candidato.get("id"),
        estado=candidato.get("estado"), versao=candidato.get("versao"),
        ator=ator, validado_por=candidato.get("validado_por"),
    )
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True,
                     help="destino em registro/operacional/<id>.yaml")
    ap.add_argument("--ator", required=True,
                     help="quem esta gravando esta versao da especificacao")
    ap.add_argument("--schema", default="registro/operacional.schema.json")
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("registro/operacional/"):
        print("especificacao operacional so grava dentro de registro/operacional/", file=sys.stderr)
        sys.exit(1)

    erro = gravar_especificacao(destino, a.ator, schema_caminho=a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"especificacao operacional gravada: {a.arquivo}")


if __name__ == "__main__":
    main()
