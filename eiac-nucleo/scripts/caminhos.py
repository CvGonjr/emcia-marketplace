"""Caminhos do hook e do shell, relativos à raiz física do caso.

Mantém também o caminho lexical: um arquivo de área protegida que seja
link para fora continua protegido. Um alias externo para dentro é
reconhecido pela resolução física. Não contém vocabulário de método.
"""
import ast, os, pathlib, re, shlex

class CaminhoInvalido(ValueError):
    pass


def raiz_caso(ev):
    candidatos = [os.environ.get('CLAUDE_PROJECT_DIR'), ev.get('cwd'), os.getcwd()]
    for candidato in candidatos:
        if not candidato:
            continue
        try:
            p = pathlib.Path(candidato).expanduser().resolve()
            for pai in (p, *p.parents):
                if (pai/'registro/estado.json').is_file():
                    return pai
        except (OSError, RuntimeError, ValueError):
            continue
    return None


class Contexto:
    def __init__(self, raiz, cwd):
        self.raiz = pathlib.Path(raiz).resolve()
        self.cwd = pathlib.Path(cwd).expanduser()
        if not self.cwd.is_absolute():
            self.cwd = self.raiz/self.cwd

    def absolutos(self, alvo, cwd=None):
        if not alvo:
            return ()
        try:
            p = pathlib.Path(os.path.expandvars(str(alvo))).expanduser()
            if not p.is_absolute():
                p = pathlib.Path(cwd or self.cwd)/p
            return (pathlib.Path(os.path.abspath(p)), p.resolve())
        except (OSError, RuntimeError, ValueError) as exc:
            raise CaminhoInvalido(f'caminho não resolvível: {alvo}: {exc}') from exc

    def relativos(self, alvo, cwd=None):
        saida = set()
        for p in self.absolutos(alvo, cwd):
            try:
                saida.add(p.relative_to(self.raiz).as_posix())
            except ValueError:
                pass
        return saida

    def em(self, alvo, area, cwd=None):
        return any(p == area or p.startswith(area+'/') for p in self.relativos(alvo,cwd))

    def em_segmento(self, alvo, segmento, cwd=None):
        return any(segmento in pathlib.PurePosixPath(p).parts for p in self.relativos(alvo,cwd))

    def nomes(self, alvo, cwd=None):
        return {parte for p in self.absolutos(alvo,cwd) for parte in p.parts}


class Palavra(str):
    """Mantém a distinção entre operador shell e caractere entre aspas."""
    def __new__(cls, valor, operador=False):
        obj = super().__new__(cls,valor)
        obj.operador = operador
        return obj


def tokens_shell(texto):
    pontuacao = ';&|<>()\n'
    marcas = {c:chr(0xE000+i) for i,c in enumerate(pontuacao)}
    inversas = {v:k for k,v in marcas.items()}
    aspas, escape, protegido = None, False, []
    for c in texto:
        if escape:
            protegido.append(marcas.get(c,c)); escape=False
        elif c == "\\" and aspas != "'":
            protegido.append(c); escape=True
        elif c in ("'", '"'):
            if aspas == c: aspas=None
            elif aspas is None: aspas=c
            protegido.append(c)
        else:
            protegido.append(marcas.get(c,c) if aspas else c)
    lexer = shlex.shlex(''.join(protegido), posix=True, punctuation_chars=pontuacao)
    lexer.whitespace=' \t\r'
    lexer.whitespace_split=True
    for token in lexer:
        operador = bool(token) and all(c in pontuacao for c in token)
        if operador:
            for op in re.findall(r'&&|\|\||&>>|&>|>>|>&|<<<|<<|<>|<&|>\||[;&|<>()\n]',token):
                yield Palavra(op,True)
        else:
            yield Palavra(''.join(inversas.get(c,c) for c in token))


def comandos(texto, cwd, profundidade=0):
    """Segmenta com shlex; preserva diretório de cd e shells aninhados."""
    if profundidade > 8:
        raise ValueError('shell aninhado demais para inspecao de caminhos')
    grupos, atual = [], []
    for parte in [*tokens_shell(texto), Palavra(';',True)]:
        if parte.operador and parte in (';', '&&', '||', '|', '&', '\n', '(', ')'):
            if atual:
                grupos.append((atual,parte))
                atual=[]
            if parte in ('(',')'):
                grupos.append((None,parte))
        else:
            atual.append(parte)
    diretorio = pathlib.Path(cwd)
    pilha = []
    for grupo,separador in grupos:
        if grupo is None:
            if separador=='(': pilha.append(diretorio)
            elif pilha: diretorio=pilha.pop()
            continue
        nome=pathlib.Path(grupo[0]).name
        if nome == 'cd' and len(grupo)>1:
            p=pathlib.Path(os.path.expandvars(grupo[-1])).expanduser()
            destino=p if p.is_absolute() else diretorio/p
            # cd em pipeline/background não altera o diretório do shell pai.
            if separador not in ('|','&') and destino.is_dir():
                diretorio=destino
        elif nome in ('bash','sh','zsh') and any(p.startswith('-') and 'c' in p for p in grupo[1:]):
            pos=next(i+1 for i,p in enumerate(grupo) if p.startswith('-') and 'c' in p)
            if pos<len(grupo):
                yield from comandos(grupo[pos],diretorio,profundidade+1)
        elif nome in ('command','exec','env'):
            pos=1
            while pos<len(grupo) and (grupo[pos].startswith('-') or re.match(r'^[A-Za-z_][A-Za-z0-9_]*=',grupo[pos])):
                pos+=1
            if pos<len(grupo):
                yield grupo[pos:],diretorio
        else:
            yield grupo,diretorio


def argumentos_caminho(grupo):
    for parte in grupo[1:]:
        yield parte
        yield from re.findall(r'(?:/|\.\.?/)?(?:[\w.-]+/)+[\w.-]+',parte)
        # Literais em scripts inline são inspecionados sem executar código.
        try:
            arvore=ast.parse(parte)
        except (SyntaxError, ValueError):
            continue
        for no in ast.walk(arvore):
            if isinstance(no,ast.Constant) and isinstance(no.value,str):
                yield no.value


def escritas(grupo):
    """Compatibilidade inicial da guarda; alvos já normalizados pelo chamador."""
    if any('>' in parte for parte in grupo) or pathlib.Path(grupo[0]).name in ('tee','mv','cp','rm','touch','mkdir','install'):
        return list(argumentos_caminho(grupo))
    return []
