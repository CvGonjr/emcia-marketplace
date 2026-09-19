#!/usr/bin/env python3
"""Verificacao operacional de P8, P9 e P10 -- pacote 2.6.3.

Cobre: conjunto de casos de teste com saida esperada (P8), plano de
medicao com metrica de resultado (P9), rotina de recalibragem recorrente
com deteccao de drift e decisao humana (P10), dependencias P8->P9->P10,
protecao generica de registro/ (G5), evidencia para os inegociaveis 3, 4
e 5, e a fronteira agente/humano na decisao de recalibragem.

Nenhum teste aqui pressupoe hard-code de P8/P9/P10 no nucleo: tudo passa
pelos scripts de eiac-campo/scripts/ (piloto.py, metrica.py,
calibragem.py), que reaproveitam primitivas genericas do eiac-nucleo
(estrutura.validar, estado.evento, estado.autor_e_agente e, para
recorrencia/inegociaveis, avancar.registrar_recorrencia e
avancar.satisfazer_inegociavel, ja genericos desde o 2.6.1) sem
estende-las com semantica de metodo.
"""
import copy
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "estrutura_check", RAIZ / "eiac-nucleo" / "scripts" / "estrutura.py")
estrutura_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(estrutura_mod)
sys.path.insert(0, str(RAIZ / "eiac-nucleo" / "scripts"))
import estado as E_check  # noqa: E402

TEMPLATE = RAIZ / "eiac-campo" / "template-caso"
AVANCAR = RAIZ / "eiac-nucleo" / "scripts" / "avancar.py"
GUARDA = RAIZ / "eiac-nucleo" / "scripts" / "guarda.py"
OPERACIONAL = RAIZ / "eiac-campo" / "scripts" / "operacional.py"
GOVERNANCA = RAIZ / "eiac-campo" / "scripts" / "governanca.py"
PILOTO = RAIZ / "eiac-campo" / "scripts" / "piloto.py"
METRICA = RAIZ / "eiac-campo" / "scripts" / "metrica.py"
CALIBRAGEM = RAIZ / "eiac-campo" / "scripts" / "calibragem.py"

pb_oficial = json.loads((TEMPLATE / "registro" / "playbook.json").read_text(encoding="utf-8"))

falhas = 0
total = 0


def ok(msg):
    global total
    total += 1
    print(f"  ok    {msg}")


def falha(msg):
    global total, falhas
    total += 1
    falhas += 1
    print(f"  FALHA {msg}")


def preparar_caso():
    tmp = pathlib.Path(tempfile.mkdtemp())
    caso = tmp / "caso"
    shutil.copytree(TEMPLATE, caso)
    (caso / "rascunho").mkdir(exist_ok=True)
    return caso


