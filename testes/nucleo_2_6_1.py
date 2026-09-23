#!/usr/bin/env python3
"""Verificacao do nucleo generico de protocolos -- pacote 2.6.1.

Cobre: etapa corrente, dependencias, delegabilidade, camadas EX,
criterio de verificacao (mecanismo isolado), recorrencia, cadencia,
responsavel nominal, inegociaveis por caminho autorizado, protecao de
registro/, integridade de portoes/condicoes e eventos de recusa.

Nenhum teste aqui deve depender de um nome literal de etapa alem do que o
proprio playbook oficial ja declara (P1..P10 aparecem como dados, nunca
como decisao hard-coded do nucleo).
"""
import copy
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = RAIZ / "eiac-campo" / "template-caso"
AVANCAR = RAIZ / "eiac-nucleo" / "scripts" / "avancar.py"
GUARDA = RAIZ / "eiac-nucleo" / "scripts" / "guarda.py"
SELAR = RAIZ / "eiac-nucleo" / "scripts" / "selar.py"
PLAYBOOK_SCRIPT = RAIZ / "eiac-nucleo" / "scripts" / "playbook.py"

sys.path.insert(0, str(RAIZ / "eiac-nucleo" / "scripts"))
import playbook as P  # noqa: E402

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
    # Autoria de registro (validar.py/curar.py/selar.py) le responsavel do
    # estado, fixado por novo-caso.sh fora da sessao do agente -- simula
    # esse passo aqui, ja que o teste monta o caso direto do template.
    estado_path = caso / "registro" / "estado.json"
    estado = json.loads(estado_path.read_text(encoding="utf-8"))
    estado["responsavel"] = "Celso do Vale"
    estado_path.write_text(json.dumps(estado, ensure_ascii=False), encoding="utf-8")
    # selar.py exige repositorio git (decisao 021: P3b exige selo posterior
    # ao encerramento de P2) -- percorrer_ate() precisa poder selar.
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


def eventos(caso):
    log = caso / "registro" / "eventos.jsonl"
    if not log.exists():
        return []
    return [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]


def apurar_e_encerrar_f0(caso):
    avancar(caso, apurar_nivel="N1", autor="Celso do Vale", eixos="DAD 3, GOV 3, CRI 3")
    return avancar(caso, encerrar="F0", autor="Celso do Vale")


ETAPAS_NAO_DELEGAVEIS = {e["id"] for e in pb_oficial["etapas"] if e.get("delegavel") is False}


# Referencias de exige_selo_apos, invertidas: para cada etapa-alvo (valor),
# a lista de ids de etapa que exigem selo posterior a ela. Generico -- nao
# assume que so P3b declara a exigencia, nem que o alvo e sempre P2.
ETAPAS_QUE_EXIGEM_SELO_DE = {}
for _e in pb_oficial["etapas"]:
    _ref = _e.get("exige_selo_apos")
    if _ref:
        ETAPAS_QUE_EXIGEM_SELO_DE.setdefault(_ref, []).append(_e["id"])


def percorrer_ate(caso, ate_etapa_id):
    """Encerra F0 e todas as etapas ate (e incluindo) ate_etapa_id, em
    ordem, registrando sessao para as etapas nao delegaveis do playbook e
    selando o caso logo apos encerrar qualquer etapa que seja referenciada
    por 'exige_selo_apos' de uma etapa AINDA POR VIR no percurso (decisao
    021) -- nao depende de a etapa exigente ser a proxima imediata (pode
    haver etapas intermediarias entre a etapa referenciada e a que exige
    o selo, como P3a entre P2 e P3b).
    """
    apurar_e_encerrar_f0(caso)
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


print("== testes 2.6.1 -- nucleo generico de protocolos")

# --- T01/T02: etapa corrente ---------------------------------------------
caso = preparar_caso()
apurar_e_encerrar_f0(caso)
# apos F0, etapa corrente e P1 (primeira etapa do playbook oficial)
codigo, saida, erro = avancar(caso, encerrar="P5", autor="Celso do Vale")
if codigo != 0 and "nao e a etapa corrente" in erro:
    ok(f"2.6.1-T01 encerrar etapa que NAO e corrente recusado ({erro.strip()})")
else:
    falha(f"2.6.1-T01 encerrar etapa fora de ordem foi ACEITO: exit={codigo} stderr={erro}")

