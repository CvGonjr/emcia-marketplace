"""Executa todas as suítes existentes; evidência datada por pacote."""
import concurrent.futures,datetime,pathlib,re,subprocess,sys
raiz=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'testes/negativos.sh').exists())
destino=pathlib.Path(sys.argv[1]).resolve(); destino.mkdir(parents=True,exist_ok=True)
mods=[raiz/'testes/negativos.sh']+sorted((raiz/'testes').glob('*.py'))
def executar(p):
    cmd=['bash' if p.suffix=='.sh' else sys.executable,str(p)]
    r=subprocess.run(cmd,cwd=raiz,text=True,capture_output=True)
    saida=r.stdout+r.stderr
    falha=r.returncode!=0 or bool(re.search(r'FALHA|FAILED|^FAIL:',saida,re.M))
    n=len(re.findall(r'^\s*ok\s+',saida,re.M)); unit=re.findall(r'Ran (\d+) tests?',saida)
    if unit:n=int(unit[-1])
    if p.name in ('esforco.py','metodo_empacotado.py'):n=1
    return p.name,r.returncode,n,falha,saida
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: resultados=list(ex.map(executar,mods))
resumo='Executada em: '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n'
resumo+='Base: '+subprocess.run(['git','rev-parse','HEAD'],cwd=raiz,capture_output=True,text=True).stdout.strip()+'\n'
for nome,rc,n,falha,saida in resultados:resumo+=f'{nome}: {n} verificações; saída {rc}; falha {falha}\n'
resumo+=f'TOTAL: {sum(x[2] for x in resultados)} verificações em {len(resultados)} módulos; módulos com falhas: {sum(x[3] for x in resultados)}\n'
texto=resumo+'\nSaída integral:\n'
for nome,rc,n,falha,saida in resultados:texto+='\n$ '+nome+'\n'+saida
(destino/'saida-suite.txt').write_text(texto)
print(resumo,flush=True)
sys.exit(any(x[3] for x in resultados))
