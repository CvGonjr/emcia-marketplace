#!/usr/bin/env python3
"""Testes estruturais do pacote 2.5.1 com evidência bruta opcional."""
import argparse
import datetime
import json
import pathlib
import shutil
import subprocess
import tempfile
import textwrap


RAIZ = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = RAIZ / "eiac-campo" / "template-caso"
VALIDADOR = RAIZ / "eiac-nucleo" / "scripts" / "estrutura.py"
CENTRAIS = {
    "determinismo", "frequencia", "consequencia_do_erro",
    "decisor_quando_nao_cobre", "entradas", "excecoes_conhecidas",
    "estabilidade",
}


def bloco_procedencia(procedencia, evidencia_objeto=False):
    if procedencia == "I":
        return 'premissa: "padrão demonstrado pela amostra"\nevidencia: ""'
    if procedencia == "V" and evidencia_objeto:
        return textwrap.dedent("""\
            premissa: ""
            evidencia:
              tipo: observacao
              referencia: sessao-P3b-001""")
    if procedencia == "V":
        return 'premissa: ""\nevidencia: "leitura de volta de 2026-09-18"'
    return 'premissa: ""\nevidencia: ""'


def termo(procedencia="D"):
    return "\n".join([
        "id: T-001",
        "termo: guia",
        "significado: documento de autorizacao do convenio",
        "nao_e: nota fiscal",
        "sinonimos_em_uso: [autorizacao, pedido]",
        f"procedencia: {procedencia}",
        "declarado_por: Claudia Ferreira",
        "registrado_por: Rafael Nogueira",
        'data: "2026-09-18"',
        bloco_procedencia(procedencia),
        "",
    ])


def entidade(procedencia="D"):
    return "\n".join([
        "id: E-001",
        "entidade: Guia",
        "atributos:",
        "  - nome: convenio",
        "    tipo: categoria",
        "    obrigatorio: true",
        "relacoes:",
        "  - com: Paciente",
        "    cardinalidade: muitos-para-um",
        "onde_vive: [F-001]",
        f"procedencia: {procedencia}",
        "declarado_por: Claudia Ferreira",
        "registrado_por: Rafael Nogueira",
        'data: "2026-09-18"',
        bloco_procedencia(procedencia),
        "",
    ])


def regra(procedencia="D"):
    return "\n".join([
        "id: RN-001",
        "enunciado: quando a autorizacao chega, a guia e enviada no mesmo dia",
        "gatilho: recebimento_da_autorizacao",
        f"procedencia: {procedencia}",
        "autoria_conteudo: Claudia Ferreira",
        "registrado_por: Rafael Nogueira",
        'data: "2026-09-18"',
        "origem_do_conhecimento: experiencia_propria",
        bloco_procedencia(procedencia, evidencia_objeto=True),
        "classificacao_confronto:",
        '  classe: ""',
        '  referencia_p3d: ""',
        "documento_de_origem: null",
        "determinismo: admite_julgamento",
        "frequencia: rotineira",
        "consequencia_do_erro: alta",
        "decisor_quando_nao_cobre: Claudia Ferreira",
        "entradas: [E-001, T-001, F-001]",
        "excecoes_conhecidas: []",
        "estabilidade: muda quando o convenio revisa o contrato",
        "versao: 1",
        "historico: []",
        "",
    ])


def fonte(procedencia="D"):
    return "\n".join([
        "id: F-001",
        "fonte: planilha de controle de envios",
        "tipo: planilha",
        "responsavel: Claudia Ferreira",
        "contrato:",
        "  estrutura: uma linha por guia enviada",
        "  significado: registra envio, nao emissao",
        "  qualidade: preenchida ao fim do dia",
        "acesso: leitura autorizada",
        f"procedencia: {procedencia}",
        "registrado_por: Rafael Nogueira",
        'data: "2026-09-18"',
        bloco_procedencia(procedencia),
        "",
    ])


FABRICAS = {
    "termo": termo,
    "entidade": entidade,
    "regra": regra,
    "fonte": fonte,
}


def sem_linha(texto, prefixo):
    return "\n".join(
        linha for linha in texto.splitlines()
        if not linha.lstrip().startswith(prefixo)
    ) + "\n"


