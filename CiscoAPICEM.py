import	requests
import	json
from	tabulate	import *
from	environment	import *
from    exceptions  import *


class CiscoAPICEM(object):
    """
    Integração com os serviços oferecidos pela API Northbound do Cisco APIC-EM.
    Interage com a API. Atente para o correto preenchimento de `environment.py`
    para assegurar seu correto funcionamento.
    """

    def __init__(self):
        self.credenciais    = CREDENCIAIS
        self.endpoint       = ENDPOINT
        self.http_status    = None
        self.url            = None
        self.service_ticket = None
        self.certificado    = CERTIFICADO_DIGITAL

        if  self.credenciais["username"] is None or \
            self.credenciais["username"] == "":
            raise CredencialFaltante("Username")

        if  self.credenciais["password"] is None or \
            self.credenciais["password"] == "":
            raise CredencialFaltante("Password")
        
        # Desativar warnings de certificados SSL
        if self.certificado is False:
            requests.packages.urllib3.disable_warnings()


    """
    Gera o Service Ticket (API Token), necessário para a realização de todas as transações.
    :return: str
    """
    def gerar_service_ticket(self):
        self.url = self.endpoint + "/ticket"

        resposta = requests.post(
            self.url,
            json.dumps(self.credenciais),
            headers = self.__gerar_cabecalho(),
            verify  = self.certificado
        )

        self.__definir_http_status(resposta)

        service_ticket = resposta.json()["response"]["serviceTicket"]

        return service_ticket


    """
    Gera uma lista de dispositivos do tipo host existentes na rede.
    :return: dict
    """
    def listar_hosts(self):
        service_ticket = self.gerar_service_ticket()
        self.url = self.endpoint + "/host"
        
        resposta = requests.get(
            self.url,
            headers = self.__gerar_cabecalho(service_ticket),
            verify  = self.certificado
        )
        
        self.__definir_http_status(resposta)
        atributos_desejados = ["hostType", "vlanId", "hostIp", "hostMac"]

        return self.__gerar_lista(resposta.json()["response"], atributos_desejados)


    """
    Lista os dispositivos do tipo ativo existentes na rede.
    :return: dict
    """
    def listar_dispositivos(self):
        service_ticket = self.gerar_service_ticket()
        self.url = self.endpoint + "/network-device"
        
        resposta = requests.get(
            self.url,
            headers = self.__gerar_cabecalho(service_ticket),
            verify  = self.certificado
        )

        self.__definir_http_status(resposta)

        atributos_desejados = [
            "serialNumber", "family", "type",
            "hostname", "macAddress", "managementIpAddress"
        ]

        return self.__gerar_lista(resposta.json()["response"], atributos_desejados)

    
    """
    A partir de uma requisição de análise de tráfego que gerou um ID previamente, mostra
    os dispositivos finais e intermediários envolvidos na comunicação.
    :param   endereco_origem:  Endereço IP de onde parte a análise, no seguinte formato: 0.0.0.0
    :param   endereco_destino: Endereço IP de onde se finaliza a análise, no seguinte formato: 0.0.0.0
    :return: dict
    """
    def analisar_trafego(self, endereco_origem, endereco_destino):
        service_ticket = self.gerar_service_ticket()

        flow_analysis_id = self.__gerar_flow_analysis_id(
            service_ticket,
            endereco_origem,
            endereco_destino
        )

        self.url = self.endpoint + "/flow-analysis/" + flow_analysis_id

        resposta = requests.get(
            self.url,
            headers = self.__gerar_cabecalho(service_ticket),
            verify  = self.certificado
        )

        self.__definir_http_status(resposta)

        atributos_desejados = [
            "name", "type", "ip", "role", "linkInformationSource",
            "outInterface", "inInterface"
        ]

        resposta_curada = resposta.json()["response"]["networkElementsInfo"]
        
        for item in resposta_curada:
            if "egressInterface" in item:
                item["outInterface"] = item["egressInterface"]["physicalInterface"]["name"]
            
            if "ingressInterface" in item:
                item["inInterface"]  = item["ingressInterface"]["physicalInterface"]["name"]

        return self.__gerar_lista(resposta_curada, atributos_desejados)


    """
    Inicia análise de fluxo e retorna um ID para conferência posterior de resultados.
    :param   service_ticket: Gerado pela API e obtido através do método gerar_service_ticket()
    :param   endereco_origem: Endereço IP de onde parte a análise, no seguinte formato: 0.0.0.0
    :param   endereco_destino: Endereço IP de onde parte a análise, no seguinte formato: 0.0.0.0
    :return: str
    """
    def __gerar_flow_analysis_id(self, service_ticket, endereco_origem, endereco_destino):
        self.url = self.endpoint + "/flow-analysis"

        corpo = {
            "sourceIP": endereco_origem,
            "destIP":   endereco_destino
        }

        resposta = requests.post(
            self.url,
            json.dumps(corpo),
            headers = self.__gerar_cabecalho(service_ticket),
            verify  = self.certificado
        )

        self.__definir_http_status(resposta)

        return resposta.json()["response"]["flowAnalysisId"]
    
    
    """
    Gera o cabeçalho HTTP para realizar requisições HTTP.
    :param   service_ticket: Obtido através do método gerar_service_ticket(). Opcional.
    :return: dict
    """
    def __gerar_cabecalho(self, service_ticket = None):
        if service_ticket is None:
            return {"Content-Type": "application/json"}

        return {
            "Content-Type": "application/json",
            "X-Auth-Token": service_ticket
        }


    """
    Incorpora o status HTTP da requisição ao objeto atual e trata erros, caso ocorram.
    :param   resposta: Obtida após uma chamada com a API através da biblioteca `requests`
    :return: void
    """
    def __definir_http_status(self, resposta):
        self.http_status = resposta.status_code
        
        if resposta.status_code not in [200, 201, 202, 206]:
            raise FalhaRequisicaoHttp(resposta)
    

    """
    Gera um array com a lista de retorno da API, pronto para ser exibido pela
    biblioteca tabulate.
    :param   resposta: Obtida após uma chamada com a API através da biblioteca `requests`
    :param   lista_colunas: Colunas da resposta que se deseja obter
    :return: dict
    """
    def __gerar_lista(self, resposta, lista_colunas):
        lista = []
        
        for id, item in enumerate(resposta, 1):
            host = []
            host.append(id)


            for coluna in lista_colunas:

                if coluna in item:
                    host.append(item[coluna])
                else:
                    host.append("-")

            lista.append(host)
        
        return lista

