import concurrent.futures, datetime, pathlib, re, subprocess
raiz=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'testes/negativos.sh').is_file())
mods=[raiz/'testes/negativos.sh']+sorted((raiz/'testes').glob('*.py'))
def rodar(p):
 cmd=['bash' if p.suffix=='.sh' else 'python3',str(p.relative_to(raiz))]
 r=subprocess.run(cmd,cwd=raiz,text=True,capture_output=True)
 saida=r.stdout+r.stderr
 falha=r.returncode!=0 or bool(re.search(r'FALHA|FAILED|^FAIL:',saida,re.M))
 n=len(re.findall(r'^\s*ok\s+',saida,re.M))
 unit=re.findall(r'Ran (\d+) tests?',saida)
 if unit:n=int(unit[-1])
 # Estes dois módulos encapsulam verificações e resumem seu total.
 if p.name in ('esforco.py','metodo_empacotado.py'):n=1
 return p.name,cmd,r.returncode,n,falha,saida
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: results=list(ex.map(rodar,mods))
texto='A23 — suíte completa\nExecutada em: '+datetime.datetime.now().astimezone().isoformat()+'\nBase: v-sprint3-poc.6 / 533391bb65fdd9735fa9d229d363f04f08bdff35\nConferência: códigos de saída e mensagens FALHA/FAILED/FAIL:.\n\n'
for nome,cmd,rc,n,falha,saida in results: texto+=f'{nome}: {n} verificações; saída {rc}; falha {falha}\n'
texto+=f'TOTAL: {sum(x[3] for x in results)} verificações em {len(results)} módulos; módulos com falhas: {sum(x[4] for x in results)}\n\nSaída integral:\n'
for nome,cmd,rc,n,falha,saida in results: texto+='\n$ '+' '.join(cmd)+'\n'+saida
pathlib.Path(__file__).resolve().with_name('saida-suite.txt').write_text(texto)
print(texto.split('Saída integral:')[0])
raise SystemExit(any(x[4] for x in results))
