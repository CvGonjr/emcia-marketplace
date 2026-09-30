"""A24: E5 e recorrência consultam a mesma rotina vigente do caso."""
import json
import pathlib
import subprocess
import sys

from apoio.hook_real import CasoHook, RAIZ

ENTREGAVEIS = RAIZ / 'eiac-campo/scripts/entregaveis.py'


class E5RotinaA24(CasoHook):
    def setUp(self):
        super().setUp()
        self.estado.update(
            etapa_atual='P10',
            cumprimentos={et: {'cumprido': True} for et in ('P8', 'P9', 'P10')},
            inegociaveis={str(n): {'satisfeito': True, 'autor': 'Celso do Vale',
                                   'evidencia': 'registro/fonte.yaml'} for n in (3, 4, 5)})
        self.salvar()
        self.fonte('registro/piloto/CT-001.yaml', estado='revisado',
                   modo='assistido', duracao='uma semana')
        self.fonte('registro/metricas/MET-001.yaml', estado='apurada',
                   tipo='resultado', metrica='Tempo', linha_base='10',
                   resultado_apurado='8', resultado_apurado_procedencia='D')

    def fonte(self, nome, **dados):
        caminho = self.caso / nome
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text('\n'.join(
            f'{chave}: {json.dumps(valor, ensure_ascii=False)}'
            for chave, valor in dados.items()) + '\n', encoding='utf-8')
        return caminho

    def rotina(self, nome, responsavel, versao):
        return self.fonte('registro/calibragem/' + nome,
                          responsavel=responsavel, versao=versao,
                          cadencia='mensal', data_primeira_revisao='2026-10-01')

    def e5(self, *args):
        return subprocess.run([sys.executable, str(ENTREGAVEIS), '--renderizar', 'E5',
                               '--autor', 'Celso do Vale', *args], cwd=self.caso,
                              text=True, capture_output=True)

    def recorrencia(self, responsavel):
        return self.rodar('avancar.py', '--registrar-recorrencia', 'P10',
                          '--autor', 'Celso do Vale', '--cadencia', 'mensal',
                          '--responsavel', responsavel)

    def test_01_empate_ambiguidade_bloqueia_emissao(self):
        self.rotina('CAL-001.yaml', 'Marina Prado', 10)
        self.rotina('CAL-999.yaml', 'Celso do Vale', 10)
        r = self.e5('--emitir')
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('ambigua', r.stderr)
        self.assertFalse((self.caso / 'caso/entregaveis/E5.md').exists())
        self.assertNotIn('E5', json.loads((self.caso / 'registro/estado.json').read_text())
                         .get('entregaveis_emitidos', {}))

    def test_02_versao_invalida_nao_e_escape(self):
        self.rotina('CAL-001.yaml', 'Marina Prado', 10)
        self.rotina('CAL-999.yaml', 'Celso do Vale', 'invalida')
        r = self.e5('--emitir')
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('inteiro positivo', r.stderr)
        self.assertFalse((self.caso / 'caso/entregaveis/E5.md').exists())

    def test_03_v10_precede_v2_mesmo_com_nome_anterior(self):
        self.rotina('CAL-001.yaml', 'Marina Prado', 10)
        self.rotina('CAL-999.yaml', 'Celso do Vale', 2)
        r = self.e5('--emitir')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.eventos()[-1]['evento'], 'EntregavelEmitido')
        texto = (self.caso / 'caso/entregaveis/E5.md').read_text()
        self.assertIn('Responsável pela calibragem** | Marina Prado', texto)
        self.assertNotIn('Responsável pela calibragem** | Celso do Vale', texto)

    def test_04_e5_e_recorrencia_apontam_mesma_pessoa(self):
        self.rotina('CAL-001.yaml', 'Marina Prado', 10)
        self.rotina('CAL-999.yaml', 'Celso do Vale', 2)
        r = self.recorrencia('Marina Prado')
        self.assertEqual(r.returncode, 0, r.stderr)
        fonte = json.loads((self.caso / 'registro/estado.json').read_text()) \
            ['cumprimentos']['P10']['estado_recorrente']['fonte_responsavel']
        self.assertEqual(fonte['arquivo'], 'registro/calibragem/CAL-001.yaml')
        self.assertEqual(self.e5().returncode, 0)
        self.assertIn('Responsável pela calibragem** | ' + fonte['valor'],
                      (self.caso / 'caso/entregaveis/E5.md').read_text())

    def test_05_ciclos_ficam_fora_da_selecao(self):
        self.rotina('CAL-001.yaml', 'Marina Prado', 10)
        self.rotina('CAL-001-C01.yaml', 'Celso do Vale', 99)
        r = self.e5()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Responsável pela calibragem** | Marina Prado',
                      (self.caso / 'caso/entregaveis/E5.md').read_text())


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
