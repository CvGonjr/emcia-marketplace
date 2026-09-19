"""Rotina de recalibragem e ciclos (P10). Unico caminho de escrita em
registro/calibragem/.

Uso:
  python3 calibragem.py --arquivo registro/calibragem/CAL-001.yaml --ator "Nome"
  python3 calibragem.py --arquivo registro/calibragem/CAL-001-C01.yaml --ator "Nome" --ciclo

A rotina (Anexo D) e os ciclos sao artefatos de calibragem produzidos em
P10 -- nao sao objeto CTX e nao sao semantica de maquina de etapas. Este
script vive em eiac-campo porque sabe o que e drift, ciclo e decisao de
recalibragem (EMCIA-CAM-01 3.6/Anexo D, inegociavel 5); reaproveita as
primitivas genericas do eiac-nucleo.

A recorrencia em si (cadencia, responsavel, historico de ciclos,
'ultima_verificacao') ja e mecanismo generico do nucleo desde o 2.6.1:
avancar.py --registrar-recorrencia. Este script NAO duplica esse
mecanismo -- ele cobre o que o nucleo nao pode conhecer: o conteudo da
rotina (Anexo D) e, por ciclo, se houve drift, a recomendacao do agente
e a decisao humana (recalibrar, expandir ou descontinuar -- CAT-01
3.4.5, CAM-01 3.6: 'a decisao de recalibrar, expandir ou descontinuar e
humana'). O agente pode preparar um ciclo inteiro (deteccao, quantificacao,
recomendacao); so ator humano nomeado pode gravar o campo 'decisao'.
"""
import argparse
import pathlib
import sys

RAIZ_NUCLEO = pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estado as E  # noqa: E402
import estrutura as X  # noqa: E402
import json  # noqa: E402


DIRETORIO_METRICAS = pathlib.Path("registro/metricas")
DIRETORIO_CALIBRAGEM = pathlib.Path("registro/calibragem")
DECISOES_VALIDAS = ("recalibrar", "expandir", "descontinuar")


def _ator_pessoa_nomeada(nome):
    nome = (nome or "").strip()
    if not nome or E.autor_e_agente(nome):
        return False
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
    return nome.lower() not in genericos


def checar_autoria(dados):
    """Autoria da rotina (rotina_calibragem): declarado_por, registrado_por
    e responsavel sao sempre humanos -- a rotina em si (cadencia, canal de
    incidente, responsavel pela recalibragem) e decisao de governanca, nao
    preparacao agentica.
    """
    erros = []
    for campo in ("declarado_por", "registrado_por", "responsavel"):
        valor = dados.get(campo)
        if valor is not None and E.autor_e_agente(valor):
            erros.append(f"{campo} nao pode ser agente: '{valor}'")
    return erros


def checar_autoria_ciclo(dados):
    """Autoria do ciclo (ciclo_calibragem): declarado_por/registrado_por
    podem ser agente -- o agente pode preparar um ciclo inteiro (deteccao,
    quantificacao, recomendacao), como o modulo ja documenta no cabecalho.
    So o campo 'decisao' e vedado a agente, e isso ja e responsabilidade
    de checar_decisao(), nao desta funcao.
    """
    return []


def checar_responsavel_nominal(candidato):
    """Inegociavel 5: responsavel e pessoa nomeada, area nao satisfaz
    (CAM-01 Anexo D). O schema ja exige nonempty; aqui a checagem e
    lexica (nao aceitar 'equipe de tecnologia' etc.).
    """
    resp = candidato.get("responsavel")
    if resp and not _ator_pessoa_nomeada(resp):
        return [f"'{resp}' nao e responsavel nominal aceitavel (area/equipe "
                f"generica ou agente nao substitui pessoa nomeada)"]
    return []


def checar_metricas_ref(candidato):
    """P10 pode usar indicadores de P9 (secao 36 do pacote): cada
    referencia em metricas_ref precisa resolver contra um arquivo real
    de registro/metricas/.
    """
    refs = candidato.get("metricas_ref")
    if not isinstance(refs, list):
        return []
    erros = []
    for ref in refs:
        alvo = DIRETORIO_METRICAS / f"{ref}.yaml"
        if not alvo.exists():
            erros.append(f"metricas_ref '{ref}' nao resolve — {alvo} nao existe")
    return erros


def gravar_rotina(destino, ator, schema_caminho="registro/calibragem.schema.json"):
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, "rotina_calibragem")
    erros += checar_autoria(candidato)
    erros += checar_responsavel_nominal(candidato)
    erros += checar_metricas_ref(candidato)

    if erros:
        E.evento("RotinaCalibragemRecusada", arquivo=str(destino), erros=erros,
                 ator=ator)
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    E.evento("RotinaCalibragemRegistrada", arquivo=str(destino),
             id=candidato.get("id"), responsavel=candidato.get("responsavel"),
             cadencia=candidato.get("cadencia"), versao=candidato.get("versao"),
             ator=ator)
    return None


def checar_calibragem_ref(candidato):
    ref = candidato.get("calibragem_ref")
    if not ref:
        return []
    alvo = DIRETORIO_CALIBRAGEM / f"{ref}.yaml"
    if not alvo.exists():
        return [f"calibragem_ref '{ref}' nao resolve — {alvo} nao existe"]
    return []


