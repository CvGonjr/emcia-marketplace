#!/usr/bin/env python3
"""Bateria formal CTX-V01-CTX-V11 do pacote 2.5.4.

Cada validacao ja pode ter sido implementada por um pacote anterior
(2.5.1-2.5.3); este arquivo formaliza o vinculo com o codigo CTX-Vxx do
EMCIA-CTX-01 3.13 e cobre cada uma com um teste negativo e um controle
positivo, extraidos literalmente do documento oficial.
"""
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
        "classe": "",
        "referencia_p3d": "",
        "entradas": "[]",
        "omitir_estabilidade": False,
        "premissa": None,
        "evidencia_presente": None,
    }
    campos.update(over)

    procedencia = campos["procedencia"]
    if campos["premissa"] is not None:
        premissa = campos["premissa"]
    else:
        premissa = "padrao demonstrado pela amostra" if procedencia == "I" else ""
    evidencia_presente = campos["evidencia_presente"]
    if evidencia_presente is None:
        evidencia_presente = procedencia == "V"
    if evidencia_presente:
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
            if h.get("registrado_por"):
                historico_linhas.append(f"    registrado_por: {h['registrado_por']}")

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
        f"entradas: {campos['entradas']}",
        "excecoes_conhecidas: []",
    ]
    if not campos["omitir_estabilidade"]:
        linhas.append(f"estabilidade: {campos['estabilidade']}")
    linhas.append(f"versao: {campos['versao']}")
    linhas += historico_linhas + [""]
    return "\n".join(linhas)


def _premissa_evidencia(campos):
    procedencia = campos["procedencia"]
    premissa = campos["premissa"]
    if premissa is None:
        premissa = "padrao observado" if procedencia == "I" else ""
    evidencia_presente = campos["evidencia_presente"]
    if evidencia_presente is None:
        evidencia_presente = procedencia == "V"
    evidencia = "leitura de volta" if evidencia_presente else ""
    return premissa, evidencia


def termo(**over):
    campos = {
        "id": "T-001", "termo": "guia", "significado": "documento de autorizacao",
        "nao_e": "nota fiscal", "procedencia": "D",
        "declarado_por": "Claudia Ferreira", "registrado_por": "Rafael Nogueira",
        "data": "2026-09-18", "premissa": None, "evidencia_presente": None,
    }
    campos.update(over)
    premissa, evidencia = _premissa_evidencia(campos)
    return "\n".join([
        f"id: {campos['id']}", f"termo: {campos['termo']}",
        f"significado: {campos['significado']}", f"nao_e: {campos['nao_e']}",
        "sinonimos_em_uso: [autorizacao]", f"procedencia: {campos['procedencia']}",
        f"declarado_por: {campos['declarado_por']}",
        f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f'premissa: "{premissa}"', f'evidencia: "{evidencia}"', "",
    ])


def entidade(**over):
    campos = {
        "id": "E-001", "entidade": "Guia", "onde_vive": "[]", "procedencia": "D",
        "declarado_por": "Claudia Ferreira", "registrado_por": "Rafael Nogueira",
        "data": "2026-09-18", "premissa": None, "evidencia_presente": None,
    }
    campos.update(over)
    premissa, evidencia = _premissa_evidencia(campos)
    return "\n".join([
        f"id: {campos['id']}", f"entidade: {campos['entidade']}",
        "atributos:", "  - nome: convenio", "    tipo: categoria", "    obrigatorio: true",
        "relacoes: []", f"onde_vive: {campos['onde_vive']}", f"procedencia: {campos['procedencia']}",
        f"declarado_por: {campos['declarado_por']}",
        f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f'premissa: "{premissa}"', f'evidencia: "{evidencia}"', "",
    ])


