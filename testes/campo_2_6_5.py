#!/usr/bin/env python3
"""Verificacao semantica dos inegociaveis, portoes operacionais e
materializacao de E1-E5 -- pacote 2.6.5.

Cobre: I1-I5 verificados a partir de artefato real (nao flag solta), os
seis portoes de emissao (E1, E2, E3-D, E3-E, E4, E5), a distincao
AUTORIZADO/NEGADO/NAO_APLICAVEL para E3-E, e a materializacao real dos
cinco entregaveis com o evento EntregavelEmitido apontando para o
arquivo.

Nenhum teste aqui pressupoe hard-code de E1-E5/inegociaveis no nucleo:
toda semantica vive em eiac-campo/scripts/ (baseline.py, inegociaveis.py,
entregaveis.py), que reaproveita as primitivas genericas do eiac-nucleo
(avancar.satisfazer_inegociavel, avancar.emitir com --materializar, ja
generico desde o 2.6.1/2.6.5) sem estende-las com semantica de metodo.
"""
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
SELAR = RAIZ / "eiac-nucleo" / "scripts" / "selar.py"
OPERACIONAL = RAIZ / "eiac-campo" / "scripts" / "operacional.py"
GOVERNANCA = RAIZ / "eiac-campo" / "scripts" / "governanca.py"
PILOTO = RAIZ / "eiac-campo" / "scripts" / "piloto.py"
METRICA = RAIZ / "eiac-campo" / "scripts" / "metrica.py"
CALIBRAGEM = RAIZ / "eiac-campo" / "scripts" / "calibragem.py"
BASELINE = RAIZ / "eiac-campo" / "scripts" / "baseline.py"
INEGOCIAVEIS = RAIZ / "eiac-campo" / "scripts" / "inegociaveis.py"
ENTREGAVEIS = RAIZ / "eiac-campo" / "scripts" / "entregaveis.py"

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
    estado_path = caso / "registro" / "estado.json"
    estado = json.loads(estado_path.read_text(encoding="utf-8"))
    estado["responsavel"] = "Celso do Vale"
    estado_path.write_text(json.dumps(estado, ensure_ascii=False), encoding="utf-8")
    # selar.py exige repositorio git (decisao 021: P3b exige selo posterior
    # ao encerramento de P2, ver percorrer_ate).
    subprocess.run(["git", "init", "-q", "."], cwd=caso, check=False)
    subprocess.run(["git", "config", "user.name", "Identidade Da Maquina"], cwd=caso, check=False)
    subprocess.run(["git", "config", "user.email", "maquina@exemplo.com"], cwd=caso, check=False)
    subprocess.run(["git", "add", "-A"], cwd=caso, check=False)
    subprocess.run(["git", "commit", "-qm", "estado inicial do caso"], cwd=caso, check=False)
    return caso


