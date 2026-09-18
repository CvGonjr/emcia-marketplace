#!/usr/bin/env python3
"""Testes de integracao CTX <-> P3d do pacote 2.5.3."""
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
        "classe": "",
        "referencia_p3d": "",
    }
    campos.update(over)

    procedencia = campos["procedencia"]
    premissa = "padrao demonstrado pela amostra" if procedencia == "I" else ""
    if procedencia == "V":
        evidencia_linhas = ["evidencia:", "  tipo: observacao", "  referencia: sessao-P3b-001"]
    else:
        evidencia_linhas = ['evidencia: ""']

    historico = over.get("historico", [])
    if not historico:
        historico_linhas = ["historico: []"]
    else:
        historico_linhas = ["historico:"]
        for h in historico:
            historico_linhas.append(f"  - versao: {h.get('versao')}")
            historico_linhas.append(f"    data: \"{h.get('data')}\"")
            if h.get("procedencia") is not None:
                historico_linhas.append(f"    procedencia: {h.get('procedencia')}")
            if h.get("classificacao_confronto") is not None:
                historico_linhas.append(f"    classificacao_confronto: {h.get('classificacao_confronto')}")
            if h.get("registrado_por"):
                historico_linhas.append(f"    registrado_por: {h['registrado_por']}")
            if h.get("motivo"):
                historico_linhas.append(f"    motivo: \"{h['motivo']}\"")

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
        f"  classe: {campos['classe'] or chr(34)+chr(34)}",
        f"  referencia_p3d: {campos['referencia_p3d'] or chr(34)+chr(34)}",
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


def divergencia(**over):
    campos = {
        "id": "DIV-001",
        "regra_confrontada": "RN-001",
        "classe": "divergente",
        "documento_diz": "prazo de 72h conforme manual interno",
        "observado": "prazo real e 24h na pratica",
        "justificativa": "confirmado por leitura de volta com a executora do processo",
        "autor": "Claudia Ferreira",
        "data": "2026-09-18",
    }
    campos.update(over)
    linhas = [
        f"id: {campos['id']}",
        f"regra_confrontada: {campos['regra_confrontada']}",
        f"classe: {campos['classe']}",
        f"documento_diz: {campos['documento_diz']}",
        f"observado: {campos['observado']}",
        f"justificativa: {campos['justificativa']}",
        f"autor: {campos['autor']}",
        f'data: "{campos["data"]}"',
        "",
    ]
    return "\n".join(linhas)


def preparar_caso(raiz_tmp):
    caso = raiz_tmp / "caso"
    shutil.copytree(TEMPLATE, caso)
    (caso / "rascunho").mkdir(exist_ok=True)
    return caso


def curar_regra(caso, destino_relativo, conteudo, registrado_por):
    nome = pathlib.Path(destino_relativo).name
    (caso / "rascunho" / nome).write_text(conteudo, encoding="utf-8")
    comando = [
        "python3", str(CURADOR), "--tipo", "regra",
        "--arquivo", destino_relativo, "--registrado-por", registrado_por,
    ]
    proc = subprocess.run(comando, cwd=caso, text=True, capture_output=True, check=False)
    return {
        "comando": " ".join(comando), "codigo": proc.returncode,
        "stdout": proc.stdout, "stderr": proc.stderr,
    }


def curar_divergencia(caso, destino_relativo, conteudo, registrado_por):
    nome = pathlib.Path(destino_relativo).name
    (caso / "rascunho" / nome).write_text(conteudo, encoding="utf-8")
    comando = [
        "python3", str(CURADOR), "--tipo", "divergencia",
        "--arquivo", destino_relativo, "--registrado-por", registrado_por,
        "--schema", "registro/p3d.schema.json",
    ]
    proc = subprocess.run(comando, cwd=caso, text=True, capture_output=True, check=False)
    return {
        "comando": " ".join(comando), "codigo": proc.returncode,
        "stdout": proc.stdout, "stderr": proc.stderr,
    }


def eventos(caso):
    log = caso / "registro" / "eventos.jsonl"
    if not log.exists():
        return []
    return [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]


