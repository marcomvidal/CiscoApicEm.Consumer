# Importação de módulos
import json
import requests
from tabulate import *

# Desativar warnings
requests.packages.urllib3.disable_warnings()

def get_ticket():
    # Composição da requisição
    url = ""

    headers = {
        "content-type": "application/json"
    }

    body = {
        "username": "",
        "password": ""
    }

    # Envio da requisição
    response = requests.post(url, json.dumps(body), headers=headers, verify = False)

    # Inspeção da resposta
    print("Ticket request status:",  response.status_code)

    # Extrai o Service Ticket do body em JSON
    response_body  = response.json()
    service_ticket = response_body["response"]["serviceTicket"]

    # Exibição do Service Ticket solicitado
    print("The Service Ticket number is: ", service_ticket)

    return service_ticket

def print_hosts():
    # Composição da requisição
    url = ""
    
    ticket = get_ticket()
    
    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }

    # Envio da requisição
    response = requests.get(url, headers = headers, verify = False)
    
    # Inspeção da resposta
    print("Status of /host request: ", response.status_code)

    if response.status_code != 200:
        raise Exception("Status code does not equals 200. Response text: " + response.text)

    # Extrai o corpo da requisição em JSON
    response_body = response.json()

    # Exibe e formata a resposta obtida
    host_list = []
    i = 0
    
    for item in response_body["response"]:
        i += 1
        host = [i, item["hostType"], item["hostIp"]]
        host_list.append(host)

    table_header = ["Number", "Type", "IP"]
    print(tabulate(host_list, table_header))

def print_devices():
    # Composição da requisição
    url = ""
    
    ticket = get_ticket()
    
    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }

    # Envio da requisição
    response = requests.get(url, headers = headers, verify = False)
    
    # Inspeção da resposta
    print("Status of /network-device request: ", response.status_code)

    if response.status_code != 200:
        raise Exception("Status code does not equals 200. Response text: " + response.text)

    # Extrai o corpo da requisição em JSON
    response_body = response.json()

    # Exibe e formata a resposta obtida
    host_list = []
    i = 0

    for item in response_body["response"]:
        i += 1
        host = [i,
                item["serialNumber"],
                item["family"],
                item["type"],
                item["hostname"],
                item["macAddress"],
                item["managementIpAddress"]
        ]
        host_list.append(host)

    table_header = ["Serial Number", "Family", "Type", "Hostname", "MAC Address", "Mgmt. IP Address"]
    print (tabulate(host_list, table_header))

def generate_flow_analysis_id():
    # Composição da requisição
    url = ""

    ticket = get_ticket()

    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }

    # Entrada do usuário
    print("\n")
    print("Enter the desired Source IP Address of this Flow Analysis:")
    source_ip = input();

    print("Enter the desired Source IP Address of this Flow Analysis:")
    dest_ip = input();
    print("\n")

    body = {
        "sourceIP": source_ip,
        "destIP": dest_ip
    }

    #10.1.2.1
    #10.1.4.2

    # Envio da requisição
    response = requests.post(url, json.dumps(body), headers=headers, verify = False)

    # Inspeção da resposta
    print("Ticket request status:", response.status_code)

    # Extrai o Service Ticket do body em JSON
    response_body  = response.json()
    flow_analysis_id = response_body["response"]["flowAnalysisId"]

    # Exibição do Service Ticket solicitado
    print("The Flow Analysis ID number is: " +  flow_analysis_id)

    return flow_analysis_id

def retrieve_flow_analysis():
    flow_analysis_id = generate_flow_analysis_id()

    # Composição da requisição
    url = "" + flow_analysis_id
    
    ticket = get_ticket()
    
    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }

    # Envio da requisição
    response = requests.get(url, headers = headers, verify = False)
    
    # Inspeção da resposta
    print("Status of /flow-analysis request: ", response.status_code)

    if response.status_code != 200:
        raise Exception("Status code does not equals 200. Response text: " + response.text)

    # Extrai o corpo da requisição em JSON
    response_body = response.json()

    # Exibição e formatação - Origem e Destino
    print("Source IP: " + response_body["response"]["request"]["sourceIP"])
    print("Destination IP: " + response_body["response"]["request"]["destIP"])
    print("Status: " + response_body["response"]["detailedStatus"]["aclTraceCalculation"])
    print("\n")

    # Exibe e formata a resposta obtida
    network_elements_info = []
    i = 0

    for item in response_body["response"]["networkElementsInfo"]:
        i += 1

        device = [i,
                    item["name"],
                    item["type"],
                    item["ip"],
                    item["role"]
            ]

        if "egressInterface" in item:
            device.append(item["egressInterface"]["physicalInterface"]["name"])
        else:
            device.append("-")

        if "ingressInterface" in item:
            device.append(item["ingressInterface"]["physicalInterface"]["name"])
        else:
            device.append("-")

        if "linkInformationSource" in item:
            device.append(item["linkInformationSource"])
        else:
            device.append("-")
        
        network_elements_info.append(device)

    table_header = ["Name", "Type", "IP Address", "Role", "Egress Interface", "Ingress Interface", "Link Info Source"]
    print(tabulate(network_elements_info, table_header))

