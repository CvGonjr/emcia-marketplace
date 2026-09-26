"""Expediente anterior ao caso. Sem acesso a serviço de assinatura ou escrita no caso.

Autor fixado na inicialização humana; transações locais serializadas e atômicas.
O registro de revisão/assinatura é testemunho humano, não verificação criptográfica.
"""
import argparse
import copy
import datetime
import fcntl
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import uuid


class Recusa(ValueError):
    pass


TEMPLATES = {
    "HAB-01": "HAB-01-carta-de-escopo.md",
    "HAB-02": "HAB-02-acordo-confidencialidade.md",
    "HAB-03": "HAB-03-termo-de-consentimento.md",
}
TOKEN = re.compile(r"\{\{([a-z_]+)\}\}")


def exigir(condicao, motivo):
    if not condicao:
        raise Recusa(motivo)


def texto(valor):
    exigir(isinstance(valor, str) and bool(valor.strip()), "texto obrigatório ausente")
    return valor.strip()


def pessoa(valor):
    valor = texto(valor)
    chave = re.sub(r"[\s_-]", "", valor.lower())
    exigir(not re.search(r"[<>{}]", valor) and not chave.startswith(
        ("ag0", "agente", "sistema", "assistant", "chatgpt", "codex"))
        and valor.lower() not in {"equipe", "área", "area", "time", "setor", "departamento", "a definir"},
        "é necessária uma pessoa nomeada")
    return valor


