"""Conjunto de casos de teste do piloto (P8). Unico caminho de escrita em
registro/piloto/.

Uso:
  python3 piloto.py --arquivo registro/piloto/CT-001.yaml --ator "Nome"
  python3 piloto.py --arquivo registro/piloto/CT-001.yaml --ator "Nome" \
      --registrar-obtido CT-001-01 --obtido "texto da saida obtida"

O conjunto e artefato de piloto produzido em P8 -- nao e objeto CTX
(CTX-01 continua com Termo/Entidade/Regra/Fonte) e nao e semantica de
maquina de etapas. Este script vive em eiac-campo porque sabe o que um
caso de teste com saida esperada e (EMCIA-CAM-01 Anexo B, inegociavel 3);
reaproveita as primitivas genericas do eiac-nucleo (estrutura.validar
para o contrato do schema, estado.evento para a trilha,
estado.autor_e_agente para a convencao de autoria humana) sem alterar
nenhuma delas.

Cada caso dentro de 'casos' carrega, alem dos campos do Anexo B
(identificador, origem, entrada, saida_esperada, criterio_aprovacao,
categoria, revisor, data_revisao), tres campos que o Anexo B nao nomeia
mas que o pacote 2.6.3 exige para tornar a comparacao testavel:
saida_obtida, resultado (calculado, nunca declarado) e
esperado_definido_em/por (para provar que a saida esperada foi escrita
antes da execucao -- secao 13 do pacote). O nucleo nao valida a lista
'casos' item a item (estrutura.validar so percorre caminhos de topo);
este script faz essa checagem.
"""
import argparse
import datetime
import pathlib
import sys

RAIZ_NUCLEO = pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estado as E  # noqa: E402
import estrutura as X  # noqa: E402
import json  # noqa: E402


CAMPOS_CASO_ANEXO_B = (
    "identificador", "origem", "entrada", "saida_esperada",
    "criterio_aprovacao", "categoria", "revisor", "data_revisao",
)
CATEGORIAS_VALIDAS = ("comum", "excecao", "celula_critica")


def _ator_pessoa_nomeada(nome):
    nome = (nome or "").strip()
    if not nome or E.autor_e_agente(nome):
        return False
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir"}
    return nome.lower() not in genericos


def checar_autoria(dados):
    erros = []
    for campo in ("declarado_por", "registrado_por"):
        valor = dados.get(campo)
        if valor is not None and E.autor_e_agente(valor):
            erros.append(f"{campo} nao pode ser agente: '{valor}'")
    return erros


def checar_casos(candidato):
    """Cada caso do conjunto precisa ter saida esperada escrita e revisor
    humano (Anexo B); a saida esperada nao pode ter sido definida depois
    de 'saida_obtida' -- e o congelamento contra vies retrospectivo
    (secao 13 do pacote). O agente pode preparar (rascunho); so revisao
    humana leva o conjunto a 'revisado'.
    """
    casos = candidato.get("casos")
    if not isinstance(casos, list) or not casos:
        return ["conjunto precisa de ao menos um caso em 'casos'"]

    erros = []
    identificadores = set()
    tem_celula_critica = False
    for i, caso in enumerate(casos):
        if not isinstance(caso, dict):
            erros.append(f"caso #{i} nao e um objeto")
            continue
        faltando = [c for c in CAMPOS_CASO_ANEXO_B
                    if not str(caso.get(c) or "").strip()]
        if faltando:
            erros.append(f"caso #{i} ({caso.get('identificador', '?')}) "
                         f"sem campos obrigatorios: {faltando}")
            continue

        ident = caso["identificador"]
        if ident in identificadores:
            erros.append(f"identificador de caso duplicado no conjunto: '{ident}'")
        identificadores.add(ident)

        if caso.get("categoria") not in CATEGORIAS_VALIDAS:
            erros.append(f"caso {ident}: categoria '{caso.get('categoria')}' "
                         f"invalida, esperado um de {CATEGORIAS_VALIDAS}")
        if caso.get("categoria") == "celula_critica":
            tem_celula_critica = True

        if E.autor_e_agente(caso.get("revisor")):
            erros.append(f"caso {ident}: revisor nao pode ser agente")

        definido_em = caso.get("esperado_definido_em")
        if not str(definido_em or "").strip():
            erros.append(f"caso {ident}: 'esperado_definido_em' ausente -- "
                         f"a saida esperada precisa de data registrada antes "
                         f"da execucao para provar que nao foi escrita depois")
        if not str(caso.get("esperado_definido_por") or "").strip():
            erros.append(f"caso {ident}: 'esperado_definido_por' ausente")

        obtido = caso.get("saida_obtida")
        if obtido is not None and str(obtido).strip():
            data_obtido = caso.get("obtido_em")
            if data_obtido and definido_em and str(data_obtido) < str(definido_em):
                erros.append(f"caso {ident}: 'obtido_em' anterior a "
                             f"'esperado_definido_em' -- saida esperada nao pode "
                             f"ter sido escrita depois da execucao")
            resultado = caso.get("resultado")
            aderente = str(obtido).strip() == str(caso["saida_esperada"]).strip()
            esperado_resultado = "aderente" if aderente else "divergente"
            if resultado != esperado_resultado:
                erros.append(f"caso {ident}: 'resultado' declarado "
                             f"('{resultado}') nao corresponde a comparacao "
                             f"determinística esperado x obtido "
                             f"('{esperado_resultado}'). O resultado e "
                             f"calculado, nunca escrito por decisao manual.")

    if not tem_celula_critica:
        erros.append("conjunto nao cobre a celula critica (frequencia x "
                     "consequencia) -- Anexo B exige ao menos um caso "
                     "'celula_critica'; conjunto so com casos comuns nao "
                     "satisfaz o passo")
    return erros


