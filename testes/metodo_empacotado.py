#!/usr/bin/env python3
"""Linha de base aprovada: origem Git, bytes e hashes do APR-01."""
import hashlib
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PACOTE = RAIZ / 'eiac-campo/reference/metodo'
CANONICO = RAIZ.parent / 'emcia-artefatos'
CONTRASTE = RAIZ.parent / 'emcia-contraste'
APR = 'EMCIA-APR-01-registro-de-aprovacoes.md'
FIXTURES = RAIZ / 'testes/apoio/templates-hab-v1'
SPEC = importlib.util.spec_from_file_location('habilitacao_pacote', RAIZ / 'eiac-campo/scripts/habilitacao.py')
H = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(H)
DOCUMENTOS = {
    APR,
    'EMCIA-ROT-02-roteiro-de-habilitacao.md',
    'EMCIA-HAB-01-protocolo-de-habilitacao.md',
    'EMCIA-CAN-01-protocolo-de-canais-externos.md',
    'EMCIA-CAM-01-protocolo-de-campo-por-passo.md',
    'EMCIA-CAT-01-fronteira-de-delegacao.md',
    'EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md',
    'EMCIA-E1-ficha-de-enquadramento.md',
    'EMCIA-E2-diagnostico-e-oportunidade.md',
    'EMCIA-E3-blueprint-da-solucao.md',
    'EMCIA-E4-guia-operacional.md',
    'EMCIA-E5-relatorio-de-piloto.md',
    'EMCIA-FER-01-quadro-de-ferramentas.md',
    'EMCIA-GLO-01-glossario-do-metodo.md',
    'EMCIA-MAN-01-manual-de-aplicacao.md',
    'EMCIA-MET-01-documento-do-metodo.md',
    'EMCIA-ROT-01-roteiro-de-levantamento-de-regras-nao-documentadas.md',
    'EMCIA-TRA-01-procedimentos-transversais-do-metodo.md',
    'EMCIA-TRI-01-instrumento-de-triagem.md',
    *H.TEMPLATES.values(),
}


def exigir(condicao, motivo):
    if not condicao:
        raise ValueError(motivo)


def conferir_tag(canonico, tag, commit):
    try:
        resolvido = subprocess.check_output(['git', 'rev-parse', '--verify', f'refs/tags/{tag}^{{commit}}'],
                                           cwd=canonico, stderr=subprocess.PIPE, text=True).strip()
    except subprocess.CalledProcessError as erro:
        raise ValueError('tag canônica indisponível: ' + tag) from erro
    exigir(resolvido == commit, 'tag não resolve para o commit declarado')


def conferir_templates(canonico, aprovados):
    for filename in H.TEMPLATES.values():
        nome = 'auxiliares/' + filename
        exigir(hashlib.sha256((canonico / nome).read_bytes()).hexdigest() == aprovados.get(nome),
               'template do checkout diverge do APR-01: ' + filename)


def conferir(pacote, canonico):
    exigir(pacote.is_dir(), 'diretório do pacote ausente')
    m = json.loads((pacote / 'manifesto.json').read_text())
    exigir(set(m.get('documentos', {})) == DOCUMENTOS, 'inventário do manifesto divergente')
    exigir({p.name for p in pacote.iterdir()} == DOCUMENTOS | {'manifesto.json'}, 'arquivos fora do manifesto')
    caminhos = m.get('caminhos_canonicos', {})
    exigir(set(caminhos) == DOCUMENTOS, 'caminhos canônicos divergentes')
    origem = re.search(r'tag (metodo-v\d+\.\d+), commit ([0-9a-f]{40})$', m.get('origem_controlada', ''))
    exigir(origem is not None, 'origem deve declarar tag e commit completo')
    tag, commit = origem.groups()
    exigir(m.get('linha_de_base') == tag, 'linha de base diverge da tag')
    aprovados = H.aprovacoes(pacote / APR, tag)
    exigir(set(caminhos.values()) == set(aprovados) | {APR}, 'documento fora da aprovação do APR-01')
    for nome, sha in m['documentos'].items():
        caminho = pathlib.PurePosixPath(caminhos[nome])
        exigir(not caminho.is_absolute() and '..' not in caminho.parts and caminho.name == nome,
               'caminho canônico inválido: ' + nome)
        exigir(not (pacote / nome).is_symlink(), 'symlink no pacote: ' + nome)
        raw = (pacote / nome).read_bytes()
        obtido = hashlib.sha256(raw).hexdigest()
        exigir(obtido == sha, 'hash divergente no manifesto: ' + nome)
        if nome != APR:
            exigir(obtido == aprovados.get(caminhos[nome]), 'hash divergente do APR-01: ' + nome)
    # O pacote funciona offline. Quando há checkout canônico, a tag, seus objetos
    # e os templates usados pela habilitação também precisam conferir.
    if canonico is not None and canonico.is_dir():
        conferir_tag(canonico, tag, commit)
        for nome in DOCUMENTOS:
            original = subprocess.check_output(['git', 'show', f'{commit}:{caminhos[nome]}'],
                                               cwd=canonico, stderr=subprocess.PIPE)
            exigir((pacote / nome).read_bytes() == original, 'bytes diferentes da tag: ' + nome)
        conferir_templates(canonico, aprovados)
    return m