def identificador(valor):
    exigir(isinstance(valor, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", valor),
           "identificador inválido")
    return valor


def agora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def salvar(root, state):
    fd, name = tempfile.mkstemp(dir=root, prefix=".estado-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, root / "expediente.json")
    finally:
        if os.path.exists(name):
            os.unlink(name)


def evento(state, tipo, **dados):
    state["eventos"].append(dict(tipo=tipo, data=agora(), autor=state["responsavel"], **dados))


def local_externo(root):
    root = pathlib.Path(root).absolute()
    exigir(not any(p.is_symlink() for p in [root, *root.parents]), "expediente não admite symlinks")
    for p in [root, *root.parents]:
        exigir(not (p / ".git").exists() and not (p / "registro/estado.json").exists(),
               "expediente deve ficar fora de repositórios e casos")
    return root


def iniciar(root, hab_id, responsavel, caso_id=None):
    root = local_externo(root)
    pessoa(responsavel)
    identificador(hab_id)
    identificador(caso_id or hab_id)
    exigir(not root.exists(), "expediente já existe")
    root.mkdir(parents=True, mode=0o700)
    state = dict(schema=1, habilitacao=hab_id, caso_reservado=caso_id or hab_id,
                 caso_aberto=False, responsavel=responsavel, fontes={}, pendencias={},
                 campos={}, documentos={}, eventos=[], tratamento=None, revisao=None, acessos=None)
    evento(state, "ExpedienteAberto")
    salvar(root, state)
    return root


def guardar(root, data, suffix):
    path = root / "arquivos" / (uuid.uuid4().hex + suffix)
    path.parent.mkdir(exist_ok=True, mode=0o700)
    exigir(not path.parent.is_symlink(), "diretório de arquivos inválido")
    with path.open("xb") as f:
        f.write(data)
    return {"caminho": str(path.relative_to(root)), "sha256": digest(data)}


def importar(root, source, pdf=False):
    data = pathlib.Path(texto(source)).read_bytes()
    exigir(bool(data), "arquivo vazio")
    if pdf:
        exigir(data.startswith(b"%PDF-") and b"%%EOF" in data[-2048:], "arquivo não é um PDF completo")
    return guardar(root, data, ".pdf" if pdf else ".bin")


def ler_arquivo(root, ref):
    path = root / ref["caminho"]
    exigir(path.resolve().is_relative_to(root.resolve()) and not path.is_symlink(), "arquivo fora do expediente")
    data = path.read_bytes()
    exigir(digest(data) == ref["sha256"], "integridade divergente: " + ref["caminho"])
    return data


def integridade(root, node):
    if isinstance(node, dict):
        if "caminho" in node and "sha256" in node:
            ler_arquivo(root, node)
        else:
            for value in node.values():
                integridade(root, value)
    elif isinstance(node, list):
        for value in node:
            integridade(root, value)


def invalidar(state):
    state["revisao"] = None
    state["acessos"] = None
    for versions in state["documentos"].values():
        for version in versions:
            version["vigente"] = False


def inline(value):
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html.escape(value))


def documento_html(md):
    """Renderizador local do subconjunto usado pelos templates HAB; sem conteúdo remoto."""
    lines, table = [], False
    for line in md.splitlines():
        if line.startswith("|"):
            if not table:
                lines.append("<table>")
                table = True
            if re.fullmatch(r"[| :\-]+", line):
                continue
            lines.append("<tr>" + "".join("<td>" + inline(c.strip()) + "</td>"
                         for c in line.strip("|").split("|")) + "</tr>")
            continue
        if table:
            lines.append("</table>")
            table = False
        heading = re.match(r"^(#{1,6}) (.*)", line)
        if heading:
            n = len(heading[1])
            lines.append(f"<h{n}>" + inline(heading[2]) + f"</h{n}>")
        elif line == "---":
            lines.append("<hr>")
        elif line:
            lines.append("<div>" + inline(line) + "</div>")
        else:
            lines.append("<br>")
    if table:
        lines.append("</table>")
    return ('<!doctype html><html lang="pt-BR"><meta charset="utf-8">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">'
            '<style>@page{size:A4;margin:20mm}body{font:11pt Arial;line-height:1.45;color:#18212b}'
            'table{border-collapse:collapse;width:100%;margin:12px 0}td{border:1px solid #ccc;padding:6px}'
            'h1{font-size:21pt}h2{font-size:15pt;break-after:avoid}h3{font-size:12pt;break-after:avoid}'
            'div,td{overflow-wrap:break-word}td{min-width:75px}tr{break-inside:avoid}</style><body>' + "\n".join(lines) + '</body></html>')


def pdf_bytes(md, browser):
    executable = shutil.which(texto(browser))
    exigir(executable, "navegador ausente; informe Chrome/Chromium instalado")
    with tempfile.TemporaryDirectory(prefix="emcia-hab-pdf-") as tmp:
        base = pathlib.Path(tmp)
        (base / "documento.html").write_text(documento_html(md), encoding="utf-8")
        result = subprocess.run([executable, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                                 "--disable-background-networking", "--no-first-run",
                                 "--user-data-dir=" + str(base / "perfil"),
                                 "--print-to-pdf=" + str(base / "documento.pdf"),
                                 (base / "documento.html").as_uri()], capture_output=True, timeout=60)
        exigir(result.returncode == 0 and (base / "documento.pdf").exists(), "falha ao gerar PDF no navegador")
        data = (base / "documento.pdf").read_bytes()
        exigir(data.startswith(b"%PDF-") and b"%%EOF" in data[-2048:], "PDF gerado inválido")
        return data


def completa(state):
    for doc in TEMPLATES:
        versions = state["documentos"].get(doc, [])
        if not versions:
            return False
        v = versions[-1]
        if not v["vigente"] or not v.get("liberacao") or not v.get("assinatura"):
            return False
    return True


def aplicar(root, s, action, p):
    exigir(not ({"autor", "responsavel"} & p.keys()), "autoria vem do expediente, não do argumento")
    if action == "estado":
        return {"habilitacao": s["habilitacao"], "caso_reservado": s["caso_reservado"],
                "caso_aberto": False, "formalizacao_completa": completa(s),
                "pendencias": s["pendencias"], "documentos": s["documentos"],
                "tratamento_registrado": bool(s["tratamento"]), "acessos": s["acessos"]}
    if action == "tratamento":
        exigir(not s["fontes"], "condições devem ser registradas antes da coleta")
        exigir(p.get("escopo") == "administrativo", "somente informações administrativas antes de 0d")
        s["tratamento"] = {"escopo": "administrativo", "condicoes": texto(p.get("condicoes")),
                           "provedor": texto(p.get("provedor")), "decisor": pessoa(p.get("decisor")),
                           "evidencia": importar(root, p.get("evidencia"))}
    elif action == "receber":
        ident = identificador(p.get("id"))
        exigir(ident not in s["fontes"], "fonte já registrada")
        form, submission = texto(p.get("formulario")), texto(p.get("submissao"))
        exigir(not any(f["formulario"] == form and f["submissao"] == submission for f in s["fontes"].values()),
               "submissão duplicada")
        rodada = p.get("rodada")
        exigir(type(rodada) is int and rodada >= 0, "rodada inválida")
        if rodada:
            exigir(any(x["rodada"] == rodada and x["estado"] == "aberta" for x in s["pendencias"].values()),
                   "rodada sem pendência aberta")
        canal = p.get("canal", "manual")
        exigir(canal in {"manual", "tally-mcp"}, "canal inválido")
        exigir(canal != "tally-mcp" or bool(s["tratamento"]), "MCP exige condições de tratamento prévias")
        exigir(p.get("escopo", "administrativo") == "administrativo", "dados operacionais aguardam 0d")
        s["fontes"][ident] = dict(formulario=form, submissao=submission, rodada=rodada, canal=canal,
                                  respondente=pessoa(p.get("respondente")),
                                  versao_perguntas=texto(p.get("versao_perguntas")),
                                  recebido_em=agora(), arquivo=importar(root, p.get("arquivo")))
        invalidar(s)
    elif action == "pendencia":
        ident = identificador(p.get("id"))
        exigir(ident not in s["pendencias"], "pendência já existe; use reabrir")
        exigir(p.get("origem") in s["fontes"], "origem ausente")
        rodada = p.get("rodada")
        exigir(type(rodada) is int and rodada > 0, "rodada inválida")
        s["pendencias"][ident] = dict(origem=p["origem"], pergunta=texto(p.get("pergunta")),
                                       efeito=texto(p.get("efeito")), rodada=rodada, estado="aberta")
        invalidar(s)
    elif action in {"resolver", "reabrir"}:
        pend = s["pendencias"].get(p.get("id"))
        exigir(pend is not None, "pendência ausente")
        decision = dict(decisor=pessoa(p.get("decisor")), motivo=texto(p.get("motivo")), data=agora())
        if action == "resolver":
            exigir(pend["estado"] == "aberta", "pendência já resolvida")
            source = s["fontes"].get(p.get("resposta"))
            exigir(source is not None and source["rodada"] == pend["rodada"], "resposta de rodada incorreta")
            decision["resposta"] = p["resposta"]
            pend["estado"] = "resolvida"
        else:
            exigir(pend["estado"] == "resolvida", "pendência já aberta")
            exigir(type(p.get("rodada")) is int and p["rodada"] > pend["rodada"], "nova rodada deve ser posterior")
            pend["rodada"], pend["estado"] = p["rodada"], "aberta"
        pend.setdefault("decisoes", []).append(decision)
        invalidar(s)
    elif action == "consolidar":
        exigir(not any(x["estado"] == "aberta" for x in s["pendencias"].values()), "há pendências abertas")
        campos = p.get("campos")
        exigir(isinstance(campos, dict) and campos, "campos ausentes")
        for key, value in campos.items():
            exigir(re.fullmatch(r"[a-z_]+", key) and isinstance(value, dict), "campo inválido")
            texto(value.get("valor"))
            exigir("{{" not in value["valor"] and "}}" not in value["valor"], "placeholder em valor")
            exigir(value.get("fonte") in s["fontes"], "campo sem fonte registrada: " + key)
        invalidar(s)
        s["campos"] = campos
    elif action == "revisar":
        exigir(bool(s["campos"]), "consolidação ausente")
        exigir(not any(x["estado"] == "aberta" for x in s["pendencias"].values()), "há pendências abertas")
        exigir(p.get("qualificacao_0a") is True and p.get("conteudo_conferido") is True,
               "revisão exige qualificação e conferência humana do conteúdo canônico")
        s["revisao"] = dict(decisor=pessoa(p.get("decisor")), motivo=texto(p.get("motivo")),
                             evidencia=importar(root, p.get("evidencia")), data=agora())
    elif action == "gerar":
        exigir(s["revisao"] is not None, "revisão humana ausente")
        template_root = pathlib.Path(texto(p.get("templates")))
        browser = p.get("navegador", "google-chrome")
        prepared = {}
        for doc, filename in TEMPLATES.items():
            raw = (template_root / filename).read_bytes()
            md = raw.decode("utf-8")
            md = md.replace("| **Estado** | Template |", "| **Estado** | Para assinatura |")
            n = len(s["documentos"].get(doc, [])) + 1
            controls = {"caso_id": s["caso_reservado"], "responsavel_emcia": s["responsavel"],
                        "status_assinatura": "Aguardando assinatura", "versao_assinada": "Pendente",
                        "evidencia_assinatura": "Pendente", "data_assinatura_cliente": "A registrar na assinatura",
                        "data_assinatura_emcia": "A registrar na assinatura"}
            fields = {k: v["valor"] for k, v in s["campos"].items()}
            fields.update(controls)
            missing = set(TOKEN.findall(md)) - fields.keys()
            exigir(not missing, "campos ausentes em " + doc + ": " + ", ".join(sorted(missing)))
            md = TOKEN.sub(lambda m: fields[m[1]], md)
            md += (f"\n\n---\n\nIdentificação de emissão: {doc} · versão {n}.\n"
                   f"Habilitação: {s['habilitacao']}. Identificador do futuro caso reservado: {s['caso_reservado']}. "
                   "O caso ainda não foi aberto.\n"
                   "O controle acima descreve a emissão; a conclusão da assinatura será registrada "
                   "no expediente, preservando este arquivo e os comprovantes do serviço escolhido.\n")
            exigir("{{" not in md and "}}" not in md, "placeholder não resolvido")
            prepared[doc] = (raw, md, pdf_bytes(md, browser), n)
        for doc, (raw, md, pdf, n) in prepared.items():
            for previous in s["documentos"].get(doc, []):
                previous["vigente"] = False
            s["documentos"].setdefault(doc, []).append(dict(versao=n, vigente=True,
                template=guardar(root, raw, ".md"), markdown=guardar(root, md.encode(), ".md"),
                pdf=guardar(root, pdf, ".pdf"), revisao=copy.deepcopy(s["revisao"]),
                campos=copy.deepcopy(s["campos"]), liberacao=None, assinatura=None))
        s["acessos"] = None
    elif action in {"liberar", "assinatura", "ocorrencia"}:
        versions = s["documentos"].get(p.get("documento"), [])
        exigir(bool(versions), "documento ainda não foi gerado")
        v = versions[-1]
        exigir(v["vigente"] and p.get("versao") == v["versao"], "versão não vigente")
        decisor = pessoa(p.get("decisor"))
        if action == "liberar":
            exigir(v["liberacao"] is None, "versão já liberada; gere nova versão para alterar")
            exigir(p.get("pdf_conferido") is True, "conferência visual dos PDFs obrigatória")
            signers = p.get("signatarios")
            exigir(isinstance(signers, list) and bool(signers), "signatários ausentes")
            for signer in signers:
                exigir(isinstance(signer, dict), "signatário inválido")
                pessoa(signer.get("nome"))
                exigir(signer.get("papel") in {"organizacao", "emcia"}, "papel inválido")
                texto(signer.get("competencia"))
            exigir({x["papel"] for x in signers} == {"organizacao", "emcia"}, "assinaturas de ambas as partes exigidas")
            exigir(len({(x["nome"], x["papel"]) for x in signers}) == len(signers), "signatário duplicado")
            expected_client = v["campos"].get("signatario", {}).get("valor")
            if expected_client:
                exigir(any(x["nome"] == expected_client and x["papel"] == "organizacao" for x in signers),
                       "signatário da organização diverge do documento")
            exigir(any(x["nome"] == s["responsavel"] and x["papel"] == "emcia" for x in signers),
                   "signatário EMCIA diverge do documento")
            v["liberacao"] = dict(decisor=decisor, data=agora(), signatarios=signers,
                                  ferramenta=texto(p.get("ferramenta")), operador=pessoa(p.get("operador")))
        elif action == "assinatura":
            exigir(v["liberacao"] is not None, "documento não liberado")
            exigir(v["assinatura"] is None, "assinatura já registrada")
            expected = {(x["nome"], x["papel"]) for x in v["liberacao"]["signatarios"]}
            signed = p.get("signatarios", [])
            exigir(isinstance(signed, list), "signatários inválidos")
            actual = {(pessoa(x.get("nome")), x.get("papel")) for x in signed}
            exigir(actual == expected and len(signed) == len(expected), "assinaturas incompletas ou divergentes")
            for signer in signed:
                datetime.date.fromisoformat(texto(signer.get("data")))
            exigir(p.get("conteudo_conferido") is True and p.get("evidencias_conferidas") is True,
                   "assinatura exige conferência humana do conteúdo e das evidências")
            v["assinatura"] = dict(decisor=decisor, data=agora(), signatarios=signed,
                arquivo=importar(root, p.get("arquivo"), pdf=True),
                evidencia=importar(root, p.get("evidencia")), referencia=texto(p.get("referencia")))
        else:
            exigir(p.get("status") in {"recusado", "expirado", "cancelado"}, "ocorrência inválida")
            v.setdefault("ocorrencias", []).append(dict(status=p["status"], decisor=decisor,
                                                       motivo=texto(p.get("motivo")), data=agora()))
            v["vigente"] = False
            s["acessos"] = None
    elif action == "acessos":
        exigir(completa(s), "0b precisa estar concluída antes de confirmar acessos")
        pessoa(p.get("patrocinador"))
        pessoa(p.get("executor"))
        pessoa(p.get("decisor"))
        datetime.date.fromisoformat(texto(p.get("data_sessao")))
        exigir(p.get("executor_liberado") is True and p.get("agenda_reservada") is True,
               "executor liberado e agenda reservada são obrigatórios")
        texto(p.get("autoridade_patrocinador"))
        itens = p.get("itens")
        exigir(isinstance(itens, list) and itens, "matriz de acessos ausente")
        for item in itens:
            texto(item.get("item"))
            exigir(item.get("status") in {"concedido", "negado"}, "acesso deve ser efetivo ou negado")
            texto(item.get("evidencia"))
            if item["status"] == "negado":
                texto(item.get("motivo"))
                texto(item.get("restricao"))
        exigir(any(i["status"] == "concedido" for i in itens), "ao menos uma fonte deve estar acessível")
        s["acessos"] = copy.deepcopy(p)
        s["acessos"]["data_registro"] = agora()
    elif action == "preparar-0d":
        exigir(completa(s) and s["acessos"] is not None, "formalização e acessos efetivos são obrigatórios")
        desfecho = "prosseguir com restrição" if any(
            i["status"] == "negado" for i in s["acessos"]["itens"]) else "prosseguir"
        return {"pronto_para_0d": True, "desfecho_proposto": desfecho,
                "caso_reservado": s["caso_reservado"], "caso_aberto": False,
                "instrucoes": "Abrir com novo-caso.sh fora da sessão, importar o expediente pelos mecanismos autorizados, registrar desfecho e selar antes de F0."}
    elif action == "nao-prosseguir":
        s["recusa"] = dict(decisor=pessoa(p.get("decisor")), motivo=texto(p.get("motivo")),
                            condicao_retomada=texto(p.get("condicao_retomada")), data=agora())
        invalidar(s)
    elif action == "concluir-0b":
        exigir(completa(s), "três documentos vigentes, liberados e assinados são obrigatórios")
        return {"formalizacao_completa": True, "proxima_etapa": "0c", "caso_aberto": False}
    else:
        raise Recusa("operação desconhecida")
    return {"operacao": action, "registrado": True, "formalizacao_completa": completa(s)}


def executar(root, action, payload):
    root = local_externo(root)
    exigir((root / "expediente.json").is_file(), "expediente ausente; inicialize fora da sessão do agente")
    exigir(not (root / "expediente.json").is_symlink() and not (root / ".lock").is_symlink(), "symlink recusado")
    with (root / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        original = json.loads((root / "expediente.json").read_text(encoding="utf-8"))
        pessoa(original["responsavel"])
        s = copy.deepcopy(original)
        try:
            if isinstance(payload, pathlib.Path):
                payload = json.loads(payload.read_text(encoding="utf-8"))
            exigir(isinstance(payload, dict), "entrada deve ser objeto JSON")
            integridade(root, s)
            result = aplicar(root, s, action, payload)
            evento(s, "OperacaoRegistrada", operacao=action,
                   entrada=copy.deepcopy(payload),
                   entrada_sha256=digest(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()))
        except (ValueError, OSError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as error:
            evento(original, "Recusado", operacao=action, motivo=str(error))
            salvar(root, original)
            raise Recusa(str(error)) from error
        salvar(root, s)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operacao", help="iniciar, estado, tratamento, receber, pendencia, resolver, reabrir, consolidar, revisar, gerar, liberar, assinatura, ocorrencia, concluir-0b, acessos, preparar-0d, nao-prosseguir")
    parser.add_argument("--expediente", required=True, type=pathlib.Path)
    parser.add_argument("--entrada", type=pathlib.Path, help="arquivo JSON conforme reference/habilitacao.md")
    parser.add_argument("--responsavel", help="somente na inicialização humana fora do agente")
    parser.add_argument("--id", help="identificador da habilitação na inicialização")
    parser.add_argument("--caso", help="identificador reservado do futuro caso")
    args = parser.parse_args()
    try:
        if args.operacao == "iniciar":
            result = {"expediente": str(iniciar(args.expediente, args.id, args.responsavel, args.caso))}
        else:
            if args.responsavel is not None or args.id is not None or args.caso is not None:
                executar(args.expediente, args.operacao, {"autor": args.responsavel})
            result = executar(args.expediente, args.operacao,
                              args.entrada if args.entrada else {})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (Recusa, OSError, ValueError) as error:
        parser.exit(1, "Recusado: " + str(error) + "\n")


if __name__ == "__main__":
    main()
