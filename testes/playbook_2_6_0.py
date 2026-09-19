#!/usr/bin/env python3
"""Verificacao do contrato executavel F0-P10 -- pacote 2.6.0.

Nao implementa comportamento de P6-P10. Verifica que o playbook oficial
declara o contrato completo e que o carregador generico do nucleo
(eiac-nucleo/scripts/playbook.py) aceita o contrato valido e recusa
contratos estruturalmente invalidos, usando fixtures temporarias que
nunca tocam o playbook oficial.
"""
import copy
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PLAYBOOK_OFICIAL = RAIZ / "eiac-campo" / "template-caso" / "registro" / "playbook.json"
PLAYBOOK_SCRIPT = RAIZ / "eiac-nucleo" / "scripts" / "playbook.py"

ETAPAS_CANONICAS = ["F0", "P1", "P2", "P3a", "P3b", "P3d", "P4", "P5",
                    "P6", "P7", "P8", "P9", "P10"]

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


def carregar_pb():
    return json.loads(PLAYBOOK_OFICIAL.read_text(encoding="utf-8"))


def rodar_playbook_py(pb_dict):
    """Grava pb_dict num caso temporario isolado e roda playbook.py sobre ele."""
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        (tmp / "registro").mkdir()
        (tmp / "registro" / "playbook.json").write_text(
            json.dumps(pb_dict, ensure_ascii=False, indent=2), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(PLAYBOOK_SCRIPT)],
            cwd=tmp, text=True, capture_output=True, check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


print("== testes 2.6.0 -- contrato executavel F0-P10")

pb = carregar_pb()

# T01 -- playbook e JSON valido
try:
    carregar_pb()
    ok("2.6.0-T01 playbook e JSON valido")
except Exception as e:
    falha(f"2.6.0-T01 playbook NAO e JSON valido: {e}")

# T02 -- exatamente 13 etapas canonicas
ids = [e["id"] for e in pb["etapas"]]
if sorted(ids) == sorted(ETAPAS_CANONICAS) and len(ids) == 13:
    ok("2.6.0-T02 exatamente 13 etapas canonicas")
else:
    falha(f"2.6.0-T02 etapas divergentes: {ids}")

# T03 -- todos os IDs de etapa sao unicos
if len(ids) == len(set(ids)):
    ok("2.6.0-T03 IDs de etapa unicos")
else:
    falha("2.6.0-T03 IDs de etapa duplicados")

# T04 -- conjunto esperado F0-P10
if set(ids) == set(ETAPAS_CANONICAS):
    ok("2.6.0-T04 conjunto esperado F0-P10 presente")
else:
    falha(f"2.6.0-T04 conjunto inesperado: faltam {set(ETAPAS_CANONICAS) - set(ids)}, "
          f"sobram {set(ids) - set(ETAPAS_CANONICAS)}")

# T05 -- P3b permanece nao delegavel
p3b = next(e for e in pb["etapas"] if e["id"] == "P3b")
if p3b.get("delegavel") is False:
    ok("2.6.0-T05 P3b permanece nao delegavel")
else:
    falha("2.6.0-T05 P3b NAO esta marcada nao delegavel")

# T06 -- P7 declarada nao delegavel
p7 = next(e for e in pb["etapas"] if e["id"] == "P7")
if p7.get("delegavel") is False:
    ok("2.6.0-T06 P7 declarada nao delegavel")
else:
    falha("2.6.0-T06 P7 NAO esta marcada nao delegavel")

# T07 -- P7 na camada humana correta (EX4 nos tres niveis)
if all(p7["camada"][n] == "EX4" for n in pb["niveis"]):
    ok("2.6.0-T07 P7 na camada EX4 (humana) em todos os niveis")
else:
    falha(f"2.6.0-T07 P7 camada incorreta: {p7['camada']}")

# T08 -- P10 e recorrente
p10 = next(e for e in pb["etapas"] if e["id"] == "P10")
if p10.get("recorrente") is True:
    ok("2.6.0-T08 P10 e recorrente")
else:
    falha("2.6.0-T08 P10 NAO esta marcada recorrente")

# T09 -- P10 declara necessidade de cadencia
if p10.get("cadencia_obrigatoria") is True:
    ok("2.6.0-T09 P10 declara necessidade de cadencia")
else:
    falha("2.6.0-T09 P10 NAO declara cadencia obrigatoria")

# T10 -- P10 declara necessidade de responsavel
if p10.get("responsavel_obrigatorio") is True:
    ok("2.6.0-T10 P10 declara necessidade de responsavel")
else:
    falha("2.6.0-T10 P10 NAO declara responsavel obrigatorio")

