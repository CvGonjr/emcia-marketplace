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
from contextvars import ContextVar
from collections.abc import Mapping
REGRA_PESSOA = ContextVar("regra_pessoa", default=None)


class Recusa(ValueError):
    pass


CODIGOS_HAB = ('HAB-01', 'HAB-02', 'HAB-03')


class Templates(Mapping):
    """Códigos estáveis; nomes resolvidos no APR-01 vigente, sem cache."""

    def __iter__(self):
        return iter(CODIGOS_HAB)

    def __len__(self):
        return len(CODIGOS_HAB)

    def __getitem__(self, codigo):
        if codigo not in CODIGOS_HAB:
            raise KeyError(codigo)
        return pathlib.PurePosixPath(templates_aprovados()[codigo]).name


TEMPLATES = Templates()
TOKEN = re.compile(r"\{\{([a-z_]+)\}\}")
APR = pathlib.Path(__file__).resolve().parents[1] / 'reference/metodo/EMCIA-APR-01-registro-de-aprovacoes.md'


def exigir(condicao, motivo):
    if not condicao:
        raise Recusa(motivo)


def texto(valor):
    exigir(isinstance(valor, str) and bool(valor.strip()), "texto obrigatório ausente")
    return valor.strip()


def pessoa(valor):
    valor = texto(valor)
    # Habilitação é anterior ao caso: a regra vem do template do método,
    # explicitamente, e é copiada para o expediente na abertura.
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'eiac-nucleo/scripts'))
    import estado as E
    regra = REGRA_PESSOA.get() or json.loads((pathlib.Path(__file__).resolve().parents[1] /
        'template-caso/registro/playbook.json').read_text())['pessoa_nomeada']
    exigir(E.pessoa_nomeada(valor, regra), 'é necessária uma pessoa nomeada com nome e sobrenome')
    return valor


