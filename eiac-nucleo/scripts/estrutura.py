"""Validador estrutural genérico orientado por schema declarado no caso.

O núcleo não conhece Termo, Entidade, Regra ou Fonte. Ele lê os tipos,
campos e restrições de ``registro/contexto.schema.json`` e valida um arquivo
YAML sem decidir mérito, curadoria ou referências entre objetos.
"""
import argparse
import ast
import datetime
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None


class ErroYaml(ValueError):
    """Erro de sintaxe no subconjunto YAML usado pelos modelos do Estúdio."""


def _sem_comentario(texto):
    aspas = None
    escape = False
    for indice, caractere in enumerate(texto):
        if escape:
            escape = False
            continue
        if caractere == "\\" and aspas == '"':
            escape = True
            continue
        if caractere in ("'", '"'):
            if aspas == caractere:
                aspas = None
            elif aspas is None:
                aspas = caractere
            continue
        if caractere == "#" and aspas is None:
            return texto[:indice].rstrip()
    return texto.rstrip()


def _itens_inline(texto):
    itens, atual, aspas = [], [], None
    for caractere in texto:
        if caractere in ("'", '"'):
            if aspas == caractere:
                aspas = None
            elif aspas is None:
                aspas = caractere
            atual.append(caractere)
        elif caractere == "," and aspas is None:
            itens.append("".join(atual).strip())
            atual = []
        else:
            atual.append(caractere)
    itens.append("".join(atual).strip())
    return itens


def _escalar(valor):
    valor = valor.strip()
    if valor in ("null", "Null", "NULL", "~"):
        return None
    if valor.lower() == "true":
        return True
    if valor.lower() == "false":
        return False
    if valor.startswith("[") and valor.endswith("]"):
        miolo = valor[1:-1].strip()
        return [] if not miolo else [_escalar(item) for item in _itens_inline(miolo)]
    if valor.startswith(("'", '"')) and valor.endswith(("'", '"')):
        try:
            return ast.literal_eval(valor)
        except (SyntaxError, ValueError):
            return valor[1:-1]
    if re.fullmatch(r"-?\d+", valor):
        return int(valor)
    return valor


def _tokens(texto):
    saida = []
    for numero, original in enumerate(texto.splitlines(), 1):
        if "\t" in original[:len(original) - len(original.lstrip())]:
            raise ErroYaml(f"linha {numero}: tabulacao nao permitida na indentacao")
        linha = _sem_comentario(original)
        if not linha.strip():
            continue
        indentacao = len(linha) - len(linha.lstrip(" "))
        saida.append((indentacao, linha.strip(), numero))
    return saida


def _separar_chave(conteudo, numero):
    if ":" not in conteudo:
        raise ErroYaml(f"linha {numero}: esperado campo no formato chave: valor")
    chave, valor = conteudo.split(":", 1)
    chave = chave.strip()
    if not chave:
        raise ErroYaml(f"linha {numero}: chave vazia")
    return chave, valor.strip()


def _mapa(tokens, indice, indentacao):
    resultado = {}
    while indice < len(tokens):
        nivel, conteudo, numero = tokens[indice]
        if nivel < indentacao:
            break
        if nivel > indentacao:
            raise ErroYaml(f"linha {numero}: indentacao inesperada")
        if conteudo.startswith("- ") or conteudo == "-":
            break
        chave, valor = _separar_chave(conteudo, numero)
        if chave in resultado:
            raise ErroYaml(f"linha {numero}: campo duplicado '{chave}'")
        indice += 1
        if valor:
            resultado[chave] = _escalar(valor)
        elif indice < len(tokens) and tokens[indice][0] > nivel:
            resultado[chave], indice = _bloco(tokens, indice, tokens[indice][0])
        else:
            resultado[chave] = None
    return resultado, indice


def _lista(tokens, indice, indentacao):
    resultado = []
    while indice < len(tokens):
        nivel, conteudo, numero = tokens[indice]
        if nivel < indentacao:
            break
        if nivel != indentacao or not (conteudo.startswith("- ") or conteudo == "-"):
            break
        item = conteudo[1:].strip()
        indice += 1
        if not item:
            if indice >= len(tokens) or tokens[indice][0] <= nivel:
                resultado.append(None)
            else:
                valor, indice = _bloco(tokens, indice, tokens[indice][0])
                resultado.append(valor)
            continue
        if ":" not in item:
            resultado.append(_escalar(item))
            continue

        chave, valor = _separar_chave(item, numero)
        mapa = {chave: _escalar(valor) if valor else None}
        if indice < len(tokens) and tokens[indice][0] > nivel:
            proximo_nivel = tokens[indice][0]
            if valor:
                complemento, indice = _mapa(tokens, indice, proximo_nivel)
                mapa.update(complemento)
            else:
                mapa[chave], indice = _bloco(tokens, indice, proximo_nivel)
        resultado.append(mapa)
    return resultado, indice