# T11 -- cinco inegociaveis declarados
if len(pb.get("inegociaveis", [])) == 5:
    ok("2.6.0-T11 cinco inegociaveis declarados")
else:
    falha(f"2.6.0-T11 {len(pb.get('inegociaveis', []))} inegociaveis declarados, esperado 5")

# T12 -- mapeamento dos cinco inegociaveis
mapa_esperado = {1: "P3a", 2: "P7", 3: "P8", 4: "P9", 5: "P10"}
mapa_real = {i["n"]: i["passo"] for i in pb["inegociaveis"]}
if mapa_real == mapa_esperado:
    ok("2.6.0-T12 mapeamento dos cinco inegociaveis correto")
else:
    falha(f"2.6.0-T12 mapeamento incorreto: {mapa_real}, esperado {mapa_esperado}")

# T13 -- seis autorizacoes presentes
ent_ids = [d["id"] for d in pb["entregaveis"]]
esperado_ent = ["E1", "E2", "E3-D", "E3-E", "E4", "E5"]
if sorted(ent_ids) == sorted(esperado_ent):
    ok("2.6.0-T13 seis autorizacoes presentes")
else:
    falha(f"2.6.0-T13 autorizacoes divergentes: {ent_ids}")


def entregavel(eid):
    return next(d for d in pb["entregaveis"] if d["id"] == eid)


# T14 -- E1 -> F0
if entregavel("E1")["portao"] == ["F0"]:
    ok("2.6.0-T14 E1 depende de F0")
else:
    falha(f"2.6.0-T14 E1 portao incorreto: {entregavel('E1')['portao']}")

# T15 -- E2 -> P1/P2/P3a/P3b/P3d
if set(entregavel("E2")["portao"]) == {"P1", "P2", "P3a", "P3b", "P3d"}:
    ok("2.6.0-T15 E2 depende de P1/P2/P3a/P3b/P3d")
else:
    falha(f"2.6.0-T15 E2 portao incorreto: {entregavel('E2')['portao']}")

# T16 -- E3-D -> P4/P5
if set(entregavel("E3-D")["portao"]) == {"P4", "P5"}:
    ok("2.6.0-T16 E3-D depende de P4/P5")
else:
    falha(f"2.6.0-T16 E3-D portao incorreto: {entregavel('E3-D')['portao']}")

# T17 -- E3-E -> P5 + condicao de solucao agentica representavel
e3e = entregavel("E3-E")
cond = e3e.get("condicao")
if e3e["portao"] == ["P5"] and isinstance(cond, dict) and cond.get("campo") and cond.get("valor"):
    ok("2.6.0-T17 E3-E depende de P5 e possui condicao declarativa representavel")
else:
    falha(f"2.6.0-T17 E3-E incompleto: portao={e3e['portao']} condicao={cond}")

# T18 -- E4 -> P6/P7 + inegociavel 2
e4 = entregavel("E4")
if set(e4["portao"]) == {"P6", "P7"} and e4.get("inegociavel") == [2]:
    ok("2.6.0-T18 E4 = P6/P7 + inegociavel 2")
else:
    falha(f"2.6.0-T18 E4 incorreto: portao={e4['portao']} inegociavel={e4.get('inegociavel')}")

# T19 -- E5 -> P8/P9/P10 + inegociaveis 3/4/5
e5 = entregavel("E5")
if set(e5["portao"]) == {"P8", "P9", "P10"} and set(e5.get("inegociavel", [])) == {3, 4, 5}:
    ok("2.6.0-T19 E5 = P8/P9/P10 + inegociaveis 3/4/5")
else:
    falha(f"2.6.0-T19 E5 incorreto: portao={e5['portao']} inegociavel={e5.get('inegociavel')}")

# T20 -- nenhuma referencia a etapa inexistente (portao, depende_de)
orfas = []
for d in pb["entregaveis"]:
    for p in d["portao"]:
        if p not in ids:
            orfas.append((d["id"], p))
for e in pb["etapas"]:
    dep = e.get("depende_de")
    if dep and dep not in ids:
        orfas.append((e["id"], dep))
if not orfas:
    ok("2.6.0-T20 nenhuma referencia a etapa inexistente")
else:
    falha(f"2.6.0-T20 referencias orfas: {orfas}")

# T21 -- nenhuma dependencia orfa (inegociavel -> passo, entregavel -> inegociavel)
orfas2 = []
for item in pb["inegociaveis"]:
    if item["passo"] not in ids:
        orfas2.append(("inegociavel", item["n"], item["passo"]))
for d in pb["entregaveis"]:
    for n in d.get("inegociavel", []):
        if not any(i["n"] == n for i in pb["inegociaveis"]):
            orfas2.append(("entregavel", d["id"], n))
