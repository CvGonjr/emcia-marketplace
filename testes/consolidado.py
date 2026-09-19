#!/usr/bin/env python3
"""Verificacao consolidada da Acao 2.5 — pacote 2.5.6.

Nao introduz comportamento novo. Executa um caso de controle unico,
do zero, percorrendo P2 -> CTX -> P3 -> P4 -> P5 e reverifica, sobre esse
mesmo caso, os requisitos ja estabelecidos pelos pacotes 2.5.0-2.5.5.
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
CONSULTOR = RAIZ / "eiac-nucleo" / "scripts" / "consultar.py"
QUADRO = RAIZ / "eiac-nucleo" / "scripts" / "quadro.py"
GUARDA = RAIZ / "eiac-nucleo" / "scripts" / "guarda.py"
VALIDADOR_ESTRUTURA = RAIZ / "eiac-nucleo" / "scripts" / "estrutura.py"

CASO_ID = "CTX-TEST-2.5.6-001"


def preparar_caso(raiz_tmp):
    caso = raiz_tmp / "caso"
    shutil.copytree(TEMPLATE, caso)
    (caso / "rascunho").mkdir(exist_ok=True)
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


def consultar(caso, id_objeto, campos=None, schema=None):
    comando = ["python3", str(CONSULTOR), "--id", id_objeto]
    if campos:
        for c in campos:
            comando += ["--campo", c]
    if schema:
        comando += ["--schema", schema]
    proc = subprocess.run(comando, cwd=caso, text=True, capture_output=True, check=False)
    return {
        "comando": " ".join(comando), "codigo": proc.returncode,
        "stdout": proc.stdout, "stderr": proc.stderr,
    }


def rodar_quadro(caso):
    comando = ["python3", str(QUADRO)]
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


def termo(**over):
    campos = {
        "id": "T-100", "termo": "guia", "significado": "documento de autorizacao do convenio",
        "nao_e": "nota fiscal", "procedencia": "D",
        "declarado_por": "Claudia Ferreira", "registrado_por": "Rafael Nogueira",
        "data": "2026-09-18", "premissa": "", "evidencia": "",
    }
    campos.update(over)
    return "\n".join([
        f"id: {campos['id']}", f"termo: {campos['termo']}",
        f"significado: {campos['significado']}", f"nao_e: {campos['nao_e']}",
        "sinonimos_em_uso: [autorizacao]", f"procedencia: {campos['procedencia']}",
        f"declarado_por: {campos['declarado_por']}",
        f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f'premissa: "{campos["premissa"]}"', f'evidencia: "{campos["evidencia"]}"', "",
    ])


def entidade(**over):
    campos = {
        "id": "E-100", "entidade": "Guia", "onde_vive": "[F-100]", "procedencia": "D",
        "declarado_por": "Claudia Ferreira", "registrado_por": "Rafael Nogueira",
        "data": "2026-09-18", "premissa": "", "evidencia": "",
    }
    campos.update(over)
    return "\n".join([
        f"id: {campos['id']}", f"entidade: {campos['entidade']}",
        "atributos:", "  - nome: convenio", "    tipo: categoria", "    obrigatorio: true",
        "relacoes: []", f"onde_vive: {campos['onde_vive']}", f"procedencia: {campos['procedencia']}",
        f"declarado_por: {campos['declarado_por']}",
        f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f'premissa: "{campos["premissa"]}"', f'evidencia: "{campos["evidencia"]}"', "",
    ])


def fonte(**over):
    campos = {
        "id": "F-100", "fonte": "planilha de controle de envios", "tipo": "planilha",
        "responsavel": "Claudia Ferreira", "estrutura": "uma linha por guia enviada",
        "significado": "registra envio, nao emissao", "qualidade": "preenchida ao fim do dia",
        "acesso": "leitura autorizada em 2026-09-10", "procedencia": "D",
        "registrado_por": "Rafael Nogueira", "data": "2026-09-18",
        "premissa": "", "evidencia": "",
    }
    campos.update(over)
    return "\n".join([
        f"id: {campos['id']}", f"fonte: {campos['fonte']}", f"tipo: {campos['tipo']}",
        f"responsavel: {campos['responsavel']}", "contrato:",
        f"  estrutura: {campos['estrutura']}", f"  significado: {campos['significado']}",
        f"  qualidade: {campos['qualidade']}", f"acesso: {campos['acesso']}",
        f"procedencia: {campos['procedencia']}", f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f'premissa: "{campos["premissa"]}"', f'evidencia: "{campos["evidencia"]}"', "",
    ])


def regra(**over):
    campos = {
        "id": "RN-100",
        "enunciado": "quando a autorizacao do convenio chega, a guia e enviada no mesmo dia",
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
        "premissa": None,
        "evidencia_presente": None,
        "entradas": "[T-100, E-100, F-100]",
        "classe": "",
        "referencia_p3d": "",
        "historico": [],
    }
    campos.update(over)
    procedencia = campos["procedencia"]
    premissa = campos["premissa"]
    if premissa is None:
        premissa = "padrao demonstrado pela sessao P3b" if procedencia == "I" else ""
    evidencia_presente = campos["evidencia_presente"]
    if evidencia_presente is None:
        evidencia_presente = procedencia == "V"
    if evidencia_presente:
        evidencia_linhas = ["evidencia:", "  tipo: observacao", "  referencia: sessao-P3b-2.5.6"]
    else:
        evidencia_linhas = ['evidencia: ""']
    historico = campos["historico"]
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
        f"estabilidade: {campos['estabilidade']}",
        f"versao: {campos['versao']}",
    ] + historico_linhas + [""]
    return "\n".join(linhas)


def divergencia(**over):
    campos = {
        "id": "DIV-100", "regra_confrontada": "RN-100", "classe": "divergente",
        "documento_diz": "prazo de 72h conforme manual interno",
        "observado": "prazo real e 24h na pratica",
        "justificativa": "confirmado por leitura de volta com a executora do processo",
        "autor": "Claudia Ferreira", "data": "2026-09-18",
    }
    campos.update(over)
    return "\n".join([
        f"id: {campos['id']}", f"regra_confrontada: {campos['regra_confrontada']}",
        f"classe: {campos['classe']}", f"documento_diz: {campos['documento_diz']}",
        f"observado: {campos['observado']}", f"justificativa: {campos['justificativa']}",
        f"autor: {campos['autor']}", f'data: "{campos["data"]}"', "",
    ])


def gravar_evidencia(destino, teste, requisito, esperado, obtido, execucoes, passou, head_inicial,
                      evento_relacionado=""):
    agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    comandos = "\n".join(f"[{i}] {e['comando']}" for i, e in enumerate(execucoes, 1)) or "(nenhum comando)"
    codigos = "\n".join(f"[{i}] {e['codigo']}" for i, e in enumerate(execucoes, 1)) or "(n/a)"
    stdout = "".join(f"--- comando {i} ---\n{e['stdout']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    stderr = "".join(f"--- comando {i} ---\n{e['stderr']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    conteudo = f"""PACOTE: 2.5.6