def checar_revisao(candidato):
    if candidato.get("estado") != "revisado":
        return []
    if not str(candidato.get("revisado_por") or "").strip():
        return ["estado 'revisado' exige 'revisado_por' preenchido"]
    if E.autor_e_agente(candidato.get("revisado_por")):
        return ["'revisado_por' nao pode ser agente -- a revisao do conjunto "
                "e condicao de validade, nao etapa opcional (CAM-01 3.4)"]
    if not str(candidato.get("data_revisao") or "").strip():
        return ["estado 'revisado' exige 'data_revisao' preenchida"]
    return []


def gravar_conjunto(destino, ator, schema_caminho="registro/piloto.schema.json"):
    rascunho = pathlib.Path("rascunho") / destino.name
    if not rascunho.exists():
        return f"rascunho/{destino.name} nao existe. Escreva o candidato la primeiro."

    try:
        schema = json.loads(pathlib.Path(schema_caminho).read_text(encoding="utf-8"))
        candidato = X.carregar_yaml(rascunho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, X.ErroYaml, ValueError) as erro:
        return f"estrutura invalida: {erro}"

    erros = X.validar(candidato, schema, "conjunto_piloto")
    erros += checar_autoria(candidato)
    erros += checar_casos(candidato)
    erros += checar_revisao(candidato)

    if erros:
        E.evento("ConjuntoPilotoRecusado", arquivo=str(destino), erros=erros,
                 ator=ator, estado_tentado=candidato.get("estado"))
        return "\n".join(erros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(rascunho.read_text(encoding="utf-8"), encoding="utf-8")
    evento_tipo = "ConjuntoPilotoRevisado" if candidato.get("estado") == "revisado" \
        else "ConjuntoPilotoRegistrado"
    E.evento(evento_tipo, arquivo=str(destino), id=candidato.get("id"),
             estado=candidato.get("estado"), versao=candidato.get("versao"),
             ator=ator, n_casos=len(candidato.get("casos", [])))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", required=True,
                     help="destino em registro/piloto/<id>.yaml")
    ap.add_argument("--ator", required=True)
    ap.add_argument("--schema", default="registro/piloto.schema.json")
    a = ap.parse_args()

    destino = pathlib.Path(a.arquivo)
    if not str(destino).startswith("registro/piloto/"):
        print("conjunto de piloto so grava dentro de registro/piloto/", file=sys.stderr)
        sys.exit(1)

    erro = gravar_conjunto(destino, a.ator, schema_caminho=a.schema)
    if erro:
        print(erro, file=sys.stderr)
        sys.exit(1)
    print(f"conjunto de piloto gravado: {a.arquivo}")


if __name__ == "__main__":
    main()
