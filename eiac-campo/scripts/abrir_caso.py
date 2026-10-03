"""Bootstrap humano: prepara caso novo com pacote do método conferido."""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

RAIZ=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RAIZ/'eiac-nucleo/scripts'))
import estado as E
from importar_habilitacao import conferir


def pacote():
    root=RAIZ/'eiac-campo/reference/metodo'
    arquivo=root/'manifesto.json'
    if arquivo.is_symlink(): raise ValueError('manifesto não admite symlink')
    raw=arquivo.read_bytes(); manifesto=json.loads(raw)
    docs=manifesto.get('documentos')
    if not isinstance(docs,dict) or not docs: raise ValueError('manifesto sem documentos')
    copias={}
    for nome,sha in docs.items():
        if (not isinstance(nome,str) or pathlib.Path(nome).name!=nome or nome in ('.','..','manifesto.json')
                or not isinstance(sha,str) or not re.fullmatch('[0-9a-f]{64}',sha)):
            raise ValueError('entrada inválida no manifesto')
        p=root/nome
        if not p.is_file() or p.is_symlink(): raise ValueError('documento ausente ou inválido: '+nome)
        dados=p.read_bytes()
        if hashlib.sha256(dados).hexdigest()!=sha: raise ValueError('SHA-256 divergente: '+nome)
        copias[nome]=dados
    copias['manifesto.json']=raw
    return copias


def git(cwd,*args):
    return subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True)


def abrir(nome,base,responsavel,expediente=None):
    template=RAIZ/'eiac-campo/template-caso'
    pb=json.loads((template/'registro/playbook.json').read_text())
    if E.autor_e_agente(responsavel): raise ValueError('responsavel nao pode ser codigo de agente')
    if not E.pessoa_nomeada(responsavel,pb['pessoa_nomeada']):
        raise ValueError('responsavel precisa ser pessoa nomeada, nao agente, placeholder nem coletivo generico')
    if not nome or '/' in nome or nome.startswith('.'):
        raise ValueError('nome invalido: use apenas o nome do caso, sem barras')
    base=pathlib.Path(base).expanduser().absolute()
    if any(p.is_symlink() for p in [base,*base.parents]): raise ValueError('base não admite symlink')
    ancestral=next(p for p in [base,*base.parents] if p.exists())
    if git(ancestral,'rev-parse','--show-toplevel').returncode==0:
        raise ValueError('base esta dentro de um repositorio git; um repositorio por caso')
    destino=base/nome
    if destino.exists() or destino.is_symlink(): raise ValueError('ja existe: '+str(destino))
    if expediente is not None: conferir(expediente,nome,responsavel)
    copias=pacote()  # Todas as entradas são conferidas antes de criar o caso.
    base.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.abertura-',dir=base) as tmp:
        stage=pathlib.Path(tmp)/'caso'
        shutil.copytree(template,stage)
        for area in ('metodo','rascunho','caso','fontes'): (stage/area).mkdir(exist_ok=True)
        for nome_arq,data in copias.items():
            p=stage/'metodo'/nome_arq;p.write_bytes(data)
            if hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(data).digest():
                raise ValueError('SHA-256 divergente após cópia: '+nome_arq)
        st_path=stage/'registro/estado.json';st=json.loads(st_path.read_text())
        st.update(caso=nome,responsavel=responsavel)
        st_path.write_text(json.dumps(st,indent=2,ensure_ascii=False)+'\n')
        c=stage/'CLAUDE.md';c.write_text(c.read_text().replace('ALTERE-ME',nome))
        for area in ('rascunho','caso'): (stage/area/'.gitkeep').touch()
        # Claim exclusivo impede substituir destino criado por outra chamada.
        destino.mkdir()
        try: os.replace(stage,destino)
        except Exception:
            destino.rmdir()
            raise
    anterior=pathlib.Path.cwd()
    try:
        os.chdir(destino)
        E.evento('CasoAberto',caso=nome,responsavel=responsavel,autor=responsavel)
        if git(destino,'init','-q').returncode: raise ValueError('git init recusou abertura')
        if git(destino,'add','-A').returncode: raise ValueError('git add recusou abertura')
        commit=git(destino,'commit','-qm','abertura do caso '+nome)
    finally: os.chdir(anterior)
    print(f'caso "{nome}" criado em {destino}\nMétodo copiado e SHA-256 conferido; manifesto preservado.')
    print('Importe a habilitação no terminal, grave o rascunho pelo validador e sele antes de F0.')
    print('Os artefatos da organização entram em fontes/ pelo engenheiro; consulte seu README.')
    if commit.returncode:
        print('ATENCAO: o commit inicial nao foi feito. Configure a identidade do git e commite; a trilha depende do historico.')
    return destino


def recusar(args,motivo):
    """Antes do caso: diagnóstico estruturado e diário na base existente.

    Não cria base nem caso para registrar a negativa. Não grava na ferramenta.
    Falta de identidade humana é erro de bootstrap, sem autoria inventada.
    """
    evento=dict(evento='TentativaNegada',data=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                operacao='abrir-caso',motivo=motivo)
    try:
        regra=json.loads((RAIZ/'eiac-campo/template-caso/registro/playbook.json').read_text())['pessoa_nomeada']
        if E.pessoa_nomeada(args.responsavel,regra): evento['autor']=args.responsavel
        base=pathlib.Path(args.base).expanduser().absolute()
        if base.is_dir() and not any(p.is_symlink() for p in [base,*base.parents]) and git(base,'rev-parse','--show-toplevel').returncode!=0:
            log=base/'.emcia-abertura-eventos.jsonl'
            if not log.is_symlink():
                with log.open('a',encoding='utf-8') as f: f.write(json.dumps(evento,ensure_ascii=False)+'\n')
    except (OSError,ValueError,KeyError): pass
    print(json.dumps(evento,ensure_ascii=False),file=sys.stderr)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('nome');ap.add_argument('base',nargs='?',default=str(pathlib.Path.home()/'casos'))
    ap.add_argument('--responsavel',required=True)
    ap.add_argument('--expediente',type=pathlib.Path)
    a=ap.parse_intermixed_args()
    try: abrir(a.nome,a.base,a.responsavel,a.expediente)
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        recusar(a,str(exc));ap.exit(1,'Recusado: '+str(exc)+'\n')


if __name__=='__main__':main()
