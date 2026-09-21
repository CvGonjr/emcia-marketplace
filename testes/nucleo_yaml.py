#!/usr/bin/env python3
"""Determinismo de carregar_yaml/ler_yaml entre os dois caminhos de leitura.

`estrutura.carregar_yaml` (eiac-nucleo) e `quadro.ler_yaml` (eiac-nucleo)
usam PyYAML quando o pacote esta instalado e um parser proprio quando nao
esta. Achado 2026-09: com PyYAML instalado, `yaml.safe_load` converte uma
data bare ('2026-09-19') em `datetime.date`; sem PyYAML, o parser proprio
devolve `str` para o mesmo texto. Codigo consumidor (`operacional.py`,
`piloto.py`) chama `.strip()` direto no campo de data, o que quebra com
`datetime.date` -- P6 nunca chega a `validado`, P7 recusa em cascata
(campo_2_6_2.py aborta, campo_2_6_5.py acumula falhas), tudo dependendo
apenas de PyYAML estar ou nao no ambiente.

Este teste forca os dois caminhos (com PyYAML real e com PyYAML
indisponivel, via monkeypatch do modulo) sobre a mesma fixture e exige
resultado identico, campo a campo -- inclusive o tipo do campo de data.
Falha aqui e regressao do defeito, nao de funcionalidade.
"""
import datetime
import importlib.util
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]

falhas = 0
total = 0


def ok(msg):
    global total
    total += 1
    print(f"  ok    {msg}")


def falha(msg):
    global total, falhas
    total += 1
    falhas += 1
    print(f"  FALHA {msg}")


def _carregar_modulo(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FIXTURE = (
    "id: OP-001\n"
    "estado: validado\n"
    "validado_por: Rafael Nogueira\n"
    "data_validacao: 2026-09-19\n"
    "versao: 2\n"
)


def carregar_com_pyyaml_real(caminho_script, funcao):
    try:
        import yaml  # noqa: F401
    except ImportError:
        return None, "PyYAML nao instalado neste ambiente de teste"
    mod = _carregar_modulo(caminho_script, f"{caminho_script.stem}_com_yaml")
    return getattr(mod, funcao)(FIXTURE), None


def carregar_sem_pyyaml(caminho_script, funcao):
    mod = _carregar_modulo(caminho_script, f"{caminho_script.stem}_sem_yaml")
    mod.yaml = None  # simula ambiente sem PyYAML, sem exigir desinstalar nada
    return getattr(mod, funcao)(FIXTURE)


def checar(nome_pacote, caminho_script, funcao):
    com_dict, motivo_pulado = carregar_com_pyyaml_real(caminho_script, funcao)
    sem_dict = carregar_sem_pyyaml(caminho_script, funcao)

    if motivo_pulado:
        ok(f"{nome_pacote} caminho sem-PyYAML executa e devolve dict "
           f"({motivo_pulado}, comparacao com-PyYAML pulada)")
        if not isinstance(sem_dict.get("data_validacao"), str):
            falha(f"{nome_pacote} data_validacao sem PyYAML deveria ser str, "
                  f"veio {type(sem_dict.get('data_validacao'))}")
        else:
            ok(f"{nome_pacote} data_validacao sem PyYAML e str")
        return

    if com_dict != sem_dict:
        falha(f"{nome_pacote} com-PyYAML e sem-PyYAML divergem: "
              f"{com_dict!r} != {sem_dict!r}")
    else:
        ok(f"{nome_pacote} com-PyYAML e sem-PyYAML produzem o mesmo dict")

    tipo_com = type(com_dict.get("data_validacao"))
    tipo_sem = type(sem_dict.get("data_validacao"))
    if tipo_com is datetime.date:
        falha(f"{nome_pacote} com PyYAML devolveu datetime.date para "
              f"data_validacao -- deveria ser str, mesmo contrato do "
              f"parser proprio (regressao do achado 2026-09)")
    elif tipo_com is not str:
        falha(f"{nome_pacote} com PyYAML devolveu tipo inesperado "
              f"{tipo_com} para data_validacao")
    else:
        ok(f"{nome_pacote} data_validacao com PyYAML e str (nao "
           f"datetime.date)")

    if tipo_com != tipo_sem:
        falha(f"{nome_pacote} tipo de data_validacao difere entre "
              f"caminhos: com-PyYAML={tipo_com}, sem-PyYAML={tipo_sem}")
    else:
        ok(f"{nome_pacote} tipo de data_validacao identico nos dois "
           f"caminhos ({tipo_com.__name__})")


def checar_checar_validacao_nao_quebra():
    """Reproduz literalmente o ponto de quebra original: operacional.py
    chamando .strip() no campo de data vindo de carregar_yaml."""
    scripts_campo = RAIZ / "eiac-campo" / "scripts"
    sys.path.insert(0, str(RAIZ / "eiac-nucleo" / "scripts"))
    sys.path.insert(0, str(scripts_campo))
    import estrutura as X

    candidato = X.carregar_yaml(FIXTURE)
    import operacional as OP
    try:
        erros = OP.checar_validacao(candidato)
    except AttributeError as e:
        falha(f"checar_validacao quebrou com carregar_yaml real: {e}")
        return
    if erros:
        falha(f"checar_validacao recusou candidato valido: {erros}")
    else:
        ok("checar_validacao aceita data_validacao vinda de carregar_yaml "
           "sem quebrar (controle positivo do achado 2026-09)")


print("== determinismo de leitura YAML entre ambientes com/sem PyYAML")

checar("estrutura.carregar_yaml",
       RAIZ / "eiac-nucleo" / "scripts" / "estrutura.py", "carregar_yaml")
checar("quadro.ler_yaml",
       RAIZ / "eiac-nucleo" / "scripts" / "quadro.py", "ler_yaml")
checar_checar_validacao_nao_quebra()

print(f"\n{total} verificacoes de determinismo YAML, {falhas} falhas")
sys.exit(1 if falhas else 0)