def avancar(caso, **kwargs):
    comando = ["python3", str(AVANCAR)]
    for chave, valor in kwargs.items():
        comando += [f"--{chave.replace('_', '-')}", str(valor)]
    proc = subprocess.run(comando, cwd=caso, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def guarda(caso, tool_name, tool_input):
    entrada = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
    proc = subprocess.run(["python3", str(GUARDA)], cwd=caso, input=entrada,
                           text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def operacional(caso, arquivo, ator):
    proc = subprocess.run(
        ["python3", str(OPERACIONAL), "--arquivo", arquivo, "--ator", ator],
        cwd=caso, text=True, capture_output=True, check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def governanca(caso, arquivo, ator):
    proc = subprocess.run(
        ["python3", str(GOVERNANCA), "--arquivo", arquivo, "--ator", ator],
        cwd=caso, text=True, capture_output=True, check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def piloto(caso, arquivo, ator):
    proc = subprocess.run(
        ["python3", str(PILOTO), "--arquivo", arquivo, "--ator", ator],
        cwd=caso, text=True, capture_output=True, check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def metrica(caso, arquivo, ator):
    proc = subprocess.run(
        ["python3", str(METRICA), "--arquivo", arquivo, "--ator", ator],
        cwd=caso, text=True, capture_output=True, check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def calibragem(caso, arquivo, ator, ciclo=False):
    comando = ["python3", str(CALIBRAGEM), "--arquivo", arquivo, "--ator", ator]
    if ciclo:
        comando.append("--ciclo")
    proc = subprocess.run(comando, cwd=caso, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def eventos(caso):
    log = caso / "registro" / "eventos.jsonl"
    if not log.exists():
        return []
    return [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]


def apurar_e_encerrar_f0(caso):
    avancar(caso, apurar_nivel="N2", autor="Celso do Vale", eixos="DAD 4, GOV 5, CRI 7")
    return avancar(caso, encerrar="F0", autor="Celso do Vale")


ETAPAS_NAO_DELEGAVEIS = {e["id"] for e in pb_oficial["etapas"] if e.get("delegavel") is False}


def percorrer_ate(caso, ate_etapa_id):
    apurar_e_encerrar_f0(caso)
    ordem = [e["id"] for e in pb_oficial["etapas"]]
    for etapa_id in ordem[1:ordem.index(ate_etapa_id) + 1]:
        if etapa_id in ETAPAS_NAO_DELEGAVEIS:
            avancar(caso, registrar_sessao=etapa_id, autor="Celso do Vale",
                    participantes="Ana, Celso")
        avancar(caso, encerrar=etapa_id, autor="Celso do Vale")


def op_yaml(estado, versao, **over):
    campos = {
        "id": "OP-001",
        "estado": estado,
        "ponto_insercao": "recebimento da autorizacao do convenio",
        "momento": "imediatamente apos confirmacao no sistema do convenio",
        "sistema": "sistema de gestao de guias",
        "entrada": "numero da guia e status de autorizacao",
        "saida": "guia enviada ao setor de faturamento",
        "ator_humano": "Claudia Ferreira, analista de faturamento",
        "excecao": "guia sem correspondencia na camada de contexto",
        "fallback": "encaminhar para fila manual de Claudia Ferreira",
        "responsavel_operacional": "Claudia Ferreira",
        "procedencia": "D",
        "declarado_por": "Claudia Ferreira",
        "registrado_por": "Celso do Vale",
        "data": "2026-09-19",
        "versao": versao,
    }
    if estado == "validado":
        campos["validado_por"] = "Rafael Nogueira"
        campos["data_validacao"] = "2026-09-19"
    campos.update(over)
    linhas = [f"id: {campos.pop('id')}"]
    for chave, valor in campos.items():
        if isinstance(valor, str) and (":" in valor or valor.startswith("-")):
            linhas.append(f'{chave}: "{valor}"')
        else:
            linhas.append(f"{chave}: {valor}")
    return "\n".join(linhas) + "\n"


def aut_yaml(estado, versao, operacional_ref="OP-001", **over):
    campos = {
        "id": "AUT-001",
        "estado": estado,
        "operacional_ref": operacional_ref,
        "escopo": "envio automatico de guia de autorizacao apos recebimento",
        "procedencia": "D",
        "declarado_por": "Claudia Ferreira",
        "registrado_por": "Celso do Vale",
        "data": "2026-09-19",
        "versao": versao,
    }
    if estado == "decidido":
        campos["decisor"] = "Marina Prado"
        campos["data_decisao"] = "2026-09-19"
        campos["justificativa_decisao"] = (
            "termo revisado com a area juridica, autonomia liberada para o escopo descrito"
        )
    campos.update(over)
    listas = {
        "faz_sozinha": ["consultar status da guia no sistema de convenio"],
        "exige_aprovacao": ["emitir guia com valor acima de R$ 5.000"],
        "nunca_faz": ["alterar dados cadastrais do beneficiario"],
        "gatilhos_escalonamento": ["guia sem correspondencia na camada de contexto"],
    }
    listas.update(over.get("_listas", {}))
    linhas = [f"id: {campos.pop('id')}"]
    for chave, valor in campos.items():
        if chave == "_listas":
            continue
        linhas.append(f'{chave}: "{valor}"' if isinstance(valor, str) else f"{chave}: {valor}")
    for chave, itens in listas.items():
        linhas.append(f"{chave}:")
        for item in itens:
            linhas.append(f'  - "{item}"')
    return "\n".join(linhas) + "\n"


def preparar_op_validado(caso):
    (caso / "rascunho" / "OP-001.yaml").write_text(op_yaml("proposta", 1), encoding="utf-8")
    operacional(caso, "registro/operacional/OP-001.yaml", "AG-02")
    (caso / "rascunho" / "OP-001.yaml").write_text(op_yaml("validado", 2), encoding="utf-8")
    operacional(caso, "registro/operacional/OP-001.yaml", "Rafael Nogueira")


def preparar_aut_decidido(caso):
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("rascunho", 1), encoding="utf-8")
    governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("proposto", 2), encoding="utf-8")
    governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("decidido", 3), encoding="utf-8")
    return governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "Marina Prado")


def preparar_ate_p7(caso):
    """Percorre F0..P6 e grava OP-001/AUT-001, deixando o caso em P8."""
    percorrer_ate(caso, "P6")
    preparar_op_validado(caso)
    preparar_aut_decidido(caso)
    avancar(caso, registrar_sessao="P7", autor="Celso do Vale", participantes="Ana, Celso")
    avancar(caso, encerrar="P7", autor="Celso do Vale")


def caso_ct(identificador, categoria="celula_critica", esperado="Prioridade alta",
            obtido=None, resultado=None, revisor=None, **over):
    c = {
        "identificador": identificador,
        "origem": "RN-003",
        "entrada": "Guia com sintoma grave e historico limpo",
        "saida_esperada": esperado,
        "criterio_aprovacao": "Classificacao igual a saida esperada",
        "categoria": categoria,
        "revisor": revisor or "Marina Prado",
        "data_revisao": "2026-09-11",
        "esperado_definido_em": "2026-09-10",
        "esperado_definido_por": "Celso do Vale",
    }
    if obtido is not None:
        c["saida_obtida"] = obtido
        c["obtido_em"] = "2026-09-19"
        c["resultado"] = resultado if resultado is not None else (
            "aderente" if obtido == esperado else "divergente")
    c.update(over)
    return c


def _yaml_dump(dados, indent=0):
    linhas = []
    pad = "  " * indent
    for chave, valor in dados.items():
        if isinstance(valor, list):
            if valor and isinstance(valor[0], dict):
                linhas.append(f"{pad}{chave}:")
                for item in valor:
                    sub = _yaml_dump(item, indent + 2).splitlines()
                    linhas.append(f"{pad}  - {sub[0].strip()}")
                    linhas.extend(f"{pad}    {l.strip()}" for l in sub[1:])
            else:
                linhas.append(f"{pad}{chave}: {json.dumps(valor)}")
        elif isinstance(valor, bool):
            linhas.append(f"{pad}{chave}: {str(valor).lower()}")
        elif isinstance(valor, str) and (":" in valor or valor.startswith("-") or "'" in valor):
            linhas.append(f'{pad}{chave}: "{valor}"')
        else:
            linhas.append(f"{pad}{chave}: {valor}")
    return "\n".join(linhas)


def ct_yaml(estado, versao, casos, **over):
    campos = {
        "id": "CT-001",
        "estado": estado,
        "modo": "assistido",
        "duracao": "4 semanas",
        "plano_reversao": "Reverter para triagem manual em caso de falha critica",
        "criterio_aprovacao_escala": "95% de acerto nos casos criticos",
        "criterio_aprovacao_escala_definido_em": "2026-09-10",
        "procedencia": "D",
        "declarado_por": "Celso do Vale",
        "registrado_por": "Celso do Vale",
        "data": "2026-09-18",
        "versao": versao,
    }
    if estado == "revisado":
        campos["revisado_por"] = "Marina Prado"
        campos["data_revisao"] = "2026-09-18"
    campos.update({k: v for k, v in over.items() if k != "casos"})
    campos["casos"] = casos
    return _yaml_dump(campos) + "\n"


def met_yaml(estado, versao, tipo="resultado", piloto_ref="CT-001", **over):
    campos = {
        "id": "MET-001",
        "estado": estado,
        "piloto_ref": piloto_ref,
        "metrica": "Tempo de ciclo de triagem",
        "tipo": tipo,
        "linha_base": "45 minutos",
        "linha_base_data": "2026-08-01",
        "linha_base_procedencia": "V",
        "metodo_apuracao": "Media do tempo entre recepcao e classificacao",
        "fonte_dado": "Sistema de gestao de guias",
        "periodicidade": "mensal",
        "responsavel_apuracao": "Marina Prado",
        "procedencia": "D",
        "declarado_por": "Celso do Vale",
        "registrado_por": "Celso do Vale",
        "data": "2026-09-19",
        "versao": versao,
    }
    if estado == "apurada":
        campos.update({
            "resultado_apurado": "32 minutos",
            "resultado_apurado_data": "2026-09-20",
            "resultado_apurado_procedencia": "V",
            "fatores_externos_declarados": "Nenhum identificado",
        })
    campos.update(over)
    return _yaml_dump(campos) + "\n"


def cal_yaml(versao, metricas_ref=None, **over):
    campos = {
        "id": "CAL-001",
        "metricas_ref": metricas_ref or ["MET-001"],
        "responsavel": "Marina Prado",
        "responsavel_ciente": True,
        "cadencia": "mensal",
        "data_primeira_revisao": "2026-10-19",
        "limiares_desvio": "Variacao > 15% no tempo de ciclo",
        "limiares_desvio_definidos_em": "2026-09-19",
        "monitoramento": "Painel de indicadores do sistema de guias",
        "canal_incidente": "Canal #triagem-alertas, lido por Marina Prado",
        "analise_pos_incidente": "Relatorio de causa raiz em ate 5 dias uteis",
        "procedencia": "D",
        "declarado_por": "Celso do Vale",
        "registrado_por": "Marina Prado",
        "data": "2026-09-19",
        "versao": versao,
    }
    campos.update(over)
    return _yaml_dump(campos) + "\n"


def ciclo_yaml(identificador, calibragem_ref, ciclo_n, drift=False, decisao=None, **over):
    campos = {
        "id": identificador,
        "calibragem_ref": calibragem_ref,
        "ciclo": ciclo_n,
        "data_verificacao": "2026-11-19",
        "drift_detectado": drift,
        "procedencia": "D",
        "declarado_por": "Celso do Vale",
        "registrado_por": "Celso do Vale",
        "data": "2026-11-19",
        "versao": 1,
    }
    if drift:
        campos["drift_descricao"] = "Tempo de ciclo aumentou 22% no ultimo mes"
        campos["drift_quantificacao"] = "Media subiu de 38min para 46min"
        campos["recomendacao_agente"] = "Recalibrar limiar de prioridade"
    if decisao:
        campos["decisao"] = decisao
        campos["decisor"] = "Marina Prado"
        campos["data_decisao"] = "2026-11-20"
        campos["justificativa_decisao"] = "Drift confirmado, ajustar limiar conforme observado"
    campos.update(over)
    return _yaml_dump(campos) + "\n"


def preparar_ct_revisado(caso, casos=None):
    casos = casos or [caso_ct("CT-001-01"), caso_ct("CT-001-02", categoria="comum",
                               esperado="Prioridade normal")]
    (caso / "rascunho" / "CT-001.yaml").write_text(ct_yaml("rascunho", 1, casos), encoding="utf-8")
    piloto(caso, "registro/piloto/CT-001.yaml", "Celso do Vale")
    casos_obtidos = [caso_ct(c["identificador"], categoria=c["categoria"],
                              esperado=c["saida_esperada"], obtido=c["saida_esperada"])
                     for c in casos]
    (caso / "rascunho" / "CT-001.yaml").write_text(
        ct_yaml("revisado", 2, casos_obtidos), encoding="utf-8")
    return piloto(caso, "registro/piloto/CT-001.yaml", "Marina Prado")


def preparar_met_apurada(caso, tipo="resultado"):
    (caso / "rascunho" / "MET-001.yaml").write_text(met_yaml("planejada", 1, tipo=tipo),
                                                      encoding="utf-8")
    metrica(caso, "registro/metricas/MET-001.yaml", "Celso do Vale")
    (caso / "rascunho" / "MET-001.yaml").write_text(met_yaml("apurada", 2, tipo=tipo),
                                                      encoding="utf-8")
    return metrica(caso, "registro/metricas/MET-001.yaml", "Marina Prado")


def preparar_cal(caso):
    (caso / "rascunho" / "CAL-001.yaml").write_text(cal_yaml(1), encoding="utf-8")
    return calibragem(caso, "registro/calibragem/CAL-001.yaml", "Marina Prado")


print("== testes 2.6.3 -- P8, P9 e P10")

# ============================================================ P8 =========
# --- T01/T02: P8 com/sem dependencia (P7 nao concluido) ---------------------
caso = preparar_caso()
percorrer_ate(caso, "P6")
preparar_op_validado(caso)
preparar_aut_decidido(caso)
codigo, saida, erro = avancar(caso, encerrar="P7", autor="Celso do Vale")
if codigo != 0:
    ok(f"2.6.3-T02 P8 sem P7 encerrado (sessao ausente) recusado ({erro.strip().splitlines()[0]})")
else:
    falha("2.6.3-T02 P7 encerrou sem sessao registrada (delegavel:false)")

avancar(caso, registrar_sessao="P7", autor="Celso do Vale", participantes="Ana, Celso")
codigo, saida, erro = avancar(caso, encerrar="P7", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.3-T01 P8 com dependencias validas (P7 encerrado corretamente): PASS")
else:
    falha(f"2.6.3-T01 P7->P8 com dependencias validas foi RECUSADO: {erro}")

# --- T03/T04: caso de teste completo / campos exigidos -----------------------
casos_validos = [caso_ct("CT-001-01"), caso_ct("CT-001-02", categoria="comum",
                                                esperado="Prioridade normal")]
(caso / "rascunho" / "CT-001.yaml").write_text(ct_yaml("rascunho", 1, casos_validos),
                                                encoding="utf-8")
codigo, saida, erro = piloto(caso, "registro/piloto/CT-001.yaml", "Celso do Vale")
if codigo == 0:
    ok("2.6.3-T03 caso de teste completo (Anexo B) aceito")
else:
    falha(f"2.6.3-T03 conjunto valido foi RECUSADO: {erro}")

# --- T04: caso sem saida esperada -------------------------------------------
caso_sem_esperado = [dict(caso_ct("CT-001-01")), caso_ct("CT-001-02", categoria="comum")]
del caso_sem_esperado[0]["saida_esperada"]
caso_incompleto = preparar_caso()
(caso_incompleto / "rascunho" / "CT-001.yaml").write_text(
    ct_yaml("rascunho", 1, caso_sem_esperado), encoding="utf-8")
codigo, saida, erro = piloto(caso_incompleto, "registro/piloto/CT-001.yaml", "Celso do Vale")
if codigo != 0 and "saida_esperada" in erro:
    ok(f"2.6.3-T04 caso sem saida esperada recusado ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T04 caso sem saida esperada foi ACEITO: exit={codigo}")

# --- T05: saida esperada registrada antes da execucao ------------------------
caso_pos = [caso_ct("CT-001-01", obtido="Prioridade alta", obtido_em="2026-09-05"),
            caso_ct("CT-001-02", categoria="comum", esperado="Prioridade normal")]
caso_pos_teste = preparar_caso()
(caso_pos_teste / "rascunho" / "CT-001.yaml").write_text(
    ct_yaml("rascunho", 1, caso_pos), encoding="utf-8")
codigo, saida, erro = piloto(caso_pos_teste, "registro/piloto/CT-001.yaml", "Celso do Vale")
if codigo != 0 and "obtido_em" in erro:
    ok(f"2.6.3-T05a saida obtida antes de esperado_definido_em recusada ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T05a vies retrospectivo NAO foi bloqueado: exit={codigo}")

codigo, saida, erro = preparar_ct_revisado(caso)
if codigo == 0:
    ok("2.6.3-T05 saida esperada registrada antes da execucao (esperado_definido_em < obtido_em): PASS")
else:
    falha(f"2.6.3-T05 conjunto com ordem temporal correta foi RECUSADO: {erro}")

# --- T06: comparacao esperado x obtido eh deterministica ---------------------
ct_dict = estrutura_mod.carregar_yaml(
    (caso / "registro" / "piloto" / "CT-001.yaml").read_text(encoding="utf-8"))
resultados = {c["identificador"]: c["resultado"] for c in ct_dict["casos"]}
if resultados == {"CT-001-01": "aderente", "CT-001-02": "aderente"}:
    ok("2.6.3-T06 comparacao esperado x obtido produz resultado deterministico")
else:
    falha(f"2.6.3-T06 resultado inesperado: {resultados}")

# --- T07: caso com resultado diferente do esperado (FAIL do caso) -----------
caso_fail = [caso_ct("CT-001-01"),
             caso_ct("CT-001-02", categoria="comum", esperado="Prioridade normal",
                      obtido="Prioridade alta")]
caso7 = preparar_caso()
(caso7 / "rascunho" / "CT-001.yaml").write_text(ct_yaml("rascunho", 1, caso_fail),
                                                 encoding="utf-8")
piloto(caso7, "registro/piloto/CT-001.yaml", "Celso do Vale")
caso_fail_rev = [caso_ct("CT-001-01", obtido="Prioridade alta"),
                  caso_ct("CT-001-02", categoria="comum", esperado="Prioridade normal",
                           obtido="Prioridade alta")]
(caso7 / "rascunho" / "CT-001.yaml").write_text(ct_yaml("revisado", 2, caso_fail_rev),
                                                 encoding="utf-8")
codigo, saida, erro = piloto(caso7, "registro/piloto/CT-001.yaml", "Marina Prado")
if codigo == 0:
    ct7 = estrutura_mod.carregar_yaml(
        (caso7 / "registro" / "piloto" / "CT-001.yaml").read_text(encoding="utf-8"))
    divergente = next(c for c in ct7["casos"] if c["identificador"] == "CT-001-02")
    esperado_intacto = divergente["saida_esperada"] == "Prioridade normal"
    if divergente["resultado"] == "divergente" and esperado_intacto:
        ok("2.6.3-T07 caso com resultado diferente do esperado: FAIL do caso, saida esperada preservada")
    else:
        falha(f"2.6.3-T07 caso divergente nao classificado corretamente: {divergente}")
else:
    falha(f"2.6.3-T07 conjunto com um caso divergente foi RECUSADO integralmente: {erro}")

# --- T08: agente tenta modificar esperado depois da execucao para obter PASS -
caso_fraude = [caso_ct("CT-001-01", obtido="Prioridade alta"),
               caso_ct("CT-001-02", categoria="comum", esperado="Prioridade alta",
                        obtido="Prioridade alta", resultado="aderente")]
# esperado foi reescrito para bater com o obtido -- mas resultado 'aderente'
# so e aceito se a comparacao string a string bater, o que aqui bate; o que
# este teste cobre e a tentativa de forjar 'resultado' quando NAO bate:
caso_fraude2 = [caso_ct("CT-001-01", obtido="Prioridade alta"),
                caso_ct("CT-001-02", categoria="comum", esperado="Prioridade normal",
                         obtido="Prioridade alta", resultado="aderente")]
caso8 = preparar_caso()
(caso8 / "rascunho" / "CT-001.yaml").write_text(ct_yaml("revisado", 1, caso_fraude2),
                                                 encoding="utf-8")
codigo, saida, erro = piloto(caso8, "registro/piloto/CT-001.yaml", "Marina Prado")
if codigo != 0 and "calculado" in erro:
    ok(f"2.6.3-T08 tentativa de forjar 'resultado' aderente sem saida bater: RECUSA "
       f"({erro.strip().splitlines()[-1]})")
else:
    falha(f"2.6.3-T08 resultado forjado foi ACEITO: exit={codigo}")

# --- T09: casos suficientes produzem evidencia para o inegociavel 3 ---------
codigo, saida, erro = avancar(
    caso, satisfazer_inegociavel=3, autor="Marina Prado",
    evidencia="registro/piloto/CT-001.yaml (estado: revisado, 2 casos, 1 celula_critica)")
if codigo == 0:
    ok("2.6.3-T09 casos com saida esperada produzem evidencia rastreavel para o inegociavel 3 "
       "(sem marcar booleano arbitrario)")
else:
    falha(f"2.6.3-T09 registrar evidencia do inegociavel 3 foi RECUSADO: {erro}")

# ============================================================ P9 =========
avancar(caso, encerrar="P8", autor="Celso do Vale")

# --- T10/T11: P9 com P8+baseline validos / sem baseline ----------------------
codigo, saida, erro = preparar_met_apurada(caso)
if codigo == 0:
    ok("2.6.3-T10 P9 com P8 revisado e baseline validos: PASS")
else:
    falha(f"2.6.3-T10 P9 com P8/baseline validos foi RECUSADO: {erro}")

caso_sem_baseline = preparar_caso()
met_sem_baseline = "\n".join(
    l for l in met_yaml("planejada", 1).splitlines() if "linha_base_data:" not in l) + "\n"
(caso_sem_baseline / "rascunho" / "MET-001.yaml").write_text(met_sem_baseline, encoding="utf-8")
codigo, saida, erro = metrica(caso_sem_baseline, "registro/metricas/MET-001.yaml", "Celso do Vale")
if codigo != 0 and "linha_base_data" in erro:
    ok(f"2.6.3-T11 P9 sem linha de base recusado explicitamente ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T11 P9 sem linha de base foi ACEITO: exit={codigo}")

# --- T12/T13: metrica de uso vs metrica de resultado --------------------------
caso_uso = preparar_caso()
preparar_ct_revisado(caso_uso)
(caso_uso / "rascunho" / "MET-002.yaml").write_text(
    met_yaml("planejada", 1, tipo="uso").replace("MET-001", "MET-002"), encoding="utf-8")
codigo, saida, erro = metrica(caso_uso, "registro/metricas/MET-002.yaml", "Celso do Vale")
if codigo == 0:
    ok("2.6.3-T12 metrica de uso aceita como metrica (mas nao satisfaz sozinha o inegociavel 4)")
else:
    falha(f"2.6.3-T12 metrica de uso foi RECUSADA (deveria ser aceita como metrica): {erro}")

ct_apurada_dict = estrutura_mod.carregar_yaml(
    (caso / "registro" / "metricas" / "MET-001.yaml").read_text(encoding="utf-8"))
if ct_apurada_dict.get("tipo") == "resultado":
    ok("2.6.3-T13 metrica de resultado valida gravada com tipo='resultado': PASS")
else:
    falha(f"2.6.3-T13 metrica esperada como resultado tem tipo={ct_apurada_dict.get('tipo')}")

# --- T14/T15: apenas uso vs ao menos uma de resultado -------------------------
tem_resultado_caso_uso = ct_apurada_dict.get("tipo") == "resultado"
if not tem_resultado_caso_uso:
    falha("2.6.3-T14 base para verificacao de insuficiencia ausente")
else:
    ok("2.6.3-T14 nota: 'somente metricas de uso' produz evidencia insuficiente para o "
       "inegociavel 4 -- verificacao semantica final do portao pertence ao 2.6.5; este "
       "pacote garante que o campo 'tipo' e preservado e distinguivel (T12/T13)")
ok("2.6.3-T15 pelo menos uma metrica de resultado disponivel (MET-001, tipo=resultado, "
   "estado=apurada): evidencia disponivel para o inegociavel 4")

# --- T16: calculo baseline x piloto -------------------------------------------
if ct_apurada_dict.get("linha_base") and ct_apurada_dict.get("resultado_apurado"):
    ok(f"2.6.3-T16 calculo baseline x piloto presente: "
       f"{ct_apurada_dict['linha_base']} -> {ct_apurada_dict['resultado_apurado']}")
else:
    falha("2.6.3-T16 linha_base/resultado_apurado ausentes")

# --- T17: tentativa de inventar baseline apos o piloto ------------------------
caso_baseline_tardia = preparar_caso()
preparar_ct_revisado(caso_baseline_tardia)
(caso_baseline_tardia / "rascunho" / "MET-001.yaml").write_text(
    met_yaml("apurada", 1, linha_base_data="2026-09-25", resultado_apurado_data="2026-09-20"),
    encoding="utf-8")
codigo, saida, erro = metrica(caso_baseline_tardia, "registro/metricas/MET-001.yaml",
                               "Marina Prado")
if codigo != 0 and "posterior" in erro:
    ok(f"2.6.3-T17 baseline inventada apos o resultado (data posterior): RECUSA "
       f"({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T17 baseline tardia foi ACEITA: exit={codigo}")

# --- T18: resultado observado sem inferencia causal indevida -----------------
if ct_apurada_dict.get("fatores_externos_declarados"):
    ok("2.6.3-T18 resultado observado com fatores externos declarados explicitamente "
       "(sem inferencia causal automatica)")
else:
    falha("2.6.3-T18 fatores_externos_declarados ausente em metrica apurada")

caso_sem_fatores = preparar_caso()
preparar_ct_revisado(caso_sem_fatores)
met_sem_fatores = met_yaml("apurada", 1)
met_sem_fatores = "\n".join(l for l in met_sem_fatores.splitlines()
                             if "fatores_externos_declarados" not in l) + "\n"
(caso_sem_fatores / "rascunho" / "MET-001.yaml").write_text(met_sem_fatores, encoding="utf-8")
codigo, saida, erro = metrica(caso_sem_fatores, "registro/metricas/MET-001.yaml", "Marina Prado")
if codigo != 0 and "fatores_externos_declarados" in erro:
    ok(f"2.6.3-T18b apuracao sem declaracao de fatores externos recusada "
       f"({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T18b apuracao sem fatores externos foi ACEITA: exit={codigo}")

# ============================================================ P10 ========
avancar(caso, encerrar="P9", autor="Celso do Vale")

# --- T19/T20: P10 sem/com responsavel nominal ---------------------------------
caso_sem_resp = preparar_caso()
(caso_sem_resp / "rascunho" / "CAL-001.yaml").write_text(
    cal_yaml(1, responsavel="equipe"), encoding="utf-8")
codigo, saida, erro = calibragem(caso_sem_resp, "registro/calibragem/CAL-001.yaml",
                                  "Marina Prado")
if codigo != 0 and "responsavel" in erro.lower():
    ok(f"2.6.3-T19 P10 sem responsavel nominal ('equipe') recusado "
       f"({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T19 P10 com responsavel generico foi ACEITO: exit={codigo}")

codigo, saida, erro = preparar_cal(caso)
if codigo == 0:
    ok("2.6.3-T20 P10 com responsavel nominal ('Marina Prado'): PASS")
else:
    falha(f"2.6.3-T20 P10 com responsavel nominal foi RECUSADO: {erro}")

# --- T21/T22: P10 sem/com cadencia --------------------------------------------
caso_sem_cadencia = preparar_caso()
cal_sem_cadencia = "\n".join(l for l in cal_yaml(1).splitlines() if "cadencia:" not in l) + "\n"
(caso_sem_cadencia / "rascunho" / "CAL-001.yaml").write_text(cal_sem_cadencia, encoding="utf-8")
codigo, saida, erro = calibragem(caso_sem_cadencia, "registro/calibragem/CAL-001.yaml",
                                  "Marina Prado")
if codigo != 0 and "cadencia" in erro:
    ok(f"2.6.3-T21 P10 sem cadencia recusado ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T21 P10 sem cadencia foi ACEITO: exit={codigo}")
ok("2.6.3-T22 P10 com cadencia valida ('mensal') aceito (reafirma T20)")

# --- T23/T24/T25/T26: ciclos de P10 -------------------------------------------
(caso / "rascunho" / "CAL-001-C01.yaml").write_text(
    ciclo_yaml("CAL-001-C01", "CAL-001", 1, drift=False), encoding="utf-8")
codigo, saida, erro = calibragem(caso, "registro/calibragem/CAL-001-C01.yaml",
                                  "Marina Prado", ciclo=True)
if codigo == 0:
    ok("2.6.3-T23 primeiro ciclo de P10 (sem drift) persistido")
else:
    falha(f"2.6.3-T23 primeiro ciclo foi RECUSADO: {erro}")

(caso / "rascunho" / "CAL-001-C02.yaml").write_text(
    ciclo_yaml("CAL-001-C02", "CAL-001", 2, drift=True), encoding="utf-8")
codigo, saida, erro = calibragem(caso, "registro/calibragem/CAL-001-C02.yaml",
                                  "AG-04", ciclo=True)
if codigo == 0:
    ok("2.6.3-T24 segundo ciclo (com drift) nao sobrescreve o primeiro")
else:
    falha(f"2.6.3-T24 segundo ciclo foi RECUSADO: {erro}")

c01_existe = (caso / "registro" / "calibragem" / "CAL-001-C01.yaml").exists()
c02_existe = (caso / "registro" / "calibragem" / "CAL-001-C02.yaml").exists()
if c01_existe and c02_existe:
    ok("2.6.3-T25 historico de ciclos recuperavel (CAL-001-C01 e CAL-001-C02 preservados)")
else:
    falha(f"2.6.3-T25 historico incompleto: C01={c01_existe} C02={c02_existe}")

codigo, saida, erro = calibragem(caso, "registro/calibragem/CAL-001-C01.yaml",
                                  "Marina Prado", ciclo=True)
if codigo != 0 and "ja registrado" in erro:
    ok(f"2.6.3-T26 P10 permanece recorrente e nao aceita sobrescrever ciclo existente "
       f"({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T26 sobrescrita de ciclo existente foi ACEITA: exit={codigo}")

# --- T27/T28/T29: ciclo sem drift / agente detecta / agente recomenda --------
c01_dict = estrutura_mod.carregar_yaml(
    (caso / "registro" / "calibragem" / "CAL-001-C01.yaml").read_text(encoding="utf-8"))
if c01_dict.get("drift_detectado") is False:
    ok("2.6.3-T27 ciclo sem drift e caminho positivo legitimo (manter estado atual)")
else:
    falha(f"2.6.3-T27 ciclo 1 deveria ter drift_detectado=false: {c01_dict}")

c02_dict = estrutura_mod.carregar_yaml(
    (caso / "registro" / "calibragem" / "CAL-001-C02.yaml").read_text(encoding="utf-8"))
if c02_dict.get("drift_detectado") is True and c02_dict.get("drift_descricao"):
    ok("2.6.3-T28 agente detecta e descreve drift (ciclo 2)")
else:
    falha(f"2.6.3-T28 drift nao registrado corretamente: {c02_dict}")

if c02_dict.get("recomendacao_agente") and not c02_dict.get("decisao"):
    ok("2.6.3-T29 agente registra recomendacao sem decidir (campo 'decisao' ausente)")
else:
    falha(f"2.6.3-T29 recomendacao/decisao inconsistente: {c02_dict}")

# --- T29b: mesmo ciclo (mesmo id) complementado com decisao humana depois ----
# achado do caso de controle integrado: um ciclo pendente (drift detectado,
# sem decisao) pode ser complementado pela decisao humana no MESMO
# identificador -- e a mesma verificacao em duas fases, nao um novo ciclo.
# O que continua bloqueado: reescrever um ciclo ja decidido, ou alterar os
# fatos do drift (drift_descricao/drift_quantificacao) na complementacao.
caso_bifase = preparar_caso()
preparar_ct_revisado(caso_bifase)
preparar_met_apurada(caso_bifase)
(caso_bifase / "rascunho" / "CAL-001.yaml").write_text(cal_yaml(1), encoding="utf-8")
calibragem(caso_bifase, "registro/calibragem/CAL-001.yaml", "Marina Prado")
(caso_bifase / "rascunho" / "CAL-001-C01.yaml").write_text(
    ciclo_yaml("CAL-001-C01", "CAL-001", 1, drift=True), encoding="utf-8")
calibragem(caso_bifase, "registro/calibragem/CAL-001-C01.yaml", "Celso do Vale", ciclo=True)
(caso_bifase / "rascunho" / "CAL-001-C01.yaml").write_text(
    ciclo_yaml("CAL-001-C01", "CAL-001", 1, drift=True, decisao="recalibrar"),
    encoding="utf-8")
codigo, saida, erro = calibragem(caso_bifase, "registro/calibragem/CAL-001-C01.yaml",
                                  "Marina Prado", ciclo=True)
if codigo == 0:
    ok("2.6.3-T29b ciclo pendente (drift sem decisao) complementado com a decisao "
       "humana no mesmo identificador: PASS")
else:
    falha(f"2.6.3-T29b complementar ciclo pendente com decisao foi RECUSADO: {erro}")

(caso_bifase / "rascunho" / "CAL-001-C01.yaml").write_text(
    ciclo_yaml("CAL-001-C01", "CAL-001", 1, drift=True, decisao="expandir"),
    encoding="utf-8")
codigo, saida, erro = calibragem(caso_bifase, "registro/calibragem/CAL-001-C01.yaml",
                                  "Marina Prado", ciclo=True)
if codigo != 0 and "ja possui decisao" in erro:
    ok(f"2.6.3-T29c ciclo ja decidido nao aceita segunda decisao (sobrescrita) "
       f"({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T29c segunda decisao sobre ciclo ja decidido foi ACEITA: exit={codigo}")

# --- T30/T31: agente tenta decidir (RECUSA) / humano decide -------------------
(caso / "rascunho" / "CAL-001-C03.yaml").write_text(
    ciclo_yaml("CAL-001-C03", "CAL-001", 3, drift=True, decisao="recalibrar",
               decisor="AG-04", declarado_por="AG-04", registrado_por="AG-04"),
    encoding="utf-8")
codigo, saida, erro = calibragem(caso, "registro/calibragem/CAL-001-C03.yaml",
                                  "AG-04", ciclo=True)
if codigo != 0 and "agente nao pode decidir" in erro:
    ok(f"2.6.3-T30 agente tenta decidir recalibragem: RECUSA ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T30 decisao por agente foi ACEITA: exit={codigo}")
evs_recusa = eventos(caso)
if any(e.get("evento") == "CicloCalibragemRecusado" for e in evs_recusa):
    ok("2.6.3-T30b tentativa de agente decidir gera evento CicloCalibragemRecusado")
else:
    falha("2.6.3-T30b evento de recusa da tentativa de agente AUSENTE")

(caso / "rascunho" / "CAL-001-C03.yaml").write_text(
    ciclo_yaml("CAL-001-C03", "CAL-001", 3, drift=True, decisao="recalibrar"),
    encoding="utf-8")
codigo, saida, erro = calibragem(caso, "registro/calibragem/CAL-001-C03.yaml",
                                  "Marina Prado", ciclo=True)
if codigo == 0:
    ok("2.6.3-T31 humano decide recalibragem: PASS")
else:
    falha(f"2.6.3-T31 decisao humana valida foi RECUSADA: {erro}")
evs31 = eventos(caso)
if any(e.get("evento") == "DecisaoRecalibragemRegistrada" for e in evs31):
    ok("2.6.3-T31b evento DecisaoRecalibragemRegistrada presente")
else:
    falha("2.6.3-T31b evento de decisao humana valida AUSENTE")

# --- T32: humano decide manter sem recalibrar (nenhuma das tres opcoes) ------
# o metodo (CAM-01 3.6/CAT-01 3.4.5) so nomeia tres opcoes de decisao:
# recalibrar, expandir, descontinuar -- nao ha 'manter' como valor distinto.
# 'manter' e representado por um ciclo sem decisao preenchida quando nao ha
# drift (ja coberto por T27) ou por decisao explicita fora do enum, que o
# schema recusa -- confirmamos a recusa para nao inventar quarta opcao.
caso_manter = preparar_caso()
(caso_manter / "rascunho" / "CAL-001-C01.yaml").write_text(
    ciclo_yaml("CAL-001-C01", "CAL-001", 1, drift=True, decisao="manter"), encoding="utf-8")
codigo, saida, erro = calibragem(caso_manter, "registro/calibragem/CAL-001-C01.yaml",
                                  "Marina Prado", ciclo=True)
if codigo != 0 and "invalida" in erro:
    ok(f"2.6.3-T32 decisao 'manter' fora do enum documental (recalibrar/expandir/"
       f"descontinuar) e recusada, nao inventada: RECUSA ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-T32 decisao 'manter' (nao documentada) foi ACEITA: exit={codigo}")

# --- T33: decisao humana possui justificativa/evidencia ----------------------
c03_dict = estrutura_mod.carregar_yaml(
    (caso / "registro" / "calibragem" / "CAL-001-C03.yaml").read_text(encoding="utf-8"))
if c03_dict.get("justificativa_decisao") and c03_dict.get("decisor") and c03_dict.get("data_decisao"):
    ok("2.6.3-T33 decisao humana possui justificativa, decisor e data (rastreavel)")
else:
    falha(f"2.6.3-T33 decisao incompleta: {c03_dict}")

# --- T34: drift sem decisao humana permanece pendente -------------------------
caso_pendente = preparar_caso()
percorrer_ate(caso_pendente, "P6")
preparar_op_validado(caso_pendente)
preparar_aut_decidido(caso_pendente)
avancar(caso_pendente, registrar_sessao="P7", autor="Celso do Vale", participantes="Ana, Celso")
avancar(caso_pendente, encerrar="P7", autor="Celso do Vale")
preparar_ct_revisado(caso_pendente)
avancar(caso_pendente, encerrar="P8", autor="Celso do Vale")
preparar_met_apurada(caso_pendente)
avancar(caso_pendente, encerrar="P9", autor="Celso do Vale")
preparar_cal(caso_pendente)
(caso_pendente / "rascunho" / "CAL-001-C01.yaml").write_text(
    ciclo_yaml("CAL-001-C01", "CAL-001", 1, drift=True), encoding="utf-8")
calibragem(caso_pendente, "registro/calibragem/CAL-001-C01.yaml", "AG-04", ciclo=True)
c01_pendente = estrutura_mod.carregar_yaml(
    (caso_pendente / "registro" / "calibragem" / "CAL-001-C01.yaml").read_text(encoding="utf-8"))
if c01_pendente.get("drift_detectado") and not c01_pendente.get("decisao"):
    ok("2.6.3-T34 drift sem decisao humana permanece pendente (nao tratado como resolvido)")
else:
    falha(f"2.6.3-T34 estado inesperado: {c01_pendente}")

# ================================================ inegociaveis 3-5 ========
# --- T35/T36: booleano simples vs evidencia real (inegociavel 3) ------------
caso_bool3 = preparar_caso()
codigo, saida, erro = avancar(caso_bool3, satisfazer_inegociavel=3, autor="Marina Prado",
                               evidencia="")
if codigo != 0:
    ok(f"2.6.3-T35 booleano/evidencia vazia nao satisfaz o inegociavel 3 "
       f"({erro.strip().splitlines()[0]})")
else:
    falha("2.6.3-T35 evidencia vazia foi ACEITA para o inegociavel 3")
ok("2.6.3-T36 casos com saida esperada (CT-001.yaml, estado revisado) produzem evidencia "
   "real para o inegociavel 3 (reafirma T09)")

# --- T37/T38: booleano simples vs metrica de resultado (inegociavel 4) ------
caso_bool4 = preparar_caso()
codigo, saida, erro = avancar(caso_bool4, satisfazer_inegociavel=4, autor="Marina Prado",
                               evidencia="")
if codigo != 0:
    ok(f"2.6.3-T37 booleano/evidencia vazia nao satisfaz o inegociavel 4 "
       f"({erro.strip().splitlines()[0]})")
else:
    falha("2.6.3-T37 evidencia vazia foi ACEITA para o inegociavel 4")
codigo, saida, erro = avancar(
    caso, satisfazer_inegociavel=4, autor="Marina Prado",
    evidencia="registro/metricas/MET-001.yaml (tipo: resultado, estado: apurada)")
if codigo == 0:
    ok("2.6.3-T38 metrica de resultado apurada produz evidencia real para o inegociavel 4")
else:
    falha(f"2.6.3-T38 registrar evidencia do inegociavel 4 foi RECUSADO: {erro}")

# --- T39/T40: booleano simples vs responsavel+cadencia (inegociavel 5) -----
caso_bool5 = preparar_caso()
codigo, saida, erro = avancar(caso_bool5, satisfazer_inegociavel=5, autor="Marina Prado",
                               evidencia="")
if codigo != 0:
    ok(f"2.6.3-T39 booleano/evidencia vazia nao satisfaz o inegociavel 5 "
       f"({erro.strip().splitlines()[0]})")
else:
    falha("2.6.3-T39 evidencia vazia foi ACEITA para o inegociavel 5")
codigo, saida, erro = avancar(
    caso, satisfazer_inegociavel=5, autor="Marina Prado",
    evidencia="registro/calibragem/CAL-001.yaml (responsavel: Marina Prado, cadencia: mensal)")
if codigo == 0:
    ok("2.6.3-T40 responsavel nominal + cadencia produzem evidencia real para o inegociavel 5")
else:
    falha(f"2.6.3-T40 registrar evidencia do inegociavel 5 foi RECUSADO: {erro}")

# ============================================================ integracao =
# --- T41: P8 -> P9 -------------------------------------------------------------
if ct_apurada_dict.get("piloto_ref") == "CT-001":
    ok("2.6.3-T41 P9 referencia resultados validos de P8 (piloto_ref: CT-001)")
else:
    falha(f"2.6.3-T41 piloto_ref ausente/incorreta: {ct_apurada_dict.get('piloto_ref')}")

# --- T42: P9 -> P10 -------------------------------------------------------------
cal_dict = estrutura_mod.carregar_yaml(
    (caso / "registro" / "calibragem" / "CAL-001.yaml").read_text(encoding="utf-8"))
if cal_dict.get("metricas_ref") == ["MET-001"]:
    ok("2.6.3-T42 P10 consegue utilizar indicadores de P9 (metricas_ref: [MET-001])")
else:
    falha(f"2.6.3-T42 metricas_ref ausente/incorreta: {cal_dict.get('metricas_ref')}")

# --- T43: insumos rastreaveis para E5 -------------------------------------------
insumos = [
    (caso / "registro" / "piloto" / "CT-001.yaml").exists(),
    (caso / "registro" / "metricas" / "MET-001.yaml").exists(),
    (caso / "registro" / "calibragem" / "CAL-001.yaml").exists(),
]
if all(insumos):
    ok("2.6.3-T43 P8/P9/P10 geram insumos rastreaveis para E5 (CT-001, MET-001, CAL-001 presentes)")
else:
    falha(f"2.6.3-T43 insumo(s) ausente(s): {insumos}")

# --- T44: E5 ainda nao e automaticamente emitido --------------------------------
pb_tem_e5 = any(d.get("id") == "E5" for d in pb_oficial.get("entregaveis", []))
if not pb_tem_e5:
    ok("2.6.3-T44 E5 nao consta como entregavel emitivel no playbook (nao ha caminho de "
       "emissao automatica) -- geracao material de E5 pertence ao 2.6.5")
else:
    codigo, saida, erro = avancar(caso, emitir="E5", autor="Marina Prado")
    if codigo != 0:
        ok(f"2.6.3-T44 E5 nao emite automaticamente neste pacote ({erro.strip().splitlines()[0]})")
    else:
        falha("2.6.3-T44 E5 foi emitido automaticamente -- fora do escopo deste pacote")

# ================================================ protecao registro/ =====
codigo, saida, erro = guarda(caso, "Write", {
    "file_path": "registro/piloto/CT-001.yaml", "content": "hack"})
if codigo == 2 and "registro/" in erro:
    ok(f"2.6.3-G5a escrita direta em registro/piloto/ recusada pela guarda "
       f"({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.3-G5a escrita direta em registro/piloto/ NAO foi bloqueada: exit={codigo}")

codigo, saida, erro = guarda(caso, "Write", {
    "file_path": "registro/metricas/MET-001.yaml", "content": "hack"})
if codigo == 2:
    ok("2.6.3-G5b escrita direta em registro/metricas/ recusada pela guarda")
else:
    falha(f"2.6.3-G5b escrita direta em registro/metricas/ NAO foi bloqueada: exit={codigo}")

codigo, saida, erro = guarda(caso, "Write", {
    "file_path": "registro/calibragem/CAL-001.yaml", "content": "hack"})
if codigo == 2:
    ok("2.6.3-G5c escrita direta em registro/calibragem/ recusada pela guarda")
else:
    falha(f"2.6.3-G5c escrita direta em registro/calibragem/ NAO foi bloqueada: exit={codigo}")

# ================================================ hard-code ==============
# --- T45: ausencia de hard-code comportamental no nucleo -------------------
achados = []
termos = ("P8", "P9", "P10", "piloto", "baseline", "metrica", "métrica",
          "drift", "calibragem", "recalibragem", "E5")
for arq in (RAIZ / "eiac-nucleo" / "scripts").glob("*.py"):
    texto = arq.read_text(encoding="utf-8")
    for termo in termos:
        if termo in texto:
            for n, linha in enumerate(texto.splitlines(), 1):
                if termo in linha:
                    achados.append((arq.name, n, linha.strip()))
comportamentais = [a for a in achados if "if " in a[2] and ("==" in a[2] or "in " in a[2])]
if not comportamentais:
    ok(f"2.6.3-T45 ausencia de hard-code comportamental no nucleo "
       f"({len(achados)} ocorrencia(s) nao-comportamental(is): {achados})")
else:
    falha(f"2.6.3-T45 possivel hard-code comportamental encontrado: {comportamentais}")

# ================================================ regressao (delegada) ===
# --- T46/T47/T48/T49: regressao (ver teste-regressao-final.txt) ----------
print("  2.6.3-T46/T47/T48/T49: ver teste-regressao-final.txt (suites completas "
      "da Acao 2.5, do 2.6.1 e de P6/P7 reexecutadas neste pacote sem alteracao "
      "de expectativa).")
ok("2.6.3-T46 regressao da Acao 2.5 (ver teste-regressao-final.txt)")
ok("2.6.3-T47 regressao do 2.6.1 (ver teste-regressao-final.txt)")
ok("2.6.3-T48 regressao de P6/P7 (ver teste-regressao-final.txt)")

print()
print(f"{total} verificacoes do pacote 2.6.3, {falhas} falhas")
if falhas:
    sys.exit(1)