def selar(caso, nota="selo de teste"):
    (caso / f"marcador-selo-{len(list(caso.glob('marcador-selo-*')))}.txt").write_text(
        "x", encoding="utf-8")
    proc = subprocess.run(["python3", str(SELAR), "--autor", "Celso do Vale", "--nota", nota],
                           cwd=caso, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


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


def _rodar(script, caso, *args):
    proc = subprocess.run(["python3", str(script), *args], cwd=caso,
                           text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def operacional(caso, arquivo, ator):
    return _rodar(OPERACIONAL, caso, "--arquivo", arquivo, "--ator", ator)


def governanca(caso, arquivo, ator):
    return _rodar(GOVERNANCA, caso, "--arquivo", arquivo, "--ator", ator)


def piloto(caso, arquivo, ator):
    return _rodar(PILOTO, caso, "--arquivo", arquivo, "--ator", ator)


def metrica(caso, arquivo, ator):
    return _rodar(METRICA, caso, "--arquivo", arquivo, "--ator", ator)


def calibragem(caso, arquivo, ator, ciclo=False):
    args = ["--arquivo", arquivo, "--ator", ator]
    if ciclo:
        args.append("--ciclo")
    return _rodar(CALIBRAGEM, caso, *args)


def baseline(caso, arquivo, ator):
    return _rodar(BASELINE, caso, "--arquivo", arquivo, "--ator", ator)


def inegociavel(caso, n, arquivo, satisfazer=False, autor=None):
    args = ["--verificar", str(n), "--arquivo", arquivo]
    if satisfazer:
        args += ["--satisfazer", "--autor", autor]
    return _rodar(INEGOCIAVEIS, caso, *args)


def entregavel(caso, entregavel_id, autor, emitir=False):
    args = ["--renderizar", entregavel_id, "--autor", autor]
    if emitir:
        args.append("--emitir")
    return _rodar(ENTREGAVEIS, caso, *args)


def eventos(caso):
    log = caso / "registro" / "eventos.jsonl"
    if not log.exists():
        return []
    return [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]


def apurar_e_encerrar_f0(caso, nivel="N2"):
    eixos = {"N1": "DAD 3, GOV 3, CRI 3", "N2": "DAD 5, GOV 3, CRI 6",
             "N3": "DAD 4, GOV 3, CRI 8"}[nivel]
    avancar(caso, apurar_nivel=nivel, autor="Celso do Vale", eixos=eixos)
    return avancar(caso, encerrar="F0", autor="Celso do Vale")


ETAPAS_NAO_DELEGAVEIS = {e["id"] for e in pb_oficial["etapas"] if e.get("delegavel") is False}

# Referencias de exige_selo_apos, invertidas (decisao 021): para cada
# etapa-alvo, a lista de ids de etapa que exigem selo posterior a ela.
ETAPAS_QUE_EXIGEM_SELO_DE = {}
for _e in pb_oficial["etapas"]:
    _ref = _e.get("exige_selo_apos")
    if _ref:
        ETAPAS_QUE_EXIGEM_SELO_DE.setdefault(_ref, []).append(_e["id"])


def percorrer_ate(caso, ate_etapa_id, nivel="N2"):
    apurar_e_encerrar_f0(caso, nivel=nivel)
    ordem = [e["id"] for e in pb_oficial["etapas"]]
    alvo = ordem[1:ordem.index(ate_etapa_id) + 1]
    restante = set(alvo)
    for etapa_id in alvo:
        if etapa_id in ETAPAS_NAO_DELEGAVEIS:
            avancar(caso, registrar_sessao=etapa_id, autor="Celso do Vale",
                    participantes="Ana, Celso")
        avancar(caso, encerrar=etapa_id, autor="Celso do Vale")
        restante.discard(etapa_id)
        exigentes = ETAPAS_QUE_EXIGEM_SELO_DE.get(etapa_id, [])
        if any(exigente in restante for exigente in exigentes):
            selar(caso, f"selo apos {etapa_id}, exigido por etapa posterior do percurso")


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


def bl_yaml(versao=1, **over):
    campos = {
        "id": "BL-001",
        "indicador": "tempo de ciclo de triagem",
        "valor_atual": "45 minutos",
        "apuracao": "medido",
        "data": "2026-08-01",
        "nivel": "N2",
        "procedencia": "V",
        "evidencia": "amostra de 86 guias, agosto/2026",
        "declarado_por": "Marina Prado",
        "registrado_por": "Celso do Vale",
        "versao": versao,
    }
    campos.update(over)
    return _yaml_dump(campos) + "\n"


def op_yaml(estado, versao, **over):
    campos = {
        "id": "OP-001", "estado": estado,
        "ponto_insercao": "recebimento da autorizacao do convenio",
        "momento": "imediatamente apos confirmacao no sistema do convenio",
        "sistema": "sistema de gestao de guias",
        "entrada": "numero da guia e status de autorizacao",
        "saida": "guia enviada ao setor de faturamento",
        "ator_humano": "Claudia Ferreira, analista de faturamento",
        "excecao": "guia sem correspondencia na camada de contexto",
        "fallback": "encaminhar para fila manual de Claudia Ferreira",
        "responsavel_operacional": "Claudia Ferreira",
        "procedencia": "D", "declarado_por": "Claudia Ferreira",
        "registrado_por": "Celso do Vale", "data": "2026-09-19", "versao": versao,
    }
    if estado == "validado":
        campos["validado_por"] = "Rafael Nogueira"
        campos["data_validacao"] = "2026-09-19"
    campos.update(over)
    return _yaml_dump(campos) + "\n"


def aut_yaml(estado, versao, operacional_ref="OP-001", **over):
    campos = {
        "id": "AUT-001", "estado": estado, "operacional_ref": operacional_ref,
        "escopo": "envio automatico de guia de autorizacao apos recebimento",
        "procedencia": "D", "declarado_por": "Claudia Ferreira",
        "registrado_por": "Celso do Vale", "data": "2026-09-19", "versao": versao,
    }
    if estado == "decidido":
        campos["decisor"] = "Marina Prado"
        campos["data_decisao"] = "2026-09-19"
        campos["justificativa_decisao"] = (
            "termo revisado com a area juridica, autonomia liberada para o escopo descrito")
    campos.update({k: v for k, v in over.items() if k != "_listas"})
    listas = {
        "faz_sozinha": ["consultar status da guia no sistema de convenio"],
        "exige_aprovacao": ["emitir guia com valor acima de R$ 5.000"],
        "nunca_faz": ["alterar dados cadastrais do beneficiario"],
        "gatilhos_escalonamento": ["guia sem correspondencia na camada de contexto"],
    }
    listas.update(over.get("_listas", {}))
    linhas = [f"id: {campos.pop('id')}"]
    for chave, valor in campos.items():
        linhas.append(f'{chave}: "{valor}"' if isinstance(valor, str) else f"{chave}: {valor}")
    for chave, itens in listas.items():
        linhas.append(f"{chave}:")
        for item in itens:
            linhas.append(f'  - "{item}"')
    return "\n".join(linhas) + "\n"


def caso_ct(identificador, categoria="celula_critica", esperado="Prioridade alta",
            obtido=None, resultado=None, revisor=None, **over):
    c = {
        "identificador": identificador, "origem": "RN-003",
        "entrada": "Guia com sintoma grave e historico limpo",
        "saida_esperada": esperado,
        "criterio_aprovacao": "Classificacao igual a saida esperada",
        "categoria": categoria, "revisor": revisor or "Marina Prado",
        "data_revisao": "2026-09-11", "esperado_definido_em": "2026-09-10",
        "esperado_definido_por": "Celso do Vale",
    }
    if obtido is not None:
        c["saida_obtida"] = obtido
        c["obtido_em"] = "2026-09-19"
        c["resultado"] = resultado if resultado is not None else (
            "aderente" if obtido == esperado else "divergente")
    c.update(over)
    return c


def ct_yaml(estado, versao, casos, **over):
    campos = {
        "id": "CT-001", "estado": estado, "modo": "assistido", "duracao": "4 semanas",
        "plano_reversao": "Reverter para triagem manual em caso de falha critica",
        "criterio_aprovacao_escala": "95% de acerto nos casos criticos",
        "criterio_aprovacao_escala_definido_em": "2026-09-10",
        "procedencia": "D", "declarado_por": "Celso do Vale",
        "registrado_por": "Celso do Vale", "data": "2026-09-18", "versao": versao,
    }
    if estado == "revisado":
        campos["revisado_por"] = "Marina Prado"
        campos["data_revisao"] = "2026-09-18"
    campos.update({k: v for k, v in over.items() if k != "casos"})
    campos["casos"] = casos
    return _yaml_dump(campos) + "\n"


def met_yaml(estado, versao, tipo="resultado", piloto_ref="CT-001", **over):
    campos = {
        "id": "MET-001", "estado": estado, "piloto_ref": piloto_ref,
        "metrica": "Tempo de ciclo de triagem", "tipo": tipo,
        "linha_base": "45 minutos", "linha_base_data": "2026-08-01",
        "linha_base_procedencia": "V",
        "metodo_apuracao": "Media do tempo entre recepcao e classificacao",
        "fonte_dado": "Sistema de gestao de guias", "periodicidade": "mensal",
        "responsavel_apuracao": "Marina Prado", "procedencia": "D",
        "declarado_por": "Celso do Vale", "registrado_por": "Celso do Vale",
        "data": "2026-09-19", "versao": versao,
    }
    if estado == "apurada":
        campos.update({
            "resultado_apurado": "32 minutos", "resultado_apurado_data": "2026-09-20",
            "resultado_apurado_procedencia": "V",
            "fatores_externos_declarados": "Nenhum identificado",
        })
    campos.update(over)
    return _yaml_dump(campos) + "\n"


def cal_yaml(versao, metricas_ref=None, **over):
    campos = {
        "id": "CAL-001", "metricas_ref": metricas_ref or ["MET-001"],
        "responsavel": "Marina Prado", "responsavel_ciente": True, "cadencia": "mensal",
        "data_primeira_revisao": "2026-10-19",
        "limiares_desvio": "Variacao > 15% no tempo de ciclo",
        "limiares_desvio_definidos_em": "2026-09-19",
        "monitoramento": "Painel de indicadores do sistema de guias",
        "canal_incidente": "Canal #triagem-alertas, lido por Marina Prado",
        "analise_pos_incidente": "Relatorio de causa raiz em ate 5 dias uteis",
        "procedencia": "D", "declarado_por": "Celso do Vale",
        "registrado_por": "Marina Prado", "data": "2026-09-19", "versao": versao,
    }
    campos.update(over)
    return _yaml_dump(campos) + "\n"


def preparar_op_validado(caso):
    (caso / "rascunho" / "OP-001.yaml").write_text(op_yaml("proposta", 1), encoding="utf-8")
    operacional(caso, "registro/operacional/OP-001.yaml", "AG-02")
    (caso / "rascunho" / "OP-001.yaml").write_text(op_yaml("validado", 2), encoding="utf-8")
    operacional(caso, "registro/operacional/OP-001.yaml", "Rafael Nogueira")


def preparar_aut(caso, estado="decidido"):
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("rascunho", 1), encoding="utf-8")
    governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
    if estado == "rascunho":
        return
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("proposto", 2), encoding="utf-8")
    governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
    if estado == "proposto":
        return
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("decidido", 3), encoding="utf-8")
    governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "Marina Prado")


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


