"""Materializacao dos cinco entregaveis (E1-E5), 2.6.5. So renderiza a
partir de artefatos reais do caso -- nunca inventa conteudo ausente.

Uso:
  python3 entregaveis.py --renderizar E1 --autor "Nome"
  python3 entregaveis.py --renderizar E1 --autor "Nome" --emitir

--renderizar escreve caso/entregaveis/<ID>.md a partir dos artefatos
reais ja gravados em registro/ e devolve erro se um campo obrigatorio
do modelo oficial (EMCIA-E1..E5) nao tiver evidencia rastreavel no caso
-- bloqueado explicitamente, nunca preenchido com texto generico.
--emitir, apos renderizar com sucesso, chama avancar.py --emitir
--materializar apontando para o arquivo real (a unica forma de o evento
EntregavelEmitido apontar para um documento que existe -- D-12).

Este script vive em eiac-campo porque sabe o que E1-E5 significam e onde
seu conteudo mora no caso (registro/baseline, registro/governanca,
registro/piloto, registro/metricas, registro/calibragem, estado.json).
O nucleo (avancar.emitir) nao sabe nada disso -- so confere que o
arquivo indicado existe e nao esta vazio.
"""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys

import os
RAIZ_NUCLEO = pathlib.Path(os.environ["EIAC_NUCLEO_SCRIPTS"]) if os.environ.get("EIAC_NUCLEO_SCRIPTS") else pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estrutura as X  # noqa: E402

DIR_ENTREGAVEIS = pathlib.Path("caso/entregaveis")
DIR_ESTADO = pathlib.Path("registro/estado.json")


class NaoMaterializavel(Exception):
    """Campo obrigatorio do modelo oficial sem evidencia rastreavel no caso."""


def _estado():
    return json.loads(DIR_ESTADO.read_text(encoding="utf-8"))


def _cumprimento(st, etapa_id):
    return st.get("cumprimentos", {}).get(etapa_id, {}) or {}


def _yaml(caminho):
    p = pathlib.Path(caminho)
    if not p.exists():
        return None
    return X.carregar_yaml(p.read_text(encoding="utf-8"))


def _listar(diretorio):
    d = pathlib.Path(diretorio)
    if not d.exists():
        return []
    return sorted(d.glob("*.yaml"))


def _exige(valor, mensagem):
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        raise NaoMaterializavel(mensagem)
    return valor


def _cabecalho(titulo, subtitulo, st):
    caso = st.get("caso", "?")
    nivel = st.get("nivel") or "nao apurado"
    return (
        f"# {titulo}\n"
        f"### {subtitulo}\n\n"
        f"| Metadado | Valor |\n"
        f"| :--- | :--- |\n"
        f"| **Engajamento** | {caso} |\n"
        f"| **Nível apurado** | {nivel} |\n"
        f"| **Gerado em** | {datetime.date.today().isoformat()} |\n\n"
        f"---\n\n"
    )


def render_e1(st):
    """EMCIA-E1: Ficha de enquadramento. Fonte: cumprimento de F0."""
    f0 = _cumprimento(st, "F0")
    _exige(f0.get("cumprido"), "F0 nao encerrada -- E1 nao tem insumo")
    eixos = f0.get("eixos")
    _exige(eixos, "F0 sem eixos DAD/GOV/CRI registrados (avancar.py --apurar-nivel) -- "
                  "nivel de complexidade sem a conta visivel nao satisfaz o modelo E1")
    nivel = _exige(st.get("nivel"), "nivel nao apurado")

    md = _cabecalho("Ficha de enquadramento",
                     "Delimitação da dor, custo estimado e nível de complexidade declarado", st)
    md += "## 4. Nível de complexidade declarado\n\n"
    md += f"| Eixo | Valor |\n| :--- | :---: |\n"
    md += f"| **Eixos (DAD · GOV · CRI)** | {eixos} |\n"
    md += f"| **Nível apurado** | {nivel} |\n\n"
    md += "## 6. Trilha recomendada e decisão solicitada\n\n"
    md += (f"| Decisão | Responsável | Data |\n| :--- | :--- | :---: |\n"
           f"| F0 encerrada | {f0.get('autor', '?')} | — |\n")
    return md


def render_e2(st):
    """EMCIA-E2: Diagnóstico e oportunidade. Fonte: registro/baseline/ (I1)."""
    baselines = _listar("registro/baseline")
    _exige(baselines or None,
           "nenhuma linha de base em registro/baseline/ -- E2 A.3 exige a "
           "tabela de linha de base, item inegociavel 1")

    md = _cabecalho("Diagnóstico e oportunidade",
                     "Como o processo funciona de fato, quanto custa hoje e onde está a oportunidade", st)
    md += "## Parte A — Sumário executivo\n\n### A.3 Linha de base\n\n"
    md += "| Marca | Indicador | Valor atual | Como foi obtido | Data |\n"
    md += "| :---: | :--- | :--- | :--- | :---: |\n"
    for caminho in baselines:
        b = _yaml(caminho)
        marca = b.get("procedencia", "?")
        md += (f"| **[{marca}]** | {b.get('indicador','?')} | {b.get('valor_atual','?')} "
               f"| {b.get('apuracao','?')} | {b.get('data','?')} |\n")
    md += "\n*A linha de base é registrada antes de qualquer piloto e é contra ela que o resultado será medido na fase F4.*\n"
    return md