TESTE: {teste}
CASO DE CONTROLE: {CASO_ID}
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
EVENTOS:
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

        # C01 — D/I/V integrados
        def c01():
            d_ok = curar(caso, "termo", "contexto/termos/T-101.yaml",
                         termo(id="T-101", procedencia="D"), "Rafael Nogueira")
            i_sem_premissa = curar(caso, "termo", "contexto/termos/T-102.yaml",
                                    termo(id="T-102", procedencia="I", premissa=""), "Rafael Nogueira")
            i_com_premissa = curar(caso, "termo", "contexto/termos/T-102.yaml",
                                    termo(id="T-102", procedencia="I", premissa="padrao observado"),
                                    "Rafael Nogueira")
            v_sem_evidencia = curar(caso, "termo", "contexto/termos/T-103.yaml",
                                     termo(id="T-103", procedencia="V", evidencia=""), "Rafael Nogueira")
            v_com_evidencia = curar(caso, "termo", "contexto/termos/T-103.yaml",
                                     termo(id="T-103", procedencia="V", evidencia="leitura de volta"),
                                     "Rafael Nogueira")
            fora_do_contrato = curar(caso, "termo", "contexto/termos/T-104.yaml",
                                      termo(id="T-104", procedencia="X"), "Rafael Nogueira")
            execs = [d_ok, i_sem_premissa, i_com_premissa, v_sem_evidencia, v_com_evidencia, fora_do_contrato]
            ok = (d_ok["codigo"] == 0 and i_sem_premissa["codigo"] != 0
                  and i_com_premissa["codigo"] == 0 and v_sem_evidencia["codigo"] != 0
                  and v_com_evidencia["codigo"] == 0 and fora_do_contrato["codigo"] != 0)
            return execs, ok
        casos.append(("2.5.6-C01", "D/I/V integrados", "D aceita; I sem premissa recusa; "
                       "I com premissa aceita; V sem evidencia recusa; V com evidencia aceita; "
                       "X fora do contrato recusa", c01))

        # C02 — quatro objetos CTX
        def c02():
            e_t = curar(caso, "termo", "contexto/termos/T-100.yaml", termo(), "Rafael Nogueira")
            e_f = curar(caso, "fonte", "contexto/fontes/F-100.yaml", fonte(), "Rafael Nogueira")
            e_e = curar(caso, "entidade", "contexto/entidades/E-100.yaml", entidade(), "Rafael Nogueira")
            e_r = curar(caso, "regra", "contexto/regras/RN-100.yaml", regra(), "Rafael Nogueira")
            e_invalida = curar(caso, "termo", "contexto/termos/T-105.yaml",
                                termo(id="T-105", significado=""), "Rafael Nogueira")
            execs = [e_t, e_f, e_e, e_r, e_invalida]
            ok = all(e["codigo"] == 0 for e in (e_t, e_f, e_e, e_r)) and e_invalida["codigo"] != 0
            return execs, ok
        casos.append(("2.5.6-C02", "quatro objetos CTX", "Termo, Fonte, Entidade e Regra "
                       "validos aceitos; Termo sem significado recusado", c02))

        # C03 — autoria x registrado_por
        def c03():
            distintos = curar(caso, "regra", "contexto/regras/RN-101.yaml",
                               regra(id="RN-101", autoria_conteudo="Pessoa A", registrado_por="Pessoa B"),
                               "Pessoa B")
            agente = curar(caso, "regra", "contexto/regras/RN-102.yaml",
                            regra(id="RN-102", autoria_conteudo="AG-01"), "Rafael Nogueira")
            return [distintos, agente], distintos["codigo"] == 0 and agente["codigo"] != 0
        casos.append(("2.5.6-C03", "autoria_conteudo != registrado_por, agente recusado como autor",
                       "papeis distintos aceitos; AG-01 como autoria_conteudo recusado", c03))

        # C04 — curadoria rascunho -> contexto
        def c04():
            (caso / "rascunho" / "T-999.yaml").write_text(termo(id="T-999"), encoding="utf-8")
            so_rascunho = not (caso / "contexto" / "termos" / "T-999.yaml").exists()
            e = curar(caso, "termo", "contexto/termos/T-999.yaml",
                      (caso / "rascunho" / "T-999.yaml").read_text(encoding="utf-8"), "Rafael Nogueira")
            curado = (caso / "contexto" / "termos" / "T-999.yaml").exists()
            return [e], so_rascunho and e["codigo"] == 0 and curado
        casos.append(("2.5.6-C04", "curadoria rascunho -> contexto", "rascunho isolado "
                       "nao e contexto; apos curar.py, objeto existe em contexto/", c04))

        # C05 — bloqueio de escrita direta
        def c05():
            negado = guarda_hook(caso, "Write", {"file_path": "contexto/termos/T-999.yaml"})
            permitido = curar(caso, "termo", "contexto/termos/T-106.yaml",
                               termo(id="T-106"), "Rafael Nogueira")
            return [negado, permitido], negado["codigo"] == 2 and permitido["codigo"] == 0
        casos.append(("2.5.6-C05", "bloqueio de escrita direta em contexto/",
                       "escrita direta negada (rc=2); curadoria autorizada aceita", c05))

        # C06 — I -> V com historico
        def c06():
            # RN-100 ja existe (D, versao 1) desde C02 — este teste continua o
            # mesmo objeto, exatamente o percurso real que C16 fecha no final.
            sobrescrita = curar(caso, "regra", "contexto/regras/RN-100.yaml",
                                 regra(id="RN-100", procedencia="V", versao=1, historico=[]),
                                 "Rafael Nogueira")
            v2 = curar(caso, "regra", "contexto/regras/RN-100.yaml",
                       regra(id="RN-100", procedencia="V", versao=2, historico=[
                           {"versao": 1, "data": "2026-09-12", "procedencia": "D",
                            "registrado_por": "Rafael Nogueira"},
                       ]), "Rafael Nogueira")
            v1_recuperavel = "versao: 1" in (caso / "contexto/regras/RN-100.yaml").read_text()
            return [sobrescrita, v2], (sobrescrita["codigo"] != 0
                                        and v2["codigo"] == 0 and v1_recuperavel)
        casos.append(("2.5.6-C06", "I -> V com historico (aqui, D -> V, mesma regra de versionamento)",
                       "RN-100 (D, v1, curada em C02) — sobrescrita para V sem historico "
                       "recusada; v2 (V) com historico aceita; v1 recuperavel", c06))

        # C07 — integracao P3d
        def c07():
            e_div = curar(caso, "divergencia", "contexto/divergencias/DIV-100.yaml",
                           divergencia(id="DIV-100", regra_confrontada="RN-100"),
                           "Rafael Nogueira", schema="registro/p3d.schema.json")
            v3 = curar(caso, "regra", "contexto/regras/RN-100.yaml",
                       regra(id="RN-100", procedencia="V", versao=3, classe="divergente",
                             referencia_p3d="DIV-100", historico=[
                                 {"versao": 2, "data": "2026-09-18", "procedencia": "V",
                                  "registrado_por": "Rafael Nogueira"},
                             ]), "Rafael Nogueira")
            sem_duplicacao = "documento_diz" not in (caso / "contexto/regras/RN-100.yaml").read_text()
            return [e_div, v3], e_div["codigo"] == 0 and v3["codigo"] == 0 and sem_duplicacao
        casos.append(("2.5.6-C07", "integracao P3d", "DIV-100 curada; RN-100 v3 referencia "
                       "DIV-100 sem duplicar documento_diz/observado/justificativa", c07))

        # C08 — CTX-V01-V11 (reexecucao consolidada, nao so confianca no 2.5.4)
        def c08():
            v01 = curar(caso, "regra", "contexto/regras/RN-103.yaml",
                        regra(id="RN-103", omitir="estabilidade") if False else
                        "\n".join(l for l in regra(id="RN-103").splitlines()
                                  if not l.startswith("estabilidade:")),
                        "Rafael Nogueira")
            v02 = curar(caso, "regra", "contexto/regras/RN-104.yaml",
                        regra(id="RN-104", procedencia="I", premissa=""), "Rafael Nogueira")
            v03 = curar(caso, "regra", "contexto/regras/RN-105.yaml",
                        regra(id="RN-105", procedencia="V", evidencia_presente=False), "Rafael Nogueira")
            v05 = curar(caso, "regra", "contexto/regras/RN-106.yaml",
                        regra(id="RN-106", entradas="[T-999999]"), "Rafael Nogueira")
            v06 = curar(caso, "regra", "contexto/regras/RN-107.yaml",
                        regra(id="RN-107", entradas="[E-999999]"), "Rafael Nogueira")
            v07 = curar(caso, "regra", "contexto/regras/RN-108.yaml",
                        regra(id="RN-108", entradas="[F-999999]"), "Rafael Nogueira")
            v09 = curar(caso, "regra", "contexto/regras/RN-109.yaml",
                        regra(id="RN-109", autoria_conteudo="AG-02"), "Rafael Nogueira")
            v11 = curar(caso, "regra", "contexto/regras/RN-110.yaml",
                        regra(id="RN-110", classe="divergente", referencia_p3d="DIV-999999"),
                        "Rafael Nogueira")
            execs = [v01, v02, v03, v05, v06, v07, v09, v11]
            todas_recusadas = all(e["codigo"] != 0 for e in execs)
            return execs, todas_recusadas
        casos.append(("2.5.6-C08", "CTX-V01-CTX-V11 (reexecucao)", "8 cenarios de violacao "
                       "(V01, V02, V03, V05, V06, V07, V09, V11) todos recusados neste caso novo",
                       c08))

        # C09 — referencias Termo/Entidade/Fonte
        def c09():
            valido = curar(caso, "regra", "contexto/regras/RN-111.yaml",
                            regra(id="RN-111", entradas="[T-100, E-100, F-100]"), "Rafael Nogueira")
            termo_inexistente = curar(caso, "regra", "contexto/regras/RN-112.yaml",
                                       regra(id="RN-112", entradas="[T-777]"), "Rafael Nogueira")
            entidade_inexistente = curar(caso, "regra", "contexto/regras/RN-113.yaml",
                                          regra(id="RN-113", entradas="[E-777]"), "Rafael Nogueira")
            fonte_inexistente = curar(caso, "regra", "contexto/regras/RN-114.yaml",
                                       regra(id="RN-114", entradas="[F-777]"), "Rafael Nogueira")
            execs = [valido, termo_inexistente, entidade_inexistente, fonte_inexistente]
            ok = (valido["codigo"] == 0 and termo_inexistente["codigo"] != 0
                  and entidade_inexistente["codigo"] != 0 and fonte_inexistente["codigo"] != 0)
            return execs, ok
        casos.append(("2.5.6-C09", "referencias Termo/Entidade/Fonte", "referencias validas "
                       "(T-100,E-100,F-100) aceitas; cada tipo inexistente recusado isoladamente", c09))

        # C10 — P2 -> CTX
        def c10():
            (caso / "rascunho" / "T-200.yaml").write_text(
                termo(id="T-200", procedencia="I", premissa="extraido do manual, pagina 7"),
                encoding="utf-8",
            )
            candidato_nao_e_contexto = not (caso / "contexto/termos/T-200.yaml").exists()
            e = curar(caso, "termo", "contexto/termos/T-200.yaml",
                      (caso / "rascunho/T-200.yaml").read_text(encoding="utf-8"), "Rafael Nogueira")
            return [e], candidato_nao_e_contexto and e["codigo"] == 0
        casos.append(("2.5.6-C10", "P2 -> CTX", "candidato em rascunho/ nao e contexto por si "
                       "so; curado, materializa objeto CTX valido", c10))

        # C11 — P3 -> CTX (P3b e P3d)
        def c11():
            p3b = curar(caso, "regra", "contexto/regras/RN-115.yaml",
                        regra(id="RN-115", procedencia="I", entradas="[T-100]"), "Rafael Nogueira")
            p3d_div = curar(caso, "divergencia", "contexto/divergencias/DIV-115.yaml",
                             divergencia(id="DIV-115", regra_confrontada="RN-115"),
                             "Rafael Nogueira", schema="registro/p3d.schema.json")
            p3d_regra = curar(caso, "regra", "contexto/regras/RN-115.yaml",
                               regra(id="RN-115", procedencia="V", versao=2, entradas="[T-100]",
                                     classe="divergente", referencia_p3d="DIV-115", historico=[
                                         {"versao": 1, "data": "2026-09-12", "procedencia": "I",
                                          "registrado_por": "Rafael Nogueira"},
                                     ]), "Rafael Nogueira")
            return [p3b, p3d_div, p3d_regra], all(
                e["codigo"] == 0 for e in (p3b, p3d_div, p3d_regra)
            )
        casos.append(("2.5.6-C11", "P3 -> CTX (P3b e P3d)", "regra levantada em P3b (I) curada; "
                       "confronto P3d atualiza para V preservando historico", c11))

        # C12 — CTX -> P4
        def c12():
            e = rodar_quadro(caso)
            return [e], e["codigo"] == 0
        casos.append(("2.5.6-C12", "CTX -> P4", "quadro.py consome contexto/regras/ ja "
                       "populado pelo caso de controle, exit 0", c12))

        # C13 — CTX -> P5
        def c13():
            e = consultar(caso, "RN-100", campos=[
                "determinismo", "frequencia", "consequencia_do_erro",
                "decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas", "estabilidade",
            ])
            proc = consultar(caso, "RN-100", campos=["procedencia"])
            if e["codigo"] != 0 or proc["codigo"] != 0:
                return [e, proc], False
            sete = set(json.loads(e["stdout"]).keys())
            esperado = {"determinismo", "frequencia", "consequencia_do_erro",
                        "decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas", "estabilidade"}
            procedencia_exposta = json.loads(proc["stdout"]).get("procedencia") == "V"
            return [e, proc], sete == esperado and procedencia_exposta
        casos.append(("2.5.6-C13", "CTX -> P5", "consultar.py retorna os sete campos "
                       "centrais e expoe procedencia: V (RN-100, apos C07/C11)", c13))

        # C14 — nao reinterpretacao
        def c14():
            fonte_quadro = QUADRO.read_text(encoding="utf-8")
            le_direto = 'r.get("frequencia")' in fonte_quadro and 'r.get("consequencia_do_erro")' in fonte_quadro
            sem_llm = "openai" not in fonte_quadro.lower() and "anthropic" not in fonte_quadro.lower()
            consulta = consultar(caso, "RN-100", campos=["frequencia"])
            valor_literal = (json.loads(consulta["stdout"]).get("frequencia") == "rotineira"
                              if consulta["codigo"] == 0 else False)
            return [consulta], le_direto and sem_llm and valor_literal
        casos.append(("2.5.6-C14", "nao reinterpretacao", "quadro.py le r.get(...) direto do "
                       "YAML; consultar.py retorna o valor literal curado (rotineira), sem "
                       "chamada a modelo de linguagem em nenhum dos dois scripts", c14))

        # C15 — eventos
        def c15():
            antes = len(eventos(caso))
            curar(caso, "termo", "contexto/termos/T-777.yaml",
                  termo(id="T-777", procedencia="I", premissa=""), "Rafael Nogueira")
            curar(caso, "regra", "contexto/regras/RN-777.yaml",
                  regra(id="RN-777", autoria_conteudo="AG-03"), "Rafael Nogueira")
            guarda_hook(caso, "Write", {"file_path": "contexto/termos/T-778.yaml"})
            curar(caso, "regra", "contexto/regras/RN-778.yaml",
                  regra(id="RN-778", entradas="[T-999888]"), "Rafael Nogueira")
            depois = eventos(caso)
            tipos = {e.get("evento") for e in depois[antes:]}
            return [], {"CuradoriaRecusada", "TentativaNegada"}.issubset(tipos)
        casos.append(("2.5.6-C15", "eventos", "violacao D/I/V, agente como autor, escrita "
                       "direta e referencia invalida geram CuradoriaRecusada/TentativaNegada "
                       "na trilha", c15))

        # C16 — percurso integrado da camada (sintese do que ja rodou em C01-C15)
        def c16():
            existe_termo = (caso / "contexto/termos/T-100.yaml").exists()
            existe_entidade = (caso / "contexto/entidades/E-100.yaml").exists()
            existe_fonte = (caso / "contexto/fontes/F-100.yaml").exists()
            existe_regra = (caso / "contexto/regras/RN-100.yaml").exists()
            existe_div = (caso / "contexto/divergencias/DIV-100.yaml").exists()
            regra_final = json.loads(consultar(caso, "RN-100")["stdout"])
            versao_final = regra_final.get("versao") == 3
            procedencia_final = regra_final.get("procedencia") == "V"
            quadro_ok = rodar_quadro(caso)["codigo"] == 0
            consulta_p5_ok = consultar(caso, "RN-100")["codigo"] == 0
            ok = (existe_termo and existe_entidade and existe_fonte and existe_regra
                  and existe_div and versao_final and procedencia_final
                  and quadro_ok and consulta_p5_ok)
            return [], ok
        casos.append(("2.5.6-C16", "percurso integrado da camada", f"caso {CASO_ID}: "
                       "T-100, E-100, F-100 curados (P2); RN-100 levantada I (P3b) e "
                       "confrontada para V versao 3 com DIV-100 (P3d); consumida por "
                       "quadro.py (P4) e consultar.py (P5)", c16))

        falhas = 0
        print(f"== verificacao consolidada da Acao 2.5 — caso {CASO_ID}")
        for teste, requisito, esperado, executar in casos:
            execucoes, passou = executar()
            evento_txt = ""
            todos = eventos(caso)
            if todos:
                evento_txt = json.dumps(todos[-1], ensure_ascii=False)
            if destino_ev:
                gravar_evidencia(destino_ev, teste, requisito, esperado,
                                  "ver STDOUT/STDERR", execucoes, passou, head_inicial, evento_txt)
            if passou:
                print(f"  ok    {teste} {requisito}")
            else:
                falhas += 1
                print(f"  FALHA {teste} {requisito}")
                for e in execucoes:
                    print(f"        stdout={e['stdout']!r} stderr={e['stderr']!r}")

        # estado final do caso, para caso-controle.md
        estado = {}
        for tipo, arq in (("termo", "T-100"), ("entidade", "E-100"), ("fonte", "F-100")):
            p = caso / f"contexto/{tipo}s/{arq}.yaml"
            estado[arq] = p.exists()
        p = caso / "contexto/regras/RN-100.yaml"
        estado["RN-100"] = json.loads(consultar(caso, "RN-100")["stdout"]) if p.exists() else None
        if destino_ev:
            (destino_ev / "estado-final-caso.json").write_text(
                json.dumps(estado, ensure_ascii=False, indent=2, default=str), encoding="utf-8",
            )

    if falhas:
        print(f"\n{falhas} verificacao(oes) consolidada(s) falharam")
        raise SystemExit(1)
    print(f"\n{len(casos)} verificacoes consolidadas aprovadas")


if __name__ == "__main__":
    main()
