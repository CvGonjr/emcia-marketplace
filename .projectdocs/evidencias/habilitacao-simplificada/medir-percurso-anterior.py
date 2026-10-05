"""Instrumenta as operações públicas da fixture da 045 no checkout anterior."""
import collections
import contextlib
import io
import json
import pathlib
import sys
from unittest.mock import patch

raiz=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(raiz/'testes'))
import iniciar_percurso as T
counts=collections.Counter()

def medir(nome):
    func=getattr(T.I,nome)
    def chamada(*args,**kwargs):
        if nome not in ('aprovar','operar') or args[1] not in ('perfil','aceitar-minutas'):
            counts[nome]+=1
        return func(*args,**kwargs)
    return chamada

caso=T.Percurso('test_01_percurso_e_tres_retomadas');caso.setUp()
try:
    with contextlib.ExitStack() as stack:
        for nome in ('aprovar','operar','registrar_retorno','retomar'):
            stack.enter_context(patch.object(T.I,nome,side_effect=medir(nome)))
        with contextlib.redirect_stdout(io.StringIO()):caso.test_01_percurso_e_tres_retomadas()
    print(json.dumps(dict(commit='70702c6',aprovacoes_agrupadas=5,conferencias_formulario=1,
        chamadas_publicas_por_operacao=dict(counts),chamadas_script_modeladas=sum(counts.values()),
        criterio='Uma chamada por operação pública iniciar.py da fixture, excluindo perfil e aceitação reutilizáveis. Hooks/MCPs e helpers internos não contam. Não é medição do runtime Claude.',
        arquivo_fixture='testes/iniciar_percurso.py'),ensure_ascii=False,indent=2))
finally:caso.doCleanups()
