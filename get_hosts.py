import requests
import json

# Configurações da API do Zabbix
ZABBIX_URL = "http://SEU_ZABBIX/zabbix/api_jsonrpc.php"
ZABBIX_USER = "Usr_zabix"
ZABBIX_PASSWORD = "SUA_SENHA"

# Função para fazer requisições à API do Zabbix
def make_api_request(payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(ZABBIX_URL, data=json.dumps(payload), headers=headers)
    return response.json()

# Autenticação no Zabbix
auth_payload = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": ZABBIX_USER,
        "password": ZABBIX_PASSWORD
    },
    "id": 1,
    "auth": None
}

auth_response = make_api_request(auth_payload)
auth_token = auth_response.get("result")

if not auth_token:
    print("Erro ao autenticar no Zabbix")
    exit(1)

# Obtendo os grupos de usuários
group_payload = {
    "jsonrpc": "2.0",
    "method": "usergroup.get",
    "params": {
        "output": ["name"]
    },
    "auth": auth_token,
    "id": 2
}

group_response = make_api_request(group_payload)

# Extraindo nomes dos grupos de usuários
groups = [group["name"] for group in group_response.get("result", [])]

# Salvando os grupos de usuários em um arquivo
with open("usergroups.txt", "w") as file:
    for group in groups:
        file.write(group + "\n")

print("Usergroups salvos em usergroups.txt")

# Logout da API do Zabbix
logout_payload = {
    "jsonrpc": "2.0",
    "method": "user.logout",
    "params": [],
    "auth": auth_token,
    "id": 3
}
make_api_request(logout_payload)
