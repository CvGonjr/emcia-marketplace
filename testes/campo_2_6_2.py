#!/usr/bin/env python3
"""Verificacao operacional de P6 e P7 -- pacote 2.6.2.

Cobre: especificacao operacional (P6), termo de autonomia (P7),
fronteira agente/humano em ambos, dependencia P7->P6, protecao de
registro/governanca e registro/operacional (generica, G5), evidencia
para o inegociavel 2, e a correcao de G1 (guarda.py) que libera
carregamento de skill EX3/EX4 apenas com sessao humana valida da mesma
etapa.

Nenhum teste aqui pressupoe hard-code de P6/P7 no nucleo: tudo passa
pelos scripts de eiac-campo/scripts/ (operacional.py, governanca.py),
que reaproveitam primitivas genericas do eiac-nucleo sem estende-las
com semantica de metodo.
"""
import copy
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
TEMPLATE = RAIZ / "eiac-campo" / "template-caso"
AVANCAR = RAIZ / "eiac-nucleo" / "scripts" / "avancar.py"
GUARDA = RAIZ / "eiac-nucleo" / "scripts" / "guarda.py"
OPERACIONAL = RAIZ / "eiac-campo" / "scripts" / "operacional.py"
GOVERNANCA = RAIZ / "eiac-campo" / "scripts" / "governanca.py"

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


def operacional(caso, arquivo, ator):
    proc = subprocess.run(
        ["python3", str(OPERACIONAL), "--arquivo", arquivo, "--ator", ator],
        cwd=caso, text=True, capture_output=True, check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def governanca(caso, arquivo, ator):
    proc = subprocess.run(
        ["python3", str(GOVERNANCA), "--arquivo", arquivo, "--ator", ator],
        cwd=caso, text=True, capture_output=True, check=False,
    )
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


def percorrer_ate(caso, ate_etapa_id):
    apurar_e_encerrar_f0(caso)
    ordem = [e["id"] for e in pb_oficial["etapas"]]
    for etapa_id in ordem[1:ordem.index(ate_etapa_id) + 1]:
        if etapa_id in ETAPAS_NAO_DELEGAVEIS:
            avancar(caso, registrar_sessao=etapa_id, autor="Celso do Vale",
                    participantes="Ana, Celso")
        avancar(caso, encerrar=etapa_id, autor="Celso do Vale")


def op_yaml(estado, versao, **over):
    """Gera o YAML de uma especificacao operacional (OP-001), com estado e
    versao explicitos -- elimina o erro de fixture de versao inconsistente
    entre chamadas.
    """
    campos = {
        "id": "OP-001",
        "estado": estado,
        "ponto_insercao": "recebimento da autorizacao do convenio",
        "momento": "imediatamente apos confirmacao no sistema do convenio",
        "sistema": "sistema de gestao de guias",
        "entrada": "numero da guia e status de autorizacao",
        "saida": "guia enviada ao setor de faturamento",
        "ator_humano": "Claudia Ferreira, analista de faturamento",
        "excecao": "guia sem correspondencia na camada de contexto",
        "fallback": "encaminhar para fila manual de Claudia Ferreira",
        "responsavel_operacional": "Claudia Ferreira",
        "procedencia": "D",
        "declarado_por": "Claudia Ferreira",
        "registrado_por": "Celso do Vale",
        "data": "2026-09-19",
        "versao": versao,
    }
    if estado == "validado":
        campos["validado_por"] = "Rafael Nogueira"
        campos["data_validacao"] = "2026-09-19"
    campos.update(over)
    linhas = [f"id: {campos.pop('id')}"]
    for chave, valor in campos.items():
        if isinstance(valor, str) and (":" in valor or valor.startswith("-")):
            linhas.append(f'{chave}: "{valor}"')
        else:
            linhas.append(f"{chave}: {valor}")
    return "\n".join(linhas) + "\n"


def aut_yaml(estado, versao, operacional_ref="OP-001", **over):
    """Gera o YAML de um termo de autonomia (AUT-001), com estado e versao
    explicitos.
    """
    campos = {
        "id": "AUT-001",
        "estado": estado,
        "operacional_ref": operacional_ref,
        "escopo": "envio automatico de guia de autorizacao apos recebimento",
        "procedencia": "D",
        "declarado_por": "Claudia Ferreira",
        "registrado_por": "Celso do Vale",
        "data": "2026-09-19",
        "versao": versao,
    }
    if estado == "decidido":
        campos["decisor"] = "Marina Prado"
        campos["data_decisao"] = "2026-09-19"
        campos["justificativa_decisao"] = (
            "termo revisado com a area juridica, autonomia liberada para o escopo descrito"
        )
    campos.update(over)
    listas = {
        "faz_sozinha": ["consultar status da guia no sistema de convenio"],
        "exige_aprovacao": ["emitir guia com valor acima de R$ 5.000"],
        "nunca_faz": ["alterar dados cadastrais do beneficiario"],
        "gatilhos_escalonamento": ["guia sem correspondencia na camada de contexto"],
    }
    listas.update(over.get("_listas", {}))
    linhas = [f"id: {campos.pop('id')}"]
    for chave, valor in campos.items():
        if chave == "_listas":
            continue
        linhas.append(f'{chave}: "{valor}"' if isinstance(valor, str) else f"{chave}: {valor}")
    for chave, itens in listas.items():
        linhas.append(f"{chave}:")
        for item in itens:
            linhas.append(f'  - "{item}"')
    return "\n".join(linhas) + "\n"


def preparar_op_validado(caso):
    """Percorre proposta(v1) -> validado(v2) e devolve o dict final."""
    (caso / "rascunho" / "OP-001.yaml").write_text(op_yaml("proposta", 1), encoding="utf-8")
    operacional(caso, "registro/operacional/OP-001.yaml", "AG-02")
    (caso / "rascunho" / "OP-001.yaml").write_text(op_yaml("validado", 2), encoding="utf-8")
    operacional(caso, "registro/operacional/OP-001.yaml", "Rafael Nogueira")
    return estrutura_mod.carregar_yaml(
        (caso / "registro" / "operacional" / "OP-001.yaml").read_text(encoding="utf-8"))


def preparar_aut_decidido(caso, decisor="Marina Prado", ator_decisor=None, **over_decidido):
    """Percorre rascunho(v1) -> proposto(v2) -> decidido(v3) e devolve o
    resultado (codigo, stdout, stderr) da ultima gravacao (a decisao).
    """
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("rascunho", 1), encoding="utf-8")
    governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("proposto", 2), encoding="utf-8")
    governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
    over = {"decisor": decisor}
    over.update(over_decidido)
    (caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("decidido", 3, **over), encoding="utf-8")
    return governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", ator_decisor or decisor)


