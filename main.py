# Importações

import tempfile
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import base64
from anticaptchaofficial.imagecaptcha import *
from dotenv import load_dotenv

load_dotenv()

captcha_api_key = os.getenv("CHAVE_API")

# Configuração do driver (navegador Firefox)
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Acessando o site e maximizando a janela
driver.get("https://iss.fortaleza.ce.gov.br/")
driver.maximize_window()

# Localizando o input de login utilizando CPF
login_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='login:username']"))
)

# Dando o foco no input e incluindo o CPF
login_element.click()
login_element.send_keys("010.373.013-31")

# Localizando o input de senha
password_element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//input[@id='login:password']"))
)

# Dando o foco no input e incluindo a senha
password_element.click()
password_element.send_keys("Tohgia@05")

image_element = driver.find_element(By.XPATH, "//img[@class='pull-left']")

if image_element:
    image_src = image_element.get_attribute("src")
    image_element.screenshot('captchas/captcha.png')
else:
    print("Imagem não encontrada.")

with open('captchas/captcha.png', 'rb') as image_file:
    # Convertendo a imagem para base64
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Criando um arquivo temporário para salvar a imagem
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
temp_file.write(base64.b64decode(base64_image))

# Fechando o arquivo temporário
temp_file.close()

# Imprimindo o caminho do arquivo temporário
print("Caminho do arquivo temporário:", temp_file.name)

solver = imagecaptcha()
solver.set_verbose(1)
solver.set_key(captcha_api_key)

captcha_text = solver.solve_and_return_solution(temp_file.name)


if captcha_text != 0:
    print("captcha text " + captcha_text)
else:
    print("task finished with error " + solver.error_code)


# Localizando o input do captcha
captcha_element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//input[@id='login:captchaDecor:captchaLogin']"))
)

# Dando o foco no input e incluindo o captcha
captcha_element.click()
captcha_element.send_keys(captcha_text)

# Localizando o botão de submit
botao_submit_element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//input[@id='login:botaoEntrar']"))
)

# Dando o submit no formulário
botao_submit_element.click()

