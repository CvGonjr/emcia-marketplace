"""Maquina de etapas. Unico caminho de avanco.

Uso:
  python3 avancar.py --apurar-nivel <nivel> --autor "Nome" --eixos "<eixos declarados>"
  python3 avancar.py --encerrar P2 --autor "Nome"
  python3 avancar.py --registrar-campo <etapa> --campo <nome> --valor <valor> --autor "Nome"
  python3 avancar.py --registrar-sessao P3b --autor "Nome" --participantes "A, B"
  python3 avancar.py --registrar-recorrencia P10 --autor "Nome" --cadencia "trimestral" --responsavel "Nome"
  python3 avancar.py --satisfazer-inegociavel 2 --autor "Nome" --evidencia "caminho ou descricao"
  python3 avancar.py --emitir E2 --autor "Nome"

Recusas de apuração, campo e sessão produzem TentativaNegada; as demais produzem
RecusaMaquina ou RecusaEmissao,
com a acao tentada, o motivo e o estado relevante no momento da recusa —
recusa silenciosa nao e aceitavel aqui do mesmo jeito que nao e em guarda.py.
"""
import argparse, datetime, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P
import apuracao as A


class _RecusaSessao(str):
    """Recusa de sessão que deve produzir TentativaNegada."""


def _ator_valido(nome):
    """Pessoa nomeada: nao vazio, nao generico, nao agente.

    'equipe', 'area' e afins nao satisfazem responsavel_obrigatorio (ESP-01
    3.6, CAM-01 anexo D: "responsavel e pessoa, nao area"). O nucleo nao
    conhece o motivo metodologico; conhece apenas que um nome generico de
    coletivo nao e uma pessoa nomeada.
    """
    nome = (nome or "").strip()
    if not nome or E.autor_e_agente(nome):
        return False
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
    return nome.lower() not in genericos


def apurar_nivel(st, pb, nivel, autor, eixos):
    if nivel not in pb["niveis"]:
        return f"nivel '{nivel}' nao existe no playbook: {pb['niveis']}"
    calculado, conta, erro = A.calcular(pb, eixos)
    if erro:
        return erro
    if nivel != calculado:
        return f"{conta}; informado {nivel}"
    anterior = st.get("nivel")
    st["nivel"] = nivel
    st["camada_atual"] = P.camada(pb, st["etapa_atual"], nivel)
    if eixos:
        st["cumprimentos"].setdefault("F0", {})["eixos"] = eixos
    E.evento("NivelApurado", nivel=nivel, anterior=anterior, autor=autor, eixos=eixos)
    return None


def encerrar(st, pb, etapa_id, autor):
    et = P.etapa(pb, etapa_id)
    if not et:
        return f"etapa {etapa_id} nao existe no playbook"

    # A etapa so pode ser encerrada se for a etapa corrente do caso — sem
    # essa checagem, qualquer etapa declarada no playbook podia ser marcada
    # cumprida fora de ordem (2.6-BL12), inclusive pulando dependencias e
    # sessoes ainda nao satisfeitas de etapas intermediarias.
    if etapa_id != st["etapa_atual"]:
        return (f"{etapa_id} nao e a etapa corrente ({st['etapa_atual']}). "
                f"So a etapa corrente pode ser encerrada.")

    if etapa_id == "F0" and not st.get("nivel"):
        return ("F0 nao encerra sem o nivel apurado. A camada das etapas seguintes "
                "depende dele (CAT-01 3.6). Grave o nivel em registro/estado.json.")
    if st.get("nivel") and st["nivel"] not in pb["niveis"]:
        return f"nivel '{st['nivel']}' nao existe no playbook: {pb['niveis']}"
    cam = P.camada(pb, etapa_id, st.get("nivel"))
    if (pb["encerramento_por_camada"][cam]
            and not st["cumprimentos"].get(etapa_id, {}).get("sessao")):
        return _RecusaSessao(
            f"{etapa_id} | camada {cam} | nivel {st.get('nivel')} | "
            f"modalidade exigida: {et['modalidade']}; "
            "encerramento exige sessao registrada da propria etapa.")
    if et.get("delegavel") is False and not st["cumprimentos"].get(etapa_id, {}).get("sessao"):
        return (f"{etapa_id} e {et['modalidade']} e nao delegavel. "
                f"Registre a sessao antes de encerrar.")
    dep = et.get("depende_de")
    if dep and not st["cumprimentos"].get(dep, {}).get("cumprido"):
        return f"{etapa_id} depende de {dep}, ainda nao cumprida"
    selo_ok, motivo_selo = P.selo_apos_etapa(pb, etapa_id, E.eventos())
    if not selo_ok:
        return motivo_selo

    st["cumprimentos"].setdefault(etapa_id, {})
    st["cumprimentos"][etapa_id].update({"cumprido": True, "autor": autor})
    idx = [e["id"] for e in pb["etapas"]].index(etapa_id)
    if idx + 1 < len(pb["etapas"]):
        prox = pb["etapas"][idx + 1]
        st["etapa_atual"] = prox["id"]
        st["camada_atual"] = P.camada(pb, prox["id"], st.get("nivel"))
        st["modalidade_atual"] = prox["modalidade"]
    E.evento("EtapaEncerrada", etapa=etapa_id, autor=autor)
    return None