def gravar_evidencia(destino, teste, requisito, esperado, obtido, execucoes, passou, head_inicial,
                      evento_relacionado="", nao_aplicavel=False, justificativa_na=""):
    agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    comandos = "\n".join(f"[{i}] {e['comando']}" for i, e in enumerate(execucoes, 1)) or "(nenhum comando executado)"
    codigos = "\n".join(f"[{i}] {e['codigo']}" for i, e in enumerate(execucoes, 1)) or "(n/a)"
    stdout = "".join(f"--- comando {i} ---\n{e['stdout']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    stderr = "".join(f"--- comando {i} ---\n{e['stderr']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    resultado_final = "NAO APLICAVEL" if nao_aplicavel else ("PASS" if passou else "FAIL")
    extra = f"\nJUSTIFICATIVA NAO APLICAVEL:\n{justificativa_na}\n" if nao_aplicavel else ""
    conteudo = f"""PACOTE: 2.5.3
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
{extra}
RESULTADO FINAL: {resultado_final}
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

        # T01 — classificacao oficial valida
        def t01():
            e = curar_regra(caso, "contexto/regras/RN-001.yaml",
                             regra(id="RN-001", classe="alinhada"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.3-T01", "classificacao oficial valida (alinhada)", "PASS",
                       "regra curada com classe da taxonomia oficial", t01))

        # T02 — classificacao fora da taxonomia
        def t02():
            e = curar_regra(caso, "contexto/regras/RN-002.yaml",
                             regra(id="RN-002", classe="qualquer_valor_inventado"), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "classificacao_confronto.classe" in e["stderr"]
        casos.append(("2.5.3-T02", "classificacao fora da taxonomia oficial", "RECUSA",
                       "recusado: valor invalido em classificacao_confronto.classe", t02))

        # T03 — divergencia sem referencia_p3d
        def t03():
            e = curar_regra(caso, "contexto/regras/RN-003.yaml",
                             regra(id="RN-003", classe="divergente", referencia_p3d=""), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "referencia_p3d" in e["stderr"]
        casos.append(("2.5.3-T03", "divergencia sem referencia_p3d", "RECUSA",
                       "recusado: classe 'divergente' exige referencia_p3d preenchida", t03))

        # T04 — divergencia com referencia_p3d inexistente
        def t04():
            e = curar_regra(caso, "contexto/regras/RN-004.yaml",
                             regra(id="RN-004", classe="divergente", referencia_p3d="DIV-999"),
                             "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "nao resolve para registro existente" in e["stderr"]
        casos.append(("2.5.3-T04", "divergencia com referencia_p3d inexistente", "RECUSA",
                       "recusado: DIV-999 nao resolve", t04))

        # T05 — divergencia com referencia_p3d valida
        def t05():
            e_div = curar_divergencia(caso, "contexto/divergencias/DIV-005.yaml",
                                       divergencia(id="DIV-005", regra_confrontada="RN-005"),
                                       "Rafael Nogueira")
            e_regra = curar_regra(caso, "contexto/regras/RN-005.yaml",
                                   regra(id="RN-005", classe="divergente", referencia_p3d="DIV-005"),
                                   "Rafael Nogueira")
            return [e_div, e_regra], e_div["codigo"] == 0 and e_regra["codigo"] == 0
        casos.append(("2.5.3-T05", "divergencia com referencia_p3d valida", "PASS",
                       "DIV-005 curada, RN-005 referencia e e aceita", t05))

        # T06 — referencia resolve para o registro correto
        def t06():
            e_div = curar_divergencia(caso, "contexto/divergencias/DIV-006.yaml",
                                       divergencia(id="DIV-006", regra_confrontada="RN-006",
                                                    documento_diz="prazo unico de 72h",
                                                    observado="prazo efetivo de 24h"),
                                       "Rafael Nogueira")
            e_regra = curar_regra(caso, "contexto/regras/RN-006.yaml",
                                   regra(id="RN-006", classe="divergente", referencia_p3d="DIV-006"),
                                   "Rafael Nogueira")
            conteudo_div = (caso / "contexto/divergencias/DIV-006.yaml").read_text()
            resolve_correto = "regra_confrontada: RN-006" in conteudo_div and "prazo unico de 72h" in conteudo_div
            return [e_div, e_regra], e_div["codigo"] == 0 and e_regra["codigo"] == 0 and resolve_correto
        casos.append(("2.5.3-T06", "referencia resolve para o registro correto", "PASS",
                       "DIV-006 recuperado contem regra_confrontada e conteudo esperados", t06))

        # T07 — CTX nao exige duplicacao do detalhe da divergencia
        def t07():
            e_div = curar_divergencia(caso, "contexto/divergencias/DIV-007.yaml",
                                       divergencia(id="DIV-007", regra_confrontada="RN-007"),
                                       "Rafael Nogueira")
            e_regra = curar_regra(caso, "contexto/regras/RN-007.yaml",
                                   regra(id="RN-007", classe="divergente", referencia_p3d="DIV-007"),
                                   "Rafael Nogueira")
            conteudo_regra = (caso / "contexto/regras/RN-007.yaml").read_text()
            sem_duplicacao = not any(
                campo in conteudo_regra
                for campo in ("documento_diz:", "observado:", "justificativa:")
            )
            return [e_div, e_regra], e_div["codigo"] == 0 and e_regra["codigo"] == 0 and sem_duplicacao
        casos.append(("2.5.3-T07", "CTX nao exige duplicacao do detalhe", "PASS",
                       "Regra curada sem documento_diz/observado/justificativa", t07))

        # T08 — estrutura antiga duplicada (estatuto/divergencia) ja foi migrada no 2.5.1
        def t08():
            schema = json.loads((caso / "registro" / "contexto.schema.json").read_text())
            campos_regra = set(schema["objetos"]["regra"].get("required", [])) | \
                set(schema["objetos"]["regra"].get("types", {}))
            obsoletos_ausentes = not ({"estatuto", "divergencia"} & campos_regra)
            e = curar_regra(caso, "contexto/regras/RN-008.yaml",
                             regra(id="RN-008", classe="alinhada"), "Rafael Nogueira")
            return [e], obsoletos_ausentes and e["codigo"] == 0
        casos.append(("2.5.3-T08", "estrutura antiga estatuto/divergencia nao existe mais", "PASS",
                       "campos obsoletos ausentes do schema (migrados no 2.5.1); Regra atual usa classificacao_confronto",
                       t08))

        # T09 — classificacao que nao exige referencia_p3d
        def t09():
            e = curar_regra(caso, "contexto/regras/RN-009.yaml",
                             regra(id="RN-009", classe="nao_documentada", referencia_p3d=""),
                             "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.3-T09", "classificacao que nao exige referencia_p3d", "PASS",
                       "'nao_documentada' aceita sem referencia_p3d (ROT-01 3.9 nao define vinculo "
                       "obrigatorio para essa classe; CTX-01 3.5 so descreve o conteudo minimo "
                       "exigido quando classe=divergente)", t09))

        # T10 — atualizacao do confronto preserva historico
        def t10():
            e1 = curar_regra(caso, "contexto/regras/RN-010.yaml",
                              regra(id="RN-010", classe="", referencia_p3d="", versao=1),
                              "Rafael Nogueira")
            e_div = curar_divergencia(caso, "contexto/divergencias/DIV-010.yaml",
                                       divergencia(id="DIV-010", regra_confrontada="RN-010"),
                                       "Rafael Nogueira")
            e2_sem_historico = curar_regra(
                caso, "contexto/regras/RN-010.yaml",
                regra(id="RN-010", classe="divergente", referencia_p3d="DIV-010", versao=1),
                "Rafael Nogueira",
            )
            e3_com_historico = curar_regra(
                caso, "contexto/regras/RN-010.yaml",
                regra(id="RN-010", classe="divergente", referencia_p3d="DIV-010", versao=2, historico=[
                    {"versao": 1, "data": "2026-09-12", "classificacao_confronto": "{}",
                     "registrado_por": "Rafael Nogueira", "motivo": "confronto classificado apos P3d"},
                ]),
                "Rafael Nogueira",
            )
            ok = (e1["codigo"] == 0 and e_div["codigo"] == 0
                  and e2_sem_historico["codigo"] != 0 and "sobrescrita" in e2_sem_historico["stderr"]
                  and e3_com_historico["codigo"] == 0)
            return [e1, e_div, e2_sem_historico, e3_com_historico], ok
        casos.append(("2.5.3-T10", "atualizacao do confronto preserva historico", "PASS",
                       "mudar classificacao_confronto sem nova versao/historico e recusado; "
                       "com versao nova e historico e aceito", t10))

        # T11 — agente nao confirma confronto humano
        def t11():
            e = curar_divergencia(caso, "contexto/divergencias/DIV-011.yaml",
                                   divergencia(id="DIV-011", regra_confrontada="RN-011", autor="AG-01"),
                                   "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "agente" in e["stderr"]
        casos.append(("2.5.3-T11", "agente nao confirma confronto humano", "RECUSA",
                       "recusado: autor nao pode ser agente", t11))

        # T12 — controle humano valido
        def t12():
            e = curar_divergencia(caso, "contexto/divergencias/DIV-012.yaml",
                                   divergencia(id="DIV-012", regra_confrontada="RN-012",
                                                autor="Claudia Ferreira"),
                                   "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.3-T12", "controle humano valido", "PASS",
                       "registro de confronto curado por pessoa nomeada", t12))

        falhas = 0
        print("== integracao CTX <-> P3d — pacote 2.5.3")
        for teste, requisito, esperado, obtido, executar in casos:
            execucoes, passou = executar()
            evento_txt = ""
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
        print(f"\n{falhas} teste(s) de integracao CTX<->P3d falharam")
        raise SystemExit(1)
    print(f"\n{len(casos)} testes de integracao CTX<->P3d aprovados")


if __name__ == "__main__":
    main()
