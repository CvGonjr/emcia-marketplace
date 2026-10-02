"""Registra a entrega publicada e conferida pelo engenheiro, sem API ou aceite."""
import argparse
import datetime
import fcntl
import hashlib
import json
import canais as K


def entregar(entrada, autor=None):
    st, pb = K.contexto(autor)
    dados = json.loads(K.seguro(entrada, 'rascunho').read_text())
    K.exigir(isinstance(dados, dict) and set(dados) == {'entregavel', 'versao', 'sha256', 'arquivo_id',
                                                      'destino_id', 'destinatario', 'data'}, 'campos da entrega inválidos')
    emissao = st.get('entregaveis_emitidos', {}).get(dados['entregavel'])
    K.exigir(isinstance(emissao, dict), 'entregável não emitido pelo núcleo')
    K.exigir(type(dados['versao']) is int and dados['versao'] == emissao.get('versao'), 'versão diferente da emitida')
    arquivo = K.seguro(emissao['arquivo'], 'caso')
    K.exigir(arquivo.is_file(), 'arquivo emitido ausente')
    sha = hashlib.sha256(arquivo.read_bytes()).hexdigest()
    K.exigir(dados['sha256'] == emissao.get('sha256') == sha, 'hash divergente da emissão; emita novamente após revisão')
    eventos = [e for e in K.E.eventos() if e.get('evento') == 'EntregavelEmitido'
               and e.get('entregavel') == dados['entregavel']]
    K.exigir(bool(eventos) and eventos[-1].get('sha256') == sha
             and eventos[-1].get('versao') == dados['versao'], 'emissão sem evento coerente')
    canal = K.resolver(pb, dados['entregavel'], 'saida')
    K.exigir(canal['finalidade'] == 'entregas' and canal['ferramenta'] == 'drive', 'canal de entregas não declarado')
    K.exigir(dados['destino_id'] == canal['ids']['pasta_id'], 'destino não declarado para entregas')
    K.id_externo(dados['arquivo_id']); K.id_externo(dados['destino_id'])
    K.exigir(K.E.pessoa_nomeada(dados['destinatario']), 'destinatário precisa ser pessoa nomeada')
    datetime.date.fromisoformat(dados['data'])
    p = K.seguro('registro/entregas.json')
    registro = json.loads(p.read_text()) if p.exists() else {'schema': 1, 'entregas': []}
    evs = [e for e in K.E.eventos() if e.get('evento') == 'EntregavelEntregue']
    K.exigir(bool(p.exists()) == bool(evs), 'registro de entregas e trilha divergentes')
    if evs:
        K.exigir(evs[-1].get('registro_sha256') == hashlib.sha256(p.read_bytes()).hexdigest(), 'registro de entregas adulterado')
    K.exigir(isinstance(registro.get('entregas'), list), 'registro de entregas inválido')
    ref = dict(dados, id=f"ENT-{len(registro['entregas'])+1:06d}", autor=st['responsavel'],
               canais_versao=K.G.carregar(pb)['versao'], registrado_em=datetime.datetime.now(datetime.timezone.utc).isoformat())
    backup = p.read_bytes() if p.exists() else None
    try:
        registro['entregas'].append(ref); K.escrever(p, registro)
        K.E.evento('EntregavelEntregue', **ref, registro_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    except Exception:
        if backup is None: p.unlink(missing_ok=True)
        else: p.write_bytes(backup)
        raise
    return ref


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--entrada', required=True); ap.add_argument('--autor')
    a = ap.parse_args()
    try:
        with K.seguro('registro/.canais.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            resultado = entregar(a.entrada, a.autor)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        K.E.evento('TentativaNegada', autor=(K.E.ler() or {}).get('responsavel'), operacao='entregar-material', motivo=str(exc))
        ap.exit(1, 'Recusado: '+str(exc)+'\n')


if __name__ == '__main__': main()
