#!/usr/bin/env python3
"""Lê um caso, sem alterá-lo. Uso: resumo-percurso.py <caminho-do-caso>."""
import argparse
from collections import Counter
import json
import pathlib
import subprocess
import sys


def ler_eventos(texto):
    return [json.loads(linha) for linha in texto.splitlines() if linha.strip()]


def hashes_selos(caso):
    """Primeira introdução do evento em commit com nota/autoria do selo.

    Um SeloAplicado ainda fora do Git não comprova que o commit terminou.
    A posição distingue eventos iguais produzidos no mesmo segundo.
    """
    def git(*args):
        r = subprocess.run(['git', '-C', str(caso), *args],
                           text=True, capture_output=True, check=True)
        return r.stdout

    if pathlib.Path(git('rev-parse', '--show-toplevel').strip()).resolve() != caso:
        raise ValueError('o caso precisa ter seu próprio repositório Git')
    vistos, hashes = set(), {}
    for sha in git('log', '--reverse', '--format=%H', '--', 'registro/eventos.jsonl').splitlines():
        eventos = ler_eventos(git('show', sha+':registro/eventos.jsonl'))
        novos = []
        for pos, evento in enumerate(eventos):
            chave = (pos, json.dumps(evento, sort_keys=True, ensure_ascii=False))
            if evento.get('evento') == 'SeloAplicado' and chave not in vistos:
                novos.append((chave, evento))
            vistos.add(chave)
        if novos:
            autor, nota = git('show', '-s', '--format=%an%x00%B', sha).split('\0', 1)
            for chave, evento in novos:
                if evento.get('autor') == autor and evento.get('nota', '').strip() == nota.strip():
                    hashes[chave] = sha
    return hashes


def resumir(caminho):
    caso = pathlib.Path(caminho).expanduser().resolve()
    registro = caso / 'registro'
    st = json.loads((registro / 'estado.json').read_text(encoding='utf-8'))
    pb = json.loads((registro / 'playbook.json').read_text(encoding='utf-8'))
    eventos = ler_eventos((registro / 'eventos.jsonl').read_text(encoding='utf-8'))
    print('Caso: '+str(caso))
    print('Nível: '+str(st.get('nivel')))
    print('Versão do plugin — commits registrados nos eventos:')
    componentes = Counter((e.get('componente', {}).get('variante', 'ausente'),
                          e.get('componente', {}).get('commit', 'ausente')) for e in eventos)
    for (variante, commit), quantidade in sorted(componentes.items()):
        print(f'  {variante}: {commit} ({quantidade} eventos)')

    etapas = [e['id'] for e in pb['etapas']
              if st.get('cumprimentos', {}).get(e['id'], {}).get('cumprido')]
    print(f"Etapas encerradas: {len(etapas)}/{len(pb['etapas'])}")
    print('  '+(', '.join(etapas) or 'nenhuma'))

    # Um arquivo E3 contém as partes autorizadas por E3-D/E3-E.
    grupos = {}
    for item in pb['entregaveis']:
        grupos.setdefault(item['artefato'], []).append(item['id'])
    ultimo_evento = {}
    for e in eventos:
        if e.get('evento') in ('EntregavelEmitido', 'EntregavelNaoAplicavel'):
            ultimo_evento[e['entregavel']] = e['evento']
    emitidos = st.get('entregaveis_emitidos', {})
    linhas = []
    for artefato, portoes in grupos.items():
        aplicaveis = [p for p in portoes
                     if ultimo_evento.get(p) != 'EntregavelNaoAplicavel']
        if not aplicaveis or not all(p in emitidos for p in aplicaveis):
            continue
        partes = []
        for portao in portoes:
            if portao not in aplicaveis:
                partes.append(portao+': não aplicável')
            else:
                dados = emitidos[portao]
                partes.append(f"{portao}: arquivo {dados['arquivo']}, versão {dados['versao']}")
        linhas.append('  '+pathlib.Path(artefato).stem+' — '+'; '.join(partes))
    print(f'Entregáveis emitidos: {len(linhas)}/{len(grupos)}')
    for linha in linhas:
        print(linha)

    satisfeitos = []
    for item in pb['inegociaveis']:
        n = str(item['n'])
        dados = st.get('inegociaveis', {}).get(n, {})
        if isinstance(dados, dict) and dados.get('satisfeito'):
            satisfeitos.append(f"  I{n}: {dados.get('evidencia', 'evidência ausente')}")
    print(f"Inegociáveis satisfeitos: {len(satisfeitos)}/{len(pb['inegociaveis'])}")
    for linha in satisfeitos:
        print(linha)

    hashes = hashes_selos(caso)
    selos = [(pos, e) for pos, e in enumerate(eventos) if e.get('evento') == 'SeloAplicado']
    print(f'Selos: {len(selos)}')
    for pos, e in selos:
        chave = (pos, json.dumps(e, sort_keys=True, ensure_ascii=False))
        print(f"  {e.get('nota', 'sem nota')}: {hashes.get(chave, 'SEM COMMIT CONFIRMADO')}")

    contagens = Counter(e.get('evento', 'tipo ausente') for e in eventos)
    print(f'Eventos por tipo — total {len(eventos)}:')
    for tipo, quantidade in sorted(contagens.items()):
        if tipo != 'TentativaNegada':
            print(f'  {tipo}: {quantidade}')
    print(f"  >>> TentativaNegada: {contagens['TentativaNegada']} <<<")
    recorrencia = st.get('cumprimentos', {}).get('P10', {}).get('estado_recorrente')
    if recorrencia:
        print(f"Recorrência de P10: responsável {recorrencia.get('responsavel')}; "
              f"cadência {recorrencia.get('cadencia')}; ciclo {recorrencia.get('ciclo')}")
    else:
        print('Recorrência de P10: não registrada')
    decisoes = [e for e in eventos if e.get('evento') == 'DecisaoRecalibragemRegistrada']
    if decisoes:
        e = decisoes[-1]
        print(f"Última decisão de calibragem: {e.get('decisao')}; "
              f"ator {e.get('ator')}; drift detectado {e.get('drift_detectado')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('caso')
    args = ap.parse_args()
    try:
        resumir(args.caso)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print('Resumo indisponível: '+str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
