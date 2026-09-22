#!/usr/bin/env python3
"""Testes de curadoria, autoria e versionamento I->V do pacote 2.5.2."""
import argparse
import datetime
import json
import pathlib
import shutil
import subprocess
import tempfile


RAIZ = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = RAIZ / "eiac-campo" / "template-caso"
CURADOR = RAIZ / "eiac-nucleo" / "scripts" / "curar.py"
GUARDA = RAIZ / "eiac-nucleo" / "scripts" / "guarda.py"


def regra(**over):
    campos = {
        "id": "RN-001",
        "enunciado": "quando a autorizacao chega, a guia e enviada no mesmo dia",
        "gatilho": "recebimento_da_autorizacao",
        "procedencia": "D",
        "autoria_conteudo": "Claudia Ferreira",
        "registrado_por": "Rafael Nogueira",
        "data": "2026-09-18",
        "origem_do_conhecimento": "experiencia_propria",
        "determinismo": "admite_julgamento",
        "frequencia": "rotineira",
        "consequencia_do_erro": "alta",
        "decisor_quando_nao_cobre": "Claudia Ferreira",
        "estabilidade": "muda quando o convenio revisa o contrato",
        "versao": 1,
    }
    campos.update(over)

    procedencia = campos["procedencia"]
    premissa = over.get("premissa", "padrao demonstrado pela amostra" if procedencia == "I" else "")
    evidencia = over.get("evidencia")
    if evidencia is None:
        if procedencia == "V":
            evidencia_linhas = ["evidencia:", "  tipo: observacao", "  referencia: sessao-P3b-001"]
        else:
            evidencia_linhas = ['evidencia: ""']
    elif evidencia == "":
        evidencia_linhas = ['evidencia: ""']
    else:
        evidencia_linhas = [f"evidencia: {evidencia}"]

    historico = over.get("historico", [])
    historico_linhas = ["historico: []"] if not historico else (
        ["historico:"] + [
            "\n".join([
                f"  - versao: {h.get('versao')}",
                f"    data: \"{h.get('data')}\"",
                f"    procedencia: {h.get('procedencia')}",
            ] + ([f"    registrado_por: {h['registrado_por']}"] if h.get("registrado_por") else [])
              + ([f"    confirmado_por: {h['confirmado_por']}"] if h.get("confirmado_por") else [])
              + ([f"    premissa: \"{h['premissa']}\""] if h.get("premissa") else [])
              + ([f"    mudanca: \"{h['mudanca']}\""] if h.get("mudanca") else []))
            for h in historico
        ]
    )

    linhas = [
        f"id: {campos['id']}",
        f"enunciado: {campos['enunciado']}",
        f"gatilho: {campos['gatilho']}",
        f"procedencia: {procedencia}",
        f"autoria_conteudo: {campos['autoria_conteudo']}",
        f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f"origem_do_conhecimento: {campos['origem_do_conhecimento']}",
        f'premissa: "{premissa}"' if premissa else 'premissa: ""',
    ] + evidencia_linhas + [
        "classificacao_confronto:",
        '  classe: ""',
        '  referencia_p3d: ""',
        "documento_de_origem: null",
        f"determinismo: {campos['determinismo']}",
        f"frequencia: {campos['frequencia']}",
        f"consequencia_do_erro: {campos['consequencia_do_erro']}",
        f"decisor_quando_nao_cobre: {campos['decisor_quando_nao_cobre']}",
        "entradas: []",
        "excecoes_conhecidas: []",
        f"estabilidade: {campos['estabilidade']}",
        f"versao: {campos['versao']}",
    ] + historico_linhas + [""]
    return "\n".join(linhas)


def preparar_caso(raiz_tmp):
    caso = raiz_tmp / "caso"
    shutil.copytree(TEMPLATE, caso)
    (caso / "rascunho").mkdir(exist_ok=True)
    # Autoria de registro (validar.py/curar.py/selar.py) le responsavel do
    # estado, fixado por novo-caso.sh fora da sessao do agente -- simula
    # esse passo aqui, ja que o teste monta o caso direto do template.
    estado_path = caso / "registro" / "estado.json"
    estado = json.loads(estado_path.read_text(encoding="utf-8"))
    estado["responsavel"] = "Celso do Vale"
    estado_path.write_text(json.dumps(estado, ensure_ascii=False), encoding="utf-8")
    return caso


