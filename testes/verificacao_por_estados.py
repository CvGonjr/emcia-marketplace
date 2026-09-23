#!/usr/bin/env python3
"""Verificacao por estados do caso (decisao 021, substitui 004/014-020).

A execucao de contraste foi retirada do projeto por decisao metodologica.
A comparacao passou a ser interna ao mesmo caso de campo: o estado
declarado (selado ao fim de P2) e comparado ao estado verificado em campo
(apos P3b/P3d). Este arquivo cobre a unica trava de codigo dessa mudanca:
P3b nao abre nem encerra sem um selo (SeloAplicado) posterior ao
encerramento de P2.

A exigencia e declarativa: o playbook marca
{"exige_selo_apos": "P2"} em P3b; o nucleo (playbook.selo_apos_etapa,
usado por guarda.py G7 e avancar.py encerrar()) nao cita "P2" nem "P3b"
em codigo -- so compara eventos EtapaEncerrada/SeloAplicado contra o
campo declarativo, do mesmo jeito que avancar._avaliar_condicao() ja fazia
para os portoes de emissao (2.6.0).

Negativos primeiro (decisao 011): sem selo, e com selo anterior ao
encerramento de P2, ambos recusam -- abrir (guarda.py, TentativaNegada) e
encerrar (avancar.py, RecusaMaquina). Depois o controle positivo: selo
posterior abre e encerra normalmente.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = RAIZ / "eiac-campo" / "template-caso"
GUARDA = RAIZ / "eiac-nucleo" / "scripts" / "guarda.py"
AVANCAR = RAIZ / "eiac-nucleo" / "scripts" / "avancar.py"
SELAR = RAIZ / "eiac-nucleo" / "scripts" / "selar.py"

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


def preparar_caso(tmp, responsavel="Celso do Vale"):
    caso = tmp / "caso"
    shutil.copytree(TEMPLATE, caso)
    (caso / "rascunho").mkdir(exist_ok=True)
    estado_path = caso / "registro" / "estado.json"
    estado = json.loads(estado_path.read_text(encoding="utf-8"))
    if responsavel is not None:
        estado["responsavel"] = responsavel
    estado_path.write_text(json.dumps(estado, ensure_ascii=False), encoding="utf-8")
    subprocess.run(["git", "init", "-q", "."], cwd=caso, check=False)
    subprocess.run(["git", "config", "user.name", "Identidade Da Maquina"], cwd=caso, check=False)
    subprocess.run(["git", "config", "user.email", "maquina@exemplo.com"], cwd=caso, check=False)
    subprocess.run(["git", "add", "-A"], cwd=caso, check=False)
    subprocess.run(["git", "commit", "-qm", "estado inicial do caso"], cwd=caso, check=False)
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


def selar(caso, nota, autor="Celso do Vale"):
    proc = subprocess.run(["python3", str(SELAR), "--autor", autor, "--nota", nota],
                           cwd=caso, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def eventos(caso):
    log = caso / "registro" / "eventos.jsonl"
    if not log.exists():
        return []
    return [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]


def levar_ate_p3b(caso):
    """F0 -> P1 -> P2 -> P3a, sem selar. Etapa corrente fica P3b, com a
    sessao humana ja registrada (P3b e nao delegavel -- G1 recusaria antes
    de G7 sequer ser avaliado, sem a sessao)."""
    avancar(caso, apurar_nivel="N2", autor="Celso do Vale", eixos="DAD 4, GOV 5, CRI 7")
    avancar(caso, encerrar="F0", autor="Celso do Vale")
    avancar(caso, encerrar="P1", autor="Celso do Vale")
    codigo, saida, erro = avancar(caso, encerrar="P2", autor="Celso do Vale")
    if codigo != 0:
        return codigo, saida, erro
    codigo, saida, erro = avancar(caso, encerrar="P3a", autor="Celso do Vale")
    if codigo != 0:
        return codigo, saida, erro
    return avancar(caso, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")


print("== verificacao por estados do caso (decisao 021) -- selo apos P2 exigido por P3b")

# =====================================================================
# T01 (negativo) -- P3b nao ABRE sem selo algum apos P2
# =====================================================================
with tempfile.TemporaryDirectory() as tmp:
    caso = preparar_caso(pathlib.Path(tmp))
    codigo, saida, erro = levar_ate_p3b(caso)
    if codigo != 0:
        falha(f"T01 pre-condicao falhou ao chegar em P3b: {erro}")
    else:
        codigo, saida, erro = guarda(caso, "Read", {"file_path": "skills/hb-levantar-regras/SKILL.md"})
        evs = eventos(caso)
        tem_evento = any(
            e.get("evento") == "TentativaNegada" and "exige selo posterior" in (e.get("motivo") or "")
            for e in evs
        )
        if codigo == 2 and tem_evento:
            ok("T01 P3b nao abre sem selo apos P2 (guarda recusa, TentativaNegada registrada)")
        else:
            falha(f"T01 P3b abriu sem selo apos P2: exit={codigo} evento_presente={tem_evento} saida={erro}")

# =====================================================================
# T02 (negativo) -- P3b nao ENCERRA sem selo algum apos P2
# =====================================================================
with tempfile.TemporaryDirectory() as tmp:
    caso = preparar_caso(pathlib.Path(tmp))
    levar_ate_p3b(caso)
    codigo, saida, erro = avancar(caso, encerrar="P3b", autor="Celso do Vale")
    if codigo != 0 and "exige selo posterior" in erro:
        ok(f"T02 P3b nao encerra sem selo apos P2 ({erro.strip().splitlines()[0]})")
    else:
        falha(f"T02 P3b encerrou sem selo apos P2: exit={codigo} erro={erro}")

# =====================================================================
# T03 (negativo) -- selo ANTERIOR ao encerramento de P2 nao satisfaz
# (sela antes de encerrar P2; o selo existe, mas e anterior)
# =====================================================================
with tempfile.TemporaryDirectory() as tmp:
    caso = preparar_caso(pathlib.Path(tmp))
    avancar(caso, apurar_nivel="N2", autor="Celso do Vale", eixos="DAD 4, GOV 5, CRI 7")
    avancar(caso, encerrar="F0", autor="Celso do Vale")
    avancar(caso, encerrar="P1", autor="Celso do Vale")
    # sela ANTES de encerrar P2 -- este selo e anterior ao EtapaEncerrada de P2
    (caso / "marcador-selo-anterior.txt").write_text("x", encoding="utf-8")
    codigo_selo, _, erro_selo = selar(caso, "selo anterior ao encerramento de P2")
    if codigo_selo != 0:
        falha(f"T03 pre-condicao: selo anterior falhou ao ser aplicado: {erro_selo}")
    codigo, saida, erro = avancar(caso, encerrar="P2", autor="Celso do Vale")
    if codigo != 0:
        falha(f"T03 pre-condicao: P2 nao encerrou: {erro}")
    else:
        avancar(caso, encerrar="P3a", autor="Celso do Vale")
        avancar(caso, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")
        codigo, saida, erro = guarda(caso, "Read", {"file_path": "skills/hb-levantar-regras/SKILL.md"})
        if codigo == 2 and "exige selo posterior" in erro:
            ok("T03 selo anterior ao encerramento de P2 nao satisfaz P3b (guarda recusa)")
        else:
            falha(f"T03 selo anterior foi aceito indevidamente: exit={codigo} erro={erro}")

# =====================================================================
# T04 (positivo, controle) -- selo POSTERIOR ao encerramento de P2 abre
# e encerra P3b normalmente
# =====================================================================
with tempfile.TemporaryDirectory() as tmp:
    caso = preparar_caso(pathlib.Path(tmp))
    codigo, saida, erro = levar_ate_p3b(caso)
    if codigo != 0:
        falha(f"T04 pre-condicao falhou ao chegar em P3b: {erro}")
    else:
        (caso / "marcador-selo-posterior.txt").write_text("x", encoding="utf-8")
        codigo_selo, _, erro_selo = selar(caso, "selo posterior ao encerramento de P2")
        if codigo_selo != 0:
            falha(f"T04 selo posterior falhou ao ser aplicado: {erro_selo}")
        else:
            codigo, saida, erro = guarda(caso, "Read", {"file_path": "skills/hb-levantar-regras/SKILL.md"})
            if codigo == 0:
                ok("T04 P3b abre com selo posterior ao encerramento de P2")
            else:
                falha(f"T04 P3b nao abriu com selo posterior valido: exit={codigo} erro={erro}")

            avancar(caso, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")
            codigo, saida, erro = avancar(caso, encerrar="P3b", autor="Celso do Vale")
            if codigo == 0:
                ok("T04 P3b encerra com selo posterior ao encerramento de P2")
            else:
                falha(f"T04 P3b nao encerrou com selo posterior valido: exit={codigo} erro={erro}")

# =====================================================================
# T05 (controle) -- etapa sem exige_selo_apos nao e afetada (P1, P2 em si)
# =====================================================================
with tempfile.TemporaryDirectory() as tmp:
    caso = preparar_caso(pathlib.Path(tmp))
    avancar(caso, apurar_nivel="N2", autor="Celso do Vale", eixos="DAD 4, GOV 5, CRI 7")
    avancar(caso, encerrar="F0", autor="Celso do Vale")
    codigo, saida, erro = avancar(caso, encerrar="P1", autor="Celso do Vale")
    if codigo == 0:
        ok("T05 etapa sem exige_selo_apos (P1) encerra normalmente, sem exigir selo algum")
    else:
        falha(f"T05 etapa sem exige_selo_apos foi bloqueada indevidamente: {erro}")

# =====================================================================
# T06 -- nenhum vocabulario de contraste/antitese na implementacao nova
# =====================================================================
codigo = subprocess.run(
    ["grep", "-rn", "-i", "-E", "antitese|contraste",
     str(RAIZ / "eiac-nucleo" / "scripts" / "playbook.py")],
    capture_output=True, text=True,
).returncode
if codigo != 0:
    ok("T06 playbook.selo_apos_etapa() nao cita antitese/contraste (mecanismo generico)")
else:
    falha("T06 playbook.py cita antitese/contraste na nova trava")

print(f"{total} verificacoes de verificacao por estados do caso, {falhas} falhas")
if falhas:
    sys.exit(1)