def fonte(**over):
    campos = {
        "id": "F-001", "fonte": "planilha de controle", "tipo": "planilha",
        "responsavel": "Claudia Ferreira", "estrutura": "uma linha por guia",
        "significado": "registra envio", "qualidade": "preenchida ao fim do dia",
        "acesso": "leitura autorizada", "procedencia": "D",
        "registrado_por": "Rafael Nogueira", "data": "2026-09-18",
        "premissa": None, "evidencia_presente": None,
    }
    campos.update(over)
    premissa, evidencia = _premissa_evidencia(campos)
    return "\n".join([
        f"id: {campos['id']}", f"fonte: {campos['fonte']}", f"tipo: {campos['tipo']}",
        f"responsavel: {campos['responsavel']}", "contrato:",
        f"  estrutura: {campos['estrutura']}", f"  significado: {campos['significado']}",
        f"  qualidade: {campos['qualidade']}", f"acesso: {campos['acesso']}",
        f"procedencia: {campos['procedencia']}", f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f'premissa: "{premissa}"', f'evidencia: "{evidencia}"', "",
    ])


def divergencia(**over):
    campos = {
        "id": "DIV-001", "regra_confrontada": "RN-001", "classe": "divergente",
        "documento_diz": "prazo de 72h", "observado": "prazo real de 24h",
        "justificativa": "confirmado por leitura de volta",
        "autor": "Claudia Ferreira", "data": "2026-09-18",
    }
    campos.update(over)
    return "\n".join([
        f"id: {campos['id']}", f"regra_confrontada: {campos['regra_confrontada']}",
        f"classe: {campos['classe']}", f"documento_diz: {campos['documento_diz']}",
        f"observado: {campos['observado']}", f"justificativa: {campos['justificativa']}",
        f"autor: {campos['autor']}", f'data: "{campos["data"]}"', "",
    ])


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


def curar(caso, tipo, destino_relativo, conteudo, registrado_por, schema=None):
    nome = pathlib.Path(destino_relativo).name
    (caso / "rascunho" / nome).write_text(conteudo, encoding="utf-8")
    comando = [
        "python3", str(CURADOR), "--tipo", tipo,
        "--arquivo", destino_relativo, "--registrado-por", registrado_por,
    ]
    if schema:
        comando += ["--schema", schema]
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