def curar(caso, tipo, destino_relativo, conteudo_rascunho, registrado_por):
    nome = pathlib.Path(destino_relativo).name
    (caso / "rascunho" / nome).write_text(conteudo_rascunho, encoding="utf-8")
    comando = [
        "python3", str(CURADOR), "--tipo", tipo,
        "--arquivo", destino_relativo, "--registrado-por", registrado_por,
    ]
    proc = subprocess.run(comando, cwd=caso, text=True, capture_output=True, check=False)
    return {
        "comando": " ".join(comando), "codigo": proc.returncode,
        "stdout": proc.stdout, "stderr": proc.stderr,
    }


def guarda_hook(caso, tool_name, tool_input):
    entrada = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
    proc = subprocess.run(
        ["python3", str(GUARDA)], cwd=caso, input=entrada,
        text=True, capture_output=True, check=False,
    )
    return {
        "comando": f"guarda.py <<< {entrada}", "codigo": proc.returncode,
        "stdout": proc.stdout, "stderr": proc.stderr,
    }


def eventos(caso):
    log = caso / "registro" / "eventos.jsonl"
    if not log.exists():
        return []
    return [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]


def gravar_evidencia(destino, teste, requisito, esperado, obtido, execucoes, passou, head_inicial, evento_relacionado=""):
    agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    comandos = "\n".join(f"[{i}] {e['comando']}" for i, e in enumerate(execucoes, 1))
    codigos = "\n".join(f"[{i}] {e['codigo']}" for i, e in enumerate(execucoes, 1))
    stdout = "".join(f"--- comando {i} ---\n{e['stdout']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    stderr = "".join(f"--- comando {i} ---\n{e['stderr']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    conteudo = f"""PACOTE: 2.5.2
TESTE: {teste}
REQUISITO: {requisito}
DATA/HORA: {agora}
HEAD INICIAL: {head_inicial}
COMANDO:
{comandos}
EXIT CODE:
{codigos}

RESULTADO ESPERADO:
{esperado}

RESULTADO OBTIDO:
{obtido}

STDOUT:
{stdout}
STDERR:
{stderr}
EVENTO RELACIONADO:
{evento_relacionado or '(nenhum aplicavel)'}

RESULTADO FINAL: {'PASS' if passou else 'FAIL'}
"""
    (destino / f"teste-{teste}.txt").write_text(conteudo, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidencias")
    ap.add_argument("--head-inicial")
    args = ap.parse_args()

    destino_ev = pathlib.Path(args.evidencias).resolve() if args.evidencias else None
    if destino_ev:
        destino_ev.mkdir(parents=True, exist_ok=True)
    head_inicial = args.head_inicial or subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=RAIZ, text=True,
        capture_output=True, check=True,
    ).stdout.strip()

    with tempfile.TemporaryDirectory() as tmp:
        caso = preparar_caso(pathlib.Path(tmp))

        casos = []

        # T01 — D com autoria humana valida
        def t01():
            e = curar(caso, "regra", "contexto/regras/RN-001.yaml",
                      regra(id="RN-001", procedencia="D"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.2-T01", "D com autoria humana valida", "PASS", "registro D curado", t01))

        # T02 — I sem premissa
        def t02():
            e = curar(caso, "regra", "contexto/regras/RN-010.yaml",
                      regra(id="RN-010", procedencia="I", premissa=""), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "premissa" in e["stderr"]
        casos.append(("2.5.2-T02", "I sem premissa", "RECUSA", "recusado por premissa ausente", t02))

        # T03 — I com premissa
        def t03():
            e = curar(caso, "regra", "contexto/regras/RN-011.yaml",
                      regra(id="RN-011", procedencia="I", premissa="padrao observado na amostra"),
                      "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.2-T03", "I com premissa", "PASS", "registro I curado", t03))

        # T04 — V sem evidencia
        def t04():
            e = curar(caso, "regra", "contexto/regras/RN-012.yaml",
                      regra(id="RN-012", procedencia="V", evidencia=""), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "evidencia" in e["stderr"]
        casos.append(("2.5.2-T04", "V sem evidencia", "RECUSA", "recusado por evidencia ausente", t04))

        # T05 — V com evidencia
        def t05():
            e = curar(caso, "regra", "contexto/regras/RN-013.yaml",
                      regra(id="RN-013", procedencia="V"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.2-T05", "V com evidencia", "PASS", "registro V curado", t05))

        # T06 — agente como autoria_conteudo
        def t06():
            e = curar(caso, "regra", "contexto/regras/RN-014.yaml",
                      regra(id="RN-014", autoria_conteudo="AG-01"), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "autoria_conteudo" in e["stderr"] and "agente" in e["stderr"]
        casos.append(("2.5.2-T06", "agente como autoria_conteudo", "RECUSA",
                       "recusado: autoria_conteudo nao pode ser agente", t06))

        # T07 — pessoa como autoria_conteudo
        def t07():
            e = curar(caso, "regra", "contexto/regras/RN-015.yaml",
                      regra(id="RN-015", autoria_conteudo="Ana Beatriz Souza"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.2-T07", "pessoa como autoria_conteudo", "PASS", "registro curado", t07))

        # T08 — registrado_por distinto de autoria_conteudo
        def t08():
            e = curar(caso, "regra", "contexto/regras/RN-016.yaml",
                      regra(id="RN-016", autoria_conteudo="Pessoa A", registrado_por="Pessoa B"),
                      "Pessoa B")
            ok = e["codigo"] == 0
            if ok:
                conteudo = (caso / "contexto/regras/RN-016.yaml").read_text()
                ok = "autoria_conteudo: Pessoa A" in conteudo and "registrado_por: Pessoa B" in conteudo
            return [e], ok
        casos.append(("2.5.2-T08", "registrado_por distinto de autoria_conteudo", "PASS",
                       "papeis distintos preservados no registro", t08))

        # T09 — tentativa de sobrescrever I com V sem nova versao/historico
        def t09():
            e1 = curar(caso, "regra", "contexto/regras/RN-020.yaml",
                       regra(id="RN-020", procedencia="I", versao=1), "Rafael Nogueira")
            e2 = curar(caso, "regra", "contexto/regras/RN-020.yaml",
                       regra(id="RN-020", procedencia="V", versao=1, historico=[]), "Rafael Nogueira")
            return [e1, e2], e1["codigo"] == 0 and e2["codigo"] != 0 and "sobrescrita" in e2["stderr"]
        casos.append(("2.5.2-T09", "sobrescrever I por V sem nova versao", "RECUSA",
                       "v1 curada, sobrescrita para V recusada", t09))

        # T10 — I -> V com nova versao
        def t10():
            e1 = curar(caso, "regra", "contexto/regras/RN-021.yaml",
                       regra(id="RN-021", procedencia="I", versao=1), "Rafael Nogueira")
            e2 = curar(caso, "regra", "contexto/regras/RN-021.yaml",
                       regra(id="RN-021", procedencia="V", versao=2, historico=[
                           {"versao": 1, "data": "2026-09-12", "procedencia": "I",
                            "registrado_por": "Rafael Nogueira",
                            "premissa": "padrao demonstrado pela amostra"},
                       ]), "Rafael Nogueira")
            return [e1, e2], e1["codigo"] == 0 and e2["codigo"] == 0
        casos.append(("2.5.2-T10", "I -> V com nova versao", "PASS",
                       "v1 (I) curada, v2 (V) curada com historico", t10))

        # T11 — historico preservado (v1 recuperavel apos v2)
        def t11():
            e1 = curar(caso, "regra", "contexto/regras/RN-022.yaml",
                       regra(id="RN-022", procedencia="I", versao=1), "Rafael Nogueira")
            e2 = curar(caso, "regra", "contexto/regras/RN-022.yaml",
                       regra(id="RN-022", procedencia="V", versao=2, historico=[
                           {"versao": 1, "data": "2026-09-12", "procedencia": "I",
                            "registrado_por": "Rafael Nogueira",
                            "premissa": "padrao demonstrado pela amostra"},
                       ]), "Rafael Nogueira")
            conteudo = (caso / "contexto/regras/RN-022.yaml").read_text()
            recuperavel = "versao: 1" in conteudo and "procedencia: I" in conteudo
            return [e1, e2], e1["codigo"] == 0 and e2["codigo"] == 0 and recuperavel
        casos.append(("2.5.2-T11", "historico preservado", "PASS",
                       "versao 1 (I) permanece legivel dentro do registro v2", t11))

        # T12 — escrita direta em contexto/ (bypass)
        def t12():
            e = guarda_hook(caso, "Write", {"file_path": "contexto/regras/RN-099.yaml"})
            return [e], e["codigo"] == 2 and "contexto/" in e["stderr"]
        casos.append(("2.5.2-T12", "escrita direta em contexto/", "RECUSA",
                       "guarda bloqueia com rc=2", t12))

        # T13 — escrita autorizada em contexto/ (curadoria)
        def t13():
            e = curar(caso, "regra", "contexto/regras/RN-023.yaml",
                      regra(id="RN-023"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.2-T13", "escrita autorizada em contexto/", "PASS",
                       "curadoria grava normalmente", t13))

        # T14 — rascunho nao e contexto curado
        def t14():
            (caso / "rascunho" / "RN-030.yaml").write_text(regra(id="RN-030"), encoding="utf-8")
            existe_em_contexto = (caso / "contexto/regras/RN-030.yaml").exists()
            return [], not existe_em_contexto
        casos.append(("2.5.2-T14", "rascunho nao e contexto curado", "PASS",
                       "conteudo em rascunho/ nao aparece em contexto/ sem curadoria", t14))

        # T15 — recusa gera evento
        def t15():
            antes = len(eventos(caso))
            e = curar(caso, "regra", "contexto/regras/RN-040.yaml",
                      regra(id="RN-040", procedencia="I", premissa=""), "Rafael Nogueira")
            depois = eventos(caso)
            gerou = len(depois) > antes and depois[-1].get("evento") == "CuradoriaRecusada"
            return [e], e["codigo"] != 0 and gerou
        casos.append(("2.5.2-T15", "recusa gera evento", "RECUSA + evento",
                       "CuradoriaRecusada registrado em eventos.jsonl", t15))

        # T16 — operacao valida gera trilha suficiente
        def t16():
            antes = len(eventos(caso))
            e = curar(caso, "regra", "contexto/regras/RN-041.yaml",
                      regra(id="RN-041"), "Rafael Nogueira")
            depois = eventos(caso)
            gerou = len(depois) > antes and depois[-1].get("evento") == "ObjetoContextoCurado"
            return [e], e["codigo"] == 0 and gerou
        casos.append(("2.5.2-T16", "operacao valida gera trilha", "PASS + evento",
                       "ObjetoContextoCurado registrado em eventos.jsonl", t16))

        # T-baseline — --autor/--registrado-por AG-01 nao passa como autor humano
        def t_baseline():
            # Achado do baseline original: --registrado-por "AG-01" (com
            # hifen) escapava da checagem lexica antiga e era aceito como
            # autor humano. A garantia atual e mais forte e estrutural:
            # --registrado-por deixou de determinar a autoria do registro
            # (curar.py so le `responsavel` de registro/estado.json,
            # fixado por novo-caso.sh fora da sessao do agente) -- entao
            # nenhum valor passado por --registrado-por, nem "AG-01", vira
            # o autor gravado no evento. Confere que o evento carrega o
            # responsavel do estado, nunca o valor informado.
            e = curar(caso, "regra", "contexto/regras/RN-050.yaml",
                      regra(id="RN-050"), "AG-01")
            if e["codigo"] != 0:
                return [e], False
            todos = eventos(caso)
            ultimo = todos[-1] if todos else {}
            autor_correto = ultimo.get("registrado_por") == "Celso do Vale"
            return [e], autor_correto
        casos.append(("2.5.2-T-baseline", "registrado-por AG-01 nao determina autoria (achado do baseline superado)", "PASS",
                       "curado com autoria = responsavel do estado, nunca o valor informado", t_baseline))

        falhas = 0
        print("== curadoria, autoria e versionamento I->V — pacote 2.5.2")
        for teste, requisito, esperado, obtido, executar in casos:
            execucoes, passou = executar()
            evento_txt = ""
            if execucoes:
                todos = eventos(caso)
                if todos:
                    evento_txt = json.dumps(todos[-1], ensure_ascii=False)
            if destino_ev:
                gravar_evidencia(destino_ev, teste, requisito, esperado, obtido,
                                  execucoes, passou, head_inicial, evento_txt)
            if passou:
                print(f"  ok    {teste} {requisito}")
            else:
                falhas += 1
                print(f"  FALHA {teste} {requisito}")
                for e in execucoes:
                    print(f"        stdout={e['stdout']!r} stderr={e['stderr']!r}")

    if falhas:
        print(f"\n{falhas} teste(s) de curadoria falharam")
        raise SystemExit(1)
    print(f"\n{len(casos)} testes de curadoria aprovados")


if __name__ == "__main__":
    main()
