# coding: utf-8
from    tabulate    import *
from    environment import *
from    CiscoAPICEM import *
import  re


class Main(object):
    """
    Interface em modo texto de interação com a API. Pode ser substituída 
    por qualquer outro tipo de interação com o usuário utilizando a classe
    `CiscoAPIEM`, presente neste projeto.
    """

    def __init__(self):
        self.apic_em = CiscoAPICEM()


    """
    Exibe um menu para que o usuário opte pela funcionalidade desejada.
    :return: void
    """
    def menu(self):
        while True:
            print("\nInteração com o Cisco APIC-EM via API" +
                "\n-------------------------------------\n" +
                "Escolha a ação desejada: \n\n" +
                "1. Gerar Service Ticket \n" +
                "2. Listar Hosts \n" +
                "3. Listar Dispositivos \n" +
                "4. Analisar tráfego \n" +
                "5. Sair \n"
            )

            try:
                opcao = int(input("Sua opção: "))
            except Exception:
                raise OpcaoInvalida()

            if opcao == 1:
                self.gerar_service_ticket()
            elif opcao == 2:
                self.listar_hosts()
            elif opcao == 3:
                self.listar_dispositivos()
            elif opcao == 4:
                self.analisar_trafego()
            else:
                break


    """
    Gera e exibe o Service Ticket (API Token), necessário para a
    realização de todas as transações.
    :return: void
    """
    def gerar_service_ticket(self):
        service_ticket = self.apic_em.gerar_service_ticket()

        print("\nGeração do Service Ticket" +
            "\n-------------------------")

        self.__exibir_http_status()
        print("Service Ticket: " + service_ticket + "\n")
        self.__continuar()


    """
    Exibe a lista os dispositivos do tipo host existentes na rede.
    :return: void
    """
    def listar_hosts(self):
        lista = self.apic_em.listar_hosts()

        print("\nExibição da Lista de Hosts" + 
            "\n--------------------------")
        
        self.__exibir_http_status()

        print(tabulate(lista, [
            "No.", "Tipo", "VLAN", "Endereço IP", "Endereço MAC"]
        ))

        self.__continuar()


    """
    Exibe a lista os dispositivos ativos de rede existentes.
    :return: void
    """
    def listar_dispositivos(self):
        lista = self.apic_em.listar_dispositivos()

        print("\nExibição da Lista de Ativos de Rede" +
            "\n-----------------------------------")

        self.__exibir_http_status()

        print(tabulate(lista, [
            "No.", "No. de Série", "Família", "Tipo",
            "Hostname", "MAC Address", "IP de Gerenciamento"
        ]))

        self.__continuar()


    """
    Realiza todos os procedimentos necessários para analisar o tráfego
    entre dois dispositivos da rede.
    :return: void
    """
    def analisar_trafego(self):
        print("\nAnálise de Tráfego Entre Dispositivos de Rede" +
            "\n---------------------------------------------")

        origem = self.__entrada_endereco_ip(
            "Digite o Endereço IP de origem desta análise: (Ex.: 10.1.2.1)"
        )

        destino = self.__entrada_endereco_ip(
            "Digite o Endereço IP de destino desta análise: (Ex.: 10.1.4.2)"
        )

        lista = self.apic_em.analisar_trafego(origem, destino)

        self.__exibir_http_status()

        print(tabulate(lista, [
            "No.", "Hostname", "Tipo", "Endereço IP", "Função", "Situação",
            "Interface de Saída", "Interface de Entrada"
        ]))

        self.__continuar()

    
    """
    Exibe o status HTTP da requisição.
    :return: void
    """
    def __exibir_http_status(self):
        print("Status da Requisição: " + 
            str(self.apic_em.http_status) + "\n")

    
    """
    Estabelece um meio de validação de endereços IP inseridos
    pelo usuário.
    :param   frase:  Frase que será exibida para auxiliar o usuário
    na entrada de dados
    :return: str
    """
    def __entrada_endereco_ip(self, frase):
        print(frase)

        while True:
            entrada = input()
            
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", entrada):
                break

            print("Formato incorreto. Digite um Endereço IP válido.")

        print("\n")

        return entrada

    
    """
    Aguarda pela entrada através do teclado pelo usuário para continuar a
    execução.
    """
    def __continuar(self):
        print("\nPressione qualquer tecla para continuar.")
        input()


Main().menu()