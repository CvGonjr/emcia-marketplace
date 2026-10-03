#!/usr/bin/env python3
"""Confere remissões do campo contra o pacote extraído do commit canônico."""
import hashlib
import json
import pathlib
import re
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
CAMPO = RAIZ / 'eiac-campo'
PACOTE = CAMPO / 'reference/metodo'
CTX = 'EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md'
ALVO = re.compile(r'auxiliares/[\w.-]+\.md|(?:(?:EMCIA-)?[A-Z]{3}-\d{2}|EMCIA-E[1-5])(?:-[\w-]+\.md)?(?![\w-])')
SECAO = re.compile(r'(?:§+\s*|seç(?:ão|ões)\s+|sec(?:ao|oes)\s+)(\d+(?:\.\d+)*|[A-Z]\d+(?:\.\d+)*)', re.I)
DIRETA = re.compile(r'^[`*\s,():—–-]*(\d+(?:\.\d+)+|[A-Z]\d+(?:\.\d+)+)\b')
CONTINUACAO = re.compile(r'^[\s`*]*(?:,|e|a|até|/|–|—|-)\s*(\d+(?:\.\d+)+)\b')
ANTIGO = 'CTX-01-instrumento-camada-contexto.md'


def secoes(texto):
    # Exemplos YAML/JSON não são títulos de seção do documento.
    texto = re.sub(r'^```[^\n]*\n.*?^```[^\n]*$', '', texto, flags=re.M | re.S)
    return set(re.findall(r'^#{1,6}\s+(?:\*\*)?(\d+(?:\.\d+)*|[A-Z]\d+(?:\.\d+)*)[.\s]', texto, re.M))


def catalogo():
    manifesto = json.loads((PACOTE / 'manifesto.json').read_text())
    docs = {}
    for nome, sha in manifesto['documentos'].items():
        dados = (PACOTE / nome).read_bytes()
        if hashlib.sha256(dados).hexdigest() != sha:
            raise ValueError('hash divergente: ' + nome)
        sec = secoes(dados.decode('utf-8'))
        docs[nome] = sec
        docs[manifesto['caminhos_canonicos'][nome]] = sec
        match = re.match(r'EMCIA-(?:[A-Z]{3}-\d{2}|E[1-5])', nome)
        if match:
            docs[match[0]] = sec
            docs[match[0].removeprefix('EMCIA-')] = sec
    return docs


def remissoes(texto):
    """Código ou caminho seguido de §/seção/número; inclui continuações."""
    # A continuação de linha não encerra uma citação; parágrafo novo encerra.
    for bloco in re.split(r'\n\s*\n', texto):
        alvos = list(ALVO.finditer(bloco))
        for i, alvo in enumerate(alvos):
            fim = alvos[i+1].start() if i+1 < len(alvos) else len(bloco)
            trecho = bloco[alvo.end():fim]
            marcadas = list(SECAO.finditer(trecho))
            direta = DIRETA.match(trecho)
            if direta:
                marcadas.insert(0, direta)
            refs = []
            for marcada in marcadas:
                refs.append(marcada[1])
                resto = trecho[marcada.end():]
                while seguida := CONTINUACAO.match(resto):
                    refs.append(seguida[1])
                    resto = resto[seguida.end():]
            for sec in dict.fromkeys(refs):
                yield alvo[0], sec
            if alvo[0].endswith('.md') and not refs:
                yield alvo[0], None


def conferir(texto, docs, nome='<texto>'):
    erros = []
    for alvo, sec in remissoes(texto):
        if alvo not in docs:
            erros.append(f'{nome}: documento inexistente: {alvo}')
        elif sec is not None and sec not in docs[alvo]:
            erros.append(f'{nome}: seção inexistente: {alvo} §{sec}')
    if ANTIGO in texto:
        erros.append(f'{nome}: remissão ao resumo CTX retirado')
    return erros


def arquivos():
    for area in ('skills', 'commands', 'reference'):
        for p in sorted((CAMPO / area).rglob('*')):
            if p.is_file() and not p.is_relative_to(PACOTE) and p.suffix in ('.md', '.json'):
                yield p


def auditar(docs):
    erros = []
    for p in arquivos():
        texto = p.read_text(encoding='utf-8')
        nome = str(p.relative_to(RAIZ))
        erros.extend(conferir(texto, docs, nome))
        if p.suffix == '.json':
            dados = json.loads(texto)
            if isinstance(dados, dict) and 'instrumento' in dados:
                alvo = dados['instrumento']
                if alvo not in docs:
                    erros.append(f'{nome}: instrumento inexistente: {alvo}')
                else:
                    for k, v in dados.items():
                        if k.startswith('secao_') and v not in docs[alvo]:
                            erros.append(f'{nome}: {k} inexistente: {alvo} §{v}')
    return erros


class Citacoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = catalogo()

    def test_01_secao_inexistente_recusa(self):
        self.assertTrue(conferir('EMCIA-TRI-01 §99.99', self.docs))
        self.assertTrue(conferir('EMCIA-TRI-01, seção 99.99', self.docs))
        self.assertTrue(conferir('EMCIA-TRI-01 99.99', self.docs))

    def test_02_auxiliar_inexistente_recusa(self):
        self.assertTrue(conferir('auxiliares/EMCIA-ROT-99-inexistente.md §3.3', self.docs))
        self.assertTrue(conferir('auxiliares/EMCIA-ROT-02-roteiro-de-habilitacao.md §99.99', self.docs))

    def test_03_citacoes_do_campo_resolvem(self):
        self.assertEqual(auditar(self.docs), [])

    def test_04_tri_perguntas_e_pontuacao(self):
        texto = (CAMPO / 'skills/hb-enquadrar/SKILL.md').read_text()
        refs = set(remissoes(texto))
        self.assertIn(('EMCIA-TRI-01', '3.3'), refs)
        self.assertIn(('EMCIA-TRI-01', '3.4'), refs)
        self.assertRegex(texto, r'seção 3\.3 para as perguntas e seção 3\.4 para\s+a pontuação')
        instrumento = (PACOTE / 'EMCIA-TRI-01-instrumento-de-triagem.md').read_text()
        self.assertRegex(instrumento, r'(?m)^### 3\.3 As nove perguntas')
        self.assertRegex(instrumento, r'(?m)^### 3\.4 ')
        f = json.loads((CAMPO / 'reference/formularios/triagem.json').read_text())
        self.assertEqual((f['secao_perguntas'], f['secao_pontuacao']), ('3.3', '3.4'))

    def test_05_ctx_canonico_substitui_resumos(self):
        self.assertFalse((RAIZ / ANTIGO).exists())
        self.assertFalse((CAMPO / 'reference' / ANTIGO).exists())
        self.assertEqual(conferir(f'reference/metodo/{CTX} §3.7', self.docs), [])
        self.assertTrue(conferir(f'reference/{ANTIGO}', self.docs))
        for p in (RAIZ / 'README.md', RAIZ / 'INSTALACAO.md', RAIZ / '.projectdocs/map.md'):
            self.assertIn('eiac-campo/reference/metodo/' + CTX, p.read_text())

    def test_06_auxiliares_vem_do_manifesto_canonico(self):
        m = json.loads((PACOTE / 'manifesto.json').read_text())
        for n in ('EMCIA-ROT-02-roteiro-de-habilitacao.md', 'EMCIA-HAB-fluxo-operacional-proposta.md'):
            self.assertEqual(m['caminhos_canonicos'][n], 'auxiliares/' + n)
            self.assertEqual(conferir('auxiliares/' + n + ' §3.3', self.docs), [])

    def test_07_formatos_e_continuacao(self):
        for t in ('EMCIA-TRI-01 §3.3 e §3.4', 'EMCIA-TRI-01, seção 3.3 e seção 3.4',
                  'EMCIA-TRI-01 3.3 e seção 3.4', 'EMCIA-TRI-01, seção 3.3\npara perguntas e seção 3.4 para pontuação'):
            self.assertEqual(set(remissoes(t)), {('EMCIA-TRI-01', '3.3'), ('EMCIA-TRI-01', '3.4')})
            self.assertEqual(conferir(t, self.docs), [])
        for t in ('EMCIA-TRI-01 §§3.3 e 99.99', 'TRI-01, seções 3.3 e 99.99',
                  'EMCIA-TRI-01 3.3, 99.99'):
            self.assertTrue(conferir(t, self.docs))
        self.assertEqual(conferir('TRI-01 §§3.3 e 3.4', self.docs), [])

    def test_08_instrumentos_distintos_em_p1_e_p3d(self):
        for nome, secao in (('hb-mapear-contexto', '3.4.1'), ('hb-confrontar', '3.4.3'), ('hb-priorizar', '3.4.3')):
            refs = set(remissoes((CAMPO/'skills'/nome/'SKILL.md').read_text()))
            self.assertIn(('EMCIA-MET-01', secao), refs)
        refs = set(remissoes((CAMPO/'skills/hb-mapear-contexto/SKILL.md').read_text()))
        self.assertNotIn(('EMCIA-MET-01', '3.4.3'), refs)


if __name__ == '__main__':
    unittest.main(verbosity=2)
