"""
Repositório das exceções passíveis de serem geradas pela biblioteca.
"""


class CredencialFaltante(Exception):
    """
    Reporta ausência do preenchimento de credenciais.
    """
    def __init__(self, credencial):
        self.message = "Preencha a credencial '" + credencial + "' adequadamente no arquivo environment.py"

    def __str__(self):
        return self.message


class FalhaRequisicaoHttp(Exception):
    """
    Reporta falhas na comunicação com a API a nível de protocolo.
    """
    def __init__(self, resposta):
        self.message = "Comunicação com a API falhou" + \
            ". Erro: " + resposta.json()["response"]["errorCode"] + \
            ". Providência(s): " + resposta.json()["response"]["message"]

    def __str__(self):
        return self.message
