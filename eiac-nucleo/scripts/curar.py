"""Curadoria dos objetos CTX. Unico caminho de escrita em contexto/.

Uso:  python3 curar.py --tipo regra --arquivo contexto/regras/RN-001.yaml

O ato de curadoria (quem executou este comando, gravado como
`registrado_por` no evento) nao vem de --registrado-por: e sempre
`responsavel` de registro/estado.json, fixado pelo operador em
novo-caso.sh, fora da sessao do agente. Isso e distinto de
`autoria_conteudo`/`declarado_por` DENTRO do objeto YAML curado, que
continuam vindo do candidato e sao checados por checar_autoria() —
representam quem declarou o fato, nao quem executa este comando.

Le o candidato de rascunho/<mesmo-nome>, valida a estrutura pelo schema do
caso (estrutura.py), confere autoria e procedencia, e so grava em
contexto/<tipo>s/ se tudo passar. Quando ja existe uma versao anterior do
mesmo id, a gravacao so ocorre como nova versao com historico preservado
(CTX-01 3.11-3.13) — nunca como sobrescrita do registro anterior.

O nucleo nao decide merito de conteudo; decide apenas se a mudanca de
procedencia e a trilha de versao estao presentes, conforme o schema
declarado pelo caso.
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import estrutura as X
import json


def _campo(dados, nome):
    return dados.get(nome)


CAMPOS_AUTORIA = ("autoria_conteudo", "declarado_por", "registrado_por", "autor")


def checar_autoria(dados):
    """CTX-V09: autoria de conteudo e quem registra sao pessoa nomeada.

    Nem todo objeto declara os mesmos campos de autoria (Fonte nao tem
    autoria_conteudo; um registro de confronto P3d usa so `autor`). Confere
    qualquer um desses campos que o objeto de fato declarar.
    """
    erros = []
    for campo in CAMPOS_AUTORIA:
        valor = dados.get(campo)
        if valor is None:
            continue
        if E.autor_e_agente(valor):
            erros.append(f"CTX-V09: {campo} nao pode ser agente: '{valor}'")
    return erros


def checar_versao(anterior, candidato, tipo):
    """CTX-V04/V10: mudanca de procedencia so entra como versao nova,
    com historico que preserva a versao anterior recuperavel.

    ``anterior`` e o dict ja gravado em contexto/ (ou None se e registro
    novo). ``candidato`` e o dict lido do rascunho. Objetos que nao
    declaram `versao` (como o registro de confronto P3d, que e observacional
    e nao iterativo) nao entram nesta checagem — o campo e a marca de que
    o objeto participa do regime de versionamento do CTX-01 3.11-3.13.
    """
    if "versao" not in candidato:
        return []

    if anterior is None:
        versao = candidato.get("versao")
        if versao not in (1, "1"):
            return [f"registro novo deve nascer na versao 1, recebido {versao!r}"]
        return []

    erros = []
    proc_antes = anterior.get("procedencia")
    proc_depois = candidato.get("procedencia")
    confronto_antes = anterior.get("classificacao_confronto")
    confronto_depois = candidato.get("classificacao_confronto")
    versao_antes = anterior.get("versao")
    versao_depois = candidato.get("versao")

    mudou_procedencia = proc_antes != proc_depois
    mudou_confronto = confronto_antes != confronto_depois
    mudanca_relevante = mudou_procedencia or mudou_confronto
    historico = candidato.get("historico") or []

    if mudanca_relevante:
        motivo = (
            f"procedencia {proc_antes} -> {proc_depois}" if mudou_procedencia
            else "classificacao_confronto"
        )
        # CTX-V04 nomeia literalmente a transicao I->V; a mesma exigencia de
        # versao crescente para outras mudancas relevantes (classificacao de
        # confronto) segue o principio geral do CTX-01 3.12, sem codigo proprio.
        codigo = "CTX-V04" if (proc_antes == "I" and proc_depois == "V") else "CTX-01 3.12"
        try:
            cresceu = int(versao_depois) > int(versao_antes)
        except (TypeError, ValueError):
            cresceu = False
        if not cresceu:
            erros.append(
                f"{codigo}: mudanca de {motivo} exige nova versao "
                f"(recebido versao {versao_antes!r} -> {versao_depois!r}); "
                f"sobrescrita nao e permitida"
            )
        if not isinstance(historico, list) or len(historico) < 1:
            erros.append(
                f"CTX-V10: mudanca de {motivo} exige historico com a versao anterior "
                "preservada (data, responsavel e motivo)"
            )
        else:
            ultima = historico[-1] if isinstance(historico[-1], dict) else {}
            faltando = [c for c in ("versao", "data") if not ultima.get(c)]
            responsavel = ultima.get("registrado_por") or ultima.get("confirmado_por")
            if not responsavel:
                faltando.append("registrado_por ou confirmado_por")
            if faltando:
                erros.append(
                    f"CTX-V10: entrada de historico incompleta para a versao anterior: "
                    f"faltando {faltando}"
                )
            try:
                if int(ultima.get("versao")) != int(versao_antes):
                    erros.append(
                        "CTX-V10: historico nao referencia a versao imediatamente anterior"
                    )
            except (TypeError, ValueError):
                erros.append("CTX-V10: historico sem numero de versao anterior valido")
    else:
        try:
            regressao = int(versao_depois) < int(versao_antes)
        except (TypeError, ValueError):
            regressao = False
        if regressao:
            erros.append(
                f"CTX-V04: versao nao pode retroceder: {versao_antes!r} -> {versao_depois!r}"
            )
    return erros


def checar_referencias(candidato, schema, tipo):
    """CTX-V05/V06/V07: toda referencia a Termo, Entidade ou Fonte listada
    num campo declarado em `references` precisa resolver para um objeto
    curado existente; quando o alvo e Fonte, o registro referenciado
    precisa ter o contrato minimo preenchido (mesma validacao que a
    propria Fonte passa ao ser curada — nao duplica a regra).

    O nucleo nao sabe o que e Termo, Entidade ou Fonte: le o prefixo do
    id (T-, E-, F-) e o `catalogo_referencias` do schema do caso para
    decidir onde procurar. Isso mantem a resolucao generica por schema,
    do mesmo jeito que `estrutura.validar()` ja e generica por tipo.
    """
    catalogo = schema.get("catalogo_referencias", {})
    campos_ref = (schema.get("objetos", {}).get(tipo, {}) or {}).get("references", {})
    codigo_por_tipo = {"termo": "CTX-V05", "entidade": "CTX-V06", "fonte": "CTX-V07"}

    erros = []
    for campo, prefixos_permitidos in campos_ref.items():
        valores = candidato.get(campo) or []
        if not isinstance(valores, list):
            continue
        for ref_id in valores:
            ref_id = str(ref_id)
            prefixo = ref_id.split("-", 1)[0] if "-" in ref_id else ref_id
            entrada = catalogo.get(prefixo)
            if not entrada or prefixo not in prefixos_permitidos:
                erros.append(
                    f"referencia '{ref_id}' em '{campo}' tem prefixo desconhecido "
                    f"ou nao permitido; esperado um de {prefixos_permitidos}"
                )
                continue
            codigo = codigo_por_tipo.get(entrada["tipo"], "CTX-V05/V06/V07")
            alvo = pathlib.Path(entrada["diretorio"]) / f"{ref_id}.yaml"
            if not alvo.exists():
                erros.append(
                    f"{codigo}: referencia '{ref_id}' em '{campo}' "
                    f"nao resolve — {alvo} nao existe"
                )
                continue
            if entrada["tipo"] == "fonte":
                try:
                    dados_fonte = X.carregar_yaml(alvo.read_text(encoding="utf-8"))
                except (X.ErroYaml, ValueError) as erro:
                    erros.append(f"{codigo}: fonte referenciada '{ref_id}' esta ilegivel: {erro}")
                    continue
                erros_fonte = X.validar(dados_fonte, schema, "fonte")
                if erros_fonte:
                    erros.append(
                        f"{codigo}: fonte referenciada '{ref_id}' nao possui contrato minimo valido: "
                        f"{erros_fonte}"
                    )
    return erros


CLASSE_EXIGE_REFERENCIA = ("divergente",)
DIRETORIO_DIVERGENCIAS = pathlib.Path("contexto/divergencias")


def checar_confronto(candidato):
    """CTX-V11: toda classificacao_confronto possui classe e referencia_p3d
    resolvivel quando a classe exige vinculo com P3d. So a classe
    `divergente` e verificada aqui — e a unica para a qual o CTX-01 3.5
    descreve o conteudo minimo exigido do registro referenciado.
    """
    confronto = candidato.get("classificacao_confronto")
    if not isinstance(confronto, dict):
        return []
    classe = confronto.get("classe")
    if classe not in CLASSE_EXIGE_REFERENCIA:
        return []

    referencia = confronto.get("referencia_p3d")
    if not referencia:
        return [f"CTX-V11: classe '{classe}' exige referencia_p3d preenchida"]

    alvo = DIRETORIO_DIVERGENCIAS / f"{referencia}.yaml"
    if not alvo.exists():
        return [f"CTX-V11: referencia_p3d '{referencia}' nao resolve para registro existente em {DIRETORIO_DIVERGENCIAS}/"]
    return []


def curar(tipo, destino, registrado_por, schema_caminho="registro/contexto.schema.json"):
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, tipo)
    erros += checar_autoria(candidato)
    erros += checar_confronto(candidato)
    erros += checar_referencias(candidato, schema, tipo)

    anterior = None
    if destino.exists():
        try:
            anterior = X.carregar_yaml(destino.read_text(encoding="utf-8"))
        except (X.ErroYaml, ValueError) as erro:
            return f"registro curado existente esta ilegivel: {erro}"
    erros += checar_versao(anterior, candidato, tipo)

    if erros:
        E.evento(
            "CuradoriaRecusada", tipo_objeto=tipo, arquivo=str(destino),
            erros=erros, registrado_por=registrado_por,
        )
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    E.evento(
        "ObjetoContextoCurado", tipo_objeto=tipo, arquivo=str(destino),
        id=candidato.get("id"), procedencia=candidato.get("procedencia"),
        versao=candidato.get("versao"), registrado_por=registrado_por,
        versao_anterior=(anterior or {}).get("versao"),
    )
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tipo", required=True)
    ap.add_argument("--arquivo", required=True,
                     help="destino em contexto/<tipo>s/<id>.yaml")
    ap.add_argument("--registrado-por", default=None,
                     help="ignorado para fins de autoria -- ver docstring do modulo")
    ap.add_argument("--schema", default="registro/contexto.schema.json",
                     help="schema declarativo que contem o tipo curado")
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("contexto/"):
        print("curadoria so grava dentro de contexto/", file=sys.stderr)
        sys.exit(1)

    estado = E.ler()
    responsavel = (estado or {}).get("responsavel")
    if not responsavel:
        print("caso sem responsavel definido em registro/estado.json "
              "(fixado por novo-caso.sh --responsavel). Nenhuma curadoria "
              "e aceita sem isso.", file=sys.stderr)
        E.evento("CuradoriaRecusada", tipo_objeto=a.tipo, arquivo=a.arquivo,
                 erros=["responsavel nao definido"], registrado_por_informado=a.registrado_por)
        sys.exit(1)

    erro = curar(a.tipo, destino, responsavel, schema_caminho=a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"{a.tipo} curado: {a.arquivo}")


if __name__ == "__main__":
    main()
