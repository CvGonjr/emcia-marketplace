#!/usr/bin/env python3
"""A19: caminhos reais e aliases não escapam das zonas protegidas."""
import json, unittest
from apoio.hook_real import CasoHook, RAIZ

class Caminhos(CasoHook):
    pass

def verificar(area, forma, ferramenta):
    def teste(self):
        relativo = area+'/arquivo.txt'
        alvo = self.caso/relativo
        alvo.parent.mkdir(parents=True, exist_ok=True)
        if forma == 'relativo': caminho = relativo
        elif forma == 'absoluto': caminho = str(alvo)
        elif forma == 'pontos': caminho = 'rascunho/../'+relativo
        elif forma == 'link':
            link=self.base/'atalho'
            link.symlink_to(alvo.parent, target_is_directory=True)
            caminho=str(link/alvo.name)
        elif forma == 'subdiretorio': caminho = '../'+relativo
        entrada = {'file_path': caminho} if ferramenta != 'Bash' else {'command': 'printf x > '+caminho}
        self.negado(ferramenta, entrada, cwd=self.caso/'rascunho' if forma=='subdiretorio' else None)
    return teste
for area in ('registro','caso','contexto','fontes','contexto/fontes'):
    for forma in ('relativo','absoluto','pontos','link','subdiretorio'):
        for ferramenta in ('Edit','Bash'):
            setattr(Caminhos, 'test_'+area.replace('/','_')+'_'+forma+'_'+ferramenta, verificar(area,forma,ferramenta))

class Controles(CasoHook):
    def test_01_registro_link_para_fora_continua_protegido(self):
        externo=self.base/'externo.txt'; externo.write_text('controle')
        link=self.caso/'registro/alias.txt'; link.symlink_to(externo)
        self.negado('Write', {'file_path':str(link)})

    def test_02_rascunho_absoluto(self):
        self.assertEqual(self.hook('Write', {'file_path':str(self.caso/'rascunho/x.md')}).returncode,0)

    def test_03_leitura_registro(self):
        self.assertEqual(self.hook('Read', {'file_path':str(self.caso/'registro/estado.json')}).returncode,0)

    def test_04_arquivo_externo_sem_alias(self):
        self.assertEqual(self.hook('Write', {'file_path':str(self.base/'registro/x.txt')}).returncode,0)

    def test_05_cd_antes_de_escrever(self):
        self.negado('Bash', {'command':'cd '+str(self.caso/'registro')+' && printf x > estado.json'})

    def test_06_cp_absoluto(self):
        self.negado('Bash', {'command':'cp rascunho/x '+str(self.caso/'registro/estado.json')})

    def test_07_mv_absoluto(self):
        self.negado('Bash', {'command':'mv '+str(self.caso/'registro/estado.json')+' /tmp/retirado.json'})

    def test_08_tee_link(self):
        link=self.base/'log'; link.symlink_to(self.caso/'registro',target_is_directory=True)
        self.negado('Bash', {'command':'printf x | tee '+str(link/'estado.json')})

    def test_09_cwd_fora_raiz_projeto_preservada(self):
        self.negado('Edit', {'file_path':str(self.caso/'registro/estado.json')}, cwd=self.base)
    def test_10_subshell_nao_muda_diretorio_do_shell_pai(self):
        self.negado('Bash', {'command':'(cd rascunho); printf x > registro/estado.json'})

    def test_11_pipeline_nao_muda_diretorio_do_shell_pai(self):
        self.negado('Bash', {'command':'cd rascunho | cat; printf x > registro/estado.json'})
    def test_12_edit_da_sessao_real(self):
        entrada=json.loads((RAIZ/'testes/apoio/entradas_sessao_37.json').read_text())['Edit']
        entrada['file_path']=str(self.caso/'registro/estado.json')
        self.assertIn('F0',entrada['new_string'])
        self.negado('Edit',entrada)

if __name__ == '__main__': unittest.main(verbosity=2)
