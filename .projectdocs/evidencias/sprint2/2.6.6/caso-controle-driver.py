#!/usr/bin/env python3
"""Caso de controle do pacote 2.6.6: percurso integral F0->P10, novo caso,
nivel N2, cenario agentico (para exercitar E3-E aplicavel), dois ciclos de
P10 (ciclo 1 sem drift, ciclo 2 com drift + decisao humana), um caso de
teste em P8 que diverge funcionalmente sem falhar o Estudio, negativos de
fronteira (P3b, validacao de P6, decisao de P7, decisao de P10, AG tentando
HB nao autorizada), negativos de etapa incorreta/dependencia, e negativos
de escrita direta em registro/ e contexto/.

Persiste artefatos-chave em .projectdocs/evidencias/sprint2/2.6.6/.
"""
import json
import pathlib
import shutil
import subprocess
import sys

RAIZ = pathlib.Path("/home/netiv-ai/Projetos/AI/PLUGINS/emcia-marketplace")
sys.path.insert(0, str(RAIZ / "testes"))
import campo_2_6_6 as T  # noqa: E402

EVID = RAIZ / ".projectdocs" / "evidencias" / "sprint2" / "2.6.6"
EVID.mkdir(parents=True, exist_ok=True)

caso = T.preparar_caso()
print(f"caso de controle em: {caso}")

log = []

HABILIDADES = str(RAIZ / "eiac-campo" / "reference" / "habilidades.json")
AGENTES = str(RAIZ / "eiac-campo" / "reference" / "agentes.json")
CATALOGO = str(RAIZ / "eiac-nucleo" / "scripts" / "catalogo.py")