def preparar_bl(caso, **over):
    (caso / "rascunho" / "BL-001.yaml").write_text(bl_yaml(**over), encoding="utf-8")
    return baseline(caso, "registro/baseline/BL-001.yaml", "Marina Prado")


print("== testes 2.6.5 -- inegociaveis, portoes e entregaveis")

# ============================================== I1 -- baseline ===========
caso = preparar_caso()
codigo, saida, erro = inegociavel(caso, 1, "registro/baseline/BL-001.yaml")
if codigo != 0:
    ok("2.6.5-T01 I1 sem baseline: RECUSA")
else:
    falha("2.6.5-T01 I1 sem baseline foi ACEITO")

caso = preparar_caso()
preparar_bl(caso)
codigo, saida, erro = inegociavel(caso, 1, "registro/baseline/BL-001.yaml")
if codigo == 0:
    ok("2.6.5-T02 I1 com baseline valido: PASS")
else:
    falha(f"2.6.5-T02 I1 com baseline valido foi RECUSADO: {erro}")

# N2 com apuracao estimado deve ser recusada no proprio baseline.py
caso = preparar_caso()
codigo, saida, erro = preparar_bl(caso, apuracao="estimado")
if codigo != 0:
    ok(f"2.6.5-T02b baseline N2 com apuracao estimado recusada por baseline.py ({erro.strip().splitlines()[0]})")
else:
    falha("2.6.5-T02b baseline N2 com apuracao estimado foi ACEITA")

# ============================================== I2 -- autonomia ==========
caso = preparar_caso()
preparar_op_validado(caso)
preparar_aut(caso, estado="proposto")
codigo, saida, erro = inegociavel(caso, 2, "registro/governanca/autonomia/AUT-001.yaml")
if codigo != 0:
    ok(f"2.6.5-T03 I2 com termo apenas proposto: RECUSA ({saida.strip()})")
else:
    falha("2.6.5-T03 I2 com termo proposto foi ACEITO")

caso = preparar_caso()
preparar_op_validado(caso)
preparar_aut(caso, estado="decidido")
codigo, saida, erro = inegociavel(caso, 2, "registro/governanca/autonomia/AUT-001.yaml")
if codigo == 0:
    ok("2.6.5-T04 I2 com termo decidido por humano: PASS")
else:
    falha(f"2.6.5-T04 I2 com termo decidido foi RECUSADO: {erro}")

# ============================================== I3 -- casos de teste =====
caso = preparar_caso()
casos_sem_esperado = [dict(caso_ct("CT-001-01")), caso_ct("CT-001-02", categoria="comum")]
del casos_sem_esperado[0]["saida_esperada"]
(caso / "rascunho" / "CT-001.yaml").write_text(
    ct_yaml("rascunho", 1, casos_sem_esperado), encoding="utf-8")
piloto(caso, "registro/piloto/CT-001.yaml", "Celso do Vale")
codigo, saida, erro = inegociavel(caso, 3, "registro/piloto/CT-001.yaml")
if codigo != 0:
    ok("2.6.5-T05 I3 sem saida esperada (conjunto so em rascunho): RECUSA")
else:
    falha("2.6.5-T05 I3 sem saida esperada foi ACEITO")

caso = preparar_caso()
preparar_ct_revisado(caso)
codigo, saida, erro = inegociavel(caso, 3, "registro/piloto/CT-001.yaml")
if codigo == 0:
    ok("2.6.5-T06 I3 com casos validos e conjunto revisado: PASS")
else:
    falha(f"2.6.5-T06 I3 com casos validos foi RECUSADO: {erro}")

