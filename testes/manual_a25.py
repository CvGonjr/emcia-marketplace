#!/usr/bin/env python3
"""A25: o manual empacotado descreve o playbook vigente do Estúdio."""

import copy
import json
import pathlib
import re
import unicodedata
import unittest


RAIZ = pathlib.Path(__file__).resolve().parents[1]
CAMPO = RAIZ / 'eiac-campo'
MANUAL = CAMPO / 'reference/metodo/EMCIA-MAN-01-manual-de-aplicacao.md'
PLAYBOOK = CAMPO / 'template-caso/registro/playbook.json'
COLUNAS = ('etapa', 'camadas', 'comando', 'atos', 'produto', 'entregavel')
NIVEIS = ('N1', 'N2', 'N3')


def secao(texto, inicio, fim):
    return texto.split(inicio, 1)[1].split(fim, 1)[0]


def ler_tabela(texto):
    trecho = secao(texto, '### 3.3 O percurso\n', '### 3.4 Atos transversais')
    cabecalho = '| Etapa | Camada N1 · N2 · N3 | Comando do agente | Ato do engenheiro | Produto conferido pelo Estúdio | Entregável |'
    if cabecalho not in trecho:
        raise ValueError('cabeçalho da tabela 3.3 ausente')
    linhas = []
    for linha in trecho.splitlines():
        if not re.match(r'^\| (?:F0|P\d+[a-z]?) \|', linha):
            continue
        partes = [parte.strip() for parte in linha.strip('|').split('|')]
        if len(partes) != len(COLUNAS):
            raise ValueError(f'linha com {len(partes)} colunas: {linha}')
        linhas.append(dict(zip(COLUNAS, partes)))
    return linhas


def atos_transversais(texto):
    trecho = secao(texto, '### 3.4 Atos transversais\n', '### 3.5 Quando o Estúdio recusa')
    return set(re.findall(r'`([^`]+)`', trecho))


def comandos_de_etapa():
    comandos = {}
    for caminho in (CAMPO / 'commands').glob('*.md'):
        texto = caminho.read_text(encoding='utf-8')
        declaracao = re.search(r'^description: Executa a etapa (\S+) do playbook', texto, re.M)
        if declaracao:
            comandos[caminho.stem] = declaracao.group(1)
    return comandos


def sem_acentos(texto):
    return ''.join(letra for letra in unicodedata.normalize('NFD', texto.casefold())
                   if unicodedata.category(letra) != 'Mn')


def conferir(linhas, playbook, comandos, transversais):
    erros = []
    etapas = playbook['etapas']
    ids = [etapa['id'] for etapa in etapas]
    if [linha['etapa'] for linha in linhas] != ids:
        erros.append('etapas diferentes do playbook ou fora de ordem')
    por_id = {etapa['id']: etapa for etapa in etapas}
    atos_declarados = {ato['id'] for ato in playbook['decisoes_humanas']}
    atos_usados = set(transversais)
    comandos_usados = {}

    for linha in linhas:
        nome = linha['etapa']
        etapa = por_id.get(nome)
        if etapa is None:
            erros.append(f'{nome}: etapa não declarada')
            continue

        camadas = ' · '.join(etapa['camada'][nivel] for nivel in NIVEIS)
        if linha['camadas'] != camadas:
            erros.append(f'{nome}: camadas {linha["camadas"]} != {camadas}')

        comando = linha['comando']
        if comando == '—':
            if etapa.get('delegavel') is not False:
                erros.append(f'{nome}: ausência de comando em etapa delegável')
        else:
            achado = re.fullmatch(r'`/eiac-campo:([\w-]+)`', comando)
            if achado is None:
                erros.append(f'{nome}: formato de comando inválido: {comando}')
            else:
                identificador = achado.group(1)
                comandos_usados[identificador] = nome
                if comandos.get(identificador) != nome:
                    erros.append(f'{nome}: comando {identificador} ausente ou declara outra etapa')

        for ato in re.findall(r'`([^`]+)`', linha['atos']):
            atos_usados.add(ato)
            if ato not in atos_declarados:
                erros.append(f'{nome}: ato {ato} não declarado')

        produtos = etapa.get('produtos_encerramento', [])
        if not produtos:
            if linha['produto'] != '—':
                erros.append(f'{nome}: produto deveria ser —')
        elif len(produtos) != 1 or sem_acentos(linha['produto']) != sem_acentos(produtos[0]['descricao']):
            erros.append(f'{nome}: produto diferente da descrição do playbook')

        entregaveis = {item['id'].split('-')[0] for item in playbook['entregaveis']
                       if nome in item['portao']}
        if linha['entregavel'] not in entregaveis:
            erros.append(f'{nome}: entregável fora do portão: {linha["entregavel"]}')

    for identificador, nome in comandos.items():
        if comandos_usados.get(identificador) != nome:
            erros.append(f'{nome}: comando de etapa {identificador} ausente da tabela')

    for ato in sorted(atos_declarados - atos_usados - {'preparar-controle'}):
        erros.append(f'ato humano {ato} ausente das seções 3.3 e 3.4')
    return erros


class ManualA25(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texto = MANUAL.read_text(encoding='utf-8')
        cls.linhas = ler_tabela(cls.texto)
        cls.playbook = json.loads(PLAYBOOK.read_text(encoding='utf-8'))
        cls.comandos = comandos_de_etapa()
        cls.transversais = atos_transversais(cls.texto)

    def conferir(self, linhas):
        return conferir(linhas, self.playbook, self.comandos, self.transversais)

    def test_01_manual_confere_com_playbook(self):
        self.assertEqual(self.conferir(self.linhas), [])
        self.assertEqual(len(self.linhas), len(self.playbook['etapas']))

    def test_02_etapa_removida_e_detectada(self):
        linhas = copy.deepcopy(self.linhas)
        linhas.pop(0)
        self.assertTrue(any('etapas diferentes' in erro for erro in self.conferir(linhas)))

    def test_03_camada_trocada_e_detectada(self):
        linhas = copy.deepcopy(self.linhas)
        linhas[0]['camadas'] = 'EX2 · EX1 · EX1'
        self.assertTrue(any('camadas' in erro for erro in self.conferir(linhas)))

    def test_04_ato_inexistente_e_detectado(self):
        linhas = copy.deepcopy(self.linhas)
        linhas[0]['atos'] = '`ato-inexistente`'
        self.assertTrue(any('ato ato-inexistente não declarado' in erro
                            for erro in self.conferir(linhas)))

    def test_05_comando_inexistente_e_detectado(self):
        linhas = copy.deepcopy(self.linhas)
        linhas[0]['comando'] = '`/eiac-campo:comando-inexistente`'
        self.assertTrue(any('comando comando-inexistente ausente' in erro
                            for erro in self.conferir(linhas)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
