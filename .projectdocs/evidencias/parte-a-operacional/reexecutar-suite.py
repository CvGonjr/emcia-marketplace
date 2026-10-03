"""Suíte integral na versão do CI; subprocessos herdam Python pelo PATH."""
import concurrent.futures, json, pathlib, re, subprocess, sys
raiz = pathlib.Path(__file__).resolve().parents[3]
if sys.version_info[:2] != (3, 12):
    sys.exit('Execute com Python 3.12 e seu binário python3 no PATH')
excluidos = set(sys.argv[2:])  # Testes de pacote posterior ainda em construção.
mods = [raiz/'testes/negativos.sh', *sorted((raiz/'testes').glob('*.py'))]
mods = [p for p in mods if p.name not in excluidos]
def rodar(p):
    cmd = ['bash' if p.suffix == '.sh' else sys.executable, str(p.relative_to(raiz))]
    r = subprocess.run(cmd, cwd=raiz, capture_output=True, text=True)
    saida = r.stdout+r.stderr
    falha = r.returncode != 0 or bool(re.search(r'FALHA|FAILED|^FAIL:', saida, re.M))
    unit = re.findall(r'Ran (\d+) tests?', saida)
    n = int(unit[-1]) if unit else len(re.findall(r'^\s*ok\s+', saida, re.M))
    if p.name in ('esforco.py', 'metodo_empacotado.py'): n = 1
    return dict(modulo=p.name, codigo=r.returncode, testes=n, falha=falha, saida=saida)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    resultados = list(pool.map(rodar, mods))
saida = pathlib.Path(sys.argv[1])
resumo = 'Python: '+sys.version+'\nHEAD: '+subprocess.check_output(['git','rev-parse','HEAD'],cwd=raiz,text=True)
resumo += 'Excluídos explicitamente: '+', '.join(sorted(excluidos))+'\n'
resumo += '\n'.join(f"{r['modulo']}: {r['testes']} testes; saída {r['codigo']}; falha {r['falha']}" for r in resultados)
resumo += f"\nTOTAL: {sum(r['testes'] for r in resultados)} testes; {len(resultados)} módulos; {sum(r['falha'] for r in resultados)} módulos com falhas\n"
saida.write_text(resumo+'\nSaída integral:\n'+''.join('\n$ '+r['modulo']+'\n'+r['saida'] for r in resultados))
print(resumo, flush=True)
sys.exit(any(r['falha'] for r in resultados))