def registrar_sessao(st, etapa_id, autor, participantes):
    if etapa_id != st["etapa_atual"]:
        return _RecusaSessao(
            f"{etapa_id} nao e a etapa corrente ({st['etapa_atual']}). "
            "So a etapa corrente pode receber sessao.")
    if st["cumprimentos"].get(etapa_id, {}).get("cumprido"):
        return _RecusaSessao(f"{etapa_id} ja encerrada; sessao nao pode ser registrada.")
    st["cumprimentos"].setdefault(etapa_id, {})
    st["cumprimentos"][etapa_id]["sessao"] = {
        "autor": autor, "participantes": participantes
    }
    E.evento("SessaoDeCampoRegistrada", etapa=etapa_id, autor=autor,
             participantes=participantes)
    return None


def registrar_campo(st, pb, etapa_id, campo, valor, autor):
    et = P.etapa(pb, etapa_id)
    if not et:
        return f"etapa {etapa_id} nao existe no playbook"
    if etapa_id != st["etapa_atual"]:
        return f"{etapa_id} nao e a etapa corrente ({st['etapa_atual']})"
    if st["cumprimentos"].get(etapa_id, {}).get("cumprido"):
        return f"{etapa_id} ja encerrada; campo nao pode ser registrado"
    campos = et.get("campos_registraveis", {})
    if campo not in campos:
        return f"campo '{campo}' nao declarado para etapa {etapa_id}"
    if not isinstance(valor, str) or not valor.strip():
        return f"campo {campo} exige valor nao vazio"
    regra = campos[campo]
    if "valores" in regra and valor not in regra["valores"]:
        return f"campo {campo}: valor '{valor}' invalido; valores aceitos: {regra['valores']}"
    registro = st["cumprimentos"].setdefault(etapa_id, {})
    anterior = registro.get(campo)
    registro[campo] = valor
    E.evento("CampoRegistrado", etapa=etapa_id, campo=campo, valor=valor,
             anterior=anterior, autor=autor)
    return None


def registrar_recorrencia(st, pb, etapa_id, autor, cadencia, responsavel):
    """Etapa recorrente (playbook 'recorrente': true) nao desaparece apos o
    primeiro encerramento — cada novo ciclo atualiza 'ultima_verificacao'
    sem apagar o historico de ciclos anteriores (CAM-01 3.8, anexo D).

    O nucleo nao entende cadencia nem responsavel; apenas exige que ambos
    estejam presentes quando o playbook marcar a etapa como recorrente e
    cadencia_obrigatoria/responsavel_obrigatorio.
    """
    et = P.etapa(pb, etapa_id)
    if not et:
        return f"etapa {etapa_id} nao existe no playbook"
    if not et.get("recorrente"):
        return f"{etapa_id} nao e uma etapa recorrente no playbook"
    if not st["cumprimentos"].get(etapa_id, {}).get("cumprido"):
        return f"{etapa_id} precisa ser encerrada ao menos uma vez antes de registrar recorrencia"

    if et.get("cadencia_obrigatoria") and not (cadencia or "").strip():
        return f"{etapa_id} exige cadencia declarada para registrar recorrencia"
    if et.get("responsavel_obrigatorio") and not _ator_valido(responsavel):
        return (f"{etapa_id} exige responsavel nominal (pessoa nomeada, nao agente "
                f"nem area/equipe generica) para registrar recorrencia")

    registro = st["cumprimentos"].setdefault(etapa_id, {})
    ciclo = registro.setdefault("estado_recorrente", {"ciclo": 0, "historico": []})
    ciclo["ciclo"] += 1
    agora = datetime.datetime.now().isoformat(timespec="seconds")
    if ciclo.get("ultima_verificacao"):
        ciclo["historico"].append({
            "ciclo": ciclo["ciclo"] - 1,
            "verificado_em": ciclo["ultima_verificacao"],
            "responsavel": ciclo.get("responsavel"),
        })
    ciclo["ultima_verificacao"] = agora
    ciclo["cadencia"] = cadencia
    ciclo["responsavel"] = responsavel
    E.evento("RecorrenciaRegistrada", etapa=etapa_id, autor=autor,
             ciclo=ciclo["ciclo"], cadencia=cadencia, responsavel=responsavel)
    return None


