import	requests
import	json
from	tabulate	import *
from	environment	import *


class CiscoAPICEM(object):
    """
    Integração com os serviços oferecidos pela API Northbound do Cisco APIC-EM.
    """
    
    def __init__(self):
        self.credenciais	= CREDENCIAIS
        self.endpoint		= ENDPOINT
        self.http_status    = None
        self.url			= None
        self.service_ticket = None
        
        # Desativar warnings de certificados SSL
        requests.packages.urllib3.disable_warnings()


    """
	Gera o Service Ticket (API Token), necessário para a realização de todas as transações.
	"""
    def gerar_service_ticket(self):
        self.url = self.endpoint + "/ticket"

        resposta = requests.post(
			self.url,
			json.dumps(self.credenciais),
			headers = self.__gerar_cabecalho(),
			verify = False
		)

        self.http_status    = resposta.status_code
        self.service_ticket = resposta.json()["response"]["serviceTicket"]

        return self.service_ticket


    """
    Gera uma lista de dispositivos do tipo host existentes na rede.
    """
    def listar_hosts(self):
        self.gerar_service_ticket()
        self.url = self.endpoint + "/host"
        
        resposta = requests.get(
            self.url,
            headers = self.__gerar_cabecalho(),
            verify = False
        )
        
        self.http_status    = resposta.status_code
        atributos_desejados = ["hostType", "vlanId", "hostIp", "hostMac"]

        return self.__gerar_lista(resposta.json()["response"], atributos_desejados)


    """
    *********** TODO: Refatorar este método ***********
    Lista os dispositivos do tipo ativo existentes na rede.
    """
    def listar_dispositivos(self):
        self.gerar_service_ticket()
        self.url = self.endpoint + "/network-device"
        
        resposta = requests.get(
            self.url,
            headers = self.__gerar_cabecalho(),
            verify = False
        )
        
        print("Exibição da Lista de Dispositivos \n--------------------------")
        self.__exibir_http_status(resposta)
        
        lista = []
        
        for id, item in enumerate(resposta.json()["response"], 1):
            host = [id, 
                item["serialNumber"],
                item["family"],
                item["type"],
                item["hostname"],
                item["macAddress"],
                item["managementIpAddress"]
            ]
            
        lista.append(host)

        print(tabulate(lista, ["ID", "No. Série", "Família", "Tipo", "Hostname", "MAC Address", "IP Gerenciamento"]))
    
    
    """
    Gera o cabeçalho HTTP para realizar requisições HTTP.
    """
    def __gerar_cabecalho(self):
        if self.service_ticket is None:
            return {"Content-Type": "application/json"}

        return {
            "Content-Type": "application/json",
            "X-Auth-Token": self.service_ticket
        }


    """
    Incorpora o status HTTP da requisição ao objeto atual e trata erros, caso ocorram.
    """
    def __definir_http_status(self, resposta):
        self.http_status = resposta.status_code
        
        if resposta.status_code != 200:
            raise Exception("Requisição HTTP falhou. Mensagem: " + resposta.text)
    

    """
    Gera um array com a lista de retorno da API, pronto para ser exibido pela
    biblioteca tabulate.
    """
    def __gerar_lista(self, resposta, lista_colunas):
        lista = []
        
        for id, item in enumerate(resposta, 1):
            host = []
            host.append(id)

            for coluna in lista_colunas:
                host.append(item[coluna])

            lista.append(host)
        
        return lista
