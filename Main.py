from	tabulate	import *
from	environment	import *
from    CiscoAPICEM import *


class Main(object):
    """
    Exibe os resultados da interação com o Cisco APIC-EM em um aplicativo Console.
    """

    def __init__(self):
        self.apic_em = CiscoAPICEM()


    """
    Gera e exibe o Service Ticket (API Token), necessário para a realização de todas as transações.
    """
    def gerar_service_ticket(self):
        service_ticket = self.apic_em.gerar_service_ticket()

        print("Geração do Service Ticket \n-------------------------")
        self.__exibir_http_status()
        print("Service Ticket: " + service_ticket + "\n")


    """
    Exibe a lista os dispositivos do tipo host existentes na rede.
    """
    def listar_hosts(self):
        self.gerar_service_ticket()
        lista = self.apic_em.listar_hosts()

        print("Exibição da Lista de Hosts \n--------------------------")
        self.__exibir_http_status()
        print(tabulate(lista, ["No.", "Tipo", "VLAN", "Endereço IP", "Endereço MAC"]))


    """
    Exibe o status HTTP da requisição.
    """
    def __exibir_http_status(self):
        print("Status da Requisição: " + str(self.apic_em.http_status))


Main().listar_hosts()