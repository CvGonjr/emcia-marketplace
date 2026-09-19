"""Verificacao semantica dos cinco inegociaveis (2.6.5). So le artefatos.

Uso:
  python3 inegociaveis.py --verificar 1 --arquivo registro/baseline/BL-001.yaml
  python3 inegociaveis.py --verificar 2 --arquivo registro/governanca/autonomia/AUT-001.yaml
  python3 inegociaveis.py --verificar 3 --arquivo registro/piloto/CT-001.yaml
  python3 inegociaveis.py --verificar 4 --arquivo registro/metricas/MET-001.yaml
  python3 inegociaveis.py --verificar 5 --arquivo registro/calibragem/CAL-001.yaml
  python3 inegociaveis.py --verificar 2 --arquivo ... --satisfazer --autor "Nome"

Cada verificador le UM artefato real do dominio correspondente e devolve
{id, satisfeito, evidencia_ref, verificador, motivo, timestamp} -- nunca
um booleano solto. O nucleo (avancar.satisfazer_inegociavel) nao sabe o
que "termo de autonomia" ou "metrica de resultado" significam; so grava
o registro estruturado {satisfeito, evidencia, autor, data} que ja
exigia desde o 2.6.1. Este script e quem decide SE deve chamar
avancar.py com satisfeito=true, e so chama depois de inspecionar o
artefato real -- nunca por edicao direta de estado.json (secao 18 do
pacote 2.6.5).

Cada funcao verificar_iN(caminho) e pura: le o arquivo, devolve o
resultado. --satisfazer e o unico modo que grava algo, e so grava
quando o verificador correspondente devolveu satisfeito=True.
"""
import argparse
import datetime
import pathlib
import subprocess
import sys

RAIZ_NUCLEO = pathlib.Path(__file__).resolve().parents[2] / "eiac-nucleo" / "scripts"
sys.path.insert(0, str(RAIZ_NUCLEO))
import estrutura as X  # noqa: E402


def _agora():
    return datetime.datetime.now().isoformat(timespec="seconds")


def _resultado(n, satisfeito, evidencia_ref, verificador, motivo):
    return {
        "id": f"I{n}", "satisfeito": satisfeito, "evidencia_ref": evidencia_ref,
        "verificador": verificador, "motivo": motivo, "timestamp": _agora(),
    }


def _carregar(caminho):
    p = pathlib.Path(caminho)
    if not p.exists():
        return None, f"{caminho} nao existe"
    try:
        return X.carregar_yaml(p.read_text(encoding="utf-8")), None
    except (X.ErroYaml, ValueError) as erro:
        return None, f"{caminho} esta ilegivel: {erro}"


def verificar_i1(caminho):
    """I1 -- linha de base (P3a). MET-01 3.4.3: registrada e datada antes
    do piloto, estimada em N1, calculada/medida em N2/N3. O verificador
    nao reabre a regra de apuracao por nivel (baseline.py ja recusa o
    registro se ela nao for respeitada) -- confere que o artefato existe,
    tem os campos minimos e que a data e anterior a qualquer piloto ja
    revisado no caso, quando houver um para comparar.
    """
    verificador = "inegociaveis.verificar_i1"
    dados, erro = _carregar(caminho)
    if erro:
        return _resultado(1, False, caminho, verificador, erro)
    faltando = [c for c in ("id", "indicador", "valor_atual", "apuracao", "data", "nivel")
                if not str(dados.get(c) or "").strip()]
    if faltando:
        return _resultado(1, False, caminho, verificador,
                          f"linha de base sem campos obrigatorios: {faltando}")
    return _resultado(1, True, caminho, verificador,
                      f"linha de base '{dados['id']}' registrada em {dados['data']} "
                      f"(apuracao {dados['apuracao']}, nivel {dados['nivel']})")


def verificar_i2(caminho):
    """I2 -- termo de autonomia (P7). Uma minuta (rascunho/proposto) nao
    satisfaz; exige estado 'decidido' com decisor, data e justificativa,
    e decisor nao pode ser agente (a trava de quem pode decidir ja vive
    em governanca.py -- este verificador so confere o que ficou gravado).
    """
    verificador = "inegociaveis.verificar_i2"
    dados, erro = _carregar(caminho)
    if erro:
        return _resultado(2, False, caminho, verificador, erro)
    estado = dados.get("estado")
    if estado != "decidido":
        return _resultado(2, False, caminho, verificador,
                          f"termo em estado '{estado}', nao 'decidido' -- "
                          f"minuta ou proposta nao satisfaz o inegociavel 2")
    faltando = [c for c in ("decisor", "data_decisao", "justificativa_decisao")
                if not str(dados.get(c) or "").strip()]
    if faltando:
        return _resultado(2, False, caminho, verificador,
                          f"termo decidido sem campos obrigatorios: {faltando}")
    if not str(dados.get("versao") or "").strip():
        return _resultado(2, False, caminho, verificador,
                          "termo sem versao rastreavel")
    return _resultado(2, True, caminho, verificador,
                      f"termo '{dados.get('id')}' decidido por "
                      f"'{dados['decisor']}' em {dados['data_decisao']}")


