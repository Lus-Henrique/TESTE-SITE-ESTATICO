import schedule
import subprocess
import time
import os

def rodar_token_api():
    print("Rodando TokenAPI.py")
    subprocess.Popen(["python", os.path.join("Token Loggi", "TokenAPI.py")])

def rodar_pull_bd_loggi():
    print("Rodando PullBDLoggi.py")
    proc = subprocess.Popen(["python", os.path.join("Puxar Dados da Loggi", "PullBDLoggi.py")])
    proc.wait()  # Espera PullBDLoggi.py terminar
    print("Rodando Organizar.BD.py")
    subprocess.Popen(["python", os.path.join("Puxar Dados da Loggi", "Organizar.BD.py")])

# Agendamentos
schedule.every(30).minutes.do(rodar_token_api)
schedule.every(4).minutes.do(rodar_pull_bd_loggi)

print("Iniciador rodando. Pressione Ctrl+C para sair.")
while True:
    schedule.run_pending()
    time.sleep(1)
    