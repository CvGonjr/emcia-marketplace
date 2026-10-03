"""Fonte e vínculo sintéticos, pelos mesmos comandos usados no terminal humano."""
import datetime, json, pathlib, subprocess, sys
RAIZ = pathlib.Path(__file__).resolve().parents[2]

def vincular(caso, raiz=RAIZ):
    caso = pathlib.Path(caso)
    st = json.loads((caso/'registro/estado.json').read_text())
    pessoa = st['responsavel']
    fonte = dict(id='F-001',fonte='Fonte de controle sintética',tipo='planilha',responsavel='Marina Prado',
                 contrato=dict(estrutura='Uma linha por envio declarado',significado='Registra envios declarados',qualidade='Acesso negado; sem verificação'),
                 acesso='Acesso negado na habilitação sintética',procedencia='D',registrado_por=pessoa,
                 data=datetime.date.today().isoformat())
    p = caso/'rascunho/F-001.yaml'
    p.write_text('\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in fonte.items())+'\n')
    for cmd in [
        [sys.executable,str(raiz/'eiac-nucleo/scripts/curar.py'),'--tipo','fonte','--arquivo','contexto/fontes/F-001.yaml'],
        [sys.executable,str(raiz/'eiac-campo/scripts/restricoes.py'),'vincular','--restricao','RH-01','--fontes','F-001']]:
        r = subprocess.run(cmd,cwd=caso,text=True,capture_output=True)
        if r.returncode: raise RuntimeError(r.stderr)
    return ['F-001']