def identificador(valor):
    exigir(isinstance(valor, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", valor),
           "identificador inválido")
    return valor


def agora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def registros_aprovados(caminho=None, linha_de_base=None):
    """Código, caminho e hash da tabela; uma única linha de base aprovada."""
    registro = (caminho or APR).read_text(encoding='utf-8')
    exigir('| **Estado** | Aprovado |' in registro, 'APR-01 não aprovado')
    exigir('## 2. Documentos aprovados' in registro and '## 3. Regra de aprovação' in registro,
           'tabela de aprovação do APR-01 ausente')
    tabela = registro.split('## 2. Documentos aprovados', 1)[1].split('## 3. Regra de aprovação', 1)[0]
    registros = {}
    bases = set()
    for linha in tabela.splitlines():
        if not re.match(r'^\| (?:EMCIA-|HAB-)', linha):
            continue
        cols = [c.strip() for c in linha.strip('|').split('|')]
        exigir(len(cols) == 7, 'linha inválida no APR-01')
        codigo, nome, versao, sha, data, aprovador, base = cols
        p = pathlib.PurePosixPath(nome)
        exigir(not p.is_absolute() and '..' not in p.parts and nome not in registros
               and re.fullmatch(r'[0-9a-f]{64}', sha)
               and re.fullmatch(r'metodo-v\d+\.\d+', base)
               and (linha_de_base is None or base == linha_de_base),
               'hash, caminho ou linha de base inválidos no APR-01')
        bases.add(base)
        registros[nome] = {'codigo': codigo, 'sha256': sha, 'versao': versao}
    exigir(bool(registros) and len(bases) == 1, 'APR-01 sem documentos aprovados ou com linhas de base distintas')
    return registros


def aprovacoes(caminho=None, linha_de_base=None):
    """Hashes por caminho; conserva a interface usada na conferência do pacote."""
    return {nome: r['sha256'] for nome, r in registros_aprovados(caminho, linha_de_base).items()}


def templates_aprovados(registros=None):
    registros = registros if registros is not None else registros_aprovados()
    caminhos = {}
    for codigo in CODIGOS_HAB:
        candidatos = [nome for nome, r in registros.items() if r['codigo'] == codigo]
        exigir(len(candidatos) == 1,
               f'APR-01: exige exatamente um arquivo aprovado para {codigo}; encontrados {len(candidatos)}')
        caminhos[codigo] = candidatos[0]
    return caminhos


def documento_cliente(md, doc):
    """Retira seções internas delimitadas, preservando os demais bytes do texto."""
    linhas = md.splitlines(keepends=True)
    controles = [i for i, l in enumerate(linhas) if l.rstrip('\r\n') == '## Controle do modelo']
    identificacoes = [i for i, l in enumerate(linhas) if l.rstrip('\r\n') == '## Identificação do caso']
    historicos = [i for i, l in enumerate(linhas)
                 if re.fullmatch(r'## \d+\. Histórico de revisões do modelo', l.rstrip('\r\n'))]
    avisos = [i for i, l in enumerate(linhas) if re.match(r'^>\s*\*\*Revisão jurídica:\*\*', l)]
    exigir(len(controles) == len(identificacoes) == len(historicos) == 1
           and controles[0] < identificacoes[0] < historicos[0]
           and (doc == 'HAB-01' or bool(avisos)), 'marcas internas esperadas ausentes ou duplicadas em ' + doc)
    retirar = set()
    for inicio in (controles[0], historicos[0]):
        fim = next((i for i in range(inicio + 1, len(linhas)) if linhas[i].startswith('## ')), len(linhas))
        if inicio == controles[0]:
            exigir(fim == identificacoes[0], 'marcas de identificação inesperadas em ' + doc)
        retirar.update(range(inicio, fim))
    for inicio in avisos:
        fim = inicio + 1
        while fim < len(linhas) and re.match(r'^>($|\s)', linhas[fim]):
            fim += 1
        retirar.update(range(inicio, fim))
    return ''.join(l for i, l in enumerate(linhas) if i not in retirar)


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
    regra = json.loads((pathlib.Path(__file__).resolve().parents[1] / "template-caso/registro/playbook.json").read_text())["pessoa_nomeada"]
    REGRA_PESSOA.set(regra)
    pessoa(responsavel)
    identificador(hab_id)
    identificador(caso_id or hab_id)
    exigir(not root.exists(), "expediente já existe")
    root.mkdir(parents=True, mode=0o700)
    state = dict(pessoa_nomeada=regra, schema=1, habilitacao=hab_id, caso_reservado=caso_id or hab_id,
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
    state["rascunhos_documentos"] = None
    state["rascunhos_assinaturas"] = None
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


def preparar_minutas(s, p):
    template_root = pathlib.Path(texto(p.get("templates")))
    prepared = {}
    situacoes = {}
    config_path = pathlib.Path(p.get("config_emcia", pathlib.Path.home()/".emcia/config.json"))
    config = json.loads(config_path.read_text()) if config_path.is_file() and not config_path.is_symlink() else {}
    aceitacao = config.get("aceitacao_minutas")
    aceita = (isinstance(aceitacao,dict) and aceitacao.get("texto")=="uso as minutas sem ratificação jurídica"
              and aceitacao.get("responsavel")==s["responsavel"] and config.get("responsavel")==s["responsavel"]
              and bool(aceitacao.get("data")) and not aceitacao.get("revogada_em"))
    registros = registros_aprovados()
    caminhos = templates_aprovados(registros)
    for doc, caminho in caminhos.items():
        filename = pathlib.PurePosixPath(caminho).name
        raw = (template_root / filename).read_bytes()
        exigir(registros[caminho]['sha256'] == digest(raw),
               'APR-01: hash do template divergente em ' + doc)
        md = documento_cliente(raw.decode('utf-8'), doc)
        juridica = next((r for r in reversed(s.get('revisoes_juridicas', []))
                         if r.get('resultado') == 'aprovado' and r['documentos'].get(doc) == digest(raw)), None)
        exigir(doc == 'HAB-01' or juridica is not None or aceita,
               'registre revisao-juridica aprovada para o hash exato de ' + doc +
               ' ou aceite as minutas sem ratificação jurídica em /eiac-campo:iniciar antes de gerar')
        situacoes[doc] = dict(estado='ratificada' if juridica else ('sem ratificação' if doc!='HAB-01' else 'não aplicável'),
                              data=agora(), revisao=copy.deepcopy(juridica),
                              aceitacao=copy.deepcopy(aceitacao) if doc!='HAB-01' and not juridica else None)
        situacoes[doc]['minuta'] = dict(codigo=doc, arquivo=caminho, versao=registros[caminho]['versao'].split()[0], versao_aprovada=registros[caminho]['versao'], sha256=digest(raw))
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
               "Estado de emissão: Para assinatura.\n"
               f"Habilitação: {s['habilitacao']}. Identificador do futuro caso reservado: {s['caso_reservado']}. "
               "O caso ainda não foi aberto.\n"
               "O controle acima descreve a emissão; a conclusão da assinatura será registrada "
               "no expediente, preservando este arquivo e os comprovantes do serviço escolhido.\n")
        exigir("{{" not in md and "}}" not in md, "placeholder não resolvido")
        prepared[doc] = (raw, md, n, juridica)
    return prepared, situacoes


def aplicar(root, s, action, p):
    exigir(not ({"autor", "responsavel"} & p.keys()), "autoria vem do expediente, não do argumento")
    if action == "estado":
        return {"habilitacao": s["habilitacao"], "caso_reservado": s["caso_reservado"],
                "caso_aberto": False, "formalizacao_completa": completa(s),
                "pendencias": s["pendencias"], "documentos": s["documentos"],
                "tratamento_registrado": bool(s["tratamento"]), "acessos": s["acessos"],
                "revisoes_juridicas": s.get('revisoes_juridicas', [])}
    if action in {"preparar-documentos", "aprovar-documentos", "preparar-assinaturas", "aprovar-assinaturas"}:
        import habilitacao_lotes as L
        return L.aplicar(root, s, action, p)
    if action in {"planejar-acessos", "confirmar-acessos"}:
        import acessos_administrativos as C
        return C.planejar(root, s) if action == "planejar-acessos" else C.confirmar(root, s, p)
    if action == "tratamento":
        exigir(not s["fontes"], "condições devem ser registradas antes da coleta")
        exigir(p.get("escopo") == "administrativo", "somente informações administrativas antes de 0d")
        s["tratamento"] = {"escopo": "administrativo", "condicoes": texto(p.get("condicoes")),
                           "provedor": texto(p.get("provedor")), "decisor": pessoa(p.get("decisor")),
                           "evidencia": importar(root, p.get("evidencia"))}
    elif action == "tratamento-padrao":
        import coleta_administrativa as C
        C.tratamento_padrao(root, s, p)
    elif action == "receber-mensagem":
        import coleta_administrativa as C
        C.receber_mensagem(root, s, p)
    elif action == "receber-exportacao":
        import coleta_administrativa as C
        C.receber_exportacao(root, s, p)
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
        if p.get('workspace_id') is not None:
            s['fontes'][ident]['workspace_id'] = texto(p['workspace_id'])
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
    elif action == 'revisao-juridica':
        obrigatorios = {'revisor', 'decisor', 'data', 'documentos', 'evidencia', 'resultado'}
        exigir(obrigatorios <= set(p) <= obrigatorios | {'ciclo'},
               'revisao-juridica exige revisor, decisor, data, documentos, evidencia e resultado; '
               'somente ciclo é opcional; não admite dispensa')
        exigir(p.get('resultado') == 'aprovado', 'resultado jurídico obrigatório: somente "aprovado" é aceito')
        ciclo = {'ciclo': texto(p['ciclo'])} if 'ciclo' in p else {}
        revisor, decisor = pessoa(p.get('revisor')), pessoa(p.get('decisor'))
        data = texto(p.get('data'))
        exigir(datetime.date.fromisoformat(data).isoformat() == data, 'data jurídica inválida; use AAAA-MM-DD')
        docs = p.get('documentos')
        exigir(isinstance(docs, dict) and bool(docs) and set(docs) <= TEMPLATES.keys(),
               'documentos inválidos na revisao-juridica')
        registros = registros_aprovados()
        caminhos = templates_aprovados(registros)
        for doc, sha in docs.items():
            exigir(isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{64}', sha)
                   and registros[caminhos[doc]]['sha256'] == sha,
                   'APR-01: hash não aprovado para ' + doc)
        s.setdefault('revisoes_juridicas', []).append(dict(revisor=revisor, decisor=decisor, data=data,
            resultado='aprovado', **ciclo,
            documentos=copy.deepcopy(docs), evidencia=importar(root, p.get('evidencia'))))
    elif action == "gerar":
        exigir(s["revisao"] is not None, "revisão humana ausente")
        template_root = pathlib.Path(texto(p.get("templates")))
        browser = p.get("navegador", "google-chrome")
        prepared, situacoes = preparar_minutas(s, p)
        # Todas as pré-condições são conferidas antes de iniciar qualquer PDF.
        rascunhos = s.get('rascunhos_documentos')
        if rascunhos:
            for doc, (raw, md, n, juridica) in prepared.items():
                r = rascunhos[doc]
                exigir(ler_arquivo(root, r['template']) == raw and ler_arquivo(root, r['markdown']) == md.encode()
                       and r['versao'] == n, 'rascunho mudou; prepare e confira novamente os documentos')
            pdfs = {doc: ler_arquivo(root, rascunhos[doc]['pdf']) for doc in prepared}
        else:
            pdfs = {doc: pdf_bytes(md, browser) for doc, (raw, md, n, juridica) in prepared.items()}
        for doc, (raw, md, n, juridica) in prepared.items():
            for previous in s["documentos"].get(doc, []):
                previous["vigente"] = False
            s["documentos"].setdefault(doc, []).append(dict(versao=n, vigente=True,
                template=guardar(root, raw, ".md"), markdown=guardar(root, md.encode(), ".md"),
                pdf=guardar(root, pdfs[doc], ".pdf"), revisao=copy.deepcopy(s["revisao"]),
                revisao_juridica=copy.deepcopy(juridica),
                situacao_juridica={k:v for k,v in situacoes[doc].items() if k!="minuta"},
                minuta=situacoes[doc]["minuta"],
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


def executar(root, action, payload, aprovacao=None):
    root = local_externo(root)
    exigir((root / "expediente.json").is_file(), "expediente ausente; inicialize fora da sessão do agente")
    exigir(not (root / "expediente.json").is_symlink() and not (root / ".lock").is_symlink(), "symlink recusado")
    with (root / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        original = json.loads((root / "expediente.json").read_text(encoding="utf-8"))
        REGRA_PESSOA.set(original.get("pessoa_nomeada"))
        pessoa(original["responsavel"])
        s = copy.deepcopy(original)
        try:
            if isinstance(payload, pathlib.Path):
                payload = json.loads(payload.read_text(encoding="utf-8"))
            exigir(isinstance(payload, dict), "entrada deve ser objeto JSON")
            integridade(root, s)
            if aprovacao is not None:
                evento(s, "AprovacaoChatRegistrada", testemunho=copy.deepcopy(aprovacao))
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
    parser.add_argument("operacao", help="iniciar, estado, tratamento, receber, pendencia, resolver, reabrir, consolidar, revisar, revisao-juridica, gerar, liberar, assinatura, ocorrencia, concluir-0b, acessos, preparar-0d, nao-prosseguir")
    parser.add_argument("--expediente", required=True, type=pathlib.Path)
    parser.add_argument("--aprovacao", type=pathlib.Path, help="testemunho da aprovação no chat")
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