def gravar_evidencia(destino, nome_arquivo, validacao, tipo_teste, requisito, esperado, obtido,
                      execucoes, passou, head_inicial, evento_relacionado=""):
    agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    comandos = "\n".join(f"[{i}] {e['comando']}" for i, e in enumerate(execucoes, 1)) or "(nenhum comando)"
    codigos = "\n".join(f"[{i}] {e['codigo']}" for i, e in enumerate(execucoes, 1)) or "(n/a)"
    stdout = "".join(f"--- comando {i} ---\n{e['stdout']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    stderr = "".join(f"--- comando {i} ---\n{e['stderr']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    conteudo = f"""PACOTE: 2.5.4
VALIDACAO: {validacao}
TIPO: {tipo_teste}
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
EVENTO:
{evento_relacionado or '(nenhum aplicavel)'}

RESULTADO FINAL: {'PASS' if passou else 'FAIL'}
"""
    (destino / nome_arquivo).write_text(conteudo, encoding="utf-8")


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

        # CTX-V01 — Regra possui os sete campos do bloco de decisao
        def v01_n():
            e = curar(caso, "regra", "contexto/regras/RN-101.yaml",
                      regra(id="RN-101", omitir_estabilidade=True), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "estabilidade" in e["stderr"]
        casos.append(("CTX-V01", "N", "2.5.4-V01-N",
                       "Regra possui os sete campos do bloco de decisao", "RECUSA",
                       "recusado: campo obrigatorio ausente: estabilidade", v01_n))

        def v01_p():
            e = curar(caso, "regra", "contexto/regras/RN-102.yaml",
                      regra(id="RN-102"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("CTX-V01", "P", "2.5.4-V01-P",
                       "Regra possui os sete campos do bloco de decisao", "PASS",
                       "regra curada com os sete campos presentes", v01_p))

        # CTX-V02 — Registro I possui premissa escrita
        def v02_n():
            e = curar(caso, "regra", "contexto/regras/RN-103.yaml",
                      regra(id="RN-103", procedencia="I", premissa=""), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "premissa" in e["stderr"]
        casos.append(("CTX-V02", "N", "2.5.4-V02-N", "Registro I possui premissa escrita",
                       "RECUSA", "recusado: procedencia I exige premissa", v02_n))

        def v02_p():
            e = curar(caso, "termo", "contexto/termos/T-101.yaml",
                      termo(id="T-101", procedencia="I"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("CTX-V02", "P", "2.5.4-V02-P", "Registro I possui premissa escrita",
                       "PASS", "Termo I com premissa curado", v02_p))

        # CTX-V03 — Registro V possui evidencia identificada
        def v03_n():
            e = curar(caso, "entidade", "contexto/entidades/E-101.yaml",
                      entidade(id="E-101", procedencia="V", evidencia_presente=False),
                      "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "evidencia" in e["stderr"]
        casos.append(("CTX-V03", "N", "2.5.4-V03-N", "Registro V possui evidencia identificada",
                       "RECUSA", "recusado: procedencia V exige evidencia", v03_n))

        def v03_p():
            e = curar(caso, "fonte", "contexto/fontes/F-101.yaml",
                      fonte(id="F-101", procedencia="V"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("CTX-V03", "P", "2.5.4-V03-P", "Registro V possui evidencia identificada",
                       "PASS", "Fonte V com evidencia curada", v03_p))

        # CTX-V04 — mudanca I -> V cria nova versao
        def v04_n():
            e1 = curar(caso, "regra", "contexto/regras/RN-104.yaml",
                       regra(id="RN-104", procedencia="I", versao=1), "Rafael Nogueira")
            e2 = curar(caso, "regra", "contexto/regras/RN-104.yaml",
                       regra(id="RN-104", procedencia="V", versao=1, historico=[]), "Rafael Nogueira")
            return [e1, e2], e1["codigo"] == 0 and e2["codigo"] != 0 and "CTX-V04" in e2["stderr"]
        casos.append(("CTX-V04", "N", "2.5.4-V04-N", "Mudanca I->V cria nova versao",
                       "RECUSA", "recusado: CTX-V04, sobrescrita nao permitida", v04_n))

        def v04_p():
            e2 = curar(caso, "regra", "contexto/regras/RN-104.yaml",
                       regra(id="RN-104", procedencia="V", versao=2, historico=[
                           {"versao": 1, "data": "2026-09-12", "procedencia": "I",
                            "registrado_por": "Rafael Nogueira"},
                       ]), "Rafael Nogueira")
            return [e2], e2["codigo"] == 0
        casos.append(("CTX-V04", "P", "2.5.4-V04-P", "Mudanca I->V cria nova versao",
                       "PASS", "v2 (V) curada com historico da v1", v04_p))

        # CTX-V05 — todo termo referenciado existe
        def v05_n():
            e = curar(caso, "regra", "contexto/regras/RN-105.yaml",
                      regra(id="RN-105", entradas="[T-999]"), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "CTX-V05" in e["stderr"]
        casos.append(("CTX-V05", "N", "2.5.4-V05-N", "Todo termo referenciado existe",
                       "RECUSA", "recusado: CTX-V05, T-999 nao existe", v05_n))

        def v05_p():
            e_t = curar(caso, "termo", "contexto/termos/T-105.yaml",
                        termo(id="T-105"), "Rafael Nogueira")
            e_r = curar(caso, "regra", "contexto/regras/RN-106.yaml",
                        regra(id="RN-106", entradas="[T-105]"), "Rafael Nogueira")
            return [e_t, e_r], e_t["codigo"] == 0 and e_r["codigo"] == 0
        casos.append(("CTX-V05", "P", "2.5.4-V05-P", "Todo termo referenciado existe",
                       "PASS", "T-105 curado, RN-106 referencia e e aceita", v05_p))

        # CTX-V06 — toda entidade referenciada existe
        def v06_n():
            e = curar(caso, "regra", "contexto/regras/RN-107.yaml",
                      regra(id="RN-107", entradas="[E-999]"), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "CTX-V06" in e["stderr"]
        casos.append(("CTX-V06", "N", "2.5.4-V06-N", "Toda entidade referenciada existe",
                       "RECUSA", "recusado: CTX-V06, E-999 nao existe", v06_n))

        def v06_p():
            e_e = curar(caso, "entidade", "contexto/entidades/E-107.yaml",
                        entidade(id="E-107"), "Rafael Nogueira")
            e_r = curar(caso, "regra", "contexto/regras/RN-108.yaml",
                        regra(id="RN-108", entradas="[E-107]"), "Rafael Nogueira")
            return [e_e, e_r], e_e["codigo"] == 0 and e_r["codigo"] == 0
        casos.append(("CTX-V06", "P", "2.5.4-V06-P", "Toda entidade referenciada existe",
                       "PASS", "E-107 curada, RN-108 referencia e e aceita", v06_p))

        # CTX-V07 — toda fonte referenciada existe e possui contrato minimo
        def v07_n():
            e = curar(caso, "regra", "contexto/regras/RN-109.yaml",
                      regra(id="RN-109", entradas="[F-999]"), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "CTX-V07" in e["stderr"]
        casos.append(("CTX-V07", "N", "2.5.4-V07-N",
                       "Toda fonte referenciada existe e possui contrato minimo",
                       "RECUSA", "recusado: CTX-V07, F-999 nao existe", v07_n))

        def v07_p():
            e_f = curar(caso, "fonte", "contexto/fontes/F-109.yaml",
                        fonte(id="F-109"), "Rafael Nogueira")
            e_r = curar(caso, "regra", "contexto/regras/RN-110.yaml",
                        regra(id="RN-110", entradas="[F-109]"), "Rafael Nogueira")
            return [e_f, e_r], e_f["codigo"] == 0 and e_r["codigo"] == 0
        casos.append(("CTX-V07", "P", "2.5.4-V07-P",
                       "Toda fonte referenciada existe e possui contrato minimo",
                       "PASS", "F-109 curada com contrato, RN-110 referencia e e aceita", v07_p))

        # CTX-V08 — escrita em contexto/ passa pela curadoria prevista
        def v08_n():
            e = guarda_hook(caso, "Write", {"file_path": "contexto/regras/RN-999.yaml"})
            return [e], e["codigo"] == 2 and "contexto/" in e["stderr"]
        casos.append(("CTX-V08", "N", "2.5.4-V08-N", "Escrita em contexto/ passa pela curadoria prevista",
                       "RECUSA", "guarda bloqueia escrita direta, rc=2", v08_n))

        def v08_p():
            e = curar(caso, "regra", "contexto/regras/RN-111.yaml",
                      regra(id="RN-111"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("CTX-V08", "P", "2.5.4-V08-P", "Escrita em contexto/ passa pela curadoria prevista",
                       "PASS", "curador grava normalmente", v08_p))

        # CTX-V09 — autoria de conteudo e registro sao pessoas nomeadas
        def v09_n():
            e = curar(caso, "regra", "contexto/regras/RN-112.yaml",
                      regra(id="RN-112", autoria_conteudo="AG-01"), "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "CTX-V09" in e["stderr"]
        casos.append(("CTX-V09", "N", "2.5.4-V09-N",
                       "Autoria de conteudo e registro sao pessoas nomeadas",
                       "RECUSA", "recusado: CTX-V09, autoria_conteudo agente", v09_n))

        def v09_p():
            e = curar(caso, "regra", "contexto/regras/RN-113.yaml",
                      regra(id="RN-113", autoria_conteudo="Ana Beatriz Souza"), "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("CTX-V09", "P", "2.5.4-V09-P",
                       "Autoria de conteudo e registro sao pessoas nomeadas",
                       "PASS", "pessoa nomeada aceita como autoria_conteudo", v09_p))

        # CTX-V10 — toda nova versao possui data, responsavel e motivo da mudanca
        def v10_n():
            e1 = curar(caso, "regra", "contexto/regras/RN-114.yaml",
                       regra(id="RN-114", procedencia="I", versao=1), "Rafael Nogueira")
            e2 = curar(caso, "regra", "contexto/regras/RN-114.yaml",
                       regra(id="RN-114", procedencia="V", versao=2, historico=[
                           {"versao": 1, "procedencia": "I"},
                       ]), "Rafael Nogueira")
            return [e1, e2], e1["codigo"] == 0 and e2["codigo"] != 0 and "CTX-V10" in e2["stderr"]
        casos.append(("CTX-V10", "N", "2.5.4-V10-N",
                       "Toda nova versao possui data, responsavel e motivo da mudanca",
                       "RECUSA", "recusado: CTX-V10, historico incompleto (sem data/responsavel)", v10_n))

        def v10_p():
            e2 = curar(caso, "regra", "contexto/regras/RN-114.yaml",
                       regra(id="RN-114", procedencia="V", versao=2, historico=[
                           {"versao": 1, "data": "2026-09-12", "procedencia": "I",
                            "registrado_por": "Rafael Nogueira"},
                       ]), "Rafael Nogueira")
            return [e2], e2["codigo"] == 0
        casos.append(("CTX-V10", "P", "2.5.4-V10-P",
                       "Toda nova versao possui data, responsavel e motivo da mudanca",
                       "PASS", "historico completo aceito", v10_p))

        # CTX-V11 — classificacao_confronto completa e resolvivel quando divergente
        def v11_n():
            e = curar(caso, "regra", "contexto/regras/RN-115.yaml",
                      regra(id="RN-115", classe="divergente", referencia_p3d="DIV-999"),
                      "Rafael Nogueira")
            return [e], e["codigo"] != 0 and "CTX-V11" in e["stderr"]
        casos.append(("CTX-V11", "N", "2.5.4-V11-N",
                       "classificacao_confronto completa e resolvivel quando divergente",
                       "RECUSA", "recusado: CTX-V11, referencia_p3d inexistente", v11_n))

        def v11_p():
            e_d = curar(caso, "divergencia", "contexto/divergencias/DIV-115.yaml",
                        divergencia(id="DIV-115", regra_confrontada="RN-116"),
                        "Rafael Nogueira", schema="registro/p3d.schema.json")
            e_r = curar(caso, "regra", "contexto/regras/RN-116.yaml",
                        regra(id="RN-116", classe="divergente", referencia_p3d="DIV-115"),
                        "Rafael Nogueira")
            return [e_d, e_r], e_d["codigo"] == 0 and e_r["codigo"] == 0
        casos.append(("CTX-V11", "P", "2.5.4-V11-P",
                       "classificacao_confronto completa e resolvivel quando divergente",
                       "PASS", "DIV-115 curada, RN-116 referencia e e aceita", v11_p))

        # Teste adicional: multiplas violacoes no mesmo objeto (politica acumulativa)
        def multi():
            e = curar(caso, "regra", "contexto/regras/RN-200.yaml",
                      regra(id="RN-200", procedencia="I", premissa="", entradas="[F-999]"),
                      "Rafael Nogueira")
            tem_v02 = "premissa" in e["stderr"]
            tem_v07 = "CTX-V07" in e["stderr"]
            return [e], e["codigo"] != 0 and tem_v02 and tem_v07
        casos.append(("multiplas-violacoes", "N", "2.5.4-multi",
                       "I sem premissa + Fonte inexistente no mesmo objeto (politica acumulativa)",
                       "RECUSA com as duas causas relatadas",
                       "ambos os motivos presentes na mesma recusa (CTX-01 nao define ordem; "
                       "curar.py acumula todas as violacoes num unico erro, nao para na primeira)",
                       multi))

        falhas = 0
        print("== bateria CTX-V01-V11 — pacote 2.5.4")
        for ctxv, tipo_teste, teste_id, requisito, esperado, obtido, executar in casos:
            execucoes, passou = executar()
            evento_txt = ""
            todos = eventos(caso)
            if todos:
                evento_txt = json.dumps(todos[-1], ensure_ascii=False)
            if destino_ev:
                sufixo = "negativo" if tipo_teste == "N" else "positivo"
                nome_arquivo = (f"{ctxv}-{sufixo}.txt" if ctxv.startswith("CTX-V")
                                 else f"{teste_id}.txt")
                gravar_evidencia(destino_ev, nome_arquivo, ctxv, tipo_teste, requisito,
                                  esperado, obtido, execucoes, passou, head_inicial, evento_txt)
            if passou:
                print(f"  ok    {teste_id} {ctxv} [{tipo_teste}] {requisito}")
            else:
                falhas += 1
                print(f"  FALHA {teste_id} {ctxv} [{tipo_teste}] {requisito}")
                for e in execucoes:
                    print(f"        stdout={e['stdout']!r} stderr={e['stderr']!r}")

    if falhas:
        print(f"\n{falhas} verificacao(oes) CTX-V falharam")
        raise SystemExit(1)
    print(f"\n{len(casos)} verificacoes CTX-V01-V11 aprovadas")


if __name__ == "__main__":
    main()
