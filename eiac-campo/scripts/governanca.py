"""Termo de autonomia (P7). Unico caminho de escrita em registro/governanca/.

Uso:
  python3 governanca.py --arquivo registro/governanca/autonomia/AUT-001.yaml --ator "Nome"

O rascunho em rascunho/AUT-001.yaml decide, pelo campo `estado`, se esta
gravacao e uma preparacao (rascunho/proposto) ou uma decisao (decidido).
Agente pode gravar rascunho/proposto; so ator humano nomeado pode gravar
decidido.

O termo de autonomia e artefato de governanca produzido em P7 -- nao e
objeto CTX (CTX-01 continua com Termo/Entidade/Regra/Fonte, intocados) e
nao e semantica de maquina de etapas (avancar.py continua sem conhecer
"autonomia"). Este script vive em eiac-campo porque sabe o que um termo
de autonomia e; reaproveita as primitivas genericas do eiac-nucleo
(estrutura.validar para o contrato do schema, estado.evento para a
trilha, estado.autor_e_agente para a convencao de autoria humana) sem
alterar nenhuma delas.

Estados: rascunho -> proposto -> decidido. Agente pode escrever/propor;
so ator humano nomeado pode gravar decisao (estado decidido). O termo
referencia, por `operacional_ref`, a especificacao operacional de P6
(registro/operacional/) sobre a qual a decisao de autonomia é tomada —
nao se decide autonomia sem saber onde a acao ocorre (relacao P6 -> P7).
"""
import argparse
import pathlib
import sys

RAIZ_NUCLEO = pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estado as E  # noqa: E402
import estrutura as X  # noqa: E402
import json  # noqa: E402


ESTADOS = ("rascunho", "proposto", "decidido")
CAMPOS_DECISAO = ("decisor", "data_decisao", "justificativa_decisao")


def checar_autoria(dados):
    """Autoria/registro do termo e decisor final: sempre pessoa nomeada.

    Reaproveita a mesma convencao lexical usada em toda a Ação 2.5/2.6 —
    nao redefine o que e um agente, so confere os campos que este objeto
    declara.
    """
    erros = []
    for campo in ("declarado_por", "registrado_por", "decisor"):
        valor = dados.get(campo)
        if valor is None:
            continue
        if E.autor_e_agente(valor):
            erros.append(f"{campo} nao pode ser agente: '{valor}'")
    return erros


def checar_transicao_estado(anterior, candidato):
    """Estado so avanca rascunho -> proposto -> decidido, nunca retrocede
    nem pula, e versao cresce a cada mudanca de estado (mesmo principio de
    historico sem sobrescrita ja aplicado a CTX-01, adaptado ao campo
    proprio deste artefato: 'estado', nao 'procedencia').
    """
    estado_novo = candidato.get("estado")
    if estado_novo not in ESTADOS:
        return [f"estado '{estado_novo}' invalido, esperado um de {ESTADOS}"]

    if anterior is None:
        if estado_novo != "rascunho":
            return [f"termo novo deve nascer em estado 'rascunho', recebido '{estado_novo}'"]
        versao = candidato.get("versao")
        if versao not in (1, "1"):
            return [f"termo novo deve nascer na versao 1, recebido {versao!r}"]
        return []

    estado_antes = anterior.get("estado")
    idx_antes = ESTADOS.index(estado_antes) if estado_antes in ESTADOS else -1
    idx_depois = ESTADOS.index(estado_novo)

    erros = []
    if idx_depois < idx_antes:
        erros.append(f"estado nao pode retroceder: '{estado_antes}' -> '{estado_novo}'")
    elif idx_depois > idx_antes + 1:
        erros.append(
            f"estado nao pode pular etapa: '{estado_antes}' -> '{estado_novo}' "
            f"(sequencia exigida: {' -> '.join(ESTADOS)})"
        )
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


def checar_decisao(candidato):
    """Estado 'decidido' exige decisor, data e justificativa preenchidos --
    um termo nao vira decisao so porque o campo 'estado' foi trocado.
    A checagem de decisor-nao-pode-ser-agente ja e feita por
    checar_autoria(); esta funcao so cobre completude dos campos.
    """
    if candidato.get("estado") != "decidido":
        return []
    faltando = [c for c in CAMPOS_DECISAO if not (candidato.get(c) or "").strip()]
    if faltando:
        return [f"estado 'decidido' exige {sorted(faltando)} preenchidos"]
    return []


