"""Diagnóstico somente leitura de arquivos contra um manifesto declarado.

Não produz evento, altera estado ou decide permissão de qualquer operação.
"""
import hashlib
import json
import pathlib
import re


def conferir(pb):
    regra=pb.get('referencia_integridade')
    if regra is None: return {'declarada':False,'confere':None,'erros':[]}
    erros=[]
    try:
        raiz=pathlib.Path.cwd().resolve()
        def local(nome):
            p=pathlib.Path(nome)
            if p.is_absolute() or '..' in p.parts: raise ValueError('caminho declarado fora do caso')
            p=raiz/p
            if not p.resolve().is_relative_to(raiz) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(raiz)):
                raise ValueError('caminho declarado inválido ou symlink')
            return p
        diretorio=local(regra['diretorio'])
        manifest=local(str(pathlib.Path(regra['diretorio'])/regra['manifesto']))
        dados=json.loads(manifest.read_text())
        hashes=dados[regra['campo_hashes']]
        if not isinstance(hashes,dict) or not hashes: raise ValueError('manifesto sem mapa de hashes')
        for nome,esperado in hashes.items():
            if pathlib.Path(nome).name!=nome or not isinstance(esperado,str) or not re.fullmatch('[0-9a-f]{64}',esperado):
                raise ValueError('entrada inválida no manifesto')
            p=local(str(pathlib.Path(regra['diretorio'])/nome))
            if not p.is_file(): erros.append('arquivo ausente: '+nome)
            elif hashlib.sha256(p.read_bytes()).hexdigest()!=esperado: erros.append('SHA-256 divergente: '+nome)
        esperados=set(hashes)|{regra['manifesto'],'.gitkeep'}
        for p in diretorio.rglob('*'):
            if p.is_symlink() or (p.is_file() and str(p.relative_to(diretorio)) not in esperados):
                erros.append('arquivo não declarado: '+str(p.relative_to(diretorio)))
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        erros.append(str(exc))
    return {'declarada':True,'confere':not erros,'erros':erros}