def satisfazer_inegociavel(st, pb, n, autor, evidencia):
    """Caminho autorizado para satisfazer um item inegociavel.

    O baseline mostrou que uma flag manual (estado['inegociaveis'][n] = true)
    podia satisfazer o portao sem provar nada (2.6-BL26): nao havia caminho
    autorizado, so a gravacao direta do estado. Este e o unico caminho: exige
    evidencia nao vazia e autor pessoa nomeada, e o registro guarda id,
    evidencia, ator e timestamp — nao apenas um booleano.

    O nucleo nao valida a SEMANTICA da evidencia (se ela de fato prova
    baseline, termo de autonomia etc.) — isso e decisao humana/metodologica
    dos pacotes 2.6.2/2.6.3/2.6.5. O nucleo garante apenas que o registro
    de satisfacao existe, esta associado a um item real do playbook, tem
    evidencia declarada e autor humano.
    """
    item = next((i for i in pb["inegociaveis"] if str(i["n"]) == str(n)), None)
    if not item:
        return f"item inegociavel {n} nao existe no playbook"
    if not (evidencia or "").strip():
        return f"inegociavel {n} exige evidencia nao vazia para ser satisfeito"

    agora = datetime.datetime.now().isoformat(timespec="seconds")
    st.setdefault("inegociaveis", {})[str(n)] = {
        "satisfeito": True, "evidencia": evidencia, "autor": autor, "data": agora,
    }
    E.evento("InegociavelSatisfeito", n=n, item=item["item"], autor=autor,
             evidencia=evidencia)
    return None


def _avaliar_condicao(condicao, st):
    """Avalia uma condicao declarativa {campo, etapa, operador, valor}.

    O nucleo nao sabe o que 'classificacao_tecnologica' ou 'agente'
    significam; sabe ler o valor que o cumprimento da etapa registrou sob
    'campo' e comparar pelo operador declarado. Operador desconhecido e
    contrato invalido, nao condicao ignorada silenciosamente (2.6.0 28).
    """
    campo = condicao.get("campo")
    etapa_id = condicao.get("etapa")
    operador = condicao.get("operador")
    esperado = condicao.get("valor")
    if not campo or not etapa_id or not operador:
        return None, f"condicao declarativa incompleta: {condicao}"
    if operador not in P.CONDICAO_OPERADORES:
        return None, (f"condicao usa operador '{operador}' desconhecido pelo motor. "
                      f"Esperado um de {sorted(P.CONDICAO_OPERADORES)}.")
    valor = st.get("cumprimentos", {}).get(etapa_id, {}).get(campo)
    if operador == "igual":
        return valor == esperado, None
    if operador == "diferente":
        return valor != esperado, None
    # contem: valor pode ser string ou lista; ausencia do campo nao satisfaz
    if valor is None:
        return False, None
    if isinstance(valor, (list, tuple, set)):
        return esperado in valor, None
    return esperado in str(valor), None


NAO_APLICAVEL = "NAO_APLICAVEL"


