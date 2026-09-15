"""Fronteira de delegacao do caso: o que e preparavel e o que exige pessoa.

Uso:  python3 fronteira.py

Nao decide nada. Le a camada que o playbook declara para cada etapa,
resolvida pelo nivel apurado do caso, e imprime. A mesma etapa pode ser
delegavel em um nivel e humana em outro (CAT-01 3.6) — por isso a tabela
so faz sentido depois da triagem.
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import estado as E
import playbook as P


def main():
    st = E.ler()
    if not st:
        print("nenhum caso aberto neste diretorio", file=sys.stderr); sys.exit(1)
    pb, erro = P.carregar()
    if erro:
        print(erro, file=sys.stderr); sys.exit(1)

    nivel = st.get("nivel")
    corrente = st["etapa_atual"]
    print(f"Fronteira de delegacao | caso {st['caso']} | nivel {nivel or 'nao apurado'}")
    if not nivel:
        print("Sem nivel apurado, aplica-se a camada mais restritiva declarada.")
    print()
    print(f"{'':2} {'etapa':6} {'camada':7} {'modalidade':12} natureza")
    for e in pb["etapas"]:
        cam = P.camada(pb, e["id"], nivel)
        marca = "->" if e["id"] == corrente else "  "
        print(f"{marca} {e['id']:6} {cam:7} {e.get('modalidade','?'):12} "
              f"{P.natureza(pb, e['id'], nivel)}")

    print()
    prox = P.proxima_fronteira(pb, corrente, nivel)
    if prox:
        pid, pcam, motivo = prox
        print(f"A partir de {pid} ({pcam}): {motivo}.")
    elif P.humana(P.camada(pb, corrente, nivel)) or \
            (P.etapa(pb, corrente) or {}).get("delegavel") is False:
        print(f"A etapa corrente ({corrente}) ja exige pessoa.")
    else:
        print("Nenhuma fronteira humana daqui em diante neste nivel.")

    desl = pb.get("deslocamento_por_nivel", {}).get(nivel or "")
    if desl:
        print(f"Declarado no playbook para {nivel}: preparacao automatizada ate "
              f"{desl.get('preparacao_automatizada_ate','?')}, verificacao "
              f"obrigatoria a partir de {desl.get('verificacao_obrigatoria_a_partir_de','?')}.")


if __name__ == "__main__":
    main()
