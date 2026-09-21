"""Plano de medicao (P9). Unico caminho de escrita em registro/metricas/.

Uso:
  python3 metrica.py --arquivo registro/metricas/MET-001.yaml --ator "Nome"

A metrica e artefato de medicao produzido em P9 -- nao e objeto CTX e nao
e semantica de maquina de etapas. Este script vive em eiac-campo porque
sabe o que e linha de base, metrica de resultado e metrica de uso
(EMCIA-CAM-01 Anexo C, inegociavel 4); reaproveita as primitivas
genericas do eiac-nucleo sem alterar nenhuma delas.

piloto_ref resolve contra registro/piloto/ (P8 revisado) -- P9 nao mede
sobre um piloto que nao existe ou ainda nao foi revisado (relacao P8 ->
P9, secao 35 do pacote). A linha de base precisa ser anterior ao
resultado apurado: nao se inventa baseline depois do piloto so para
produzir comparacao (secao 18).
"""
import argparse
import pathlib
import sys

import os
RAIZ_NUCLEO = pathlib.Path(os.environ["EIAC_NUCLEO_SCRIPTS"]) if os.environ.get("EIAC_NUCLEO_SCRIPTS") else pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estado as E  # noqa: E402
import estrutura as X  # noqa: E402
import json  # noqa: E402


DIRETORIO_PILOTO = pathlib.Path("registro/piloto")
DIRETORIO_BASELINE = pathlib.Path("registro/baseline")


def _ator_pessoa_nomeada(nome):
    nome = (nome or "").strip()
    if not nome or E.autor_e_agente(nome):
        return False
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
    return nome.lower() not in genericos


def checar_autoria(dados):
    erros = []
    for campo in ("declarado_por", "registrado_por", "responsavel_apuracao"):
        valor = dados.get(campo)
        if valor is not None and E.autor_e_agente(valor):
            erros.append(f"{campo} nao pode ser agente: '{valor}'")
    return erros


def checar_piloto_ref(candidato):
    """P9 depende de P8 encerrado (CAM-01 3.5: 'P8 encerrado; piloto
    executado'). Referencia a conjunto ainda em rascunho nao basta.
    """
    ref = candidato.get("piloto_ref")
    if not ref:
        return []
    alvo = DIRETORIO_PILOTO / f"{ref}.yaml"
    if not alvo.exists():
        return [f"piloto_ref '{ref}' nao resolve — {alvo} nao existe"]
    try:
        conjunto = X.carregar_yaml(alvo.read_text(encoding="utf-8"))
    except (X.ErroYaml, ValueError) as erro:
        return [f"piloto_ref '{ref}' esta ilegivel: {erro}"]
    if conjunto.get("estado") != "revisado":
        return [f"piloto_ref '{ref}' aponta para conjunto em estado "
                f"'{conjunto.get('estado')}', nao 'revisado' -- P9 nao mede "
                f"sobre piloto ainda nao revisado"]
    return []


def checar_baseline(candidato):
    """Baseline nao pode ter sido inventada apos o piloto: sua data
    precisa ser anterior (ou igual) a data em que o resultado foi apurado.
    """
    erros = []
    if candidato.get("tipo") not in ("resultado", "uso", "qualidade"):
        return erros  # ja coberto por enums do schema
    base_data = candidato.get("linha_base_data")
    resultado_data = candidato.get("resultado_apurado_data")
    if base_data and resultado_data and str(base_data) > str(resultado_data):
        erros.append("linha_base_data e posterior a resultado_apurado_data -- "
                     "a linha de base nao pode ter sido criada depois do "
                     "resultado que ela deveria comparar")
    return erros


def checar_baseline_ref(candidato):
    """Quando declarado, baseline_ref precisa resolver contra o mesmo
    artefato de linha de base usado pelo inegociavel 1 (P3a) -- P9 nao
    inventa uma segunda linha de base propria (2.6.5 secao 11 do pacote,
    item 11 da diretriz do usuario). linha_base/linha_base_data continuam
    sendo os campos que este objeto declara (Anexo C); quando baseline_ref
    existe, eles precisam corresponder ao artefato referenciado -- nao
    sao dois valores independentes que por acaso concordam.
    """
    ref = candidato.get("baseline_ref")
    if not ref:
        return []
    alvo = DIRETORIO_BASELINE / f"{ref}.yaml"
    if not alvo.exists():
        return [f"baseline_ref '{ref}' nao resolve — {alvo} nao existe"]
    try:
        base = X.carregar_yaml(alvo.read_text(encoding="utf-8"))
    except (X.ErroYaml, ValueError) as erro:
        return [f"baseline_ref '{ref}' esta ilegivel: {erro}"]
    erros = []
    if str(candidato.get("linha_base") or "") != str(base.get("valor_atual") or ""):
        erros.append(f"baseline_ref '{ref}': 'linha_base' ('{candidato.get('linha_base')}') "
                     f"nao corresponde a 'valor_atual' do artefato referenciado "
                     f"('{base.get('valor_atual')}')")
    if str(candidato.get("linha_base_data") or "") != str(base.get("data") or ""):
        erros.append(f"baseline_ref '{ref}': 'linha_base_data' nao corresponde "
                     f"a 'data' do artefato referenciado")
    return erros


def checar_apuracao(candidato):
    """Estado 'apurada' exige resultado, data, procedencia do resultado e
    declaracao explicita de fatores externos que possam ter influenciado
    o periodo -- para nao transformar 'houve reducao' em causalidade nao
    sustentada (CAT-01 3.4.5: 'atribuicao de causa nao esta nos dados').
    """
    if candidato.get("estado") != "apurada":
        return []
    erros = []
    for campo in ("resultado_apurado", "resultado_apurado_data",
                  "resultado_apurado_procedencia"):
        if not str(candidato.get(campo) or "").strip():
            erros.append(f"estado 'apurada' exige '{campo}' preenchido")
    if not str(candidato.get("fatores_externos_declarados") or "").strip():
        erros.append("estado 'apurada' exige 'fatores_externos_declarados' "
                     "preenchido (mesmo que seja 'nenhum identificado') -- "
                     "separar efeito da solucao de fator externo e "
                     "julgamento que precisa ficar registrado, nao implicito")
    return erros


def gravar_metrica(destino, ator, schema_caminho="registro/metricas.schema.json"):
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, "metrica")
    erros += checar_autoria(candidato)
    erros += checar_piloto_ref(candidato)
    erros += checar_baseline(candidato)
    erros += checar_baseline_ref(candidato)
    erros += checar_apuracao(candidato)

    if erros:
        E.evento("MetricaRecusada", arquivo=str(destino), erros=erros,
                 ator=ator, estado_tentado=candidato.get("estado"))
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    evento_tipo = "MetricaApurada" if candidato.get("estado") == "apurada" \
        else "MetricaRegistrada"
    E.evento(evento_tipo, arquivo=str(destino), id=candidato.get("id"),
             estado=candidato.get("estado"), tipo_metrica=candidato.get("tipo"),
             versao=candidato.get("versao"), ator=ator)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True,
                     help="destino em registro/metricas/<id>.yaml")
    ap.add_argument("--ator", required=True)
    ap.add_argument("--schema", default="registro/metricas.schema.json")
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("registro/metricas/"):
        print("metrica so grava dentro de registro/metricas/", file=sys.stderr)
        sys.exit(1)

    erro = gravar_metrica(destino, a.ator, schema_caminho=a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"metrica gravada: {a.arquivo}")


if __name__ == "__main__":
    main()
