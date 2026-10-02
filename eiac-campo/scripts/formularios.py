"""Links preparados e seleção local de submissões; não publica nem envia."""
import argparse
import json
import urllib.parse
import canais as K


def selecionar(canal, submissoes):
    K.exigir(isinstance(submissoes, list), 'exportação precisa ser lista')
    resultado = []
    for s in submissoes:
        K.exigir(isinstance(s, dict), 'submissão inválida')
        if s.get('campos_ocultos', {}).get('caso') != canal['filtro']['valor']:
            continue
        K.exigir(s.get('formulario_id') == canal['ids']['formulario_id'], 'formulário não declarado')
        K.id_externo(s.get('submissao_id'))
        resultado.append(s)
    return resultado


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('operacao', choices=['link', 'submissoes'])
    ap.add_argument('--etapa', required=True); ap.add_argument('--entrada'); ap.add_argument('--formulario')
    a = ap.parse_args()
    try:
        st, pb = K.contexto()
        c = K.resolver(pb, a.etapa, 'entrada')
        K.exigir(c['ferramenta'] == 'tally', 'canal não é Tally')
        if a.operacao == 'link':
            resultado = {'link_preparado': 'https://tally.so/r/'+urllib.parse.quote(c['ids']['formulario_id'], safe='')+'?'+urllib.parse.urlencode({'caso': st['caso']}),
                         'publicacao_ou_envio': 'exige instrução expressa do engenheiro'}
        else:
            K.exigir(a.formulario == c['ids']['formulario_id'], 'formulário não declarado')
            resultado = selecionar(c, json.loads(K.seguro(a.entrada, 'rascunho/entrada').read_text()))
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        K.E.evento('TentativaNegada', autor=(K.E.ler() or {}).get('responsavel'), operacao='formularios-'+a.operacao, motivo=str(exc))
        ap.exit(1, 'Recusado: '+str(exc)+'\n')


if __name__ == '__main__': main()
