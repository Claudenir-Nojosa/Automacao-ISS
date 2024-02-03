# Importações

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do driver (navegador Firefox)
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Acessando o site e maximizando a janela
driver.get("https://iss.fortaleza.ce.gov.br/")
driver.maximize_window()

# Localizando o input de login utilizando CPF
login_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "login:username"))
)

# Dando o foco no input e incluindo o CPF
login_element.click()
login_element.send_keys("010.373.013-31")

# Localizando o input de senha
password_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "login:password"))
)

# Dando o foco no input e incluindo a senha
password_element.click()
password_element.send_keys("Tohgia@05")