evs = eventos(caso)
if any(e.get("evento") == "RecusaMaquina" and e.get("acao_tentada") == "encerrar" for e in evs):
    ok("2.6.1-T01b recusa de etapa fora de ordem gera evento RecusaMaquina")
else:
    falha("2.6.1-T01b recusa de etapa fora de ordem NAO gerou evento")

codigo, saida, erro = avancar(caso, encerrar="P1", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.1-T02 encerrar etapa corrente valida aceito")
else:
    falha(f"2.6.1-T02 encerrar etapa corrente RECUSADO: {erro}")

# --- T03/T04: dependencias -------------------------------------------------
# P3d depende de P3b e e delegavel (EX3, nao EX4) -- isola a checagem G3
# (dependencia) da checagem G1 (camada humana), que testamos em T06.
caso_dep = preparar_caso()
apurar_e_encerrar_f0(caso_dep)
for e in ["P1", "P2", "P3a"]:
    avancar(caso_dep, encerrar=e, autor="Celso do Vale")
# nao registra sessao nem encerra P3b -- forca o estado para P3d (que
# depende de P3b) sem que P3b esteja cumprida, e usa avancar.py --encerrar,
# que aplica a mesma checagem de dependencia que guarda.py usa (G3).
estado_path = caso_dep / "registro" / "estado.json"
st = json.loads(estado_path.read_text(encoding="utf-8"))
st["etapa_atual"] = "P3d"
st["camada_atual"] = "EX3"
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
codigo, saida, erro = avancar(caso_dep, encerrar="P3d", autor="Celso do Vale")
if codigo != 0 and "depende de" in erro:
    ok(f"2.6.1-T03 dependencia nao satisfeita bloqueada ({erro.strip()})")
else:
    falha(f"2.6.1-T03 dependencia nao satisfeita NAO foi bloqueada: exit={codigo} stderr={erro}")

# tambem confirma que a guarda (G3, fora do avancar.py) bloqueia qualquer
# ferramenta nessa condicao -- alvo neutro (nao casa com nenhuma
# 'habilidade' do playbook), para isolar G3 de G1
codigo, saida, erro = guarda(caso_dep, "Read", {"file_path": "fontes/documento-generico.md"})
if codigo == 2 and "depende de" in erro:
    ok(f"2.6.1-T03b guarda (G3) tambem bloqueia dependencia nao satisfeita ({erro.strip()})")
else:
    falha(f"2.6.1-T03b guarda NAO bloqueou dependencia nao satisfeita: exit={codigo} stderr={erro}")

caso = preparar_caso()
apurar_e_encerrar_f0(caso)
for e in ["P1", "P2", "P3a"]:
    avancar(caso, encerrar=e, autor="Celso do Vale")
selar(caso, "selo apos P2, exigido por P3b")
avancar(caso, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")
avancar(caso, encerrar="P3b", autor="Celso do Vale")
if avancar(caso, encerrar="P3d", autor="Celso do Vale")[0] == 0:
    ok("2.6.1-T04 dependencia satisfeita permite prosseguir")
else:
    falha("2.6.1-T04 dependencia satisfeita foi RECUSADA")

# --- T05/T06/T07: delegabilidade -------------------------------------------
caso = preparar_caso()
apurar_e_encerrar_f0(caso)
codigo, saida, erro = avancar(caso, encerrar="P1", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.1-T05 etapa delegavel executada por ator permitido: PASS")
else:
    falha(f"2.6.1-T05 etapa delegavel RECUSADA: {erro}")

for e in ["P2", "P3a"]:
    avancar(caso, encerrar=e, autor="Celso do Vale")
selar(caso, "selo apos P2, exigido por P3b")
# etapa corrente agora e P3b, delegavel:false
codigo, saida, erro = guarda(caso, "Read", {"file_path": "skills/hb-levantar-regras/SKILL.md"})
if codigo == 2 and "delegavel" in erro:
    ok(f"2.6.1-T06 etapa nao delegavel tentada por agente recusada ({erro.strip()})")
else:
    falha(f"2.6.1-T06 etapa nao delegavel NAO foi bloqueada: exit={codigo} stderr={erro}")

avancar(caso, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")
codigo, saida, erro = avancar(caso, encerrar="P3b", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.1-T07 etapa nao delegavel encerrada por humano autorizado apos sessao: PASS")
else:
    falha(f"2.6.1-T07 etapa nao delegavel com sessao registrada foi RECUSADA: {erro}")

# --- T08: camada invalida (fixture temporaria) ------------------------------


def rodar_playbook_py(pb_dict):
    tmp = pathlib.Path(tempfile.mkdtemp())
    (tmp / "registro").mkdir()
    (tmp / "registro" / "playbook.json").write_text(
        json.dumps(pb_dict, ensure_ascii=False, indent=2), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(PLAYBOOK_SCRIPT)], cwd=tmp,
                           text=True, capture_output=True, check=False)
    shutil.rmtree(tmp, ignore_errors=True)
    return proc.returncode, proc.stdout, proc.stderr


pb_t08 = copy.deepcopy(pb_oficial)
for e in pb_t08["etapas"]:
    if e["id"] == "P1":
        e["camada"] = {n: "EX5" for n in pb_t08["niveis"]}
codigo, saida, erro = rodar_playbook_py(pb_t08)
if codigo != 0:
    ok(f"2.6.1-T08 camada invalida recusada pelo contrato ({erro.strip()})")
else:
    falha("2.6.1-T08 camada invalida foi ACEITA")

# --- T09/T10: criterio de verificacao (mecanismo isolado, fixtures sinteticas) ---
sem_criterio = {"automatizado": True, "criterio_de_verificacao": None}
valido, motivo = P.capacidade_valida(sem_criterio)
if not valido and "criterio_de_verificacao" in motivo:
    ok(f"2.6.1-T09 capacidade automatizada sem criterio_de_verificacao recusada ({motivo})")
else:
    falha(f"2.6.1-T09 capacidade sem criterio foi ACEITA: valido={valido} motivo={motivo}")

com_criterio = {"automatizado": True, "criterio_de_verificacao": "saida revisada por humano"}
valido, motivo = P.capacidade_valida(com_criterio)
if valido:
    ok("2.6.1-T10 capacidade automatizada com criterio_de_verificacao aceita")
else:
    falha(f"2.6.1-T10 capacidade com criterio foi RECUSADA: {motivo}")

nao_automatizada = {"automatizado": False}
valido, motivo = P.capacidade_valida(nao_automatizada)
if valido:
    ok("2.6.1-T10b capacidade nao automatizada nao exige criterio (controle)")
else:
    falha(f"2.6.1-T10b capacidade nao automatizada foi RECUSADA indevidamente: {motivo}")

print("  INTEGRACAO COM HB/AG REAIS DO PLAYBOOK: PENDENTE 2.6.4 -- mecanismo "
      "generico testado isoladamente (T09/T10), sem bloco 'capacidades' no "
      "playbook oficial. Conforme decisao registrada no pacote.")

# --- T11/T12: responsavel nominal obrigatorio -------------------------------
caso = preparar_caso()
percorrer_ate(caso, "P10")
# etapa corrente agora e a seguinte a P10 (ou P10 permanece se for a
# ultima); em qualquer caso P10 ja foi encerrada ao menos uma vez.
codigo, saida, erro = avancar(caso, registrar_recorrencia="P10", autor="Celso do Vale",
                               cadencia="trimestral", responsavel="")
if codigo != 0 and "responsavel" in erro:
    ok(f"2.6.1-T11 responsavel obrigatorio ausente recusado ({erro.strip()})")
else:
    falha(f"2.6.1-T11 recorrencia sem responsavel foi ACEITA: exit={codigo} stderr={erro}")

codigo, saida, erro = avancar(caso, registrar_recorrencia="P10", autor="Celso do Vale",
                               cadencia="trimestral", responsavel="Marina Prado")
if codigo == 0:
    ok("2.6.1-T12 responsavel nominal valido aceito")
else:
    falha(f"2.6.1-T12 responsavel nominal valido foi RECUSADO: {erro}")

# controle: nome generico ("equipe") tambem deve ser recusado
codigo, saida, erro = avancar(caso, registrar_recorrencia="P10", autor="Celso do Vale",
                               cadencia="trimestral", responsavel="equipe")
if codigo != 0:
    ok(f"2.6.1-T12b responsavel generico ('equipe') recusado ({erro.strip()})")
else:
    falha("2.6.1-T12b responsavel generico 'equipe' foi ACEITO")

# --- T13/T14: cadencia obrigatoria ------------------------------------------
caso2 = preparar_caso()
percorrer_ate(caso2, "P10")
codigo, saida, erro = avancar(caso2, registrar_recorrencia="P10", autor="Celso do Vale",
                               cadencia="", responsavel="Marina Prado")
if codigo != 0 and "cadencia" in erro:
    ok(f"2.6.1-T13 cadencia obrigatoria ausente recusada ({erro.strip()})")
else:
    falha(f"2.6.1-T13 recorrencia sem cadencia foi ACEITA: exit={codigo} stderr={erro}")

codigo, saida, erro = avancar(caso2, registrar_recorrencia="P10", autor="Celso do Vale",
                               cadencia="trimestral", responsavel="Marina Prado")
if codigo == 0:
    ok("2.6.1-T14 cadencia valida aceita")
else:
    falha(f"2.6.1-T14 cadencia valida foi RECUSADA: {erro}")

# --- T15/T16: etapa recorrente sem/com contrato suficiente ------------------
pb_t15 = copy.deepcopy(pb_oficial)
for e in pb_t15["etapas"]:
    if e["id"] == "P10":
        e.pop("cadencia_obrigatoria", None)
codigo, saida, erro = rodar_playbook_py(pb_t15)
if codigo != 0 and "recorrente" in erro:
    ok(f"2.6.1-T15 recorrente sem contrato suficiente recusado no carregamento ({erro.strip()})")
else:
    falha(f"2.6.1-T15 recorrente sem cadencia_obrigatoria foi ACEITO: exit={codigo}")

codigo, saida, erro = rodar_playbook_py(pb_oficial)
if codigo == 0:
    ok("2.6.1-T16 recorrente com contrato suficiente aceito no carregamento")
else:
    falha(f"2.6.1-T16 playbook oficial (P10 recorrente valido) foi RECUSADO: {erro}")

# --- T17/T18/T19/T20: inegociaveis -------------------------------------------
caso = preparar_caso()
apurar_e_encerrar_f0(caso)
for e in ["P1", "P2", "P3a"]:
    avancar(caso, encerrar=e, autor="Celso do Vale")
selar(caso, "selo apos P2, exigido por P3b")
avancar(caso, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")
avancar(caso, encerrar="P3b", autor="Celso do Vale")
avancar(caso, encerrar="P3d", autor="Celso do Vale")
codigo, saida, erro = avancar(caso, emitir="E2", autor="Celso do Vale")
if codigo != 0 and "inegociavel" in erro:
    ok(f"2.6.1-T17 inegociavel sem satisfacao mantem portao fechado ({erro.strip()})")
else:
    falha(f"2.6.1-T17 emissao com inegociavel insatisfeito foi ACEITA: exit={codigo}")

codigo, saida, erro = guarda(caso, "Write", {"file_path": "registro/estado.json", "content": "{}"})
if codigo == 2:
    ok(f"2.6.1-T18 tentativa de satisfazer inegociavel por escrita direta em estado recusada ({erro.strip()})")
else:
    falha(f"2.6.1-T18 escrita direta em estado NAO foi bloqueada: exit={codigo}")

codigo, saida, erro = avancar(caso, satisfazer_inegociavel="1", autor="Celso do Vale", evidencia="")
if codigo != 0 and "evidencia" in erro:
    ok(f"2.6.1-T19 satisfazer inegociavel sem evidencia exigida recusado ({erro.strip()})")
else:
    falha(f"2.6.1-T19 satisfazer inegociavel sem evidencia foi ACEITO: exit={codigo}")

codigo, saida, erro = avancar(caso, satisfazer_inegociavel="1", autor="Celso do Vale",
                               evidencia="linha de base registrada em caso/P3a-linha-base.md")
if codigo == 0:
    ok("2.6.1-T20 satisfazer inegociavel por caminho autorizado valido aceito")
else:
    falha(f"2.6.1-T20 satisfazer inegociavel valido foi RECUSADO: {erro}")
evs = eventos(caso)
if any(e.get("evento") == "InegociavelSatisfeito" for e in evs):
    ok("2.6.1-T20b evento InegociavelSatisfeito presente")
else:
    falha("2.6.1-T20b evento InegociavelSatisfeito AUSENTE")

codigo, saida, erro = avancar(caso, emitir="E2", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.1-T20c E2 emite apos inegociavel 1 satisfeito por caminho autorizado")
else:
    falha(f"2.6.1-T20c E2 foi RECUSADO apos inegociavel satisfeito: {erro}")

# --- T21/T22: protecao de registro/ -----------------------------------------
caso = preparar_caso()
codigo, saida, erro = guarda(caso, "Write", {"file_path": "registro/estado.json", "content": "{}"})
if codigo == 2 and "registro/" in erro:
    ok(f"2.6.1-T21 escrita direta em registro/ recusada ({erro.strip()})")
else:
    falha(f"2.6.1-T21 escrita direta em registro/ NAO foi bloqueada: exit={codigo} stderr={erro}")

codigo, saida, erro = guarda(caso, "Bash", {
    "command": f"python3 {AVANCAR} --apurar-nivel N1 --autor 'Celso' --eixos 'DAD 3'"
})
if codigo == 0:
    ok("2.6.1-T22 escrita autorizada em registro/ (via avancar.py) funcional")
else:
    falha(f"2.6.1-T22 chamada autorizada ao nucleo foi bloqueada pela guarda: exit={codigo} stderr={erro}")

# --- T23/T24: regressao de contexto/ (Acao 2.5) ------------------------------
caso = preparar_caso()
codigo, saida, erro = guarda(caso, "Write", {"file_path": "contexto/regras/RN-001.yaml", "content": "x"})
if codigo == 2 and "contexto/" in erro:
    ok(f"2.6.1-T23 escrita direta em contexto/ continua recusada ({erro.strip()})")
else:
    falha(f"2.6.1-T23 escrita direta em contexto/ NAO foi bloqueada: exit={codigo}")

CURADOR = RAIZ / "eiac-nucleo" / "scripts" / "curar.py"
termo_yaml = (
    'id: T-900\n'
    'termo: guia de autorizacao\n'
    'significado: documento que autoriza a emissao do procedimento\n'
    'nao_e: a guia de encaminhamento medico\n'
    'sinonimos_em_uso: []\n'
    'procedencia: D\n'
    'declarado_por: Ana Paula\n'
    'registrado_por: Celso do Vale\n'
    'data: "2026-09-18"\n'
    'premissa: ""\n'
    'evidencia: ""\n'
    'versao: 1\n'
)
(caso / "rascunho" / "T-900.yaml").write_text(termo_yaml, encoding="utf-8")
proc = subprocess.run(
    ["python3", str(CURADOR), "--tipo", "termo", "--arquivo", "contexto/termos/T-900.yaml",
     "--registrado-por", "Celso do Vale"],
    cwd=caso, text=True, capture_output=True, check=False,
)
if proc.returncode == 0:
    ok("2.6.1-T24 escrita autorizada em contexto/ (via curar.py) continua funcional")
else:
    falha(f"2.6.1-T24 curadoria autorizada foi RECUSADA apos as mudancas do nucleo: {proc.stderr}")

# --- T25/T26: integridade de portoes -----------------------------------------
pb_t25 = copy.deepcopy(pb_oficial)
for d in pb_t25["entregaveis"]:
    if d["id"] == "E1":
        d["portao"] = ["P99"]
codigo, saida, erro = rodar_playbook_py(pb_t25)
if codigo != 0 and "inexistente" in erro:
    ok(f"2.6.1-T25 portao com etapa inexistente recusado ({erro.strip()})")
else:
    falha(f"2.6.1-T25 portao com etapa inexistente foi ACEITO: exit={codigo}")

pb_t26 = copy.deepcopy(pb_oficial)
for d in pb_t26["entregaveis"]:
    if d["id"] == "E4":
        d["inegociavel"] = [99]
codigo, saida, erro = rodar_playbook_py(pb_t26)
if codigo != 0 and "inegociavel" in erro:
    ok(f"2.6.1-T26 portao com inegociavel inexistente recusado ({erro.strip()})")
else:
    falha(f"2.6.1-T26 portao com inegociavel inexistente foi ACEITO: exit={codigo}")

# --- T27/T28: condicoes declarativas -----------------------------------------
caso = preparar_caso()
apurar_e_encerrar_f0(caso)
for e in ["P1", "P2", "P3a"]:
    avancar(caso, encerrar=e, autor="Celso do Vale")
selar(caso, "selo apos P2, exigido por P3b")
avancar(caso, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")
for e in ["P3b", "P3d"]:
    avancar(caso, encerrar=e, autor="Celso do Vale")
avancar(caso, encerrar="P4", autor="Celso do Vale")
# forca o cumprimento de P5 com o campo que a condicao declarativa de E3-E
# consulta (classificacao_tecnologica), simulando o que uma skill de P5
# gravaria -- o nucleo so le o campo, nao decide seu significado.
estado_path = caso / "registro" / "estado.json"
st = json.loads(estado_path.read_text(encoding="utf-8"))
st["cumprimentos"]["P5"] = {"cumprido": True, "autor": "Celso do Vale",
                             "classificacao_tecnologica": "agente"}
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
codigo, saida, erro = avancar(caso, emitir="E3-E", autor="Celso do Vale")
if codigo == 0:
    ok("2.6.1-T27 condicao declarativa suportada avaliada corretamente (satisfeita)")
else:
    falha(f"2.6.1-T27 condicao declarativa satisfeita foi RECUSADA: {erro}")

st["cumprimentos"]["P5"]["classificacao_tecnologica"] = "habilitador"
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
codigo, saida, erro = avancar(caso, emitir="E3-E", autor="Celso do Vale")
# Desde 2.6.5 (secao 24 do pacote), condicao declarativa nao satisfeita e
# NAO_APLICAVEL (exit 0), nao RECUSA (exit != 0) -- "nao aplicavel" nao e
# falha. O teste original (2.6.1) esperava recusa; corrigido aqui para o
# contrato que 2.6.5 formalizou.
if codigo == 0 and "NAO_APLICAVEL" in saida:
    ok(f"2.6.1-T27b condicao declarativa nao satisfeita e NAO_APLICAVEL, nao recusa ({saida.strip()})")
else:
    falha(f"2.6.1-T27b condicao nao satisfeita nao produziu NAO_APLICAVEL: exit={codigo} saida={saida!r} erro={erro!r}")

pb_t28 = copy.deepcopy(pb_oficial)
for d in pb_t28["entregaveis"]:
    if d["id"] == "E3-E":
        d["condicao"]["operador"] = "operador_desconhecido"
codigo, saida, erro = rodar_playbook_py(pb_t28)
if codigo != 0 and "operador" in erro:
    ok(f"2.6.1-T28 condicao declarativa desconhecida recusada explicitamente no carregamento ({erro.strip()})")
else:
    falha(f"2.6.1-T28 operador desconhecido foi ACEITO pelo carregador: exit={codigo}")

# --- T29/T30: eventos de recusa ----------------------------------------------
caso = preparar_caso()
apurar_e_encerrar_f0(caso)
avancar(caso, encerrar="P9", autor="Celso do Vale")  # fora de ordem: corrente e P1
evs = eventos(caso)
if any(e.get("evento") == "RecusaMaquina" for e in evs):
    ok("2.6.1-T29 recusa de avancar (fora de ordem) gera evento")
else:
    falha("2.6.1-T29 recusa de avancar NAO gerou evento")

avancar(caso, emitir="E5", autor="Celso do Vale")  # portao fechado
evs = eventos(caso)
if any(e.get("evento") == "RecusaEmissao" for e in evs):
    ok("2.6.1-T30 recusa de emissao gera evento")
else:
    falha("2.6.1-T30 recusa de emissao NAO gerou evento")

# --- T31: protecao de caso/ (revalidacao, nao reimplementacao) ---------------
caso = preparar_caso()
codigo, saida, erro = guarda(caso, "Write", {"file_path": "caso/x.md", "content": "texto"})
if codigo == 2 and "caso/" in erro:
    ok(f"2.6.1-T31 protecao de caso/ continua ativa ({erro.strip()})")
else:
    falha(f"2.6.1-T31 protecao de caso/ NAO esta ativa: exit={codigo}")

# --- T32: selo git continua funcional ----------------------------------------
caso = preparar_caso()
subprocess.run(["git", "init", "-q"], cwd=caso, check=False)
subprocess.run(["git", "config", "user.email", "teste@example.com"], cwd=caso, check=False)
subprocess.run(["git", "config", "user.name", "Teste"], cwd=caso, check=False)
(caso / "rascunho" / "ping.txt").write_text("marcador\n", encoding="utf-8")
proc = subprocess.run(["python3", str(SELAR), "--autor", "Celso do Vale", "--nota", "teste 2.6.1"],
                       cwd=caso, text=True, capture_output=True, check=False)
if proc.returncode == 0 and "selado" in proc.stdout:
    ok("2.6.1-T32 selo git continua funcional apos as mudancas do nucleo")
else:
    falha(f"2.6.1-T32 selo git falhou: exit={proc.returncode} stdout={proc.stdout} stderr={proc.stderr}")

print()
print(f"{total} verificacoes do pacote 2.6.1, {falhas} falhas")
if falhas:
    sys.exit(1)