def render_e3(st):
    """EMCIA-E3: Blueprint da solução. Fonte: cumprimento de P5
    (classificacao_tecnologica) para a Parte A. Parte B (E3-E) so entra
    quando a classificacao contem 'agente' -- E3-D e sempre emitido,
    E3-E e condicionado (secao 33 do pacote 2.6.5).
    """
    p5 = _cumprimento(st, "P5")
    _exige(p5.get("cumprido"), "P5 nao encerrada -- E3 nao tem insumo")
    classificacao = _exige(p5.get("classificacao_tecnologica"),
                            "P5 sem 'classificacao_tecnologica' registrada")

    md = _cabecalho("Blueprint da solução",
                     "Decisão sobre os casos e, quando couber, especificação do agente", st)
    md += "## Parte A — Decisão\n\n### A2. Classificação tecnológica\n\n"
    md += "| Caso | Classificação |\n| :--- | :--- |\n"
    md += f"| {st.get('caso','?')} | {classificacao} |\n\n"
    if "agente" in str(classificacao):
        md += ("## Parte B — Blueprint do agente\n\n"
               "*Especificação do agente (E3-E) aplicável -- P5 classificou "
               "este caso como agente.*\n")
    else:
        md += ("*Classificação não indica solução agêntica -- Parte B (E3-E) "
               "não se aplica a este caso (E3-blueprint-da-solucao.md: "
               "\"a Parte B só se abre depois do portão\").*\n")
    return md


def render_e4(st):
    """EMCIA-E4: Guia operacional. Fonte: registro/operacional/ (P6) +
    registro/governanca/autonomia/ (P7, inegociavel 2).
    """
    operacionais = [o for o in _listar("registro/operacional")
                    if (_yaml(o) or {}).get("estado") == "validado"]
    _exige(operacionais or None,
           "nenhuma especificacao operacional validada em registro/operacional/")
    termos = [t for t in _listar("registro/governanca/autonomia")
              if (_yaml(t) or {}).get("estado") == "decidido"]
    _exige(termos or None,
           "nenhum termo de autonomia decidido em registro/governanca/autonomia/ "
           "-- item inegociavel 2 bloqueia E4")

    op = _yaml(operacionais[-1])
    termo = _yaml(termos[-1])

    md = _cabecalho("Guia operacional",
                     "Como a equipe trabalha com a solução, e o que fazer quando ela erra", st)
    md += "## 1. O que muda no processo\n\n"
    md += f"| Campo | Valor |\n| :--- | :--- |\n"
    md += f"| **Ponto de inserção** | {op.get('ponto_insercao','?')} |\n"
    md += f"| **Momento** | {op.get('momento','?')} |\n"
    md += f"| **Sistema** | {op.get('sistema','?')} |\n\n"
    md += "## 3. Quando a solução erra\n\n"
    md += f"| Situação | Fallback | Ator humano |\n| :--- | :--- | :--- |\n"
    md += f"| {op.get('excecao','?')} | {op.get('fallback','?')} | {op.get('ator_humano','?')} |\n\n"
    md += "## Termo de autonomia\n\n"
    md += (f"| Decisor | Data da decisão | Justificativa |\n"
           f"| :--- | :---: | :--- |\n"
           f"| {termo.get('decisor','?')} | {termo.get('data_decisao','?')} "
           f"| {termo.get('justificativa_decisao','?')} |\n")
    return md


