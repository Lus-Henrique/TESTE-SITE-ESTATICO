from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Roda o Chrome escondido

print("Iniciando o navegador...")
caminho_driver = r"D:\Projeto inicial\chromedriver-win32\chromedriver-win32\chromedriver.exe"
print("Navegador iniciado.")

driver = webdriver.Chrome(service=Service(caminho_driver), options=chrome_options)

#Criar o arquivo que vai conter o token da API

tokens_dir = os.path.join(r"D:\Projeto inicial\Token Loggi", "tokensAPI")
os.makedirs(tokens_dir, exist_ok=True)


#Fazer o loggin no ARCO

try:
    print("Abrindo página de login...")
    driver.get("https://arco.loggi.com")
    time.sleep(5)

    # Login
    email_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="emailInput"]'))
    )
    email_input.send_keys("luisherinque55@gmail.com")
    senha_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="passwordInput"]'))
    )
    senha_input.send_keys("LuisH0067!")
    senha_input.send_keys(Keys.RETURN)

    print("Aguardando redirecionamento após login...")
    WebDriverWait(driver, 30).until(EC.url_contains("/IP3"))
    time.sleep(2)

    # FECHA O POPUP DE NOTIFICAÇÕES, SE APARECER
    try:
        btn_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Agora não')]"))
        )
        btn_popup.click()
        print("Popup de notificações fechado.")
    except Exception:
        print("Popup de notificações não apareceu.")
except Exception as e:
    print(f"Ocorreu um erro durante o login: {e}")

    # FECHA O POPUP DE NOTIFICAÇÕES, SE APARECER NOVAMENTE
    try:
            btn_popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Agora não')]"))
            )
            btn_popup.click()
            print("Popup de notificações fechado.")
    except Exception:
         pass
    
# Captura o idToken do localStorage (pega a chave que termina com .idToken)

id_token_key = None
for key in driver.execute_script("return Object.keys(window.localStorage);"):
    if key.endswith(".idToken"):
        id_token_key = key
        break

if id_token_key:
    id_token = driver.execute_script(f"return window.localStorage.getItem('{id_token_key}');")
    print(f"ID Token: {id_token[:30]}...")  # Mostra só o início do token
    # Salva o token na pasta 'tokens'
    filename = os.path.join(tokens_dir, "token_id.txt")
    with open(filename, "w") as f:
        f.write(id_token if id_token else "")
else:
    print("Não foi possível encontrar o idToken.")    
    