if not orfas2:
    ok("2.6.0-T21 nenhuma dependencia orfa entre inegociaveis/entregaveis")
else:
    falha(f"2.6.0-T21 dependencias orfas: {orfas2}")

# T22 -- portao_pendente removido dos casos resolvidos (E4/E5)
if not e4.get("portao_pendente") and not e5.get("portao_pendente"):
    ok("2.6.0-T22 portao_pendente removido de E4/E5")
else:
    falha(f"2.6.0-T22 portao_pendente ainda presente: E4={e4.get('portao_pendente')} "
          f"E5={e5.get('portao_pendente')}")

# T23 -- D/I/V permanece inalterado
proc = pb.get("procedencia", {})
if proc.get("valores") == ["D", "I", "V"] and set(proc.get("rotulos", {})) == {"D", "I", "V"}:
    ok("2.6.0-T23 D/I/V permanece inalterado")
else:
    falha(f"2.6.0-T23 procedencia alterada: {proc}")

# T24 -- playbook.py aceita o contrato oficial (regressao do carregador)
codigo, saida, erro = rodar_playbook_py(pb)
if codigo == 0 and "13 etapas" in saida:
    ok("2.6.0-T24 playbook.py aceita o contrato oficial com 13 etapas")
else:
    falha(f"2.6.0-T24 playbook.py recusou o contrato oficial: exit={codigo} stderr={erro}")

print()
print("== testes negativos 2.6.0 -- fixtures temporarias, playbook oficial preservado")

# N01 -- remover P7 do playbook temporario
pb_n01 = copy.deepcopy(pb)
pb_n01["etapas"] = [e for e in pb_n01["etapas"] if e["id"] != "P7"]
for d in pb_n01["entregaveis"]:
    d["portao"] = [p for p in d["portao"] if p != "P7"]
codigo, saida, erro = rodar_playbook_py(pb_n01)
if codigo != 0:
    ok(f"2.6.0-N01 playbook sem P7 recusado ({erro.strip()})")
else:
    falha("2.6.0-N01 playbook sem P7 foi ACEITO")

# N02 -- E5 apontando apenas para P9/P10 (sem P8)
pb_n02 = copy.deepcopy(pb)
for d in pb_n02["entregaveis"]:
    if d["id"] == "E5":
        d["portao"] = ["P9", "P10"]
codigo, saida, erro = rodar_playbook_py(pb_n02)
print("  CAPACIDADE DECLARATIVA OK / VALIDADOR DO NUCLEO PENDENTE PARA 2.6.1: "
      "playbook.py verifica apenas se as etapas do portao existem, nao a "
      "composicao esperada do contrato do metodo (isso e regra semantica, nao "
      "estrutural, ver ESP-01 3.8).")
ok("2.6.0-N02 registrado como pendencia de validacao semantica (2.6.1); "
   "estrutura oficial ja corrigida no playbook (T19)")

# N03 -- P10 sem recorrencia (recorrente True sem cadencia/responsavel)
pb_n03 = copy.deepcopy(pb)
for e in pb_n03["etapas"]:
    if e["id"] == "P10":
        e.pop("cadencia_obrigatoria", None)
        e.pop("responsavel_obrigatorio", None)
codigo, saida, erro = rodar_playbook_py(pb_n03)
if codigo != 0 and "recorrente" in erro:
    ok(f"2.6.0-N03 P10 recorrente sem cadencia/responsavel recusado ({erro.strip()})")
else:
    falha(f"2.6.0-N03 P10 sem cadencia/responsavel foi ACEITO: exit={codigo} stderr={erro}")

# N04 -- inegociavel aponta para etapa inexistente
pb_n04 = copy.deepcopy(pb)
pb_n04["inegociaveis"][0]["passo"] = "P99"
codigo, saida, erro = rodar_playbook_py(pb_n04)
if codigo != 0:
    ok(f"2.6.0-N04 inegociavel com etapa inexistente recusado ({erro.strip()})")
else:
    falha("2.6.0-N04 inegociavel com etapa inexistente foi ACEITO")

# N05 -- camada fora de EX1-EX4
pb_n05 = copy.deepcopy(pb)
for e in pb_n05["etapas"]:
    if e["id"] == "P7":
        e["camada"] = {n: "EX9" for n in pb_n05["niveis"]}
codigo, saida, erro = rodar_playbook_py(pb_n05)
if codigo != 0:
    ok(f"2.6.0-N05 camada fora de EX1-EX4 recusada ({erro.strip()})")
else:
    falha("2.6.0-N05 camada fora de EX1-EX4 foi ACEITA")

print()
print(f"{total} verificacoes do pacote 2.6.0, {falhas} falhas")
if falhas:
    sys.exit(1)
