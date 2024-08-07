import requests
import json

AUTH_URL = "https://identity.wse.zone/v3/auth/tokens?scope=project"
USERNAME = "lfernandes"
PASSWORD = "pYb|-HO[Cq"
DOMAIN_NAME = "sre.binario.cloud"
PROJECT_NAME = "project-estudos"

def get_auth_token():
    data_auth = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": USERNAME,
                    "domain": {
                        "name": DOMAIN_NAME
                    },
                    "password": PASSWORD
                     
                }
            }
        }
    }
}

    response = requests.post(AUTH_URL, data=json.dumps(data_auth), headers={'Content-Type': 'application/json'})
    if response.status_code == 201:
        token = response.headers.get('X-Subject-Token')
        return token
    else:
        print("Erro ao autenticar:", response.status_code, response.text)
        return None

#código para obter informações dos servidores
def get_server_projects_infos(token):
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    url = "https://compute.wse.zone/v2.1/servers/detail"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['servers']
    else:
        print("Erro ao obter instâncias:", response.status_code, response.text)
        return []

# Função para imprimir as informações dos servidores de forma formatada
def print_server_info(servers):
    print("Lista de instâncias:")
    for server in servers:
        print(f"Nome: {server['name']}")
        print(f"ID: {server['id']}")
        print(f"Status: {server['status']}")
        print(f"Flavor: {server['flavor']['id']}")
        try:
            print(f"Imagem: {server['image']['id']}")
        except:
            print("Imagem: Sem imagem")

        print("")

# autenticação
token = get_auth_token()
if token:
    # informações dos servidores
    servers = get_server_projects_infos(token)
    if servers:
        # Imprime na tela de forma de alinhada 
        print_server_info(servers)