def _bloco(tokens, indice, indentacao):
    if tokens[indice][1].startswith("-"):
        return _lista(tokens, indice, indentacao)
    return _mapa(tokens, indice, indentacao)


def carregar_yaml(texto):
    """Carrega YAML com PyYAML ou com parser determinístico sem dependência."""
    if yaml:
        dados = yaml.safe_load(texto)
        return dados or {}
    tokens = _tokens(texto)
    if not tokens:
        return {}
    if tokens[0][0] != 0:
        raise ErroYaml("primeiro campo deve iniciar sem indentacao")
    dados, indice = _bloco(tokens, 0, 0)
    if indice != len(tokens):
        _, _, numero = tokens[indice]
        raise ErroYaml(f"linha {numero}: conteudo nao interpretado")
    return dados


def _caminho(dados, caminho):
    atual = dados
    for parte in caminho.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            return False, None
        atual = atual[parte]
    return True, atual


def _vazio(valor):
    return valor is None or valor == "" or valor == [] or valor == {}


TIPOS = {
    "string": str,
    "date": (str, datetime.date),
    "integer": int,
    "boolean": bool,
    "list": list,
    "object": dict,
}


def validar(dados, schema, tipo):
    objetos = schema.get("objetos", {})
    contrato = objetos.get(tipo)
    if not contrato:
        return [f"tipo desconhecido '{tipo}'. Esperado um de {sorted(objetos)}"]
    if not isinstance(dados, dict):
        return ["raiz do registro deve ser um objeto"]

    erros = []
    for caminho in contrato.get("required", []):
        existe, _ = _caminho(dados, caminho)
        if not existe:
            erros.append(f"campo obrigatorio ausente: {caminho}")

    for caminho in contrato.get("nonempty", []):
        existe, valor = _caminho(dados, caminho)
        if existe and _vazio(valor):
            erros.append(f"campo obrigatorio vazio: {caminho}")

    for caminho, nome_tipo in contrato.get("types", {}).items():
        existe, valor = _caminho(dados, caminho)
        esperado = TIPOS.get(nome_tipo)
        if existe and valor is not None and esperado and not isinstance(valor, esperado):
            erros.append(f"tipo invalido em {caminho}: esperado {nome_tipo}")

    for caminho, valores_permitidos in contrato.get("enums", {}).items():
        existe, valor = _caminho(dados, caminho)
        if existe and not _vazio(valor) and valor not in valores_permitidos:
            erros.append(
                f"valor invalido em {caminho}: esperado um de {valores_permitidos}"
            )

    for caminho, padrao_campo in contrato.get("patterns", {}).items():
        existe, valor = _caminho(dados, caminho)
        if not existe or _vazio(valor):
            continue
        texto = valor.isoformat() if isinstance(valor, datetime.date) else str(valor)
        if not re.fullmatch(padrao_campo, texto):
            erros.append(f"formato invalido em {caminho}: esperado {padrao_campo}")

    existe_id, identificador = _caminho(dados, "id")
    padrao = contrato.get("id_pattern")
    if existe_id and padrao and (
        not isinstance(identificador, str) or not re.fullmatch(padrao, identificador)
    ):
        erros.append(f"id invalido para {tipo}: esperado padrao {padrao}")

    existe_proc, procedencia = _caminho(dados, "procedencia")
    valores = schema.get("procedencia", [])
    if existe_proc and procedencia not in valores:
        erros.append(f"procedencia invalida: esperado um de {valores}")

    condicionais = contrato.get("conditional_nonempty", {})
    for caminho in condicionais.get(str(procedencia), []):
        existe, valor = _caminho(dados, caminho)
        if not existe or _vazio(valor):
            erros.append(f"procedencia {procedencia} exige campo preenchido: {caminho}")
    return erros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", default="registro/contexto.schema.json")
    ap.add_argument("--tipo", required=True)
    ap.add_argument("--arquivo", required=True)
    args = ap.parse_args()

    try:
        schema = json.loads(pathlib.Path(args.schema).read_text(encoding="utf-8"))
        dados = carregar_yaml(pathlib.Path(args.arquivo).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ErroYaml, ValueError) as erro:
        print(f"estrutura invalida: {erro}", file=sys.stderr)
        sys.exit(1)

    erros = validar(dados, schema, args.tipo)
    if erros:
        for erro in erros:
            print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"{args.tipo} valido: {args.arquivo}")


if __name__ == "__main__":
    main()