def render_e5(st):
    """EMCIA-E5: Relatório de piloto. Fonte: registro/piloto/ (I3),
    registro/metricas/ (I4, com linha de base), registro/calibragem/
    (I5, rotina).
    """
    pilotos = [p for p in _listar("registro/piloto")
               if (_yaml(p) or {}).get("estado") == "revisado"]
    _exige(pilotos or None,
           "nenhum conjunto de piloto revisado em registro/piloto/ -- "
           "item inegociavel 3 bloqueia E5")
    metricas_resultado = [
        m for m in _listar("registro/metricas")
        if (_yaml(m) or {}).get("tipo") == "resultado"
        and (_yaml(m) or {}).get("estado") == "apurada"
    ]
    _exige(metricas_resultado or None,
           "nenhuma metrica de resultado apurada em registro/metricas/ -- "
           "item inegociavel 4 bloqueia E5")
    rotinas = _listar("registro/calibragem")
    rotinas = [r for r in rotinas if "-C" not in r.stem]  # exclui ciclos, so a rotina
    _exige(rotinas or None,
           "nenhuma rotina de calibragem em registro/calibragem/ -- "
           "item inegociavel 5 bloqueia E5")

    piloto = _yaml(pilotos[-1])
    rotina = _yaml(rotinas[-1])

    md = _cabecalho("Relatório de piloto",
                     "O que foi testado, o que resultou contra a linha de base e quem mantém daqui em diante", st)
    md += "## 1. O que foi testado\n\n"
    md += (f"| Parâmetro | Detalhe |\n| :--- | :--- |\n"
           f"| **Modo** | {piloto.get('modo','?')} |\n"
           f"| **Duração** | {piloto.get('duracao','?')} |\n"
           f"| **Critério de aprovação** | {piloto.get('criterio_aprovacao_escala','?')} "
           f"(definido em {piloto.get('criterio_aprovacao_escala_definido_em','?')}) |\n\n")
    md += "## 2. Resultado contra a linha de base\n\n"
    md += "| Indicador | Linha de base | No piloto | Marca |\n| :--- | :--- | :--- | :---: |\n"
    for caminho in metricas_resultado:
        m = _yaml(caminho)
        md += (f"| {m.get('metrica','?')} | {m.get('linha_base','?')} "
               f"| {m.get('resultado_apurado','?')} | [{m.get('resultado_apurado_procedencia','?')}] |\n")
    md += "\n## 6. Plano de medição e calibragem\n\n"
    md += (f"| Atributo | Definição |\n| :--- | :--- |\n"
           f"| **Responsável pela calibragem** | {rotina.get('responsavel','?')} |\n"
           f"| **Cadência de revisão** | {rotina.get('cadencia','?')} |\n"
           f"| **Primeira revisão** | {rotina.get('data_primeira_revisao','?')} |\n")
    return md


RENDERIZADORES = {"E1": render_e1, "E2": render_e2, "E3": render_e3,
                   "E4": render_e4, "E5": render_e5}
# E3 e um unico entregavel ao cliente construido por DUAS autorizacoes
# internas de portao (secao 3 do pacote 2.6.5): E3-D (decisao, sempre
# avaliado) e E3-E (especificacao, condicional -- so quando P5 classifica
# como agente). Emitir E3 exige E3-D autorizado sempre, e E3-E autorizado
# OU nao aplicavel (nunca negado quando aplicavel).
ENTREGAVEL_PORTOES = {"E1": ["E1"], "E2": ["E2"], "E3": ["E3-D", "E3-E"],
                       "E4": ["E4"], "E5": ["E5"]}


def renderizar(entregavel_id):
    st = _estado()
    fn = RENDERIZADORES[entregavel_id]
    conteudo = fn(st)
    DIR_ENTREGAVEIS.mkdir(parents=True, exist_ok=True)
    destino = DIR_ENTREGAVEIS / f"{entregavel_id}.md"
    destino.write_text(conteudo, encoding="utf-8")
    return destino


def _emitir_portao(portao_id, autor, destino):
    r = subprocess.run(
        [sys.executable, str(RAIZ_NUCLEO / "avancar.py"),
         "--emitir", portao_id, "--autor", autor,
         "--materializar", str(destino)],
        capture_output=True, text=True,
    )
    return r.returncode, r.stdout, r.stderr


def emitir(entregavel_id, autor, destino):
    """Avalia cada portao interno do entregavel. E3-D precisa ser
    AUTORIZADO; E3-E pode ser AUTORIZADO ou NAO_APLICAVEL -- nunca
    negado quando o caso e agentico e o requisito nao esta completo (ai
    e negado de fato, e retorna erro). O primeiro portao que devolve
    codigo != 0 e sem ser NAO_APLICAVEL interrompe e retorna o erro.
    """
    resultados = []
    for portao_id in ENTREGAVEL_PORTOES[entregavel_id]:
        codigo, saida, erro = _emitir_portao(portao_id, autor, destino)
        resultados.append((portao_id, codigo, saida, erro))
        if codigo != 0 and "NAO_APLICAVEL" not in saida:
            return codigo, saida, erro
    saida_consolidada = "\n".join(f"{p}: {s.strip()}" for p, _, s, _ in resultados)
    return 0, saida_consolidada, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--renderizar", required=True, choices=list(RENDERIZADORES))
    ap.add_argument("--autor", required=True)
    ap.add_argument("--emitir", action="store_true",
                     help="apos renderizar, chama avancar.py --emitir --materializar")
    a = ap.parse_args()

    try:
        destino = renderizar(a.renderizar)
    except NaoMaterializavel as erro:
        print(f"{a.renderizar} nao materializavel: {erro}", file=sys.stderr)
        sys.exit(1)

    print(f"{a.renderizar} renderizado: {destino}")

    if a.emitir:
        codigo, saida, erro = emitir(a.renderizar, a.autor, destino)
        if "NAO_APLICAVEL" in saida:
            print(saida.strip())
            sys.exit(0)
        if codigo != 0:
            print(erro.strip() or saida.strip(), file=sys.stderr)
            sys.exit(codigo)
        print(saida.strip())


if __name__ == "__main__":
    main()
