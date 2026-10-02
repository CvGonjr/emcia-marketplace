"""Referência de sessão genérica: camada, id declarado e marcador."""
import json
import unittest
from apoio.hook_real import CasoHook
from apoio.canais import definir


class Referencia(CasoHook):
    def setUp(self):
        super().setUp(); definir(self.caso)
        self.estado['etapa_atual'] = 'P3a'; self.salvar()
        self.pb = self.caso/'registro/playbook.json'

    def registrar(self, *args):
        return self.rodar('avancar.py', '--registrar-sessao', 'P3a', '--autor', 'Celso do Vale', *args)

    def argumentos(self, marcador=None):
        return ['--referencia-externa', 'EVENTO-SINTETICO', '--canal-externo', 'SINTETICO-sessoes-calendario_id',
                '--marcador', marcador or f"[{self.estado['caso']}/P3a]"]

    def recusa(self, *args):
        antes = len(self.eventos()); r = self.registrar(*args)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.eventos()[antes]['evento'], 'TentativaNegada')

    def test_01_obrigatoria_ausente(self):
        pb = json.loads(self.pb.read_text()); pb['exige_referencia_externa_por_camada'] = ['EX3']; self.pb.write_text(json.dumps(pb))
        self.recusa()

    def test_02_marcador_alheio(self):
        self.recusa(*self.argumentos('[outro/P3a]'))

    def test_03_canal_alheio(self):
        args = self.argumentos(); args[3] = 'ALHEIO'; self.recusa(*args)

    def test_04_referencia_incompleta(self):
        self.recusa('--referencia-externa', 'EVENTO-SINTETICO')

    def test_20_opcional_sem_referencia(self):
        r = self.registrar(); self.assertEqual(r.returncode, 0, r.stderr)

    def test_21_referencia_coerente(self):
        r = self.registrar(*self.argumentos()); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.eventos()[-1]['referencia_externa']['id'], 'EVENTO-SINTETICO')


if __name__ == '__main__': unittest.main(verbosity=2)