DIRETORIO_OPERACIONAL = pathlib.Path("registro/operacional")


def checar_operacional_ref(candidato):
    """P7 depende de P6 (pacote 2.6.2 secao 24): a decisao de autonomia
    precisa referenciar uma especificacao operacional validada, para que
    quem decide saiba onde a acao ocorre, o que ela modifica e qual
    consequencia possui. Referencia a rascunho/proposta nao basta.
    """
    ref = candidato.get("operacional_ref")
    if not ref:
        return []  # required/nonempty ja cobre ausencia; aqui so a resolucao
    alvo = DIRETORIO_OPERACIONAL / f"{ref}.yaml"
    if not alvo.exists():
        return [f"operacional_ref '{ref}' nao resolve — {alvo} nao existe"]
    try:
        op = X.carregar_yaml(alvo.read_text(encoding="utf-8"))
    except (X.ErroYaml, ValueError) as erro:
        return [f"operacional_ref '{ref}' esta ilegivel: {erro}"]
    if op.get("estado") != "validado":
        return [
            f"operacional_ref '{ref}' aponta para especificacao em estado "
            f"'{op.get('estado')}', nao 'validado' — P7 nao decide sobre "
            f"desenho operacional ainda nao validado por humano"
        ]
    return []


def _ator_pessoa_nomeada(nome):
    """Mesma convencao ja usada por avancar._ator_valido() (2.6.1): nao
    vazio, nao agente, nao coletivo generico.
    """
    nome = (nome or "").strip()
    if not nome or E.autor_e_agente(nome):
        return False
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
    return nome.lower() not in genericos


def gravar_termo(destino, ator, schema_caminho="registro/autonomia.schema.json",
                  exige_humano_para_decidir=True):
    """Le o rascunho correspondente, valida e grava se tudo passar.

    ``ator`` e quem esta gravando esta versao (declarado_por/registrado_por
    do candidato, conforme o campo que o rascunho preencher). Se o
    candidato tentar estado 'decidido' e ``exige_humano_para_decidir`` for
    verdadeiro, ``ator`` precisa ser pessoa nomeada -- e a trava que impede
    o agente de autoaprovar a propria minuta.
    """
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, "termo_autonomia")
    erros += checar_autoria(candidato)
    erros += checar_decisao(candidato)
    erros += checar_operacional_ref(candidato)

    if candidato.get("estado") == "decidido" and exige_humano_para_decidir:
        if E.autor_e_agente(ator):
            erros.append(
                "agente nao pode decidir autonomia: o estado 'decidido' exige "
                "ator humano nomeado, nunca agente (CAT-01 3.5.1)."
            )
        elif not _ator_pessoa_nomeada(ator):
            erros.append(
                f"decisao de autonomia exige pessoa nomeada; '{ator}' nao satisfaz "
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
            "TermoAutonomiaRecusado", arquivo=str(destino), erros=erros,
            ator=ator, estado_tentado=candidato.get("estado"),
        )
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    evento_tipo = "AutonomiaDecidida" if candidato.get("estado") == "decidido" \
        else "TermoAutonomiaRegistrado"
    E.evento(
        evento_tipo, arquivo=str(destino), id=candidato.get("id"),
        estado=candidato.get("estado"), versao=candidato.get("versao"),
        ator=ator, decisor=candidato.get("decisor"),
    )
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True,
                     help="destino em registro/governanca/autonomia/<id>.yaml")
    ap.add_argument("--ator", required=True,
                     help="quem esta gravando esta versao do termo")
    ap.add_argument("--schema", default="registro/autonomia.schema.json")
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("registro/governanca/"):
        print("termo de autonomia so grava dentro de registro/governanca/", file=sys.stderr)
        sys.exit(1)

    erro = gravar_termo(destino, a.ator, schema_caminho=a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"termo de autonomia gravado: {a.arquivo}")


if __name__ == "__main__":
    main()