def checar_drift(candidato):
    """Ciclo sem drift e caminho positivo legitimo (secao 33 do pacote):
    drift_detectado=False nao exige recomendacao/decisao. Se
    drift_detectado=True, o agente pode descrever e quantificar e
    recomendar, mas a decisao final e sempre humana.
    """
    if not candidato.get("drift_detectado"):
        return []
    erros = []
    if not str(candidato.get("drift_descricao") or "").strip():
        erros.append("drift_detectado=true exige 'drift_descricao' preenchida")
    return erros


def checar_decisao(candidato, ator):
    """A decisao de recalibrar, expandir ou descontinuar e humana (CAM-01
    3.6, CAT-01 3.4.5). O agente pode preparar recomendacao; nunca pode
    gravar 'decisao'. Um ciclo pode legitimamente nao ter decisao ainda
    (drift detectado, decisao pendente) -- isso nao e tratado como
    resolvido automaticamente (secao 34 do pacote).
    """
    decisao = candidato.get("decisao")
    if not decisao:
        return []
    erros = []
    if decisao not in DECISOES_VALIDAS:
        erros.append(f"decisao '{decisao}' invalida, esperado um de "
                     f"{DECISOES_VALIDAS}")
    if E.autor_e_agente(ator):
        erros.append("agente nao pode decidir recalibragem: a decisao de "
                     "recalibrar, expandir ou descontinuar exige ator humano "
                     "nomeado, nunca agente (CAM-01 3.6, CAT-01 3.4.5).")
    elif not _ator_pessoa_nomeada(ator):
        erros.append(f"decisao de recalibragem exige pessoa nomeada; "
                     f"'{ator}' nao satisfaz")
    for campo in ("decisor", "data_decisao", "justificativa_decisao"):
        if not str(candidato.get(campo) or "").strip():
            erros.append(f"decisao preenchida exige '{campo}' preenchido")
    if candidato.get("decisor") and E.autor_e_agente(candidato.get("decisor")):
        erros.append("'decisor' nao pode ser agente")
    return erros


def checar_ciclo_existente(destino, candidato):
    """Um ciclo pendente (drift detectado, decisao ainda nao registrada)
    pode ser complementado com a decisao humana sem trocar de
    identificador -- e o mesmo evento de verificacao, so que em duas
    fases. O que nao pode acontecer e sobrescrever um ciclo ja decidido,
    nem reescrever os fatos do drift depois que a decisao foi tomada
    (secao 32 do pacote: ciclos anteriores nao sao sobrescritos
    silenciosamente). Um ciclo *sem* drift ja nasce completo -- reescreve-lo
    tambem seria sobrescrita indevida.
    """
    if not destino.exists():
        return []
    try:
        anterior = X.carregar_yaml(destino.read_text(encoding="utf-8"))
    except (X.ErroYaml, ValueError) as erro:
        return [f"ciclo existente esta ilegivel: {erro}"]

    if anterior.get("decisao"):
        return [f"ciclo {destino.name} ja possui decisao registrada -- "
                f"ciclos decididos nao sao sobrescritos, use um novo "
                f"identificador de ciclo"]
    if not anterior.get("drift_detectado"):
        return [f"ciclo {destino.name} ja registrado sem drift -- "
                f"ciclos anteriores nao sao sobrescritos, use um novo "
                f"identificador de ciclo"]
    for campo in ("drift_descricao", "drift_quantificacao"):
        if anterior.get(campo) and candidato.get(campo) != anterior.get(campo):
            return [f"ciclo {destino.name}: '{campo}' nao pode ser alterado "
                    f"depois de registrado -- os fatos do drift ja detectado "
                    f"nao mudam quando a decisao e complementada"]
    return []


def gravar_ciclo(destino, ator, schema_caminho="registro/calibragem.schema.json"):
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, "ciclo_calibragem")
    erros += checar_autoria_ciclo(candidato)
    erros += checar_calibragem_ref(candidato)
    erros += checar_drift(candidato)
    erros += checar_decisao(candidato, ator)
    erros += checar_ciclo_existente(destino, candidato)

    if erros:
        E.evento("CicloCalibragemRecusado", arquivo=str(destino), erros=erros,
                 ator=ator)
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    evento_tipo = "DecisaoRecalibragemRegistrada" if candidato.get("decisao") \
        else "CicloCalibragemRegistrado"
    E.evento(evento_tipo, arquivo=str(destino), id=candidato.get("id"),
             ciclo=candidato.get("ciclo"), drift_detectado=candidato.get("drift_detectado"),
             decisao=candidato.get("decisao"), ator=ator)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True,
                     help="destino em registro/calibragem/<id>.yaml")
    ap.add_argument("--ator", required=True)
    ap.add_argument("--schema", default="registro/calibragem.schema.json")
    ap.add_argument("--ciclo", action="store_true",
                     help="grava um ciclo (ciclo_calibragem) em vez da rotina")
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("registro/calibragem/"):
        print("calibragem so grava dentro de registro/calibragem/", file=sys.stderr)
        sys.exit(1)

    if a.ciclo:
        erro = gravar_ciclo(destino, a.ator, schema_caminho=a.schema)
    else:
        erro = gravar_rotina(destino, a.ator, schema_caminho=a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"calibragem gravada: {a.arquivo}")


if __name__ == "__main__":
    main()