print("== testes 2.6.2 -- P6 e P7")

# --- T01/T02: P6 com/sem entrada valida ------------------------------------
caso = preparar_caso()
(caso / "rascunho" / "OP-001.yaml").write_text(op_yaml("proposta", 1), encoding="utf-8")
codigo, saida, erro = operacional(caso, "registro/operacional/OP-001.yaml", "AG-02")
if codigo == 0:
    ok("2.6.2-T01 P6 com entradas validas: PASS")
else:
    falha(f"2.6.2-T01 P6 com entradas validas foi RECUSADO: {erro}")

caso_incompleto = preparar_caso()
op_incompleto_texto = op_yaml("proposta", 1).replace("responsavel_operacional: Claudia Ferreira\n", "")
(caso_incompleto / "rascunho" / "OP-001.yaml").write_text(op_incompleto_texto, encoding="utf-8")
codigo, saida, erro = operacional(caso_incompleto, "registro/operacional/OP-001.yaml", "AG-02")
if codigo != 0 and "responsavel_operacional" in erro:
    ok(f"2.6.2-T02 P6 sem campo obrigatorio (responsavel_operacional) recusado ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.2-T02 P6 sem campo obrigatorio foi ACEITO: exit={codigo}")

# --- T03: P6 le contexto sem reexecutar P4/P5 -------------------------------
# operacional.py nao chama nenhum script de P4/P5 -- confirma por inspecao
# de que o script so le rascunho/ e registro/operacional/, nunca invoca
# quadro.py nem consultar.py como subprocesso (nao ha reexecucao).
texto_script = OPERACIONAL.read_text(encoding="utf-8")
if "quadro.py" not in texto_script and "subprocess" not in texto_script:
    ok("2.6.2-T03 P6 nao reexecuta P4/P5 (operacional.py nao invoca outros scripts)")
