"""Curadoria dos objetos CTX. Unico caminho de escrita em contexto/.

Uso:  python3 curar.py --tipo regra --arquivo contexto/regras/RN-001.yaml \
          --registrado-por "Nome"

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


def checar_autoria(dados):
    """CTX-V09: autoria de conteudo e quem registra sao pessoa nomeada.

    O objeto Fonte nao tem autoria_conteudo no CTX-01 (so registrado_por);
    os demais tres tem os dois campos.
    """
    erros = []
    for campo in ("autoria_conteudo", "declarado_por", "registrado_por"):
        valor = dados.get(campo)
        if valor is None:
            continue
        if E.autor_e_agente(valor):
            erros.append(f"{campo} nao pode ser agente: '{valor}'")
    return erros


def checar_versao(anterior, candidato, tipo):
    """CTX-V04/V10: mudanca de procedencia so entra como versao nova,
    com historico que preserva a versao anterior recuperavel.

    ``anterior`` e o dict ja gravado em contexto/ (ou None se e registro
    novo). ``candidato`` e o dict lido do rascunho.
    """
    if anterior is None:
        versao = candidato.get("versao")
        if versao not in (1, "1"):
            return [f"registro novo deve nascer na versao 1, recebido {versao!r}"]
        return []

    erros = []
    proc_antes = anterior.get("procedencia")
    proc_depois = candidato.get("procedencia")
    versao_antes = anterior.get("versao")
    versao_depois = candidato.get("versao")

    mudou_procedencia = proc_antes != proc_depois
    historico = candidato.get("historico") or []

    if mudou_procedencia:
        try:
            cresceu = int(versao_depois) > int(versao_antes)
        except (TypeError, ValueError):
            cresceu = False
        if not cresceu:
            erros.append(
                f"mudanca de procedencia {proc_antes} -> {proc_depois} exige "
                f"nova versao (recebido versao {versao_antes!r} -> {versao_depois!r}); "
                f"sobrescrita nao e permitida"
            )
        if not isinstance(historico, list) or len(historico) < 1:
            erros.append(
                "mudanca de procedencia exige historico com a versao anterior "
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
                    f"entrada de historico incompleta para a versao anterior: "
                    f"faltando {faltando}"
                )
            try:
                if int(ultima.get("versao")) != int(versao_antes):
                    erros.append(
                        "historico nao referencia a versao imediatamente anterior"
                    )
            except (TypeError, ValueError):
                erros.append("historico sem numero de versao anterior valido")
    else:
        try:
            regressao = int(versao_depois) < int(versao_antes)
        except (TypeError, ValueError):
            regressao = False
        if regressao:
            erros.append(
                f"versao nao pode retroceder: {versao_antes!r} -> {versao_depois!r}"
            )
    return erros


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
    if E.autor_e_agente(registrado_por):
        erros.append(f"quem cura precisa ser pessoa nomeada, recebido '{registrado_por}'")

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
    ap.add_argument("--registrado-por", required=True)
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("contexto/"):
        print("curadoria so grava dentro de contexto/", file=sys.stderr)
        sys.exit(1)

    erro = curar(a.tipo, destino, a.registrado_por)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"{a.tipo} curado: {a.arquivo}")


if __name__ == "__main__":
    main()