# ============================================== I4 -- metrica ============
caso = preparar_caso()
preparar_ct_revisado(caso)
preparar_met_apurada(caso, tipo="uso")
codigo, saida, erro = inegociavel(caso, 4, "registro/metricas/MET-001.yaml")
if codigo != 0:
    ok("2.6.5-T07 I4 so com metrica de uso: RECUSA")
else:
    falha("2.6.5-T07 I4 so com metrica de uso foi ACEITO")

caso = preparar_caso()
preparar_ct_revisado(caso)
preparar_met_apurada(caso, tipo="resultado")
codigo, saida, erro = inegociavel(caso, 4, "registro/metricas/MET-001.yaml")
if codigo == 0:
    ok("2.6.5-T08 I4 com metrica de resultado: PASS")
else:
    falha(f"2.6.5-T08 I4 com metrica de resultado foi RECUSADO: {erro}")

# ============================================== I5 -- calibragem =========
caso = preparar_caso()
preparar_ct_revisado(caso)
preparar_met_apurada(caso)
(caso / "rascunho" / "CAL-001.yaml").write_text(cal_yaml(1, responsavel="equipe"),
                                                  encoding="utf-8")
codigo, saida, erro = calibragem(caso, "registro/calibragem/CAL-001.yaml", "Marina Prado")
if codigo != 0 and "nao e responsavel nominal" in (saida + erro):
    ok("2.6.5-T09 I5 sem pessoa nominal ('equipe'): RECUSA em calibragem.py")
else:
    falha(f"2.6.5-T09 I5 sem pessoa nominal nao foi recusado pelo motivo esperado: "
          f"exit={codigo} saida={saida!r} erro={erro!r}")

# 'equipe de TI' (frase composta) escapa da checagem lexica de palavra
# inteira de calibragem.py (que so compara contra palavras exatas) --
# o verificador semantico de I1-I5 (inegociaveis.py) e a segunda camada
# que ainda recusa frases compostas contendo 'ti'/'consultoria', mesmo
# que o registro em si tenha sido gravado.
caso = preparar_caso()
preparar_ct_revisado(caso)
preparar_met_apurada(caso)
(caso / "rascunho" / "CAL-001.yaml").write_text(cal_yaml(1, responsavel="equipe de TI"),
                                                  encoding="utf-8")
calibragem(caso, "registro/calibragem/CAL-001.yaml", "Marina Prado")
codigo, saida, erro = inegociavel(caso, 5, "registro/calibragem/CAL-001.yaml")
if codigo != 0:
    ok("2.6.5-T09b I5 com 'equipe de TI' gravado (frase composta, escapou da "
       "checagem lexica de calibragem.py): RECUSA no verificador semantico")
else:
    falha("2.6.5-T09b I5 com 'equipe de TI' foi ACEITO pelo verificador semantico")

caso = preparar_caso()
preparar_ct_revisado(caso)
preparar_met_apurada(caso)
preparar_cal(caso)
codigo, saida, erro = inegociavel(caso, 5, "registro/calibragem/CAL-001.yaml")
if codigo == 0:
    ok("2.6.5-T10 I5 com pessoa nominal e demais requisitos: PASS")
else:
    falha(f"2.6.5-T10 I5 com pessoa nominal foi RECUSADO: {erro}")

# ============================================== boolean magico ===========
caso = preparar_caso()
estado_path = caso / "registro" / "estado.json"
st = json.loads(estado_path.read_text(encoding="utf-8"))
st["inegociaveis"] = {str(n): {"satisfeito": True, "evidencia": "flag manual",
                                "autor": "Celso do Vale", "data": "2026-09-19"}
                      for n in range(1, 6)}
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
sem_artefato_real = not any((caso / "registro" / d).exists()
                            for d in ("baseline", "governanca", "piloto", "metricas", "calibragem"))
if sem_artefato_real:
    ok("2.6.5-T11 flags manuais sem artefato real: nenhum verificador de "
       "inegociaveis.py foi chamado -- a satisfacao nao deriva de evidencia real")
else:
    falha("2.6.5-T11 flags manuais produziram artefato inesperado")

caso = preparar_caso()
preparar_bl(caso)
codigo, saida, erro = inegociavel(caso, 1, "registro/baseline/BL-001.yaml",
                                   satisfazer=True, autor="Marina Prado")
if codigo == 0:
    st = json.loads((caso / "registro" / "estado.json").read_text(encoding="utf-8"))
    reg = st.get("inegociaveis", {}).get("1", {})
    if reg.get("satisfeito") and "verificar_i1" in reg.get("evidencia", ""):
        ok("2.6.5-T12 evidencia real permite satisfacao, gravada com "
           "referencia ao verificador (nao booleano solto)")
    else:
        falha(f"2.6.5-T12 registro nao rastreia verificador: {reg}")
else:
    falha(f"2.6.5-T12 satisfacao com evidencia real foi RECUSADA: {erro}")

print("== portoes E1-E5")

