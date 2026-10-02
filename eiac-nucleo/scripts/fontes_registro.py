"""Resolve ids de recebimento e confere bytes com a origem registrada."""
import hashlib
import json
import pathlib
import estado as E


def caminho(valor):
    p = pathlib.Path(valor)
    if p.is_absolute() or '..' in p.parts or not p.resolve().is_relative_to(pathlib.Path.cwd().resolve()):
        raise ValueError('fonte fora do caso')
    if any(x.is_symlink() for x in [p, *p.parents]):
        raise ValueError('fonte contém link')
    return p


def conferir(pb, identificador=None, documento=None):
    contrato = pb.get('registro_fontes')
    if not contrato:
        if identificador: raise ValueError('registro de fontes não declarado')
        return None
    p = caminho(contrato['arquivo'])
    refs = json.loads(p.read_text())[contrato['campo']] if p.exists() else []
    encontrados = [r for r in refs if (r[contrato['id']] == identificador if identificador
                                     else r[contrato['caminho']] == 'fontes/'+documento)]
    if encontrados:
        ref = encontrados[-1]
        eventos = [e for e in E.eventos() if e.get('evento') == contrato['evento']]
        if not eventos or eventos[-1].get('registro_sha256') != hashlib.sha256(p.read_bytes()).hexdigest():
            raise ValueError('registro de fontes sem integridade na trilha')
        if not any(e.get('recebimento') == ref[contrato['id']] and e.get('sha256') == ref[contrato['hash']]
                   for e in eventos):
            raise ValueError('fonte sem evento de recebimento correspondente')
        origem = caminho(ref[contrato['caminho']])
        if hashlib.sha256(origem.read_bytes()).hexdigest() != ref[contrato['hash']]:
            raise ValueError('hash da fonte diverge do recebimento')
        return ref
    # Importações anteriores ao percurso possuem seu próprio registro.
    # Nome do evento e caminho do manifesto vêm do contrato do caso.
    if documento:
        for origem in contrato.get('registros_adicionais', []):
            p = caminho(origem['arquivo'])
            if not p.exists(): continue
            reg = json.loads(p.read_text()); refs_adicionais = reg['vigente']['arquivos'].values()
            for r in refs_adicionais:
                if r['caminho'] == 'fontes/'+documento:
                    eventos = [e for e in E.eventos() if e.get('evento') == origem['evento']]
                    if not eventos or eventos[-1].get('registro_sha256') != hashlib.sha256(p.read_bytes()).hexdigest():
                        raise ValueError('registro adicional sem integridade na trilha')
                    if hashlib.sha256(caminho(r['caminho']).read_bytes()).hexdigest() != r['sha256']:
                        raise ValueError('hash da fonte diverge da importação')
                    return r
    raise ValueError('fonte sem recebimento registrado')
