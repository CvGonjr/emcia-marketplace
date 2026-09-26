"""Carrega e valida o playbook do caso. Nao conhece nenhum metodo em particular."""
import json, pathlib, sys

OBRIGATORIO_ETAPA = {"id", "camada", "modalidade"}
OBRIGATORIO_ENTREGAVEL = {"id", "portao", "artefato", "comando_materializacao"}

# Operadores que o motor generico de condicoes declarativas (avancar.py)
# sabe avaliar. Um portao com operador fora deste conjunto e contrato
# invalido, nao condicao ignorada silenciosamente (2.6.0 secao 28).
CAMPOS_RESERVADOS = {"cumprido", "autor", "sessao", "eixos", "estado_recorrente"}

CONDICAO_OPERADORES = {"contem", "igual", "diferente"}


def carregar():
    p = pathlib.Path("registro/playbook.json")
    if not p.exists():
        return None, "registro/playbook.json ausente"
    pb = json.loads(p.read_text(encoding="utf-8"))

    niveis = pb.get("niveis")
    if not niveis:
        return None, "playbook sem lista de niveis"
    if not pb.get("etapas"):
        return None, "playbook sem etapas"

    ids_etapa = [e.get("id") for e in pb["etapas"]]
    if len(ids_etapa) != len(set(ids_etapa)):
        return None, "playbook com id de etapa duplicado"

    for e in pb["etapas"]:
        faltando = OBRIGATORIO_ETAPA - set(e)
        if faltando:
            return None, f"etapa {e.get('id','?')} sem {sorted(faltando)}"
        c = e["camada"]
        if not isinstance(c, dict):
            return None, (f"etapa {e['id']}: camada precisa ser um mapa por nivel. "
                          f"A fronteira de delegacao desloca com o nivel (CAT-01 3.6).")
        faltam = [n for n in niveis if n not in c]
        if faltam:
            return None, f"etapa {e['id']}: camada nao declarada para {faltam}"
        for cam in c.values():
            if cam not in ("EX1", "EX2", "EX3", "EX4"):
                return None, f"etapa {e['id']}: camada '{cam}' fora de EX1-EX4"
        campos = e.get("campos_registraveis", {})
        if not isinstance(campos, dict):
            return None, f"etapa {e['id']}: campos_registraveis precisa ser objeto"
        for nome, regra in campos.items():
            if nome in CAMPOS_RESERVADOS:
                return None, f"etapa {e['id']}: campo reservado '{nome}'"
            if not isinstance(nome, str) or not nome.strip() or not isinstance(regra, dict):
                return None, f"etapa {e['id']}: declaracao de campo invalida"
            if set(regra) - {"valores"}:
                return None, f"etapa {e['id']}: regra de campo desconhecida em {nome}"
            if "valores" in regra:
                valores_campo = regra["valores"]
                if (not isinstance(valores_campo, list) or not valores_campo
                        or any(not isinstance(v, str) or not v.strip() for v in valores_campo)
                        or len(valores_campo) != len(set(valores_campo))):
                    return None, f"etapa {e['id']}: valores invalidos para campo {nome}"
        dep = e.get("depende_de")
        if dep and dep not in ids_etapa:
            return None, f"etapa {e['id']}: depende de etapa inexistente '{dep}'"
        if e.get("recorrente") and not (e.get("cadencia_obrigatoria") and e.get("responsavel_obrigatorio")):
            return None, (f"etapa {e['id']}: recorrente exige cadencia e responsavel "
                          f"declarados, senao a etapa desaparece apos a primeira execucao.")

    sessoes = pb.get("encerramento_por_camada")
    if not isinstance(sessoes, dict):
        return None, "playbook sem encerramento_por_camada valido"
    for et in pb["etapas"]:
        for cam in et["camada"].values():
            if type(sessoes.get(cam)) is not bool:
                return None, f"encerramento_por_camada: {cam} precisa declarar booleano"

    for d in pb.get("entregaveis", []):
        faltando = OBRIGATORIO_ENTREGAVEL - set(d)
        if faltando:
            return None, f"entregavel {d.get('id','?')} sem {sorted(faltando)}"
        artefato = d["artefato"]
        if (not isinstance(artefato, str) or not artefato.strip()
                or pathlib.Path(artefato).is_absolute()
                or ".." in pathlib.Path(artefato).parts):
            return None, f"entregavel {d['id']}: artefato precisa ser caminho relativo dentro do caso"
        if not isinstance(d["comando_materializacao"], str) or not d["comando_materializacao"].strip():
            return None, f"entregavel {d['id']}: comando_materializacao precisa ser declarado"
        orfas = [p for p in d["portao"] if p not in ids_etapa]
        if orfas:
            return None, f"entregavel {d['id']}: portao referencia etapa inexistente {orfas}"
        condicao = d.get("condicao")
        if condicao is not None:
            if not isinstance(condicao, dict):
                return None, f"entregavel {d['id']}: condicao precisa ser um objeto declarativo"
            faltando_cond = {"campo", "etapa", "operador"} - set(condicao)
            if faltando_cond:
                return None, f"entregavel {d['id']}: condicao sem {sorted(faltando_cond)}"
            if condicao["etapa"] not in ids_etapa:
                return None, (f"entregavel {d['id']}: condicao referencia etapa "
                              f"inexistente '{condicao['etapa']}'")
            if condicao["operador"] not in CONDICAO_OPERADORES:
                return None, (f"entregavel {d['id']}: condicao usa operador "
                              f"'{condicao['operador']}' desconhecido pelo motor. "
                              f"Esperado um de {sorted(CONDICAO_OPERADORES)}.")

    if not pb.get("inegociaveis"):
        return None, "playbook sem itens inegociaveis"
    for item in pb["inegociaveis"]:
        passo = item.get("passo")
        if passo and passo not in ids_etapa:
            return None, f"inegociavel {item.get('n','?')}: passo referencia etapa inexistente '{passo}'"
    for d in pb.get("entregaveis", []):
        for n in d.get("inegociavel", []):
            if not any(i["n"] == n for i in pb["inegociaveis"]):
                return None, f"entregavel {d['id']}: referencia inegociavel inexistente {n}"
    procedencia = pb.get("procedencia", {})
    valores = procedencia.get("valores")
    rotulos = procedencia.get("rotulos")
    if not isinstance(valores, list) or not valores:
        return None, "playbook sem valores de procedencia"
    if len(valores) != len(set(valores)):
        return None, "playbook com valores de procedencia duplicados"
    if not isinstance(rotulos, dict) or set(rotulos) != set(valores):
        return None, "rotulos de procedencia nao correspondem aos valores declarados"
    return pb, None


