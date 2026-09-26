"""Calcula um nível pelas faixas e eixos declarados no playbook do caso."""
import re


def _intervalo(obj):
    return (isinstance(obj, dict)
            and type(obj.get("minimo")) is int
            and type(obj.get("maximo")) is int
            and obj["minimo"] <= obj["maximo"])


def calcular(pb, texto):
    regra = pb.get("apuracao_nivel")
    if not isinstance(regra, dict):
        return None, None, "regra de apuracao_nivel ausente ou invalida"
    eixos = regra.get("eixos")
    if (not isinstance(eixos, dict) or not eixos
            or any(not isinstance(e, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", e)
                   or not _intervalo(faixa) for e, faixa in eixos.items())):
        return None, None, "eixos declarados invalidos"
    if regra.get("agregacao") != "maximo":
        return None, None, "agregacao nao suportada"
    faixas = regra.get("faixas")
    if (not isinstance(faixas, list) or not faixas
            or any(not _intervalo(f) or f.get("nivel") not in pb["niveis"] for f in faixas)):
        return None, None, "faixas de nivel invalidas"
    faixas = sorted(faixas, key=lambda f: f["minimo"])
    inicio = max(f["minimo"] for f in eixos.values())
    fim = max(f["maximo"] for f in eixos.values())
    seguinte = inicio
    for faixa in faixas:
        if faixa["minimo"] != seguinte:
            return None, None, "faixas sobrepostas ou incompletas"
        seguinte = faixa["maximo"] + 1
    if seguinte != fim + 1:
        return None, None, "faixas sobrepostas ou incompletas"

    if not texto.strip():
        return None, None, "eixos obrigatorios"
    valores = {}
    for item in texto.split(","):
        par = re.fullmatch(r"\s*([A-Za-z][A-Za-z0-9_-]*)\s+(-?\d+)\s*", item)
        if not par:
            return None, None, "formato dos eixos invalido: use SIGLA inteiro, separados por virgula"
        eixo, valor = par.group(1), int(par.group(2))
        if eixo not in eixos:
            return None, None, f"eixo desconhecido: {eixo}"
        if eixo in valores:
            return None, None, f"eixo duplicado: {eixo}"
        faixa = eixos[eixo]
        if not faixa["minimo"] <= valor <= faixa["maximo"]:
            return None, None, (f"{eixo} {valor} fora da faixa "
                                f"{faixa['minimo']} a {faixa['maximo']}")
        valores[eixo] = valor
    ausentes = [e for e in eixos if e not in valores]
    if ausentes:
        return None, None, "eixos ausentes: " + ", ".join(ausentes)
    maior = max(eixos, key=lambda e: valores[e])
    soma = valores[maior]
    nivel = next(f["nivel"] for f in faixas if f["minimo"] <= soma <= f["maximo"])
    return nivel, f"maior eixo {maior} {soma} -> {nivel}", None