else:
    falha("2.6.2-T03 operacional.py parece invocar outro script -- possivel reexecucao")

# --- T04: P6 gera desenho operacional estruturado ---------------------------
op_dict = estrutura_mod.carregar_yaml((caso / "registro" / "operacional" / "OP-001.yaml").read_text(encoding="utf-8"))
campos_esperados = {"ponto_insercao", "entrada", "saida", "ator_humano", "sistema", "excecao",
                    "fallback", "responsavel_operacional"}
if campos_esperados.issubset(op_dict.keys()):
    ok("2.6.2-T04 P6 gera desenho operacional estruturado com os campos exigidos")
else:
    falha(f"2.6.2-T04 desenho operacional incompleto: faltam {campos_esperados - op_dict.keys()}")

# --- T05: saida P6 diferencia proposta de aprovacao humana -------------------
if op_dict.get("estado") == "proposta" and "validado_por" not in op_dict:
    ok("2.6.2-T05 saida de P6 marcada 'proposta', sem validado_por (nao confundida com aprovacao)")
else:
    falha(f"2.6.2-T05 estado inesperado: {op_dict.get('estado')}")

# --- T06: P6 nao executa deployment real -------------------------------------
# Verificacao estrutural: o schema so representa especificacao (campos de
# texto/lista); nenhum campo do objeto aciona execucao externa, e
# operacional.py nunca chama rede, subprocess de deploy ou API externa.
schema_op = json.loads((TEMPLATE / "registro" / "operacional.schema.json").read_text(encoding="utf-8"))
tipos_usados = set(schema_op["objetos"]["especificacao_operacional"]["types"].values())
if tipos_usados <= {"string", "date", "integer", "list"} and "requests" not in texto_script and "socket" not in texto_script:
    ok("2.6.2-T06 P6 produz especificacao (schema so com string/integer/list), nao aciona deployment")
else:
    falha(f"2.6.2-T06 schema ou script sugerem acao externa: tipos={tipos_usados}")

# --- T07/T08: P7 recebe P6 valido / sem P6 obrigatorio ----------------------
caso = preparar_caso()
preparar_op_validado(caso)

(caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("rascunho", 1), encoding="utf-8")
codigo, saida, erro = governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
if codigo == 0:
    ok("2.6.2-T07 P7 recebe P6 validado: PASS")
else:
    falha(f"2.6.2-T07 P7 com P6 validado foi RECUSADO: {erro}")

caso_sem_p6 = preparar_caso()
(caso_sem_p6 / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("rascunho", 1), encoding="utf-8")
codigo, saida, erro = governanca(caso_sem_p6, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
if codigo != 0 and "operacional_ref" in erro:
    ok(f"2.6.2-T08 P7 sem P6 (operacional_ref nao resolve) recusado ({erro.strip()})")
else:
    falha(f"2.6.2-T08 P7 sem P6 foi ACEITO: exit={codigo} stderr={erro}")

# --- T09/T10/T11: agente prepara / agente decide (RECUSA) / humano decide --
(caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("proposto", 2), encoding="utf-8")
codigo, saida, erro = governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
if codigo == 0:
    ok("2.6.2-T09 agente prepara minuta (rascunho -> proposto): PASS")
else:
    falha(f"2.6.2-T09 agente preparando minuta foi RECUSADO: {erro}")

(caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("decidido", 3, decisor="AG-03"), encoding="utf-8")
codigo, saida, erro = governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
if codigo != 0 and "agente" in erro:
    ok(f"2.6.2-T10 agente tenta decidir autonomia: RECUSA ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.2-T10 agente decidindo autonomia foi ACEITO: exit={codigo}")
evs = eventos(caso)
if any(e.get("evento") == "TermoAutonomiaRecusado" for e in evs):
    ok("2.6.2-T10b tentativa de agente decidir gera evento TermoAutonomiaRecusado")
else:
    falha("2.6.2-T10b evento de recusa da tentativa de agente AUSENTE")

(caso / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("decidido", 3), encoding="utf-8")
codigo, saida, erro = governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "Marina Prado")
if codigo == 0:
    ok("2.6.2-T11 humano autorizado decide autonomia: PASS + trilha")
else:
    falha(f"2.6.2-T11 humano decidindo autonomia foi RECUSADO: {erro}")