def etapa(pb, etapa_id):
    for e in pb["etapas"]:
        if e["id"] == etapa_id:
            return e
    return None


def camada(pb, etapa_id, nivel):
    """Camada de execucao da etapa, resolvida pelo nivel do caso.

    Sem nivel definido, aplica a mais restritiva declarada — nao se assume
    o nivel mais permissivo enquanto a triagem nao apurou.
    """
    e = etapa(pb, etapa_id)
    if not e:
        return None
    c = e["camada"]
    if nivel and nivel in c:
        return c[nivel]
    ordem = ["EX1", "EX2", "EX3", "EX4"]
    return max(c.values(), key=lambda x: ordem.index(x) if x in ordem else 99)


HUMANA = ("EX3", "EX4")


def humana(cam):
    """A camada exige pessoa? A guarda ja aplica esta regra em G1."""
    return cam in HUMANA


def natureza(pb, etapa_id, nivel):
    """Como esta etapa se comporta para este nivel, em uma linha."""
    e = etapa(pb, etapa_id)
    if not e:
        return "?"
    if e.get("delegavel") is False:
        return "nao delegavel"
    return "exige verificacao humana" if humana(camada(pb, etapa_id, nivel)) \
        else "preparacao delegavel"


def capacidade_valida(capacidade):
    """Mecanismo generico de criterio de verificacao (ESP-01 G6).

    Recebe um dict {automatizado: bool, criterio_de_verificacao: str|None,
    ...} e devolve (True, None) ou (False, motivo). Nao sabe o que e HB,
    AG ou qualquer semantica EMCIA — so aplica a regra "capacidade
    automatizada sem criterio de verificacao nao e valida para carregamento".

    A integracao com as 18 HB e 4 AG reais, estruturados no playbook
    oficial, pertence ao pacote 2.6.4. Este pacote (2.6.1) so constroi e
    testa o mecanismo, isolado de qualquer contrato concreto.
    """
    if not isinstance(capacidade, dict):
        return False, "capacidade precisa ser um objeto com 'automatizado' e 'criterio_de_verificacao'"
    if not capacidade.get("automatizado"):
        return True, None
    criterio = capacidade.get("criterio_de_verificacao")
    if not (isinstance(criterio, str) and criterio.strip()):
        return False, (
            "capacidade automatizada sem criterio_de_verificacao nao e valida "
            "para carregamento/execucao"
        )
    return True, None