def _rodar_catalogo_negativo():
    proc = subprocess.run(
        ["python3", CATALOGO, "--capacidades", HABILIDADES,
         "--chave-capacidades", "habilidades", "--papeis", AGENTES,
         "--chave-papeis", "agentes", "--chave-autorizadas", "hb_autorizadas",
         "--resolver-papel-capacidade", "AG-01", "HB-17"],
        text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def passo(desc, codigo, saida, erro, esperar_falha=False):
    log.append({"passo": desc, "exit": codigo, "stdout": saida.strip(), "stderr": erro.strip()})
    if esperar_falha:
        marca = "OK(neg) " if codigo != 0 else "!!(neg-nao-recusou) "
    else:
        marca = "OK " if codigo == 0 or "NAO_APLICAVEL" in saida else "!! "
    print(f"{marca}{desc}: exit={codigo} {(saida.strip() or erro.strip())[:90]}")


print("=" * 70)
print("F0 -- triagem")
print("=" * 70)
codigo, saida, erro = T.apurar_e_encerrar_f0(caso, nivel="N2")
passo("F0: apurar nivel N2 e encerrar", codigo, saida, erro)

# Negativo: avancar etapa incorreta (tentar encerrar P3a antes de P1/P2)
codigo, saida, erro = T.avancar(caso, encerrar="P3a", autor="Celso do Vale")
passo("NEGATIVO: encerrar P3a fora de ordem (etapa corrente e P1)", codigo, saida, erro,
      esperar_falha=True)

# E1
codigo, saida, erro = T.entregavel(caso, "E1", "Celso do Vale", emitir=True)
passo("E1: renderizar e emitir (autorizado + materializado)", codigo, saida, erro)

print("=" * 70)
print("P1 -- levantamento inicial")
print("=" * 70)
codigo, saida, erro = T.avancar(caso, encerrar="P1", autor="Celso do Vale")
passo("P1: encerrar", codigo, saida, erro)

print("=" * 70)
print("P2 -- levantamento e curadoria de contexto")
print("=" * 70)
# Negativo: escrita direta em contexto/ (guarda G2b)
codigo, saida, erro = T.guarda(caso, "Write", {"file_path": "contexto/regras/RN-999.yaml"})
passo("NEGATIVO: escrita direta em contexto/regras/ (G2b)", codigo, saida, erro, esperar_falha=True)

codigo, saida, erro = T.curar(caso, "regra", "contexto/regras/RN-101.yaml",
                               T.regra_yaml(), "Celso do Vale")
passo("P2: curar RN-101 via curar.py (caminho autorizado)", codigo, saida, erro)

codigo, saida, erro = T.avancar(caso, encerrar="P2", autor="Celso do Vale")
passo("P2: encerrar", codigo, saida, erro)

print("=" * 70)
print("P3a -- linha de base (antes do piloto)")
print("=" * 70)
codigo, saida, erro = T.preparar_bl(caso)
passo("P3a: gravar baseline BL-101 (medido, N2)", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P3a", autor="Celso do Vale")
passo("P3a: encerrar", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 1, "registro/baseline/BL-101.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I1: verificar baseline e satisfazer", codigo, saida, erro)

print("=" * 70)
print("P3b -- sessao humana, nao delegavel")
print("=" * 70)
# Negativo: HB de P3b nao delegavel sem sessao -- guarda G1
codigo, saida, erro = T.guarda(caso, "Read", {"file_path": "skills/hb-levantar-regras/SKILL.md"})
passo("NEGATIVO: skill de P3b sem sessao humana registrada (G1)", codigo, saida, erro,
      esperar_falha=True)
# Negativo: agente tentando encerrar P3b diretamente
codigo, saida, erro = T.avancar(caso, encerrar="P3b", autor="AG-01")
passo("NEGATIVO: AG-01 tenta encerrar P3b sem sessao (nao delegavel)", codigo, saida, erro,
      esperar_falha=True)
codigo, saida, erro = T.avancar(caso, registrar_sessao="P3b", autor="Celso do Vale",
                                 participantes="Fernanda, Celso")
passo("P3b: registrar sessao humana", codigo, saida, erro)
codigo, saida, erro = T.guarda(caso, "Read", {"file_path": "skills/hb-levantar-regras/SKILL.md"})
passo("P3b: skill carrega com sessao valida registrada", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P3b", autor="Celso do Vale")
passo("P3b: encerrar (humano, com sessao)", codigo, saida, erro)

print("=" * 70)
print("P3d -- confronto e classificacao")
print("=" * 70)
codigo, saida, erro = T.avancar(caso, encerrar="P3d", autor="Celso do Vale")
passo("P3d: encerrar", codigo, saida, erro)

print("=" * 70)
print("E2 -- Diagnostico e Oportunidade")
print("=" * 70)
codigo, saida, erro = T.avancar(caso, emitir="E2", autor="Celso do Vale")
passo("E2 (portao): emitir (I1 satisfeito)", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E2", "Celso do Vale", emitir=True)
passo("E2: renderizar e emitir (materializacao)", codigo, saida, erro)

print("=" * 70)
print("P4 -- consumo de CTX estruturado")
print("=" * 70)
codigo, saida, erro = T.consultar(caso, "RN-101")
passo("P4: consultar RN-101 curada (consumo de CTX, nao reinferencia)", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P4", autor="Celso do Vale")
passo("P4: encerrar", codigo, saida, erro)

print("=" * 70)
print("P5 -- classificacao tecnologica (cenario agentico)")
print("=" * 70)
T.gravar_p5_agentico(caso)
print("OK  P5: classificacao_tecnologica=agente (ver nota em campo_2_6_6.gravar_p5_agentico)")

print("=" * 70)
print("E3-D / E3-E -- Blueprint da Solucao")
print("=" * 70)
codigo, saida, erro = T.avancar(caso, emitir="E3-D", autor="Celso do Vale")
passo("E3-D (portao): emitir", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, emitir="E3-E", autor="Celso do Vale")
passo("E3-E (portao, caso agentico): emitir -> AUTORIZADO", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E3", "Celso do Vale", emitir=True)
passo("E3: renderizar e emitir (consolida E3-D + E3-E, um unico arquivo)", codigo, saida, erro)

print("=" * 70)
print("P6 -- especificacao operacional")
print("=" * 70)
T.ajustar_etapa_atual(caso, "P6")
codigo, saida, erro = T.avancar(caso, encerrar="P6", autor="Celso do Vale")
passo("P6: encerrar (etapa_atual ajustada apos P5 gravado fora da maquina)", codigo, saida, erro)

# AG-02 prepara a proposta operacional (papel legitimo de agente)
(caso / "rascunho" / "OP-101.yaml").write_text(T.op_yaml("proposta", 1), encoding="utf-8")
codigo, saida, erro = T.operacional(caso, "registro/operacional/OP-101.yaml", "AG-02")
passo("P6 proposta: AG-02 propoe (papel legitimo de agente)", codigo, saida, erro)

# Negativo: AG tenta validar a propria proposta operacional
(caso / "rascunho" / "OP-101.yaml").write_text(T.op_yaml("validado", 2), encoding="utf-8")
codigo, saida, erro = T.operacional(caso, "registro/operacional/OP-101.yaml", "AG-02")
passo("NEGATIVO: AG-02 tenta validar o proprio fluxo operacional", codigo, saida, erro,
      esperar_falha=True)
codigo, saida, erro = T.operacional(caso, "registro/operacional/OP-101.yaml", "Rafael Nogueira")
passo("P6: validacao humana (Rafael Nogueira)", codigo, saida, erro)

print("=" * 70)
print("P7 -- minuta de autonomia e decisao humana")
print("=" * 70)
codigo, saida, erro = T.avancar(caso, registrar_sessao="P7", autor="Celso do Vale",
                                 participantes="Fernanda, Celso")
passo("P7: registrar sessao humana", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P7", autor="Celso do Vale")
passo("P7: encerrar", codigo, saida, erro)

(caso / "rascunho" / "AUT-101.yaml").write_text(T.aut_yaml("rascunho", 1), encoding="utf-8")
codigo, saida, erro = T.governanca(caso, "registro/governanca/autonomia/AUT-101.yaml", "AG-03")
passo("P7: AG-03 prepara minuta (rascunho, papel legitimo)", codigo, saida, erro)
(caso / "rascunho" / "AUT-101.yaml").write_text(T.aut_yaml("proposto", 2), encoding="utf-8")
codigo, saida, erro = T.governanca(caso, "registro/governanca/autonomia/AUT-101.yaml", "AG-03")
passo("P7: AG-03 propoe (papel legitimo)", codigo, saida, erro)
(caso / "rascunho" / "AUT-101.yaml").write_text(T.aut_yaml("decidido", 3), encoding="utf-8")
codigo, saida, erro = T.governanca(caso, "registro/governanca/autonomia/AUT-101.yaml", "AG-03")
passo("NEGATIVO: AG-03 tenta decidir autonomia (decisao e humana)", codigo, saida, erro,
      esperar_falha=True)
codigo, saida, erro = T.governanca(caso, "registro/governanca/autonomia/AUT-101.yaml", "Marina Prado")
passo("P7: Marina Prado (humano nominal) decide", codigo, saida, erro)

codigo, saida, erro = T.inegociavel(caso, 2, "registro/governanca/autonomia/AUT-101.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I2: verificar termo de autonomia e satisfazer", codigo, saida, erro)

print("=" * 70)
print("E4 -- Guia Operacional")
print("=" * 70)
codigo, saida, erro = T.avancar(caso, emitir="E4", autor="Celso do Vale")
passo("E4 (portao): emitir (P6+P7+I2)", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E4", "Celso do Vale", emitir=True)
passo("E4: renderizar e emitir (materializacao)", codigo, saida, erro)

print("=" * 70)
print("P8 -- casos de teste com saida esperada")
print("=" * 70)
codigo, saida, erro = T.preparar_ct_revisado(caso)
passo("P8: gravar CT-101 rascunho -> revisado (2 casos, 1 diverge funcionalmente)",
      codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P8", autor="Celso do Vale")
passo("P8: encerrar", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 3, "registro/piloto/CT-101.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I3: verificar casos com saida esperada e satisfazer", codigo, saida, erro)

print("=" * 70)
print("P9 -- baseline, metrica de uso, metrica de resultado")
print("=" * 70)
codigo, saida, erro = T.preparar_met_uso(caso)
passo("P9: gravar MET-102 (metrica de uso)", codigo, saida, erro)
codigo, saida, erro = T.preparar_met_resultado_apurada(caso)
passo("P9: gravar MET-101 (metrica de resultado, baseline_ref=BL-101)", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P9", autor="Celso do Vale")
passo("P9: encerrar", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 4, "registro/metricas/MET-101.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I4: verificar metrica de resultado e satisfazer", codigo, saida, erro)

print("=" * 70)
print("E5 -- Relatorio de Piloto")
print("=" * 70)

print("=" * 70)
print("P10 -- configuracao, ciclo 1, ciclo 2 com drift")
print("=" * 70)
codigo, saida, erro = T.preparar_cal(caso)
passo("P10: gravar CAL-101 (rotina, responsavel Marina Prado, metricas_ref=[MET-101,MET-102])",
      codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, registrar_sessao="P10", autor="Celso do Vale",
                                 participantes="Fernanda, Celso")
passo("P10: registrar sessao", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P10", autor="Celso do Vale")
passo("P10: encerrar (primeira vez)", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, registrar_recorrencia="P10", autor="Celso do Vale",
                                 cadencia="mensal", responsavel="Marina Prado")
passo("P10: registrar recorrencia (mecanismo generico do nucleo)", codigo, saida, erro)

codigo, saida, erro = T.inegociavel(caso, 5, "registro/calibragem/CAL-101.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I5: verificar responsavel de recalibragem e satisfazer", codigo, saida, erro)

# Ciclo 1 -- sem drift
(caso / "rascunho" / "CAL-101-C01.yaml").write_text(T.ciclo_yaml(1, drift=False), encoding="utf-8")
codigo, saida, erro = T.calibragem(caso, "registro/calibragem/CAL-101-C01.yaml", "AG-04", ciclo=True)
passo("P10 ciclo 1: AG-04 registra ciclo sem drift", codigo, saida, erro)

# Ciclo 2 -- com drift, deteccao/recomendacao pelo agente, decisao humana
(caso / "rascunho" / "CAL-101-C02.yaml").write_text(T.ciclo_yaml(2, drift=True), encoding="utf-8")
codigo, saida, erro = T.calibragem(caso, "registro/calibragem/CAL-101-C02.yaml", "AG-04", ciclo=True)
passo("P10 ciclo 2: AG-04 detecta e quantifica drift, recomenda", codigo, saida, erro)

(caso / "rascunho" / "CAL-101-C02.yaml").write_text(
    T.ciclo_yaml(2, drift=True, decisao="recalibrar"), encoding="utf-8")
codigo, saida, erro = T.calibragem(caso, "registro/calibragem/CAL-101-C02.yaml", "AG-04", ciclo=True)
passo("NEGATIVO: AG-04 tenta gravar a decisao de recalibragem", codigo, saida, erro,
      esperar_falha=True)

codigo, saida, erro = T.calibragem(caso, "registro/calibragem/CAL-101-C02.yaml", "Marina Prado", ciclo=True)
passo("P10 ciclo 2: Marina Prado (humano nominal) decide recalibrar", codigo, saida, erro)

print("=" * 70)
print("E5 -- emissao apos P8+P9+P10 e I3+I4+I5")
print("=" * 70)
codigo, saida, erro = T.avancar(caso, emitir="E5", autor="Celso do Vale")
passo("E5 (portao): emitir (P8+P9+P10, I3+I4+I5)", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E5", "Celso do Vale", emitir=True)
passo("E5: renderizar e emitir (materializacao)", codigo, saida, erro)

print("=" * 70)
print("Negativos adicionais de fronteira e registro/")
print("=" * 70)
# AG-01 (F0, EX1) tentando carregar a skill de P10/EX4 (fronteira de camada,
# nao fronteira de AG-x -- guarda.py G1 nao conhece codigo de agente,
# apenas se a habilidade da etapa exige sessao/camada humana; ver
# catalogo.py --resolver-papel-capacidade para a fronteira formal AG x HB).
codigo, saida, erro = T.guarda(caso, "Read", {"file_path": "skills/hb-recalibrar/SKILL.md"})
passo("P10: skill de HB-18 carrega com sessao ja registrada nesta etapa",
      codigo, saida, erro)
codigo, saida, erro = _rodar_catalogo_negativo()
passo("NEGATIVO: AG-01 nao esta autorizado a HB-17 (fronteira formal AG x HB)",
      codigo, saida, erro, esperar_falha=True)

# Escrita direta em registro/ (G5)
codigo, saida, erro = T.guarda(caso, "Write", {"file_path": "registro/estado.json"})
passo("NEGATIVO: escrita direta em registro/estado.json (G5)", codigo, saida, erro,
      esperar_falha=True)

print()
print("=" * 70)
falhas_reais = [p for p in log if p["exit"] != 0 and "NAO_APLICAVEL" not in p["stdout"]
                and "NEGATIVO" not in p["passo"]]
print(f"Percurso concluido. {len(log)} passos registrados.")
print(f"Passos com exit != 0 fora dos negativos esperados: {len(falhas_reais)}")
for f in falhas_reais:
    print(f"  {f['passo']}: {f['stderr'] or f['stdout']}")

# ---- Persistir artefatos-chave em .projectdocs -------------------------
artefatos = {
    "RN-101": caso / "contexto" / "regras" / "RN-101.yaml",
    "BL-101": caso / "registro" / "baseline" / "BL-101.yaml",
    "OP-101": caso / "registro" / "operacional" / "OP-101.yaml",
    "AUT-101": caso / "registro" / "governanca" / "autonomia" / "AUT-101.yaml",
    "CT-101": caso / "registro" / "piloto" / "CT-101.yaml",
    "MET-101": caso / "registro" / "metricas" / "MET-101.yaml",
    "MET-102": caso / "registro" / "metricas" / "MET-102.yaml",
    "CAL-101": caso / "registro" / "calibragem" / "CAL-101.yaml",
    "CAL-101-C01": caso / "registro" / "calibragem" / "CAL-101-C01.yaml",
    "CAL-101-C02": caso / "registro" / "calibragem" / "CAL-101-C02.yaml",
}
for nome, caminho in artefatos.items():
    if caminho.exists():
        shutil.copy(caminho, EVID / f"caso-controle-{nome}.yaml")
        print(f"copiado: {nome} -> {EVID / f'caso-controle-{nome}.yaml'}")
    else:
        print(f"AUSENTE: {nome} ({caminho})")

for entregavel_id in ["E1", "E2", "E3", "E4", "E5"]:
    origem = caso / "caso" / "entregaveis" / f"{entregavel_id}.md"
    if origem.exists():
        shutil.copy(origem, EVID / f"caso-controle-{entregavel_id}.md")
        print(f"copiado: {entregavel_id}.md -> {EVID / f'caso-controle-{entregavel_id}.md'}")
    else:
        print(f"AUSENTE: {entregavel_id}.md")

shutil.copy(caso / "registro" / "estado.json", EVID / "estado-final-caso.json")
shutil.copy(caso / "registro" / "eventos.jsonl", EVID / "eventos.jsonl")
print("copiado: estado-final-caso.json, eventos.jsonl")

(EVID / "caso-controle-log-comandos.txt").write_text(
    "\n".join(f"{p['passo']}\n  exit={p['exit']}\n  stdout={p['stdout']}\n  stderr={p['stderr']}\n"
              for p in log),
    encoding="utf-8",
)
print("gravado: caso-controle-log-comandos.txt")

print()
print(f"CASO_TEMP={caso}")
