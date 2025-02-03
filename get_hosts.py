import requests
import json
import csv

# Configurações de autenticação e URL da API do Zabbix
zabbix_url = 'http://172.16.32.82/zabbix/api_jsonrpc.php'
zabbix_user = 'srv_zabbix'
zabbix_password = 'ZBXHpt@e3ZRh'

# Método para fazer uma chamada à API do Zabbix
def make_api_request(data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(zabbix_url, data=json.dumps(data), headers=headers)
    return response.json()

# Fazendo login na API do Zabbix e obtendo o token de autenticação
login_data = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'user': zabbix_user,
        'password': zabbix_password
    },
    'id': 1
}

auth_response = make_api_request(login_data)
auth_token = auth_response['result']

# Obtendo a lista de hosts com informações específicas
host_data = {
    'jsonrpc': '2.0',
    'method': 'host.get',
    'params': {
        'output': ['hostid', 'name', 'groups', 'parentTemplates', 'status'],
        'selectGroups': ['name'],
        'selectParentTemplates': ['name'],
        'filter': {}
    },
    'auth': auth_token,
    'id': 2
}

host_response = make_api_request(host_data)

# Processando e salvando as informações dos hosts em um arquivo CSV
if 'result' in host_response:
    with open('hosts_info.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Host ID', 'Host Name', 'Host IP', 'Host Groups', 'Templates', 'Status'])
        
        for host in host_response['result']:
            host_id = host['hostid']
            host_name = host['name']
            host_groups = ', '.join([group['name'] for group in host['groups']])
            templates = ', '.join([template['name'] for template in host['parentTemplates']])
            status = "Ativo" if int(host['status']) == 0 else "Desativado"
            
            # Consulta adicional para obter as interfaces do host
            interface_data = {
                'jsonrpc': '2.0',
                'method': 'hostinterface.get',
                'params': {
                    'output': ['ip'],
                    'hostids': [host_id]
                },
                'auth': auth_token,
                'id': 3
            }
            
            interface_response = make_api_request(interface_data)
            if 'result' in interface_response and len(interface_response['result']) > 0:
                host_ip = "'{}'".format(interface_response['result'][0]['ip'])  # Adicionando aspas simples
            else:
                host_ip = "N/A"
            
            csv_writer.writerow([host_id, host_name, host_ip, host_groups, templates, status])
            
    print("As informações dos hosts foram salvas no arquivo 'hosts_info.csv'.")

else:
    print("Erro ao obter a lista de hosts.")

# Fazendo logout da API do Zabbix (opcional)
logout_data = {
    'jsonrpc': '2.0',
    'method': 'user.logout',
    'params': [],
    'auth': auth_token,
    'id': 4
}

make_api_request(logout_data)