def selo_apos_etapa(pb, etapa_id, trilha):
    """Verifica a exigencia declarativa 'exige_selo_apos' de uma etapa.

    Uma etapa pode declarar {"exige_selo_apos": "<outro-id-de-etapa>"} no
    playbook. Quando declarada, essa etapa (abrir ou encerrar) exige um
    evento SeloAplicado posterior ao EtapaEncerrada da etapa referenciada.
    O nucleo nao sabe por que -- so compara a ORDEM de dois tipos de evento
    genericos contra um campo declarativo do contrato, do mesmo jeito que
    _avaliar_condicao() em avancar.py compara campo/etapa/valor sem saber
    o que "P2" ou "P3b" significam.

    "Posterior" e definido pela POSICAO do evento na trilha (a ordem em
    que estado.evento() gravou cada linha), nao pelo campo `data`: dois
    eventos podem cair no mesmo segundo (timespec="seconds" em
    estado.evento()) quando o percurso e rapido -- um comando de teste ou
    um script automatizado emite varios eventos no mesmo segundo com
    frequencia. Comparar por timestamp ali produziria falso negativo
    (selo real, no lugar certo, recusado por empate de relogio). A ordem
    de gravacao e o unico ordenador confiavel dessa trilha.

    Devolve (True, None) quando a exigencia nao existe ou esta satisfeita;
    (False, motivo) quando a etapa referenciada ainda nao foi encerrada, ou
    quando nao ha selo posterior a esse encerramento.

    ``trilha`` e a lista de eventos ja lida (estado.eventos()) -- esta
    funcao nao le arquivo, para permanecer pura e testavel sem tocar disco.
    """
    et = etapa(pb, etapa_id)
    if not et:
        return True, None
    referencia = et.get("exige_selo_apos")
    if not referencia:
        return True, None

    posicoes_encerramento = [i for i, e in enumerate(trilha)
                              if e.get("evento") == "EtapaEncerrada" and e.get("etapa") == referencia]
    if not posicoes_encerramento:
        return False, (f"{etapa_id} exige selo posterior ao encerramento de "
                        f"{referencia}, mas {referencia} ainda nao foi encerrada.")
    ultima_posicao_encerramento = max(posicoes_encerramento)

    posicoes_selo = [i for i, e in enumerate(trilha) if e.get("evento") == "SeloAplicado"]
    selo_posterior = any(i > ultima_posicao_encerramento for i in posicoes_selo)
    if not selo_posterior:
        return False, (f"{etapa_id} exige selo posterior ao encerramento de "
                        f"{referencia}. Nenhum SeloAplicado encontrado depois "
                        f"desse encerramento -- sele o caso antes de prosseguir.")
    return True, None


def proxima_fronteira(pb, etapa_id, nivel):
    """Primeira etapa daqui em diante que exige pessoa. None se nao houver.

    Devolve (id, camada, motivo) da etapa, ou None se a etapa corrente ja
    exigir pessoa — nesse caso nao ha fronteira a anunciar, ela ja chegou.
    """
    ids = [e["id"] for e in pb["etapas"]]
    if etapa_id not in ids:
        return None
    if humana(camada(pb, etapa_id, nivel)) or (etapa(pb, etapa_id) or {}).get("delegavel") is False:
        return None
    for e in pb["etapas"][ids.index(etapa_id) + 1:]:
        cam = camada(pb, e["id"], nivel)
        if e.get("delegavel") is False:
            return e["id"], cam, "nao delegavel"
        if humana(cam):
            return e["id"], cam, "exige verificacao humana"
    return None


if __name__ == "__main__":
    pb, erro = carregar()
    if erro:
        print(erro, file=sys.stderr); sys.exit(1)
    print(f"playbook '{pb.get('nome','?')}' v{pb.get('versao','?')} valido: "
          f"{len(pb['etapas'])} etapas, {len(pb.get('entregaveis', []))} entregaveis, "
          f"{len(pb['inegociaveis'])} itens inegociaveis, "
          f"niveis {pb['niveis']}")