def executar_validador(caso, tipo, conteudo, sufixo):
    arquivo = caso / f"teste-{sufixo}.yaml"
    arquivo.write_text(conteudo, encoding="utf-8")
    comando = [
        "python3", str(VALIDADOR), "--tipo", tipo,
        "--arquivo", str(arquivo.relative_to(caso)),
    ]
    proc = subprocess.run(
        comando, cwd=caso, text=True, capture_output=True, check=False,
    )
    return {
        "comando": " ".join(comando),
        "codigo": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def resultado_simples(caso, tipo, conteudo, sufixo, codigo, trecho=None):
    execucao = executar_validador(caso, tipo, conteudo, sufixo)
    passou = execucao["codigo"] == codigo
    if trecho:
        passou = passou and trecho in execucao["stderr"]
    return [execucao], passou


def t09(caso):
    execucoes = []
    for tipo, fabrica in FABRICAS.items():
        for procedencia in ("D", "I", "V"):
            execucoes.append(executar_validador(
                caso, tipo, fabrica(procedencia), f"T09-{tipo}-{procedencia}",
            ))
    return execucoes, all(item["codigo"] == 0 for item in execucoes)


def t10(caso):
    execucoes = []
    obsoletas = ("campo", "antitese", "conversa", "livre", "externo",
                 "declarado", "inferido", "verificado")
    for valor in obsoletas:
        execucoes.append(executar_validador(
            caso, "termo", termo().replace("procedencia: D", f"procedencia: {valor}"),
            f"T10-{valor}",
        ))
    passou = all(
        item["codigo"] == 1 and "procedencia invalida" in item["stderr"]
        for item in execucoes
    )
    return execucoes, passou


def t11(caso):
    execucao = executar_validador(caso, "regra", regra(), "T11")
    schema = json.loads((caso / "registro" / "contexto.schema.json").read_text())
    obrigatorios = set(schema["objetos"]["regra"]["required"])
    faltando = sorted(CENTRAIS - obrigatorios)
    execucao["stdout"] += (
        "sete campos centrais presentes no schema\n" if not faltando
        else f"campos centrais ausentes no schema: {faltando}\n"
    )
    return [execucao], execucao["codigo"] == 0 and not faltando


def gravar_evidencia(destino, teste, requisito, esperado, obtido,
                     execucoes, passou, head_inicial):
    agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    comandos = "\n".join(
        f"[{indice}] {item['comando']}" for indice, item in enumerate(execucoes, 1)
    )
    codigos = "\n".join(
        f"[{indice}] {item['codigo']}" for indice, item in enumerate(execucoes, 1)
    )
    stdout = "".join(
        f"--- comando {indice} ---\n{item['stdout']}"
        for indice, item in enumerate(execucoes, 1)
    ) or "(vazio)\n"
    stderr = "".join(
        f"--- comando {indice} ---\n{item['stderr']}"
        for indice, item in enumerate(execucoes, 1)
    ) or "(vazio)\n"
    conteudo = f"""PACOTE: 2.5.1
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
RESULTADO FINAL: {'PASS' if passou else 'FAIL'}
"""
    (destino / f"teste-{teste}.txt").write_text(conteudo, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidencias")
    ap.add_argument("--head-inicial")
    args = ap.parse_args()

    destino = pathlib.Path(args.evidencias).resolve() if args.evidencias else None
    if destino:
        destino.mkdir(parents=True, exist_ok=True)
    head_inicial = args.head_inicial or subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=RAIZ, text=True,
        capture_output=True, check=True,
    ).stdout.strip()

    with tempfile.TemporaryDirectory() as temporario:
        caso = pathlib.Path(temporario) / "caso"
        shutil.copytree(TEMPLATE, caso)
        casos = [
            ("2.5.1-T01", "Termo válido", "aceite", "termo aceito",
             lambda: resultado_simples(caso, "termo", termo(), "T01", 0)),
            ("2.5.1-T02", "Entidade válida", "aceite", "entidade aceita",
             lambda: resultado_simples(caso, "entidade", entidade(), "T02", 0)),
            ("2.5.1-T03", "Regra válida", "aceite", "regra aceita",
             lambda: resultado_simples(caso, "regra", regra(), "T03", 0)),
            ("2.5.1-T04", "Fonte válida", "aceite", "fonte aceita",
             lambda: resultado_simples(caso, "fonte", fonte(), "T04", 0)),
            ("2.5.1-T05", "Termo sem significado", "recusa",
             "campo significado recusado",
             lambda: resultado_simples(
                 caso, "termo", sem_linha(termo(), "significado:"), "T05", 1,
                 "campo obrigatorio ausente: significado",
             )),
            ("2.5.1-T06", "Entidade sem nome", "recusa",
             "campo entidade recusado",
             lambda: resultado_simples(
                 caso, "entidade", sem_linha(entidade(), "entidade:"), "T06", 1,
                 "campo obrigatorio ausente: entidade",
             )),
            ("2.5.1-T07", "Regra sem estabilidade", "recusa",
             "campo central estabilidade recusado",
             lambda: resultado_simples(
                 caso, "regra", sem_linha(regra(), "estabilidade:"), "T07", 1,
                 "campo obrigatorio ausente: estabilidade",
             )),
            ("2.5.1-T08", "Fonte sem contrato.significado", "recusa",
             "contrato sem significado recusado",
             lambda: resultado_simples(
                 caso, "fonte", sem_linha(fonte(), "significado:"), "T08", 1,
                 "campo obrigatorio ausente: contrato.significado",
             )),
            ("2.5.1-T09", "D/I/V nos quatro objetos", "aceite",
             "12 combinações aceitas", lambda: t09(caso)),
            ("2.5.1-T10", "Taxonomias obsoletas", "recusa",
             "8 valores obsoletos recusados", lambda: t10(caso)),
            ("2.5.1-T11", "Sete campos centrais da Regra", "aceite",
             "sete campos presentes e regra aceita", lambda: t11(caso)),
        ]

        falhas = 0
        print("== objetos CTX — pacote 2.5.1")
        for teste, requisito, esperado, obtido, executar in casos:
            execucoes, passou = executar()
            if destino:
                gravar_evidencia(
                    destino, teste, requisito, esperado, obtido,
                    execucoes, passou, head_inicial,
                )
            if passou:
                print(f"  ok    {teste} {requisito}")
            else:
                falhas += 1
                print(f"  FALHA {teste} {requisito}")

    if falhas:
        print(f"\n{falhas} teste(s) estrutural(is) falharam")
        raise SystemExit(1)
    print("\n11 testes estruturais aprovados")


if __name__ == "__main__":
    main()
