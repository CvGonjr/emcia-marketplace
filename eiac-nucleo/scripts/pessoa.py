"""Validação lexical de pessoa conforme regra fornecida pelo playbook."""
import re
import unicodedata


def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto.casefold())
                   if not unicodedata.combining(c))


def validar_regra(regra):
    if (not isinstance(regra, dict) or set(regra) != {'minimo_partes', 'termos_coletivos'}
            or type(regra.get('minimo_partes')) is not int or regra['minimo_partes'] < 1
            or not isinstance(regra.get('termos_coletivos'), list)
            or not regra['termos_coletivos']
            or any(not isinstance(t, str) or not t.strip() for t in regra['termos_coletivos'])):
        return 'pessoa_nomeada: regra invalida ou ausente'


def aceita(nome, regra):
    if validar_regra(regra) or not isinstance(nome, str) or re.search(r'[<>{}]', nome):
        return False
    palavras = re.findall(r'[^\W\d_]+', normalizar(nome), re.UNICODE)
    termos = {normalizar(t) for t in regra['termos_coletivos']}
    # Partes são palavras de nome; pontuação não cria sobrenome.
    return len(palavras) >= regra['minimo_partes'] and not any(p in termos for p in palavras)
