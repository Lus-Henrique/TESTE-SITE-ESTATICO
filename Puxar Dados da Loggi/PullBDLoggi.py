import requests
import os
import datetime

# Caminho do token único
token_file = r"D:\Projeto inicial\Token Loggi\tokensAPI\token_id.txt"
if not os.path.exists(token_file):
    print(f"Arquivo de token não encontrado: {token_file}")
    exit(1)

with open(token_file, "r") as f:
    token = f.read().strip()

# Cria a pasta única para todos os relatórios
pasta = os.path.join(r"D:\Projeto inicial\Puxar Dados da Loggi", "BD_Loggi")
os.makedirs(pasta, exist_ok=True)

# Lista de bases
bases = [
    {
        "sigla": "IP3",
        "url": "https://leve.loggi.com/api/v2/last_mile/leve-mg-ipatinga-3-porto-gui_xxxx:xxxx/packages/report",
        "distribution_center_id": "xxxx",
        "last_mile_company_id": "leve-mg-ipatinga-3-porto-gui_xxxx",
        "routing_code": "IP3"
    },
    {
        "sigla": "ST2",
        "url": "https://leve.loggi.com/api/v2/last_mile/leve-mg-sete-lagoas-2-porto-gui_xxxx:xxxx/packages/report",
        "distribution_center_id": "xxxx",
        "last_mile_company_id": "leve-mg-sete-lagoas-2-porto-gui_xxxx",
        "routing_code": "ST2"
    },
    {
        "sigla": "GV3",
        "url": "https://leve.loggi.com/api/v2/last_mile/leve-mg-governador-valadares-3-porto-gu_1080e:1382/packages/report",
        "distribution_center_id": "1382",
        "last_mile_company_id": "leve-mg-governador-valadares-3-porto-gu_1080e",
        "routing_code": "GV3"
    },
    {
        "sigla": "RDN",
        "url": "https://leve.loggi.com/api/v2/last_mile/leve-mg-ribeirao-das-neves-3-porto-gui_xxxx:xxxx/packages/report",
        "distribution_center_id": "xxxx",
        "last_mile_company_id": "leve-mg-ribeirao-das-neves-3-porto-gui_xxxx",
        "routing_code": "RDN"
    },
    {
        "sigla": "CT4",
        "url": "https://leve.loggi.com/api/v2/last_mile/leve-mg-contagem-4-porto-gui_xxxx:xxxx/packages/report",
        "distribution_center_id": "xxxx",
        "last_mile_company_id": "leve-mg-contagem-4-porto-gui_xxxx",
        "routing_code": "CT4"
    },
    {
        "sigla": "GVS",
        "url": "https://leve.loggi.com/api/v2/last_mile/leve-mg-governador-valadares-3-porto-gui_9aaf:6664/packages/report",
        "distribution_center_id": "6664",
        "last_mile_company_id": "leve-mg-governador-valadares-3-porto-gui_9aaf",
        "routing_code": "GVS"
    }
]

for base in bases:
    params = {
        "timezone": "-0300",
        "view": "rua",
        "token": token,
        "distribution_center_id": base["distribution_center_id"],
        "last_mile_company_id": base["last_mile_company_id"],
        "routing_code": base["routing_code"],
        "companyType": "LEVE"
    }

    print(f"Baixando para base: {base['sigla']}")

    arquivo = os.path.join(pasta, f"{base['sigla']}.Rua.csv")
    if os.path.exists(arquivo):
        print(f"Atenção: O arquivo {arquivo} já existe e será substituído.")

    response = requests.get(base["url"], params=params)
    if response.status_code == 200:
        with open(arquivo, "wb") as f:
            f.write(response.content)
        print(f"Arquivo salvo em: {arquivo}")
    else:
        print(f"Erro ao baixar o arquivo da base {base['sigla']}: {response.status_code}")
        print(f"Resposta: {response.text}")




# Pasta para salvar os relatórios
output_dir = os.path.join(r"D:\Projeto inicial\Puxar Dados da Loggi", "BD_Loggi")
os.makedirs(output_dir, exist_ok=True)

# Bases para puxar os dados (v1)
bases = [
    {
        "sigla": "IP3",
        "url": "https://leve.loggi.com/api/v1/last_mile/leve-ipatinga-3-betania_11a50:1294/packages/report",
        "distribution_center_id": "1294",
        "last_mile_company_id": "leve-ipatinga-3-betania_11a50",
        "routing_code": "IP3"
    },
    {
        "sigla": "ST2",
        "url": "https://leve.loggi.com/api/v1/last_mile/leve-mg-sete-lagoas-2-canaa_11ec6:1198/packages/report",
        "distribution_center_id": "1198",
        "last_mile_company_id": "leve-mg-sete-lagoas-2-canaa_11ec6",
        "routing_code": "ST2"
    },
    {
        "sigla": "GV3",
        "url": "https://leve.loggi.com/api/v1/last_mile/leve-mg-governador-valadares-3-porto-gu_1080e:1382/packages/report",
        "distribution_center_id": "1382",
        "last_mile_company_id": "leve-mg-governador-valadares-3-porto-gu_1080e",
        "routing_code": "GV3"
    },
    {
        "sigla": "RDN",
        "url": "https://leve.loggi.com/api/v1/last_mile/leve-mg-ribeirao-das-neves-santa-martin_1022c:867/packages/report",
        "distribution_center_id": "867",
        "last_mile_company_id": "leve-mg-ribeirao-das-neves-santa-martin_1022c",
        "routing_code": "RDN"
    },
    {
        "sigla": "CT4",
        "url": "https://leve.loggi.com/api/v1/last_mile/leve-mg-contagem-4-bandeirantes_bab6:5493/packages/report",
        "distribution_center_id": "5493",
        "last_mile_company_id": "leve-mg-contagem-4-bandeirantes_bab6",
        "routing_code": "CT4"
    },
    {
        "sigla": "GVS",
        "url": "https://leve.loggi.com/api/v1/last_mile/leve-mg-governador-valadares-3-porto-gui_9aaf:6664/packages/report",
        "distribution_center_id": "6664",
        "last_mile_company_id": "leve-mg-governador-valadares-3-porto-gui_9aaf",
        "routing_code": "GVS"
    }
]

params_base = {
    "timezone": "-0300",
    "view": "base"
}

for base in bases:
    params = params_base.copy()
    params["distribution_center_id"] = base["distribution_center_id"]
    params["last_mile_company_id"] = base["last_mile_company_id"]
    params["routing_code"] = base["routing_code"]

    headers = {
        "Authorization": f"Bearer {token}"
    }


    filename = os.path.join(output_dir, f"{base['sigla']}.Base.csv")

    print(f"Baixando base {base['sigla']}...")
    response = requests.get(base["url"], params=params, headers=headers)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Salvo como {filename}")
    else:
        print(f"Erro ao baixar {base['sigla']}: {response.status_code}")
        print(f"Resposta: {response.text}")
print("Download das bases concluído.")
       