def emitir(st, pb, ent_id, autor, materializar=None):
    """Avalia o portao de um entregavel e, se autorizado, registra a emissao.

    Devolve (None, None) quando autorizado, (NAO_APLICAVEL, motivo) quando a
    condicao declarativa do entregavel nao se aplica a este caso (isso nao e
    falha), ou (erro, None) quando negado. O nucleo nao sabe o que "E3-E" ou
    "condicao agentica" significam -- so avalia etapas do portao, a condicao
    declarativa {campo, etapa, operador, valor} e os registros estruturados
    de inegociavel ja gravados por satisfazer_inegociavel().

    O artefato e o comando de materializacao sao declarados no playbook.
    O arquivo esperado precisa existir e nao estar vazio. ``materializar``
    pode confirmar esse caminho, mas nao substitui a declaracao do caso.
    Toda emissao autorizada guarda arquivo, versao e autoria.
    """
    ent = next((d for d in pb.get("entregaveis", []) if d["id"] == ent_id), None)
    if not ent:
        return f"entregavel {ent_id} nao existe no playbook", None
    if ent.get("portao_pendente"):
        return (f"{ent_id} tem portao pendente de decisao no playbook. "
                f"Nao emita ate a pendencia ser resolvida."), None
    faltando = [e for e in ent["portao"]
                if not st["cumprimentos"].get(e, {}).get("cumprido")]
    if faltando:
        return f"{ent_id} exige as etapas {faltando} encerradas", None

    condicao = ent.get("condicao")
    if isinstance(condicao, dict):
        satisfeita, erro = _avaliar_condicao(condicao, st)
        if erro:
            return f"{ent_id}: {erro}", None
        if not satisfeita:
            return None, (f"{ent_id} nao aplicavel a este caso: condicao "
                          f"declarativa nao satisfeita "
                          f"({condicao.get('descricao', condicao)})")

    for n in ent.get("inegociavel", []):
        item = next(i for i in pb["inegociaveis"] if i["n"] == n)
        registro = st.get("inegociaveis", {}).get(str(n))
        if not registro or not isinstance(registro, dict) or not registro.get("satisfeito"):
            return f"{ent_id} bloqueado pelo item inegociavel {n}: {item['item']}", None
        if not (registro.get("evidencia") or "").strip() or not registro.get("autor"):
            return (f"{ent_id} bloqueado: registro do inegociavel {n} "
                    f"nao possui evidencia/autor rastreaveis"), None

    esperado = pathlib.Path(ent["artefato"])
    orientacao = (f"Artefato esperado: {ent['artefato']}. "
                  f"Use {ent['comando_materializacao']}.")
    caminho = pathlib.Path(materializar) if materializar is not None else esperado
    if caminho.resolve() != esperado.resolve():
        return f"{ent_id} bloqueado: materializacao diverge do playbook. {orientacao}", None
    if not esperado.resolve().is_relative_to(pathlib.Path.cwd().resolve()):
        return f"{ent_id} bloqueado: artefato fora do caso. {orientacao}", None
    if not caminho.is_file():
        return f"{ent_id} bloqueado: artefato nao existe como arquivo. {orientacao}", None
    try:
        conteudo = caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return f"{ent_id} bloqueado: artefato ilegivel ({exc}). {orientacao}", None
    if not conteudo.strip():
        return f"{ent_id} bloqueado: artefato esta vazio. {orientacao}", None
    arquivo = str(caminho.resolve())
    registro_emissao = st.setdefault("entregaveis_emitidos", {})
    anterior = registro_emissao.get(ent_id)
    versao = (anterior.get("versao") + 1) if anterior else 1
    registro_emissao[ent_id] = {
        "arquivo": arquivo, "versao": versao, "autor": autor,
    }

    E.evento("EntregavelEmitido", entregavel=ent_id, autor=autor,
             arquivo=arquivo, versao=versao)
    return None, None