class MetodoEmpacotado(unittest.TestCase):
    def copia(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = pathlib.Path(tmp.name) / 'pacote'
        shutil.copytree(PACOTE, p)
        return p

    def test_01_hash_divergente_do_apr_recusa_mesmo_com_manifesto_coerente(self):
        p = self.copia()
        apr = p / APR
        m = json.loads((p / 'manifesto.json').read_text())
        nome = 'EMCIA-MET-01-documento-do-metodo.md'
        apr.write_text(apr.read_text().replace(m['documentos'][nome], '0' * 64))
        m['documentos'][APR] = hashlib.sha256(apr.read_bytes()).hexdigest()
        (p / 'manifesto.json').write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError, 'hash divergente do APR-01'):
            conferir(p, None)

    def test_02_tag_para_outro_commit_recusa(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp)
            subprocess.run(['git', 'init', '-q', str(p)], check=True)
            subprocess.run(['git', '-c', 'user.name=Pessoa Sintetica', '-c', 'user.email=sintetico@example.invalid',
                            'commit', '--allow-empty', '-qm', 'Controle sintético'], cwd=p, check=True)
            subprocess.run(['git', 'tag', 'metodo-v1.0'], cwd=p, check=True)
            with self.assertRaisesRegex(ValueError, 'tag não resolve'):
                conferir_tag(p, 'metodo-v1.0', '0' * 40)
            with self.assertRaisesRegex(ValueError, 'tag canônica indisponível'):
                conferir_tag(p, 'metodo-v9.9', '0' * 40)

    def test_03_template_do_checkout_com_hash_divergente_recusa(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = pathlib.Path(tmp)
            shutil.copytree(FIXTURES, c / 'auxiliares')
            nome = H.TEMPLATES['HAB-02']
            (c / 'auxiliares' / nome).write_text('Alteração sintética não aprovada')
            with self.assertRaisesRegex(ValueError, 'template do checkout diverge'):
                conferir_templates(c, H.aprovacoes(PACOTE / APR))

    def test_04_hash_divergente_do_manifesto_recusa(self):
        p = self.copia()
        (p / 'EMCIA-MET-01-documento-do-metodo.md').write_text('bytes divergentes')
        with self.assertRaisesRegex(ValueError, 'hash divergente no manifesto'):
            conferir(p, None)

    def test_05_origem_e_linha_de_base_divergentes_recusam(self):
        for campo, valor in [('linha_de_base', 'metodo-v9.9'), ('origem_controlada', 'commit abreviado')]:
            with self.subTest(campo=campo):
                p = self.copia()
                m = json.loads((p / 'manifesto.json').read_text())
                m[campo] = valor
                (p / 'manifesto.json').write_text(json.dumps(m))
                with self.assertRaises(ValueError):
                    conferir(p, None)

    def test_06_fixtures_sao_os_templates_aprovados(self):
        aprovados = H.aprovacoes(PACOTE / APR)
        self.assertEqual((FIXTURES / APR).read_bytes(), (PACOTE / APR).read_bytes())
        for nome in H.TEMPLATES.values():
            self.assertEqual(hashlib.sha256((FIXTURES / nome).read_bytes()).hexdigest(), aprovados['auxiliares/' + nome])
            self.assertEqual((FIXTURES / nome).read_bytes(), (PACOTE / nome).read_bytes())

    def test_07_pacote_offline_confere_com_aprovacao(self):
        self.assertEqual(conferir(PACOTE, None)['linha_de_base'], 'metodo-v1.0')

    def test_08_pacote_confere_com_tag_e_checkout_quando_disponivel(self):
        m = conferir(PACOTE, CANONICO)
        self.assertEqual(m['linha_de_base'], 'metodo-v1.0')
        self.assertFalse([p for p in CONTRASTE.glob('**/EMCIA-*.md') if '.git' not in p.parts])
        print(f"metodo empacotado: {len(DOCUMENTOS)} documentos; tag {m['linha_de_base']}; comparação Git: {CANONICO.is_dir()}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
