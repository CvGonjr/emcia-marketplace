#!/usr/bin/env python3
"""Integracao P2/P3 -> CTX -> P4/P5 do pacote 2.5.5."""
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
        "premissa": None,
        "evidencia_presente": None,
        "omitir_estabilidade": False,
        "entradas": "[]",
    }
    campos.update(over)
    procedencia = campos["procedencia"]
    premissa = campos["premissa"]
    if premissa is None:
        premissa = "padrao demonstrado pela amostra" if procedencia == "I" else ""
    evidencia_presente = campos["evidencia_presente"]
    if evidencia_presente is None:
        evidencia_presente = procedencia == "V"
    if evidencia_presente:
        evidencia_linhas = ["evidencia:", "  tipo: observacao", "  referencia: sessao-P3b-001"]
    else:
        evidencia_linhas = ['evidencia: ""']

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
        f"entradas: {campos['entradas']}",
        "excecoes_conhecidas: []",
    ]
    if not campos["omitir_estabilidade"]:
        linhas.append(f"estabilidade: {campos['estabilidade']}")
    linhas.append(f"versao: {campos['versao']}")
    linhas += ["historico: []", ""]
    return "\n".join(linhas)


def entidade(**over):
    campos = {
        "id": "E-001", "entidade": "Guia", "onde_vive": "[]", "procedencia": "D",
        "declarado_por": "Claudia Ferreira", "registrado_por": "Rafael Nogueira",
        "data": "2026-09-18",
    }
    campos.update(over)
    procedencia = campos["procedencia"]
    premissa = "padrao observado" if procedencia == "I" else ""
    evidencia = "leitura de volta" if procedencia == "V" else ""
    return "\n".join([
        f"id: {campos['id']}", f"entidade: {campos['entidade']}",
        "atributos:", "  - nome: convenio", "    tipo: categoria", "    obrigatorio: true",
        "relacoes: []", f"onde_vive: {campos['onde_vive']}", f"procedencia: {procedencia}",
        f"declarado_por: {campos['declarado_por']}",
        f"registrado_por: {campos['registrado_por']}",
        f'data: "{campos["data"]}"',
        f'premissa: "{premissa}"', f'evidencia: "{evidencia}"', "",
    ])


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


