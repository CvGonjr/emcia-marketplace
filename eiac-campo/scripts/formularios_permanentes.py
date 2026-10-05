"""Conferência reutilizável por contrato, sem chamadas remotas."""
import datetime
import json
import pathlib
import urllib.parse
import habilitacao as H

RAIZ = pathlib.Path(__file__).resolve().parents[1]/'reference/formularios'


def modelo(tipo):
    H.exigir(tipo in ('habilitacao', 'triagem', 'ciclo'), 'tipo de formulário não declarado')
    return RAIZ/(tipo+'.json')


def contrato(tipo):
    import aprovacao as A
    p = modelo(tipo); sha = A.hash_arquivo(p)
    return dict(versao_contrato=json.loads(p.read_text()).get('versao', 'sha256:'+sha), contrato_sha256=sha)


def eventos(config):
    return [json.loads(l) for l in pathlib.Path(config).with_name('eventos.jsonl').read_text().splitlines()]


def registrar(config, c, d):
    import iniciar as I
    ev = I.conferir_relatorio_vigente(config, c, d, eventos(config))
    H.exigir(ev and ev.get('resultado') == 'conferido' and ev.get('relatorio')
             and not ev.get('diferencas'), 'formulário permanente exige relatório automático conferido')
    r = ev['relatorio']; tipo = d['modelo']
    H.exigir(r['modelo'] == tipo, 'modelo diverge da conferência')
    reg = dict(formId=d['formulario_id'], **contrato(tipo), data_conferencia=ev['data'],
               relatorio_sha256=r['sha256'], relatorio=r, workspace_id=c['workspace_tally'],
               responsavel=c['responsavel'], habilitacao=d['habilitacao'], caso=d['caso'])
    c.setdefault('formularios_permanentes', {})[tipo] = reg
    I.escrever(config, c); I.log(config, c, 'FormularioPermanenteDeclarado', modelo=tipo, registro=reg)
    return reg


def validar(config, c, tipo):
    import iniciar as I
    reg = c.get('formularios_permanentes', {}).get(tipo)
    H.exigir(isinstance(reg, dict), 'formulário permanente não conferido: '+tipo)
    atual = contrato(tipo)
    H.exigir(all(reg.get(k) == v for k,v in atual.items()), 'contrato mudou; nova conferência obrigatória: '+tipo)
    datetime.datetime.fromisoformat(reg['data_conferencia'])
    H.exigir(reg['responsavel'] == c['responsavel'] and reg['workspace_id'] == c['workspace_tally'],
             'responsável/workspace da conferência diverge da configuração')
    evs = eventos(config)
    declaracoes = [e for e in evs if e.get('evento') == 'FormularioPermanenteDeclarado' and e.get('modelo') == tipo]
    H.exigir(declaracoes and declaracoes[-1]['registro'] == reg, 'declaração permanente sem evento íntegro')
    # Uma leitura posterior em qualquer contexto invalida o formulário permanente.
    conferencias = [e for e in evs if e.get('evento') == 'ConferenciaExternaRegistrada' and e.get('objeto_id') == reg['formId']]
    H.exigir(conferencias and conferencias[-1].get('resultado') == 'conferido'
             and conferencias[-1].get('relatorio') == reg['relatorio'], 'nova conferência do formulário necessária')
    d = dict(habilitacao=reg['habilitacao'], caso=reg['caso'], formulario_id=reg['formId'])
    ev = I.conferir_relatorio_vigente(config, c, d, evs)
    H.exigir(ev['data'] == reg['data_conferencia'] and ev['evidencia_sha256'] == reg['relatorio_sha256'],
             'data/hash da conferência divergente')
    return reg


def link(reg, caso):
    H.identificador(caso)
    return 'https://tally.so/r/'+urllib.parse.quote(reg['formId'], safe='')+'?'+urllib.parse.urlencode({'caso':caso})