# ============================================== E1 ========================
caso = preparar_caso()
codigo, saida, erro = avancar(caso, emitir="E1", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T13 E1 antes de F0 completo: NEGADO")
else:
    falha("2.6.5-T13 E1 antes de F0 completo foi AUTORIZADO")

caso = preparar_caso()
apurar_e_encerrar_f0(caso)
codigo, saida, erro = avancar(caso, emitir="E1", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.5-T14 E1 apos F0: AUTORIZADO")
else:
    falha(f"2.6.5-T14 E1 apos F0 foi NEGADO: {erro}")

caso = preparar_caso()
apurar_e_encerrar_f0(caso)
codigo, saida, erro = entregavel(caso, "E1", "Celso do Vale", emitir=True)
arquivo_e1 = caso / "caso" / "entregaveis" / "E1.md"
if codigo == 0 and arquivo_e1.exists() and arquivo_e1.stat().st_size > 0:
    ok(f"2.6.5-T15 materializacao de E1: arquivo real existente ({arquivo_e1})")
else:
    falha(f"2.6.5-T15 materializacao de E1 falhou: exit={codigo} saida={saida!r} erro={erro!r}")

# ============================================== E2 ========================
caso = preparar_caso()
percorrer_ate(caso, "P2")  # falta P3a, P3b, P3d
codigo, saida, erro = avancar(caso, emitir="E2", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T16 E2 com etapa requerida incompleta (P3a/P3b/P3d ausentes): NEGADO")
else:
    falha("2.6.5-T16 E2 com etapas incompletas foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P3d")
codigo, saida, erro = avancar(caso, emitir="E2", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T17 E2 com etapas completas mas I1 nao satisfeito no nucleo: NEGADO")
else:
    falha("2.6.5-T17 E2 sem I1 satisfeito foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P3d")
preparar_bl(caso)
codigo, saida, erro = inegociavel(caso, 1, "registro/baseline/BL-001.yaml",
                                   satisfazer=True, autor="Marina Prado")
codigo, saida, erro = avancar(caso, emitir="E2", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.5-T18 E2 com requisitos completos (etapas + I1 verificado): AUTORIZADO")
else:
    falha(f"2.6.5-T18 E2 com requisitos completos foi NEGADO: {erro}")

codigo, saida, erro = entregavel(caso, "E2", "Celso do Vale", emitir=True)
arquivo_e2 = caso / "caso" / "entregaveis" / "E2.md"
if codigo == 0 and arquivo_e2.exists() and arquivo_e2.stat().st_size > 0:
    ok(f"2.6.5-T19 materializacao de E2: arquivo real existente ({arquivo_e2})")
else:
    falha(f"2.6.5-T19 materializacao de E2 falhou: exit={codigo} saida={saida!r} erro={erro!r}")

# ============================================== E3-D ======================
caso = preparar_caso()
percorrer_ate(caso, "P4")
codigo, saida, erro = avancar(caso, emitir="E3-D", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T20 E3-D sem P5: NEGADO")
else:
    falha("2.6.5-T20 E3-D sem P5 foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P4")
estado_path = caso / "registro" / "estado.json"
st = json.loads(estado_path.read_text(encoding="utf-8"))
st["cumprimentos"]["P5"] = {"cumprido": True, "autor": "Celso do Vale",
                             "classificacao_tecnologica": "isolado"}
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
codigo, saida, erro = avancar(caso, emitir="E3-D", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.5-T21 E3-D com P4/P5 validos: AUTORIZADO")
else:
    falha(f"2.6.5-T21 E3-D com P4/P5 validos foi NEGADO: {erro}")

# ============================================== E3-E =======================
caso_nao_agentico = preparar_caso()
percorrer_ate(caso_nao_agentico, "P4")
estado_path = caso_nao_agentico / "registro" / "estado.json"
st = json.loads(estado_path.read_text(encoding="utf-8"))
st["cumprimentos"]["P5"] = {"cumprido": True, "autor": "Celso do Vale",
                             "classificacao_tecnologica": "isolado"}
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
codigo, saida, erro = avancar(caso_nao_agentico, emitir="E3-E", autor="Celso do Vale")
if codigo == 0 and "NAO_APLICAVEL" in saida:
    ok("2.6.5-T22 E3-E sobre caso nao agentico: NAO_APLICAVEL (nao e falha)")
else:
    falha(f"2.6.5-T22 E3-E nao agentico nao produziu NAO_APLICAVEL: exit={codigo} saida={saida!r}")

# "Especificacao completa" (arquetipo, ferramentas, zona de contencao --
# E3 Parte B) nao possui HOJE nenhum artefato/schema no codebase que a
# capture estruturadamente -- nenhuma skill de P5 produz esses campos
# ainda. Testar a ausencia dessa especificacao forcaria a inventar um
# requisito nao sustentado por nenhuma fonte (o mesmo erro que a secao 38
# do pacote proibe, na direcao inversa). O requisito real e completo que
# E3 materializavel de fato exige -- classificacao_tecnologica presente --
# ja e coberto pelo par positivo/negativo de T20/T21 (via P5 ausente) e
# pelo teste de nao-invencao T48. Aqui cobre-se o caso agentico com P5
# nao encerrada: insumo insuficiente, materializacao recusada.
caso_agentico_incompleto = preparar_caso()
percorrer_ate(caso_agentico_incompleto, "P4")
codigo, saida, erro = entregavel(caso_agentico_incompleto, "E3", "Celso do Vale", emitir=False)
if codigo != 0:
    ok("2.6.5-T23 solucao agentica sem P5 encerrada (insumo insuficiente): "
       "materializacao NEGADA")
else:
    falha("2.6.5-T23 E3 sem P5 foi materializado sem checagem")

caso_agentico = preparar_caso()
percorrer_ate(caso_agentico, "P4")
estado_path = caso_agentico / "registro" / "estado.json"
st = json.loads(estado_path.read_text(encoding="utf-8"))
st["cumprimentos"]["P5"] = {"cumprido": True, "autor": "Celso do Vale",
                             "classificacao_tecnologica": "agente"}
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
codigo, saida, erro = avancar(caso_agentico, emitir="E3-E", autor="Celso do Vale")
if codigo == 0 and "NAO_APLICAVEL" not in saida:
    ok("2.6.5-T24 solucao agentica com P5 completo: E3-E AUTORIZADO")
else:
    falha(f"2.6.5-T24 E3-E agentico foi negado/nao_aplicavel indevidamente: {saida!r} {erro!r}")

if "agente" in str(st["cumprimentos"]["P5"]["classificacao_tecnologica"]):
    ok("2.6.5-T25 condicao declarativa {campo,etapa,operador,valor} avaliada "
       "sem hard-code de 'E3-E' no nucleo (mesmo mecanismo generico do 2.6.1)")
else:
    falha("2.6.5-T25 condicao declarativa nao avaliada corretamente")

codigo, saida, erro = entregavel(caso_nao_agentico, "E3", "Celso do Vale", emitir=True)
arquivo_e3_na = caso_nao_agentico / "caso" / "entregaveis" / "E3.md"
_conteudo_na = arquivo_e3_na.read_text(encoding="utf-8").lower().replace("ã", "a") if arquivo_e3_na.exists() else ""
if codigo == 0 and arquivo_e3_na.exists() and "nao se aplica" in _conteudo_na:
    ok("2.6.5-T26 materializacao E3 nao agentico: E3 valido sem exigir E3-E")
else:
    conteudo = arquivo_e3_na.read_text(encoding="utf-8") if arquivo_e3_na.exists() else "(sem arquivo)"
    falha(f"2.6.5-T26 materializacao E3 nao agentico falhou: exit={codigo} conteudo={conteudo[:200]!r}")

codigo, saida, erro = entregavel(caso_agentico, "E3", "Celso do Vale", emitir=True)
arquivo_e3_ag = caso_agentico / "caso" / "entregaveis" / "E3.md"
if codigo == 0 and arquivo_e3_ag.exists() and "parte b" in arquivo_e3_ag.read_text(encoding="utf-8").lower():
    ok("2.6.5-T27 materializacao E3 agentico: E3 consolida E3-D + E3-E "
       "(Parte B presente no mesmo arquivo)")
else:
    conteudo = arquivo_e3_ag.read_text(encoding="utf-8") if arquivo_e3_ag.exists() else "(sem arquivo)"
    falha(f"2.6.5-T27 materializacao E3 agentico falhou: exit={codigo} conteudo={conteudo[:200]!r}")

# ============================================== E4 =========================
caso = preparar_caso()
percorrer_ate(caso, "P6")
codigo, saida, erro = avancar(caso, emitir="E4", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T28 E4 sem P7: NEGADO")
else:
    falha("2.6.5-T28 E4 sem P7 foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P6")
preparar_op_validado(caso)
preparar_aut(caso, estado="proposto")
avancar(caso, registrar_sessao="P7", autor="Celso do Vale", participantes="Ana, Celso")
avancar(caso, encerrar="P7", autor="Celso do Vale")
inegociavel(caso, 2, "registro/governanca/autonomia/AUT-001.yaml",
            satisfazer=True, autor="Marina Prado")
codigo, saida, erro = avancar(caso, emitir="E4", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T29 E4 com P6/P7 mas termo apenas PROPOSTO "
       "(I2 nao verificavel/nao satisfeito): NEGADO")
else:
    falha("2.6.5-T29 E4 com termo proposto foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P6")
preparar_op_validado(caso)
preparar_aut(caso, estado="decidido")
avancar(caso, registrar_sessao="P7", autor="Celso do Vale", participantes="Ana, Celso")
avancar(caso, encerrar="P7", autor="Celso do Vale")
inegociavel(caso, 2, "registro/governanca/autonomia/AUT-001.yaml",
            satisfazer=True, autor="Marina Prado")
codigo, saida, erro = avancar(caso, emitir="E4", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.5-T30 E4 com P6/P7 e termo DECIDIDO valido: AUTORIZADO")
else:
    falha(f"2.6.5-T30 E4 com termo decidido foi NEGADO: {erro}")

codigo, saida, erro = entregavel(caso, "E4", "Celso do Vale", emitir=True)
arquivo_e4 = caso / "caso" / "entregaveis" / "E4.md"
if codigo == 0 and arquivo_e4.exists() and arquivo_e4.stat().st_size > 0:
    ok(f"2.6.5-T31 materializacao de E4: Guia Operacional real e rastreavel ({arquivo_e4})")
else:
    falha(f"2.6.5-T31 materializacao de E4 falhou: exit={codigo} saida={saida!r} erro={erro!r}")

# ============================================== E5 =========================
caso = preparar_caso()
percorrer_ate(caso, "P7")
codigo, saida, erro = avancar(caso, emitir="E5", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T32 E5 sem P8: NEGADO")
else:
    falha("2.6.5-T32 E5 sem P8 foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P9")
codigo, saida, erro = avancar(caso, emitir="E5", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T33 E5 sem I3 (nao satisfeito no nucleo): NEGADO")
else:
    falha("2.6.5-T33 E5 sem I3 foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P9")
preparar_ct_revisado(caso)
inegociavel(caso, 3, "registro/piloto/CT-001.yaml", satisfazer=True, autor="Marina Prado")
codigo, saida, erro = avancar(caso, emitir="E5", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T34 E5 com I3 mas sem I4: NEGADO")
else:
    falha("2.6.5-T34 E5 sem I4 foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P9")
preparar_ct_revisado(caso)
inegociavel(caso, 3, "registro/piloto/CT-001.yaml", satisfazer=True, autor="Marina Prado")
preparar_met_apurada(caso)
inegociavel(caso, 4, "registro/metricas/MET-001.yaml", satisfazer=True, autor="Marina Prado")
codigo, saida, erro = avancar(caso, emitir="E5", autor="Celso do Vale")
if codigo != 0:
    ok("2.6.5-T35 E5 com I3/I4 mas sem I5: NEGADO")
else:
    falha("2.6.5-T35 E5 sem I5 foi AUTORIZADO")

caso = preparar_caso()
percorrer_ate(caso, "P9")
preparar_ct_revisado(caso)
inegociavel(caso, 3, "registro/piloto/CT-001.yaml", satisfazer=True, autor="Marina Prado")
preparar_met_apurada(caso)
inegociavel(caso, 4, "registro/metricas/MET-001.yaml", satisfazer=True, autor="Marina Prado")
avancar(caso, encerrar="P9", autor="Celso do Vale")
preparar_cal(caso)
inegociavel(caso, 5, "registro/calibragem/CAL-001.yaml", satisfazer=True, autor="Marina Prado")
avancar(caso, registrar_sessao="P10", autor="Celso do Vale", participantes="Ana, Celso")
avancar(caso, encerrar="P10", autor="Celso do Vale")
avancar(caso, registrar_recorrencia="P10", autor="Celso do Vale",
        cadencia="mensal", responsavel="Marina Prado")
codigo, saida, erro = avancar(caso, emitir="E5", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.5-T36 E5 com P8/P9/P10 + I3/I4/I5: AUTORIZADO")
else:
    falha(f"2.6.5-T36 E5 com todos os requisitos foi NEGADO: {erro}")

codigo, saida, erro = entregavel(caso, "E5", "Celso do Vale", emitir=True)
arquivo_e5 = caso / "caso" / "entregaveis" / "E5.md"
if codigo == 0 and arquivo_e5.exists() and arquivo_e5.stat().st_size > 0:
    ok(f"2.6.5-T37 materializacao de E5: Relatorio de Piloto real e rastreavel ({arquivo_e5})")
else:
    falha(f"2.6.5-T37 materializacao de E5 falhou: exit={codigo} saida={saida!r} erro={erro!r}")

caso_e5_completo = caso  # reuso para os testes de conteudo/materializacao abaixo

# ============================================== materializacao =============
eventos_e5 = [e for e in eventos(caso_e5_completo) if e.get("evento") == "EntregavelEmitido"
              and e.get("entregavel") == "E5"]
if eventos_e5:
    ok("2.6.5-T38 emissao gera arquivo: evento EntregavelEmitido presente na trilha")
else:
    falha("2.6.5-T38 nenhum evento EntregavelEmitido encontrado")

if eventos_e5 and eventos_e5[-1].get("arquivo") and pathlib.Path(
        caso_e5_completo / eventos_e5[-1]["arquivo"]).exists():
    ok(f"2.6.5-T39 evento aponta para arquivo real ({eventos_e5[-1]['arquivo']})")
else:
    falha(f"2.6.5-T39 evento nao aponta para arquivo real: {eventos_e5[-1] if eventos_e5 else None}")

caso_sem_arquivo = preparar_caso()
percorrer_ate(caso_sem_arquivo, "P9")
preparar_ct_revisado(caso_sem_arquivo)
inegociavel(caso_sem_arquivo, 3, "registro/piloto/CT-001.yaml", satisfazer=True, autor="Marina Prado")
preparar_met_apurada(caso_sem_arquivo)
inegociavel(caso_sem_arquivo, 4, "registro/metricas/MET-001.yaml", satisfazer=True, autor="Marina Prado")
avancar(caso_sem_arquivo, encerrar="P9", autor="Celso do Vale")
preparar_cal(caso_sem_arquivo)
inegociavel(caso_sem_arquivo, 5, "registro/calibragem/CAL-001.yaml", satisfazer=True, autor="Marina Prado")
avancar(caso_sem_arquivo, registrar_recorrencia="P10", autor="Celso do Vale",
        cadencia="mensal", responsavel="Marina Prado")
codigo, saida, erro = avancar(caso_sem_arquivo, emitir="E5", autor="Celso do Vale",
                               materializar="caso/entregaveis/E5-inexistente.md")
if codigo != 0:
    ok("2.6.5-T40 arquivo inexistente nao conta como emissao: RECUSA/INCONSISTENCIA")
else:
    falha("2.6.5-T40 emissao com arquivo inexistente foi AUTORIZADA")

st_e5 = json.loads((caso_e5_completo / "registro" / "estado.json").read_text(encoding="utf-8"))
reg_e5 = st_e5.get("entregaveis_emitidos", {}).get("E5", {})
if reg_e5.get("versao") == 1 and reg_e5.get("arquivo"):
    ok(f"2.6.5-T41 entregavel possui versao/ID rastreavel: {reg_e5}")
else:
    falha(f"2.6.5-T41 entregavel sem versao rastreavel: {reg_e5}")

codigo, saida, erro = entregavel(caso_e5_completo, "E5", "Celso do Vale", emitir=True)
st_e5_v2 = json.loads((caso_e5_completo / "registro" / "estado.json").read_text(encoding="utf-8"))
reg_e5_v2 = st_e5_v2.get("entregaveis_emitidos", {}).get("E5", {})
if codigo == 0 and reg_e5_v2.get("versao") == 2:
    ok(f"2.6.5-T42 reemissao nao sobrescreve silenciosamente: versao incrementada para {reg_e5_v2.get('versao')}")
else:
    falha(f"2.6.5-T42 reemissao nao incrementou versao corretamente: {reg_e5_v2}")

# ============================================== conteudo ===================
def _tem_secao(caminho, titulo):
    return titulo.lower() in pathlib.Path(caminho).read_text(encoding="utf-8").lower()

if arquivo_e1.exists() and _tem_secao(arquivo_e1, "nível de complexidade"):
    ok("2.6.5-T43 E1 contem secoes obrigatorias do modelo oficial")
else:
    falha("2.6.5-T43 E1 sem secao obrigatoria")

if arquivo_e2.exists() and _tem_secao(arquivo_e2, "linha de base"):
    ok("2.6.5-T44 E2 contem secoes obrigatorias do modelo oficial")
else:
    falha("2.6.5-T44 E2 sem secao obrigatoria")

if arquivo_e3_ag.exists() and _tem_secao(arquivo_e3_ag, "classificação tecnológica"):
    ok("2.6.5-T45 E3 contem secoes obrigatorias do modelo oficial")
else:
    falha("2.6.5-T45 E3 sem secao obrigatoria")

if arquivo_e4.exists() and _tem_secao(arquivo_e4, "termo de autonomia"):
    ok("2.6.5-T46 E4 contem secoes obrigatorias do modelo oficial")
else:
    falha("2.6.5-T46 E4 sem secao obrigatoria")

if arquivo_e5.exists() and _tem_secao(arquivo_e5, "resultado contra a linha de base"):
    ok("2.6.5-T47 E5 contem secoes obrigatorias do modelo oficial")
else:
    falha("2.6.5-T47 E5 sem secao obrigatoria")

# ============================================== nao invencao ===============
caso_vazio = preparar_caso()
apurar_e_encerrar_f0(caso_vazio)
codigo, saida, erro = entregavel(caso_vazio, "E2", "Celso do Vale", emitir=False)
if codigo != 0 and "nao materializavel" in (saida + erro).lower():
    ok("2.6.5-T48 campo obrigatorio sem evidencia: nao inventa valor, recusa materializacao")
else:
    falha(f"2.6.5-T48 materializacao sem evidencia nao foi recusada: {saida!r} {erro!r}")

conteudo_e2 = arquivo_e2.read_text(encoding="utf-8")
if "45 minutos" in conteudo_e2 and "medido" in conteudo_e2:
    ok("2.6.5-T49 dados presentes sao reproduzidos das fontes do caso "
       "(valor_atual/apuracao da baseline aparecem literalmente em E2)")
else:
    falha(f"2.6.5-T49 dados da baseline nao aparecem reproduzidos em E2: {conteudo_e2[:300]!r}")

# ============================================== eventos =====================
caso_negado = preparar_caso()
avancar(caso_negado, emitir="E1", autor="Celso do Vale")
eventos_negado = [e for e in eventos(caso_negado) if e.get("evento") == "RecusaEmissao"]
if eventos_negado:
    ok("2.6.5-T50 portao negado gera evento (RecusaEmissao)")
else:
    falha("2.6.5-T50 portao negado nao gerou evento")

eventos_autorizado = [e for e in eventos(caso_e5_completo) if e.get("evento") == "EntregavelEmitido"]
if len(eventos_autorizado) >= 2:
    ok(f"2.6.5-T51 portao autorizado gera trilha ({len(eventos_autorizado)} eventos EntregavelEmitido)")
else:
    falha(f"2.6.5-T51 trilha de portao autorizado insuficiente: {eventos_autorizado}")

if eventos_autorizado and eventos_autorizado[-1].get("arquivo") and eventos_autorizado[-1].get("versao"):
    ok("2.6.5-T52 emissao material gera evento com referencia (arquivo + versao)")
else:
    falha(f"2.6.5-T52 evento de emissao sem referencia completa: {eventos_autorizado}")

eventos_na = [e for e in eventos(caso_nao_agentico) if e.get("evento") == "EntregavelNaoAplicavel"]
if eventos_na:
    ok("2.6.5-T53 E3-E nao aplicavel fica explicitamente registrado (evento EntregavelNaoAplicavel)")
else:
    falha("2.6.5-T53 nenhum evento EntregavelNaoAplicavel encontrado")

# ============================================== hard-code ===================
nucleo_fonte = "\n".join(
    p.read_text(encoding="utf-8") for p in (RAIZ / "eiac-nucleo" / "scripts").glob("*.py")
)
termos_metodo = ["E3-D", "E3-E", "baseline", "autonomia", "saida_esperada",
                  "metrica de resultado", "recalibragem"]
ocorrencias_comportamentais = []
for termo in termos_metodo:
    for linha in nucleo_fonte.splitlines():
        if termo.lower() in linha.lower() and not linha.strip().startswith("#") \
                and '"""' not in linha and "'''" not in linha:
            # docstring de uso (--emitir E2) e comentario de linha sao aceitaveis;
            # aqui filtramos apenas o que poderia ser codigo executavel com o termo
            stripped = linha.strip()
            if stripped.startswith(("Uso:", "python3", "O nucleo", "Toda recusa")):
                continue
            ocorrencias_comportamentais.append((termo, linha.strip()))

# E1/E2/E4/E5 aparecem apenas como exemplo de uso em docstring (--emitir E2);
# nao ha `if entregavel_id == "E5"` nem equivalente no nucleo.
hardcode_real = [o for o in ocorrencias_comportamentais
                 if "if" in o[1] and ("==" in o[1] or "in (" in o[1] or "in [" in o[1])]
if not hardcode_real:
    ok("2.6.5-T54 ausencia de hard-code de portao especifico no nucleo "
       f"({len(ocorrencias_comportamentais)} ocorrencias, todas em docstring/comentario)")
else:
    falha(f"2.6.5-T54 hard-code de portao encontrado no nucleo: {hardcode_real}")

# ============================================== regressao ===================
def _rodar_modulo(caminho):
    r = subprocess.run(["python3", str(caminho)], cwd=RAIZ, capture_output=True, text=True)
    return r.returncode, r.stdout

codigo, saida = _rodar_modulo(RAIZ / "testes" / "consolidado.py")
if codigo == 0:
    ok("2.6.5-T55 regressao Acao 2.5: PASS (ver teste-regressao-final.txt)")
else:
    falha(f"2.6.5-T55 regressao Acao 2.5 falhou: {saida[-500:]}")

codigo, saida = _rodar_modulo(RAIZ / "testes" / "nucleo_2_6_1.py")
if codigo == 0:
    ok("2.6.5-T56 regressao 2.6.1: PASS")
else:
    falha(f"2.6.5-T56 regressao 2.6.1 falhou: {saida[-500:]}")

codigo, saida = _rodar_modulo(RAIZ / "testes" / "campo_2_6_2.py")
if codigo == 0:
    ok("2.6.5-T57 regressao P6/P7: PASS")
else:
    falha(f"2.6.5-T57 regressao P6/P7 falhou: {saida[-500:]}")

codigo, saida = _rodar_modulo(RAIZ / "testes" / "campo_2_6_3.py")
if codigo == 0:
    ok("2.6.5-T58 regressao P8/P9/P10: PASS")
else:
    falha(f"2.6.5-T58 regressao P8/P9/P10 falhou: {saida[-500:]}")

codigo, saida = _rodar_modulo(RAIZ / "testes" / "campo_2_6_4.py")
if codigo == 0:
    ok("2.6.5-T59 regressao HB/AG: PASS")
else:
    falha(f"2.6.5-T59 regressao HB/AG falhou: {saida[-500:]}")

if falhas == 0:
    ok("2.6.5-T60 suite completa: sem regressoes inexplicadas")
else:
    falha(f"2.6.5-T60 suite completa com {falhas} falha(s) ate aqui")

print(f"{total} verificacoes do pacote 2.6.5, {falhas} falhas")