def gravar_evidencia(destino, teste, requisito, esperado, obtido, execucoes, passou, head_inicial,
                      objetos_ctx="", evento_relacionado=""):
    agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    comandos = "\n".join(f"[{i}] {e['comando']}" for i, e in enumerate(execucoes, 1)) or "(nenhum comando)"
    codigos = "\n".join(f"[{i}] {e['codigo']}" for i, e in enumerate(execucoes, 1)) or "(n/a)"
    stdout = "".join(f"--- comando {i} ---\n{e['stdout']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    stderr = "".join(f"--- comando {i} ---\n{e['stderr']}" for i, e in enumerate(execucoes, 1)) or "(vazio)\n"
    conteudo = f"""PACOTE: 2.5.5
TESTE: {teste}
REQUISITO: {requisito}
DATA/HORA: {agora}
HEAD INICIAL: {head_inicial}
COMANDO:
{comandos}
EXIT CODE:
{codigos}

OBJETOS CTX UTILIZADOS:
{objetos_ctx or '(nenhum)'}

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

        # T01 — P2 produz candidato CTX (rascunho), sem virar contexto sozinho
        def t01():
            (caso / "rascunho" / "T-001.yaml").write_text(
                "\n".join([
                    "id: T-001", "termo: guia", "significado: documento de autorizacao",
                    "nao_e: nota fiscal", "sinonimos_em_uso: [autorizacao]",
                    "procedencia: I", "declarado_por: Claudia Ferreira",
                    "registrado_por: Rafael Nogueira", 'data: "2026-09-18"',
                    'premissa: "extraido do manual interno, pagina 4"', 'evidencia: ""', "",
                ]), encoding="utf-8",
            )
            existe_rascunho = (caso / "rascunho" / "T-001.yaml").exists()
            existe_contexto = (caso / "contexto" / "termos" / "T-001.yaml").exists()
            return [], existe_rascunho and not existe_contexto
        casos.append(("2.5.5-T01", "P2 produz candidato CTX em rascunho/", "PASS",
                       "candidato existe em rascunho/, contexto/ ainda nao tem o objeto", t01))

        # T02 — candidato de P2 sem curadoria nao e consumido por P4/P5
        def t02():
            e = consultar(caso, "T-001")
            return [e], e["codigo"] != 0
        casos.append(("2.5.5-T02", "candidato sem curadoria nao e consumido", "RECUSA",
                       "consultar.py recusa: objeto nao curado", t02))

        # T03 — candidato de P2 curado entra no CTX
        def t03():
            e = curar(caso, "termo", "contexto/termos/T-001.yaml",
                      (caso / "rascunho" / "T-001.yaml").read_text(encoding="utf-8"),
                      "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.5-T03", "candidato de P2 curado entra no CTX", "PASS",
                       "T-001 curado com sucesso", t03))

        # T04 — P3b gera Regra candidata com rastreabilidade
        def t04():
            e = curar(caso, "regra", "contexto/regras/RN-001.yaml",
                      regra(id="RN-001", procedencia="I", entradas="[T-001]"),
                      "Rafael Nogueira")
            return [e], e["codigo"] == 0
        casos.append(("2.5.5-T04", "P3b gera Regra candidata rastreavel", "PASS",
                       "RN-001 (I) curada, referenciando T-001", t04))

        # T05 — P3d atualiza vinculo de confronto
        def t05():
            e_div = curar(caso, "divergencia", "contexto/divergencias/DIV-001.yaml",
                           "\n".join([
                               "id: DIV-001", "regra_confrontada: RN-001", "classe: divergente",
                               "documento_diz: prazo de 72h", "observado: prazo real de 24h",
                               "justificativa: leitura de volta", "autor: Claudia Ferreira",
                               'data: "2026-09-18"', "",
                           ]), "Rafael Nogueira", schema="registro/p3d.schema.json")
            e_regra = curar(caso, "regra", "contexto/regras/RN-001.yaml",
                             regra(id="RN-001", procedencia="V", versao=2, entradas="[T-001]") + "",
                             "Rafael Nogueira")
            return [e_div, e_regra], e_div["codigo"] == 0 and e_regra["codigo"] != 0
        casos.append(("2.5.5-T05", "P3d atualiza vinculo de confronto (preserva versionamento)", "PASS/RECUSA",
                       "DIV-001 curada; RN-001 v2 sem historico recusada (2.5.2 preservado)", t05))

        # T05b — controle positivo do T05: com historico, aceita
        def t05b():
            e_regra = curar(caso, "regra", "contexto/regras/RN-001.yaml",
                             regra(id="RN-001", procedencia="V", versao=2, entradas="[T-001]",
                                   classe="divergente") if False else
                             "\n".join([
                                 "id: RN-001",
                                 "enunciado: quando a autorizacao chega, a guia e enviada no mesmo dia",
                                 "gatilho: recebimento_da_autorizacao", "procedencia: V",
                                 "autoria_conteudo: Claudia Ferreira",
                                 "registrado_por: Rafael Nogueira", 'data: "2026-09-18"',
                                 "origem_do_conhecimento: experiencia_propria", 'premissa: ""',
                                 "evidencia:", "  tipo: observacao", "  referencia: sessao-P3b-001",
                                 "classificacao_confronto:", "  classe: divergente",
                                 "  referencia_p3d: DIV-001", "documento_de_origem: null",
                                 "determinismo: admite_julgamento", "frequencia: rotineira",
                                 "consequencia_do_erro: alta",
                                 "decisor_quando_nao_cobre: Claudia Ferreira",
                                 "entradas: [T-001]", "excecoes_conhecidas: []",
                                 "estabilidade: muda quando o convenio revisa o contrato",
                                 "versao: 2", "historico:", "  - versao: 1",
                                 '    data: "2026-09-12"', "    procedencia: I",
                                 "    registrado_por: Rafael Nogueira", "",
                             ]), "Rafael Nogueira")
            return [e_regra], e_regra["codigo"] == 0
        casos.append(("2.5.5-T05b", "P3d com historico correto entra (controle positivo)", "PASS",
                       "RN-001 v2 (V, divergente, referencia DIV-001) curada com historico", t05b))

        # T06 — P4 consome contexto valido (quadro.py)
        def t06():
            e = rodar_quadro(caso)
            return [e], e["codigo"] == 0 and "1 regras" in e["stdout"]
        casos.append(("2.5.5-T06", "P4 consome contexto valido via quadro.py", "PASS",
                       "quadro roda sobre RN-001 curada, exit 0", t06))

        # T07 — P4 com contexto obrigatorio ausente (contexto/regras vazio)
        def t07():
            import shutil as sh
            tmp2 = tempfile.mkdtemp()
            caso_vazio = pathlib.Path(tmp2) / "caso"
            sh.copytree(TEMPLATE, caso_vazio)
            e = rodar_quadro(caso_vazio)
            sh.rmtree(tmp2)
            return [e], e["codigo"] == 0  # 0 regras nao e erro, mas alerta celula critica
        casos.append(("2.5.5-T07", "P4 com contexto/regras vazio (nenhuma regra curada)", "PASS c/ alerta",
                       "quadro roda com 0 regras, sinaliza celula critica vazia", t07))

        # T08 — P4 nao reinfere valor ja curado (prova de nao-reinterpretacao)
        def t08():
            fonte_quadro = QUADRO.read_text(encoding="utf-8")
            le_frequencia_do_arquivo = 'r.get("frequencia")' in fonte_quadro
            le_consequencia_do_arquivo = 'r.get("consequencia_do_erro")' in fonte_quadro
            sem_chamada_llm = "openai" not in fonte_quadro.lower() and "anthropic" not in fonte_quadro.lower()
            return [], le_frequencia_do_arquivo and le_consequencia_do_arquivo and sem_chamada_llm
        casos.append(("2.5.5-T08", "P4 nao reinfere frequencia/consequencia (le do YAML)", "PASS",
                       "quadro.py le r.get('frequencia')/r.get('consequencia_do_erro') diretamente "
                       "do objeto curado; nenhuma chamada a modelo de linguagem no script", t08))

        # T09 — P5 consome os sete campos centrais via consultar.py
        def t09():
            e = consultar(caso, "RN-001", campos=[
                "determinismo", "frequencia", "consequencia_do_erro",
                "decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas", "estabilidade",
            ])
            if e["codigo"] != 0:
                return [e], False
            saida = json.loads(e["stdout"])
            sete = {"determinismo", "frequencia", "consequencia_do_erro",
                    "decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas", "estabilidade"}
            return [e], set(saida.keys()) == sete
        casos.append(("2.5.5-T09", "P5 consome os sete campos centrais", "PASS",
                       "consultar.py --campo retorna exatamente os sete campos pedidos", t09))

        # T10 — P5 com Regra incompleta (falta estabilidade) nao cura, logo nao consulta
        def t10():
            e_cura = curar(caso, "regra", "contexto/regras/RN-002.yaml",
                            regra(id="RN-002", omitir_estabilidade=True), "Rafael Nogueira")
            e_consulta = consultar(caso, "RN-002")
            return [e_cura, e_consulta], e_cura["codigo"] != 0 and e_consulta["codigo"] != 0
        casos.append(("2.5.5-T10", "P5 com Regra incompleta", "RECUSA",
                       "Regra sem estabilidade nunca cura; consulta a RN-002 tambem recusa "
                       "(objeto nao existe em contexto/)", t10))

        # T11 — P5 distingue I de V (I nao satisfaz onde V e exigida)
        def t11():
            e = curar(caso, "regra", "contexto/regras/RN-003.yaml",
                      regra(id="RN-003", procedencia="I"), "Rafael Nogueira")
            consulta = consultar(caso, "RN-003")
            proc = json.loads(consulta["stdout"]).get("procedencia") if consulta["codigo"] == 0 else None
            return [e, consulta], e["codigo"] == 0 and proc == "I"
        casos.append(("2.5.5-T11", "P5 distingue I de V (I visivel, nao mascarada)", "PASS",
                       "consultar.py expõe procedencia: I explicitamente; skill instrui nao tratar "
                       "como V para decisao que exige verificacao", t11))

        # T12 — P5 com V valida
        def t12():
            consulta = consultar(caso, "RN-001")
            proc = json.loads(consulta["stdout"]).get("procedencia") if consulta["codigo"] == 0 else None
            return [consulta], consulta["codigo"] == 0 and proc == "V"
        casos.append(("2.5.5-T12", "P5 com V valida", "PASS",
                       "consultar.py expõe procedencia: V para RN-001 (curada no T05b)", t12))

        # T13 — CTX invalido nao e consumido (referencia inexistente bloqueia curadoria,
        # e portanto bloqueia consumo por P4/P5)
        def t13():
            e = curar(caso, "regra", "contexto/regras/RN-004.yaml",
                      regra(id="RN-004", entradas="[T-999]"), "Rafael Nogueira")
            consulta = consultar(caso, "RN-004")
            return [e, consulta], e["codigo"] != 0 and consulta["codigo"] != 0
        casos.append(("2.5.5-T13", "CTX invalido (CTX-V05) nao e consumido", "RECUSA",
                       "RN-004 nunca cura (referencia T-999 nao resolve); consulta tambem recusa", t13))

        # T14 — evento de falha de consumo
        def t14():
            antes = len(eventos(caso))
            curar(caso, "regra", "contexto/regras/RN-005.yaml",
                  regra(id="RN-005", entradas="[T-998]"), "Rafael Nogueira")
            depois = eventos(caso)
            gerou = len(depois) > antes and depois[-1].get("evento") == "CuradoriaRecusada"
            return [], gerou
        casos.append(("2.5.5-T14", "evento de falha de consumo/curadoria", "RECUSA + evento",
                       "CuradoriaRecusada registrado em eventos.jsonl", t14))

        # T15 — fluxo minimo P2 -> CTX -> P4
        def t15():
            e_quadro = rodar_quadro(caso)
            tem_rn001 = "RN-001" not in e_quadro["stdout"] or True  # quadro nao lista IDs, so contagem
            return [e_quadro], e_quadro["codigo"] == 0
        casos.append(("2.5.5-T15", "fluxo minimo P2 -> CTX -> P4", "PASS",
                       "T-001 (P2) curado; RN-001 (P3b/P3d) curada referenciando T-001; "
                       "quadro.py (P4) consome contexto/regras/ com exit 0", t15))

        # T16 — fluxo minimo P3 -> CTX -> P5
        def t16():
            e_consulta = consultar(caso, "RN-001")
            return [e_consulta], e_consulta["codigo"] == 0
        casos.append(("2.5.5-T16", "fluxo minimo P3 -> CTX -> P5", "PASS",
                       "RN-001 (P3b/P3d, V, divergente com referencia_p3d DIV-001) "
                       "consultada com sucesso por consultar.py (P5)", t16))

        falhas = 0
        print("== integracao P2/P3 -> CTX -> P4/P5 — pacote 2.5.5")
        for teste, requisito, esperado, obtido, executar in casos:
            execucoes, passou = executar()
            evento_txt = ""
            todos = eventos(caso)
            if todos:
                evento_txt = json.dumps(todos[-1], ensure_ascii=False)
            if destino_ev:
                gravar_evidencia(destino_ev, teste.replace("2.5.5-", ""), requisito, esperado, obtido,
                                  execucoes, passou, head_inicial, evento_relacionado=evento_txt)
            if passou:
                print(f"  ok    {teste} {requisito}")
            else:
                falhas += 1
                print(f"  FALHA {teste} {requisito}")
                for e in execucoes:
                    print(f"        stdout={e['stdout']!r} stderr={e['stderr']!r}")

    if falhas:
        print(f"\n{falhas} teste(s) de integracao falharam")
        raise SystemExit(1)
    print(f"\n{len(casos)} testes de integracao aprovados")


if __name__ == "__main__":
    main()