def _recusar_operacao(st, autor, motivo, acao="apurar_nivel"):
    # A tentativa de agente é atribuída ao responsável nominal do caso;
    # identificadores de agente nunca entram como autor na trilha.
    responsavel = (st or {}).get("responsavel")
    pessoa = responsavel if _ator_valido(responsavel) else autor
    if not _ator_valido(pessoa):
        raise ValueError("recusa sem pessoa nomeada: caso precisa de responsavel nominal")
    E.evento("TentativaNegada", acao_tentada=acao, motivo=motivo,
             autor=pessoa, etapa_corrente=(st or {}).get("etapa_atual"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apurar-nivel")
    ap.add_argument("--encerrar"); ap.add_argument("--registrar-sessao")
    ap.add_argument("--registrar-recorrencia")
    ap.add_argument("--registrar-campo")
    ap.add_argument("--campo", default="")
    ap.add_argument("--valor", default="")
    ap.add_argument("--satisfazer-inegociavel")
    ap.add_argument("--emitir"); ap.add_argument("--autor", required=True)
    ap.add_argument("--participantes", default="")
    ap.add_argument("--eixos", default="")
    ap.add_argument("--cadencia", default="")
    ap.add_argument("--responsavel", default="")
    ap.add_argument("--evidencia", default="")
    ap.add_argument("--materializar", default=None,
                     help="caminho do artefato real ja renderizado pelo chamador")
    a = ap.parse_args()

    st = E.ler()
    try:
        pb, erro = P.carregar()
    except (ValueError, TypeError, KeyError) as exc:
        if not (a.apurar_nivel or a.registrar_campo):
            raise
        pb, erro = None, f"playbook invalido: {exc}"
    if not st or erro:
        if a.apurar_nivel or a.registrar_campo:
            _recusar_operacao(st, a.autor, erro or "nenhum caso aberto",
                             "registrar_campo" if a.registrar_campo else "apurar_nivel")
        elif a.encerrar or a.registrar_sessao or a.emitir:
            _recusar_operacao(st, a.autor, erro or "nenhum caso aberto",
                             "encerrar" if a.encerrar else ("registrar_sessao" if a.registrar_sessao else "emitir"))
        print(erro or "nenhum caso aberto", file=sys.stderr); sys.exit(1)
    if (a.apurar_nivel or a.registrar_campo) and not _ator_valido(a.autor):
        _recusar_operacao(st, a.autor, "autor precisa ser pessoa nomeada",
                         "registrar_campo" if a.registrar_campo else "apurar_nivel")
        print("autor precisa ser pessoa nomeada", file=sys.stderr); sys.exit(1)
    if E.autor_e_agente(a.autor):
        print("autor precisa ser pessoa nomeada", file=sys.stderr); sys.exit(1)

    if a.apurar_nivel:
        acao, alvo = "apurar_nivel", a.apurar_nivel
        err = apurar_nivel(st, pb, a.apurar_nivel, a.autor, a.eixos)
    elif a.registrar_campo:
        acao, alvo = "registrar_campo", a.registrar_campo
        err = registrar_campo(st, pb, a.registrar_campo, a.campo, a.valor, a.autor)
    elif a.registrar_sessao:
        acao, alvo = "registrar_sessao", a.registrar_sessao
        err = registrar_sessao(st, a.registrar_sessao, a.autor, a.participantes)
    elif a.registrar_recorrencia:
        acao, alvo = "registrar_recorrencia", a.registrar_recorrencia
        err = registrar_recorrencia(st, pb, a.registrar_recorrencia, a.autor,
                                     a.cadencia, a.responsavel)
    elif a.satisfazer_inegociavel:
        acao, alvo = "satisfazer_inegociavel", a.satisfazer_inegociavel
        err = satisfazer_inegociavel(st, pb, a.satisfazer_inegociavel, a.autor, a.evidencia)
    elif a.encerrar:
        acao, alvo = "encerrar", a.encerrar
        err = encerrar(st, pb, a.encerrar, a.autor)
    elif a.emitir:
        acao, alvo = "emitir", a.emitir
        err, nao_aplicavel = emitir(st, pb, a.emitir, a.autor,
                                     materializar=a.materializar)
        if nao_aplicavel:
            E.evento("EntregavelNaoAplicavel", entregavel=a.emitir, motivo=nao_aplicavel,
                     autor=a.autor)
            print(f"NAO_APLICAVEL | {nao_aplicavel}")
            sys.exit(0)
    else:
        print("nada a fazer", file=sys.stderr); sys.exit(1)

    if err:
        if a.apurar_nivel or a.registrar_campo or isinstance(err, _RecusaSessao):
            _recusar_operacao(st, a.autor, err, acao)
            print(err, file=sys.stderr); sys.exit(1)
        tipo_evento = "RecusaEmissao" if acao == "emitir" else "RecusaMaquina"
        E.evento(tipo_evento, acao_tentada=acao, alvo=alvo, motivo=err,
                 autor=a.autor, etapa_corrente=st.get("etapa_atual"))
        print(err, file=sys.stderr); sys.exit(1)
    E.gravar(st)
    print(f"ok | etapa atual: {st['etapa_atual']} | camada: {st.get('camada_atual')}")


if __name__ == "__main__":
    main()