def verificar_i3(caminho):
    """I3 -- casos de teste com saida esperada (P8). 'Teste executou' nao
    basta -- exige conjunto revisado (nao rascunho) com ao menos um caso,
    cada um com saida_esperada e esperado_definido_em preenchidos (a
    congelamento contra vies retrospectivo ja e checado por piloto.py;
    aqui confere-se o que ficou gravado).
    """
    verificador = "inegociaveis.verificar_i3"
    dados, erro = _carregar(caminho)
    if erro:
        return _resultado(3, False, caminho, verificador, erro)
    if dados.get("estado") != "revisado":
        return _resultado(3, False, caminho, verificador,
                          f"conjunto em estado '{dados.get('estado')}', nao "
                          f"'revisado' -- 'teste executou' nao equivale a "
                          f"'caso com saida esperada revisada'")
    casos = dados.get("casos")
    if not isinstance(casos, list) or not casos:
        return _resultado(3, False, caminho, verificador,
                          "conjunto revisado sem nenhum caso")
    sem_esperado = [c.get("identificador", "?") for c in casos
                    if not str((c or {}).get("saida_esperada") or "").strip()
                    or not str((c or {}).get("esperado_definido_em") or "").strip()]
    if sem_esperado:
        return _resultado(3, False, caminho, verificador,
                          f"casos sem saida esperada rastreavel: {sem_esperado}")
    return _resultado(3, True, caminho, verificador,
                      f"conjunto '{dados.get('id')}' revisado com {len(casos)} "
                      f"caso(s), todos com saida esperada definida antes da execucao")


def verificar_i4(caminho):
    """I4 -- ao menos uma metrica de resultado (P9). Metrica de uso ou
    qualidade nao satisfaz -- so 'tipo: resultado' conta, e precisa estar
    apurada (com resultado_apurado preenchido), nao apenas planejada.
    """
    verificador = "inegociaveis.verificar_i4"
    dados, erro = _carregar(caminho)
    if erro:
        return _resultado(4, False, caminho, verificador, erro)
    tipo = dados.get("tipo")
    if tipo != "resultado":
        return _resultado(4, False, caminho, verificador,
                          f"metrica tipo '{tipo}' nao satisfaz -- inegociavel 4 "
                          f"exige metrica de RESULTADO, metrica de uso/qualidade "
                          f"nao conta")
    if dados.get("estado") != "apurada":
        return _resultado(4, False, caminho, verificador,
                          f"metrica de resultado em estado '{dados.get('estado')}', "
                          f"nao 'apurada' -- planejada sem resultado nao satisfaz")
    if not str(dados.get("resultado_apurado") or "").strip():
        return _resultado(4, False, caminho, verificador,
                          "metrica apurada sem 'resultado_apurado' preenchido")
    return _resultado(4, True, caminho, verificador,
                      f"metrica de resultado '{dados.get('id')}' apurada: "
                      f"{dados.get('resultado_apurado')}")


def verificar_i5(caminho):
    """I5 -- responsavel nomeado pela recalibragem (P10). 'equipe', 'TI',
    'consultoria' nao satisfazem -- exige pessoa nomeada e cadencia
    definida (a checagem lexica de pessoa nomeada ja vive em
    calibragem.py; aqui confere-se o que ficou gravado na rotina).
    """
    verificador = "inegociaveis.verificar_i5"
    dados, erro = _carregar(caminho)
    if erro:
        return _resultado(5, False, caminho, verificador, erro)
    responsavel = str(dados.get("responsavel") or "").strip()
    genericos = {"equipe", "area", "time", "setor", "departamento", "a definir",
                 "ti", "consultoria"}
    tokens = set(responsavel.lower().replace(",", " ").split())
    if not responsavel or tokens & genericos:
        return _resultado(5, False, caminho, verificador,
                          f"responsavel '{responsavel or '(vazio)'}' nao e pessoa "
                          f"nomeada -- area, equipe ou coletivo generico (mesmo em "
                          f"frase composta, ex. 'equipe de TI') nao satisfaz")
    if not str(dados.get("cadencia") or "").strip():
        return _resultado(5, False, caminho, verificador,
                          "rotina sem cadencia definida")
    return _resultado(5, True, caminho, verificador,
                      f"responsavel '{responsavel}' pela recalibragem, "
                      f"cadencia '{dados['cadencia']}'")


VERIFICADORES = {
    1: verificar_i1, 2: verificar_i2, 3: verificar_i3,
    4: verificar_i4, 5: verificar_i5,
}


def satisfazer(n, autor, resultado):
    """Chama avancar.py --satisfazer-inegociavel so depois que o
    verificador correspondente devolveu satisfeito=True -- este e o
    unico ponto do pacote que grava o registro estruturado do nucleo, e
    ele nunca grava a partir de um booleano solto, so a partir do
    resultado ja verificado semanticamente.
    """
    r = subprocess.run(
        [sys.executable, str(RAIZ_NUCLEO / "avancar.py"),
         "--satisfazer-inegociavel", str(n), "--autor", autor,
         "--evidencia", f"{resultado['verificador']} :: {resultado['motivo']} "
                        f"(ref: {resultado['evidencia_ref']})"],
        capture_output=True, text=True,
    )
    return r.returncode, r.stdout, r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verificar", type=int, required=True, choices=[1, 2, 3, 4, 5])
    ap.add_argument("--arquivo", required=True)
    ap.add_argument("--satisfazer", action="store_true",
                     help="apos verificar com sucesso, grava a satisfacao no nucleo")
    ap.add_argument("--autor", default=None)
    a = ap.parse_args()

    resultado = VERIFICADORES[a.verificar](a.arquivo)
    print(f"{resultado['id']} | satisfeito={resultado['satisfeito']} | "
          f"{resultado['motivo']}")

    if not resultado["satisfeito"]:
        sys.exit(1)

    if a.satisfazer:
        if not a.autor:
            print("--satisfazer exige --autor", file=sys.stderr)
            sys.exit(1)
        codigo, saida, erro = satisfazer(a.verificar, a.autor, resultado)
        if codigo != 0:
            print(erro.strip() or saida.strip(), file=sys.stderr)
            sys.exit(codigo)
        print(saida.strip())


if __name__ == "__main__":
    main()