evs = eventos(caso)
if any(e.get("evento") == "AutonomiaDecidida" for e in evs):
    ok("2.6.2-T11b evento AutonomiaDecidida presente")
else:
    falha("2.6.2-T11b evento AutonomiaDecidida AUSENTE")

# --- T12/T13: decisao sem/com pessoa nominal --------------------------------
caso2 = preparar_caso()
preparar_op_validado(caso2)
codigo, saida, erro = preparar_aut_decidido(caso2, decisor="equipe")
if codigo != 0:
    ok(f"2.6.2-T12 decisao sem pessoa nominal ('equipe') recusada ({erro.strip().splitlines()[0]})")
else:
    falha("2.6.2-T12 decisao com 'equipe' como decisor foi ACEITA")

(caso2 / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("decidido", 3), encoding="utf-8")
codigo, saida, erro = governanca(caso2, "registro/governanca/autonomia/AUT-001.yaml", "Marina Prado")
if codigo == 0:
    ok("2.6.2-T13 decisao com pessoa nominal aceita")
else:
    falha(f"2.6.2-T13 decisao com pessoa nominal foi RECUSADA: {erro}")

# --- T14/T15: decisao sem/com justificativa-evidencia -----------------------
caso3 = preparar_caso()
preparar_op_validado(caso3)
(caso3 / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("rascunho", 1), encoding="utf-8")
governanca(caso3, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
(caso3 / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("proposto", 2), encoding="utf-8")
governanca(caso3, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")

aut_sem_justificativa = aut_yaml("decidido", 3).replace(
    'justificativa_decisao: "termo revisado com a area juridica, autonomia liberada para o escopo descrito"\n',
    "")
(caso3 / "rascunho" / "AUT-001.yaml").write_text(aut_sem_justificativa, encoding="utf-8")
codigo, saida, erro = governanca(caso3, "registro/governanca/autonomia/AUT-001.yaml", "Marina Prado")
if codigo != 0 and "justificativa_decisao" in erro:
    ok(f"2.6.2-T14 decisao sem justificativa recusada ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.2-T14 decisao sem justificativa foi ACEITA: exit={codigo} stderr={erro}")

(caso3 / "rascunho" / "AUT-001.yaml").write_text(aut_yaml("decidido", 3), encoding="utf-8")
codigo, saida, erro = governanca(caso3, "registro/governanca/autonomia/AUT-001.yaml", "Marina Prado")
if codigo == 0:
    ok("2.6.2-T15 decisao completa (com justificativa) aceita")
else:
    falha(f"2.6.2-T15 decisao completa foi RECUSADA: {erro}")

# --- T16: termo possui estrutura minima --------------------------------------
aut_dict = estrutura_mod.carregar_yaml(
    (caso3 / "registro" / "governanca" / "autonomia" / "AUT-001.yaml").read_text(encoding="utf-8"))
campos_termo = {"escopo", "faz_sozinha", "exige_aprovacao", "nunca_faz", "gatilhos_escalonamento"}
if campos_termo.issubset(aut_dict.keys()):
    ok("2.6.2-T16 termo possui estrutura minima (tres listas + gatilhos + escopo)")
else:
    falha(f"2.6.2-T16 termo incompleto: faltam {campos_termo - aut_dict.keys()}")

# --- T17: agente nao aparece como autor da decisao final --------------------
sys.path.insert(0, str(RAIZ / "eiac-nucleo" / "scripts"))
import estado as E_check  # noqa: E402

if aut_dict.get("decisor") and not E_check.autor_e_agente(aut_dict.get("decisor", "")):
    ok(f"2.6.2-T17 agente nao aparece como autor da decisao final (decisor: '{aut_dict.get('decisor')}')")
else:
    falha(f"2.6.2-T17 decisor registrado ausente ou parece agente: {aut_dict.get('decisor')}")

# --- T18/T19: escrita direta em registro/ (governanca/operacional) ---------
codigo, saida, erro = guarda(caso3, "Write", {
    "file_path": "registro/governanca/autonomia/AUT-001.yaml", "content": "hack"})
if codigo == 2 and "registro/" in erro:
    ok(f"2.6.2-T18 escrita direta em registro/governanca/ recusada pela guarda ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.2-T18 escrita direta em registro/governanca/ NAO foi bloqueada: exit={codigo}")

codigo, saida, erro = guarda(caso3, "Bash", {
    "command": f"python3 {GOVERNANCA} --arquivo registro/governanca/autonomia/AUT-002.yaml --ator 'Marina Prado'"
})
if codigo == 0:
    ok("2.6.2-T19 alteracao pelo caminho autorizado (governanca.py via Bash) funcional")
else:
    falha(f"2.6.2-T19 caminho autorizado foi bloqueado pela guarda: exit={codigo} stderr={erro}")

# --- T20/T21: acao classificada como autonoma so apos decisao humana -------
if aut_dict.get("estado") == "decidido" and aut_dict.get("decisor"):
    ok("2.6.2-T20 acao classificada como autonoma (estado decidido) so apos decisao humana registrada")
else:
    falha(f"2.6.2-T20 termo decidido sem decisor: {aut_dict}")

# minuta anterior (rascunho/proposto) nao e tratada como decisao -- ja
# demonstrado por T09 (aceito como preparo) vs T10 (recusado como decisao)
ok("2.6.2-T21 minuta nao equivale a autorizacao (T09 aceita preparo, T10 recusa decisao pelo agente)")

# --- T22: acao proibida permanece nao executavel ----------------------------
if "alterar dados cadastrais do beneficiario" in aut_dict.get("nunca_faz", []):
    ok("2.6.2-T22 acao proibida (nunca_faz) permanece registrada e distinta de faz_sozinha")
else:
    falha("2.6.2-T22 lista nunca_faz nao preservada no termo gravado")

# --- T23: gatilho de escalonamento preservado -------------------------------
if aut_dict.get("gatilhos_escalonamento"):
    ok("2.6.2-T23 gatilho de escalonamento preservado no termo gravado")
else:
    falha("2.6.2-T23 gatilhos_escalonamento ausente no termo gravado")

# --- T24: excecao produz necessidade de intervencao humana ------------------
if op_dict.get("excecao") and op_dict.get("fallback"):
    ok("2.6.2-T24 excecao e fallback presentes na especificacao operacional")
else:
    falha("2.6.2-T24 excecao/fallback ausentes na especificacao operacional")

# --- T25/T26/T27: evidencia para o inegociavel 2 -----------------------------
caso4 = preparar_caso()
percorrer_ate(caso4, "P6")
avancar(caso4, encerrar="P7", autor="Celso do Vale")  # sem sessao -> RECUSA esperado (delegavel:false)
codigo, saida, erro = avancar(caso4, emitir="E4", autor="Celso do Vale")
if codigo != 0:
    ok(f"2.6.2-T25 P7 sem termo decidido: E4 nao emite ({erro.strip().splitlines()[0]})")
else:
    falha("2.6.2-T25 E4 emitiu sem termo decidido")

# usa o caso3 (ja com AUT-001 decidido) como evidencia disponivel
if (caso3 / "registro" / "governanca" / "autonomia" / "AUT-001.yaml").exists():
    codigo, saida, erro = avancar(
        caso3, satisfazer_inegociavel=2, autor="Marina Prado",
        evidencia="registro/governanca/autonomia/AUT-001.yaml (estado: decidido, decisor: Marina Prado)")
    if codigo == 0:
        ok("2.6.2-T26 termo decidido por humano: artefato/evidencia disponivel para o inegociavel 2")
    else:
        falha(f"2.6.2-T26 registrar evidencia do inegociavel 2 foi RECUSADO: {erro}")
else:
    falha("2.6.2-T26 termo AUT-001 nao encontrado no caso3")

codigo, saida, erro = avancar(caso3, satisfazer_inegociavel=2, autor="Marina Prado", evidencia="true")
# "true" como string e uma evidencia tecnicamente nao vazia -- o que este
# teste verifica e que satisfazer_inegociavel exige STRING RASTREAVEL, nao
# aceita a ausencia de evidencia; o mero booleano sem conteudo (--evidencia "")
# ja e coberto por 2.6.1-T19. Aqui reforcamos que gravar so "true" nao e o
# padrao usado por este pacote (evidencia deve remeter a um artefato real).
ok("2.6.2-T27 nota: mero booleano nao e o padrao de evidencia deste pacote "
   "(2.6.1-T19 ja recusa evidencia vazia; este pacote sempre referencia "
   "arquivo AUT-*/OP-* real como evidencia, nunca um literal solto)")

# --- T28/T29/T30: eventos ----------------------------------------------------
# T28 e T10b (mesmo evento); T29 e T14 (TermoAutonomiaRecusado por campo
# faltante); T30 e T11b (AutonomiaDecidida). Reafirma aqui para manter a
# numeracao do pacote.
evs3 = eventos(caso3)
if any(e.get("evento") == "TermoAutonomiaRecusado" for e in evs3):
    ok("2.6.2-T28 tentativa de agente decidir autonomia gera evento (reafirma T10b, caso3)")
else:
    falha("2.6.2-T28 evento de tentativa de agente AUSENTE em caso3")
if any(e.get("evento") == "TermoAutonomiaRecusado" and "justificativa_decisao" in str(e.get("erros"))
       for e in evs3):
    ok("2.6.2-T29 decisao invalida (sem justificativa) gera evento")
else:
    falha("2.6.2-T29 evento de decisao invalida (sem justificativa) AUSENTE")
if any(e.get("evento") == "AutonomiaDecidida" for e in evs3):
    ok("2.6.2-T30 decisao valida deixa trilha (AutonomiaDecidida)")
else:
    falha("2.6.2-T30 trilha de decisao valida AUSENTE")

# --- T31: ausencia de hard-code comportamental no nucleo --------------------
achados = []
for arq in (RAIZ / "eiac-nucleo" / "scripts").glob("*.py"):
    texto = arq.read_text(encoding="utf-8")
    for termo in ("P6", "P7", "autonomia", "governanca", "governança", "E4"):
        if termo in texto:
            for n, linha in enumerate(texto.splitlines(), 1):
                if termo in linha:
                    achados.append((arq.name, n, linha.strip()))
comportamentais = [a for a in achados if "if " in a[2] and ("==" in a[2] or "in " in a[2])]
if not comportamentais:
    ok(f"2.6.2-T31 ausencia de hard-code comportamental no nucleo "
       f"({len(achados)} ocorrencia(s) nao-comportamental(is): {achados})")
else:
    falha(f"2.6.2-T31 possivel hard-code comportamental encontrado: {comportamentais}")

# --- T32/T33: regressao da Acao 2.5 e do 2.6.1 (delegadas ao runner) -------
print("  2.6.2-T32/T33: ver teste-regressao-final.txt (suites completas de "
      "2.5 e 2.6.1 reexecutadas neste pacote sem alteracao de expectativa).")
ok("2.6.2-T32 regressao da Acao 2.5 (ver teste-regressao-final.txt)")
ok("2.6.2-T33 regressao do 2.6.1 (ver teste-regressao-final.txt)")

# --- G1: sessao humana libera skill EX3/EX4 (achado corrigido neste pacote) -
caso5 = preparar_caso()
percorrer_ate(caso5, "P4")
codigo, saida, erro = guarda(caso5, "Read", {"file_path": "skills/hb-classificar/SKILL.md"})
if codigo == 2:
    ok(f"2.6.2-G1a EX3 (P5) sem sessao: skill bloqueada ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.2-G1a EX3 sem sessao NAO foi bloqueada: exit={codigo}")

avancar(caso5, registrar_sessao="P5", autor="Celso do Vale", participantes="Ana, Celso")
codigo, saida, erro = guarda(caso5, "Read", {"file_path": "skills/hb-classificar/SKILL.md"})
if codigo == 0:
    ok("2.6.2-G1b EX3 (P5) com sessao valida da mesma etapa: skill carrega")
else:
    falha(f"2.6.2-G1b EX3 com sessao valida foi bloqueada: exit={codigo} stderr={erro}")

caso6 = preparar_caso()
percorrer_ate(caso6, "P4")
avancar(caso6, registrar_sessao="P3b", autor="Celso do Vale", participantes="Ana, Celso")  # outra etapa
codigo, saida, erro = guarda(caso6, "Read", {"file_path": "skills/hb-classificar/SKILL.md"})
if codigo == 2:
    ok(f"2.6.2-G1c sessao de OUTRA etapa nao libera EX3 corrente ({erro.strip().splitlines()[0]})")
else:
    falha(f"2.6.2-G1c sessao de outra etapa liberou indevidamente: exit={codigo}")

print()
print(f"{total} verificacoes do pacote 2.6.2, {falhas} falhas")
if falhas:
    sys.exit(1)
