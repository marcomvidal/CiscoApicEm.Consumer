# Cisco APIC-EM - Interação com a API

## Descrição
Biblioteca que realiza chamadas com a API REST do Cisco APIC-EM. Gera Service Tickets, lista hosts e dispositivos, analisa tráfego e exibe seus resultados. Inclui um Front-End em Console para fácil apreciação e análise das consultas disponíveis.

## Tecnicalidades da API
Cisco APIC-EM é a implementação de Rede Definida por Software (SDN) da Cisco Systems. Consiste em:
- Um servidor que concentra sua funcionalidade;
- API Southbound, que envia comandos do servidor aos ativos de rede (Routers, Switches, Firewalls, etc) através do protocolo OpenFlow ou SSH / Telnet / SNMP;
- API Northbound, que disponibiliza uma API REST como interface para atender a comandos de consulta e configuração. Esta biblioteca interage com este ponto.
É documentada em Swagger e pode devolver resultados nos formatos JSON e XML.

## Tecnicalidades da biblioteca
Desenvolvida em Python 3, traz retornos em tipos de baixíssimo acoplamento, como `dictionaries` e `strings`. Há forte separação entre o Front-End e a interação com a API, permitindo que seja facilmente incorporada a projetos desktop ou web - como Django ou Flask - sem que sejam necessárias adaptações no código fonte.

## Composição
- `CiscoAPICEM.py`: Contém a interação com a API em si;
- `environment.py`: Define endpoint, credenciais e certificado digital que serão usados nas chamadas da API;
- `exceptions.py`: Exceções personalizadas que enriquecem a solução de problemas de execução, caso ocorram;
- `Main.py`: Front-end em Console. É cliente das funcionalidade de `CiscoAPIC-EM.py`. Pode ser removido caso o objetivo aplicar a biblioteca em aplicações de outra natureza;
- `requirements.txt`: Outras bibliotecas necessárias.

## Requisitos
- Python 3.5 ou superior;
- Bibliotecas `requests` e `json`: Necessárias para que a comunicação com a API funcione. `requests` deve ser instalada através do `pip`, enquanto `json` é nativa;
- Biblioteca `tabulate`: Necessária apenas se for utilizado o Front-End em Console. Formata os dados de um dicionário para exibição em tabelas.

## Instalação
### 1. Crie um `virtualenv`
Caso esta biblioteca seja instalada independentemente, crie um `virtualenv` exclusivo para ela. Se for incorporada a um projeto Django ou Flask, por exemplo, utilize o mesmo ambiente do restante da aplicação.

### 2. Acomode a biblioteca
Crie um diretório dedicado à biblioteca, que pode estar isolado ou dentro dos diretórios de outro projeto, dependendo de como for desejado implantá-la.

### 3. Instale as dependências
Todas as dependências necessárias estão contidas em `requirements.txt`. Basta direcionar que o `pip` as resolva:
```
pip install -r requirements.txt
```

### 4. Preencha as constantes
Abra `environment.py`, observe e avalie a necessidade de preencher:
- `CREDENCIAIS`: `username` e `password`, para que o servidor não retorne status HTTP 403 e impeça a execução das chamadas;
- `ENDPOINT`, por padrão, aponta para o ambiente de sandbox. Altere-o caso esteja em ambiente de produção;
- `CERTIFICADO_DIGITAL` é dispensável caso esteja utilizando ambiente de sandbox, mas pode ser necessário em produção.

### 5. Referencie a biblioteca (opcional)
Para o caso de estar integrando esta biblioteca a um projeto maior, é necessário referenciá-la no arquivo que desejar obter seus resultados:
```
from CiscoAPICEM import *
```

## Utilização
### A. Utilize o Front-End em Console
Basta chamar `Main.py` através do `python` em seu shell preferido. Será exibido um menu interativo pelo qual você poderá realizar chamadas de modo direto e simples.

### B. Integrando com uma Aplicação Existente
Observe a implementação existente em `Main.py` e adapte-a às suas necessidades. Observe que todas as requisições dependem de um Service Ticket que já tem sua obtenção implementada em cada uma das chamadas de `CiscoAPICEM.py`.
