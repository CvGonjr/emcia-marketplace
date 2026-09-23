"""Maquina de etapas. Unico caminho de avanco.

Uso:
  python3 avancar.py --apurar-nivel N2 --autor "Nome" --eixos "DAD 4, GOV 5, CRI 7"
  python3 avancar.py --encerrar P2 --autor "Nome"
  python3 avancar.py --registrar-sessao P3b --autor "Nome" --participantes "A, B"
  python3 avancar.py --registrar-recorrencia P10 --autor "Nome" --cadencia "trimestral" --responsavel "Nome"
  python3 avancar.py --satisfazer-inegociavel 2 --autor "Nome" --evidencia "caminho ou descricao"
  python3 avancar.py --emitir E2 --autor "Nome"

Toda recusa desta maquina produz evento RecusaMaquina ou RecusaEmissao,
com a acao tentada, o motivo e o estado relevante no momento da recusa —
recusa silenciosa nao e aceitavel aqui do mesmo jeito que nao e em guarda.py.
"""
import argparse, datetime, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P


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
    st["cumprimentos"].setdefault(etapa_id, {})
    st["cumprimentos"][etapa_id]["sessao"] = {
        "autor": autor, "participantes": participantes
    }
    E.evento("SessaoDeCampoRegistrada", etapa=etapa_id, autor=autor,
             participantes=participantes)
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

    ``materializar``, quando informado, e o caminho de um arquivo que o
    chamador (eiac-campo) ja renderizou a partir do conteudo real do caso.
    O nucleo nao sabe gerar esse conteudo -- so recusa registrar a emissao
    se o arquivo nao existir ou estiver vazio, para que 'EntregavelEmitido'
    nunca aponte para um documento que nao existe (2.6.5, D-12).
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

    arquivo, versao = None, None
    if materializar is not None:
        caminho = pathlib.Path(materializar)
        if not caminho.exists():
            return (f"{ent_id} bloqueado: materializacao '{materializar}' "
                    f"nao existe. Emissao sem artefato real nao e emissao "
                    f"conforme (2.6.5, D-12)."), None
        conteudo = caminho.read_text(encoding="utf-8")
        if not conteudo.strip():
            return (f"{ent_id} bloqueado: materializacao '{materializar}' "
                    f"esta vazia."), None
        arquivo = str(caminho)
        registro_emissao = st.setdefault("entregaveis_emitidos", {})
        anterior = registro_emissao.get(ent_id)
        versao = (anterior.get("versao") + 1) if anterior else 1
        registro_emissao[ent_id] = {
            "arquivo": arquivo, "versao": versao, "autor": autor,
        }

    E.evento("EntregavelEmitido", entregavel=ent_id, autor=autor,
             arquivo=arquivo, versao=versao)
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apurar-nivel")
    ap.add_argument("--encerrar"); ap.add_argument("--registrar-sessao")
    ap.add_argument("--registrar-recorrencia")
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
    pb, erro = P.carregar()
    if not st or erro:
        print(erro or "nenhum caso aberto", file=sys.stderr); sys.exit(1)
    if E.autor_e_agente(a.autor):
        print("autor precisa ser pessoa nomeada", file=sys.stderr); sys.exit(1)

    if a.apurar_nivel:
        acao, alvo = "apurar_nivel", a.apurar_nivel
        err = apurar_nivel(st, pb, a.apurar_nivel, a.autor, a.eixos)
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
        tipo_evento = "RecusaEmissao" if acao == "emitir" else "RecusaMaquina"
        E.evento(tipo_evento, acao_tentada=acao, alvo=alvo, motivo=err,
                 autor=a.autor, etapa_corrente=st.get("etapa_atual"))
        print(err, file=sys.stderr); sys.exit(1)
    E.gravar(st)
    print(f"ok | etapa atual: {st['etapa_atual']} | camada: {st.get('camada_atual')}")


if __name__ == "__main__":
    main()
