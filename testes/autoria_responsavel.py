#!/usr/bin/env python3
"""Autoria de registro atribuida pelo componente, nao informada pelo agente.

Achado 2026-09: validar.py, curar.py e selar.py aceitavam --autor/
--registrado-por digitado a cada chamada -- inclusive quando o valor era um
codigo de agente disfarcado ("AG-01" com hifen escapava da checagem lexica
antiga; ver 2.5.2-T-baseline em testes/curadoria.py). O CLAUDE.md do caso
dizia "autor e sempre pessoa nomeada", mas nada impedia o agente de tentar
outro valor a cada chamada -- a garantia dependia de checagem lexica, nao de
estrutura.

Correcao: a autoria do registro (quem gravou, nao quem decide -- ver nota
abaixo) deixa de vir de argumento de linha de comando. validar.py, curar.py
e selar.py leem sempre `responsavel` de registro/estado.json, fixado pelo
operador em novo-caso.sh, fora da sessao do agente. --autor/--registrado-por
continuam aceitos como argumentos (para nao quebrar nenhum comando existente)
mas sao ignorados para fins de autoria.

Distinto disso: o `--ator` que seis habilidades (P6-P10: hb-operacionalizar,
hb-governar, hb-pilotar, hb-medir, hb-medir-valor, hb-recalibrar) mandam o
agente informar em scripts de eiac-campo/scripts/ NAO e autoria de registro
-- e o ator de uma decisao de metodo (quem valida, quem decide autonomia,
quem decide recalibragem), dado que so o metodo sabe, nunca atribuido pelo
componente. Esse comportamento permanece como esta; nao e testado aqui.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = RAIZ / "eiac-campo" / "template-caso"
NOVO_CASO = RAIZ / "novo-caso.sh"
VALIDAR = RAIZ / "eiac-nucleo" / "scripts" / "validar.py"
CURAR = RAIZ / "eiac-nucleo" / "scripts" / "curar.py"
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
    return caso


def rodar(script, caso, *args):
    proc = subprocess.run(["python3", str(script), *args], cwd=caso,
                           text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def ultimo_evento(caso):
    log = caso / "registro" / "eventos.jsonl"
    if not log.exists():
        return {}
    linhas = [l for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]
    return json.loads(linhas[-1]) if linhas else {}


with tempfile.TemporaryDirectory() as tmp_novo_caso:
    print("== novo-caso.sh recusa responsavel invalido")
    base = pathlib.Path(tmp_novo_caso)

    for valor, motivo in [
        ("AG-01", "codigo de agente"),
        ("agente", "codigo de agente"),
        ("<nome da pessoa>", "placeholder"),
        ("equipe", "coletivo generico"),
        ("", "vazio"),
    ]:
        nome_caso = f"caso-{abs(hash(valor))}"
        proc = subprocess.run(
            ["bash", str(NOVO_CASO), nome_caso, "--responsavel", valor, str(base)],
            text=True, capture_output=True, check=False,
        )
        if proc.returncode != 0 and not (base / nome_caso).exists():
            ok(f"novo-caso.sh recusa responsavel {motivo} ('{valor}')")
        else:
            falha(f"novo-caso.sh ACEITOU responsavel {motivo} ('{valor}')")

    nome_valido = "caso-valido"
    proc = subprocess.run(
        ["bash", str(NOVO_CASO), nome_valido, "--responsavel", "Marina Prado", str(base)],
        text=True, capture_output=True, check=False,
    )
    destino = base / nome_valido
    if proc.returncode == 0 and destino.exists():
        estado = json.loads((destino / "registro" / "estado.json").read_text(encoding="utf-8"))
        if estado.get("responsavel") == "Marina Prado":
            ok("novo-caso.sh grava responsavel valido em registro/estado.json")
        else:
            falha(f"novo-caso.sh nao gravou responsavel valido: {estado.get('responsavel')!r}")
        eventos = (destino / "registro" / "eventos.jsonl")
        if eventos.exists() and any(
            json.loads(l).get("evento") == "CasoAberto" and json.loads(l).get("responsavel") == "Marina Prado"
            for l in eventos.read_text(encoding="utf-8").splitlines() if l.strip()
        ):
            ok("novo-caso.sh emite CasoAberto com o responsavel")
        else:
            falha("novo-caso.sh NAO emitiu CasoAberto com o responsavel")
    else:
        falha(f"novo-caso.sh com responsavel valido falhou: {proc.stderr}")


with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    print("\n== validar.py: autoria vem de responsavel, nao de --autor")

    caso = preparar_caso(tmp, responsavel="Celso do Vale")
    (caso / "rascunho" / "t.md").write_text(
        "- [D · Helena · 2026-09-11] fato declarado\n", encoding="utf-8")
    codigo, saida, erro = rodar(VALIDAR, caso, "--arquivo", "caso/t.md", "--autor", "AG-03")
    ev = ultimo_evento(caso)
    if codigo == 0 and ev.get("evento") == "AssercaoRegistrada" and ev.get("autor") == "Celso do Vale":
        ok("validar.py grava com autor=responsavel mesmo recebendo --autor AG-03")
    else:
        falha(f"validar.py nao atribuiu autoria corretamente: codigo={codigo} evento={ev}")
    if ev.get("autor_informado") == "AG-03":
        ok("validar.py preserva --autor informado em autor_informado, para auditoria")
    else:
        falha(f"validar.py nao preservou autor_informado: {ev}")

    caso2 = tmp / "caso2"
    shutil.copytree(TEMPLATE, caso2)
    (caso2 / "rascunho").mkdir(exist_ok=True)
    (caso2 / "rascunho" / "t.md").write_text(
        "- [D · Helena · 2026-09-11] fato declarado\n", encoding="utf-8")
    codigo, saida, erro = rodar(VALIDAR, caso2, "--arquivo", "caso/t.md", "--autor", "Celso")
    if codigo != 0 and "responsavel" in erro:
        ok("validar.py recusa gravar em caso sem responsavel definido")
    else:
        falha(f"validar.py gravou sem responsavel definido: codigo={codigo} erro={erro}")


with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    print("\n== curar.py: autoria vem de responsavel, nao de --registrado-por")

    caso = preparar_caso(tmp, responsavel="Rafael Nogueira")
    termo = (
        "id: T-900\ntermo: prazo de retorno\nsignificado: teste\n"
        "nao_e: prazo de resposta\nsinonimos_em_uso: []\nprocedencia: D\n"
        "declarado_por: Helena\nregistrado_por: Helena\ndata: 2026-09-22\nversao: 1\n"
    )
    (caso / "rascunho" / "T-900.yaml").write_text(termo, encoding="utf-8")
    codigo, saida, erro = rodar(
        CURAR, caso, "--tipo", "termo", "--arquivo", "contexto/termos/T-900.yaml",
        "--registrado-por", "AG-01",
    )
    ev = ultimo_evento(caso)
    if codigo == 0 and ev.get("evento") == "ObjetoContextoCurado" and ev.get("registrado_por") == "Rafael Nogueira":
        ok("curar.py cura com registrado_por=responsavel mesmo recebendo --registrado-por AG-01")
    else:
        falha(f"curar.py nao atribuiu autoria corretamente: codigo={codigo} saida={saida} erro={erro} evento={ev}")

    caso2 = tmp / "caso2"
    shutil.copytree(TEMPLATE, caso2)
    (caso2 / "rascunho").mkdir(exist_ok=True)
    (caso2 / "rascunho" / "T-901.yaml").write_text(
        termo.replace("T-900", "T-901"), encoding="utf-8")
    codigo, saida, erro = rodar(
        CURAR, caso2, "--tipo", "termo", "--arquivo", "contexto/termos/T-901.yaml",
        "--registrado-por", "Helena",
    )
    if codigo != 0 and "responsavel" in erro:
        ok("curar.py recusa curar em caso sem responsavel definido")
    else:
        falha(f"curar.py curou sem responsavel definido: codigo={codigo} erro={erro}")


with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    print("\n== selar.py: autor do commit vem de responsavel, nao de --autor")

    caso = preparar_caso(tmp, responsavel="Ana Beatriz")
    subprocess.run(["git", "init", "-q", "."], cwd=caso, check=False)
    subprocess.run(["git", "config", "user.name", "Identidade Da Maquina"], cwd=caso, check=False)
    subprocess.run(["git", "config", "user.email", "maquina@exemplo.com"], cwd=caso, check=False)
    (caso / "marcador.txt").write_text("x", encoding="utf-8")
    codigo, saida, erro = rodar(SELAR, caso, "--autor", "AG-04", "--nota", "teste de autoria no selo")
    autor_commit = subprocess.run(
        ["git", "log", "-1", "--format=%an"], cwd=caso, text=True, capture_output=True,
    ).stdout.strip()
    if codigo == 0 and autor_commit == "Ana Beatriz":
        ok("selar.py commita com autor=responsavel mesmo recebendo --autor AG-04")
    else:
        falha(f"selar.py nao usou o responsavel como autor: codigo={codigo} "
              f"autor_commit={autor_commit!r} erro={erro}")

    caso2 = tmp / "caso2"
    shutil.copytree(TEMPLATE, caso2)
    subprocess.run(["git", "init", "-q", "."], cwd=caso2, check=False)
    subprocess.run(["git", "config", "user.name", "Identidade Da Maquina"], cwd=caso2, check=False)
    subprocess.run(["git", "config", "user.email", "maquina@exemplo.com"], cwd=caso2, check=False)
    (caso2 / "marcador.txt").write_text("x", encoding="utf-8")
    codigo, saida, erro = rodar(SELAR, caso2, "--nota", "sem responsavel")
    if codigo != 0 and "responsavel" in erro:
        ok("selar.py recusa selar caso sem responsavel definido")
    else:
        falha(f"selar.py selou sem responsavel definido: codigo={codigo} erro={erro}")


print(f"\n{total} verificacoes de autoria por responsavel, {falhas} falhas")
sys.exit(1 if falhas else 0)
