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

		print("Geração do Service Ticket \n-------------------------")
		self.__exibir_http_status(resposta)

		self.service_ticket = resposta.json()["response"]["serviceTicket"]
		print("Service Ticket: " + self.service_ticket + "\n")


	"""
	Lista os hosts existentes na rede.
	"""
	def listar_hosts(self):
		self.gerar_service_ticket()
		self.url = self.endpoint + "/host"

		resposta = requests.get(
			self.url,
			headers = self.__gerar_cabecalho(),
			verify = False
		)

		print("Exibição da Lista de Hosts \n--------------------------")
		self.__exibir_http_status(resposta)

		lista_hosts = []

		for id, item in enumerate(resposta.json()["response"]):
			host = [id, item["hostType"], item["hostIp"]]
			lista_hosts.append(host)

		print(tabulate(lista_hosts, ["Número", "Tipo", "Endereço IP"]))


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
	Exibe o status HTTP da requisição e trata erros, caso ocorram.
	"""
	def __exibir_http_status(self, resposta):
		print("HTTP Status:   ", resposta.status_code)

		if resposta.status_code != 200:
			raise Exception("Requisição HTTP falhou. Mensagem: " + resposta.text)


CiscoAPICEM().listar_hosts()
