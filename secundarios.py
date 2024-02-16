# Importações

import tempfile
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import base64
import pyautogui
import calendar
from anticaptchaofficial.imagecaptcha import *
from dotenv import load_dotenv
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta

load_dotenv()

data_atual = datetime.now()
primeiro_dia_mes_anterior = datetime(data_atual.year, data_atual.month, 1) - timedelta(days=1)
primeiro_dia_mes_atual = datetime(data_atual.year, data_atual.month, 1)
ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
ultimo_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=calendar.monthrange(ultimo_dia_mes_anterior.year, ultimo_dia_mes_anterior.month)[1])

data_formatada = primeiro_dia_mes_anterior.strftime('%d%m%Y')
data_final_formatada = ultimo_dia_mes_anterior.strftime('%d%m%Y')

mes_anterior = data_atual - timedelta(days=30)
meses = {
    1: 'jan',
    2: 'fev',
    3: 'mar',
    4: 'abr',
    5: 'mai',
    6: 'jun',
    7: 'jul',
    8: 'ago',
    9: 'set',
    10: 'out',
    11: 'nov',
    12: 'dez'
}

mes_anterior_nome = meses[mes_anterior.month]

captcha_api_key = os.getenv("CHAVE_API")

contribuintes = {
    'CONTRIBUINTE_1': {'login': os.getenv('CONTRIBUINTE_1_LOGIN'), 'password': os.getenv('CONTRIBUINTE_1_PASSWORD')},
    'CONTRIBUINTE_2': {'login': os.getenv('CONTRIBUINTE_2_LOGIN'), 'password': os.getenv('CONTRIBUINTE_2_PASSWORD')},
    'CONTRIBUINTE_3': {'login': os.getenv('CONTRIBUINTE_3_LOGIN'), 'password': os.getenv('CONTRIBUINTE_3_PASSWORD')},
    'CONTRIBUINTE_4': {'login': os.getenv('CONTRIBUINTE_4_LOGIN'), 'password': os.getenv('CONTRIBUINTE_4_PASSWORD')},
    'CONTRIBUINTE_5': {'login': os.getenv('CONTRIBUINTE_5_LOGIN'), 'password': os.getenv('CONTRIBUINTE_5_PASSWORD')},
    'CONTRIBUINTE_6': {'login': os.getenv('CONTRIBUINTE_6_LOGIN'), 'password': os.getenv('CONTRIBUINTE_6_PASSWORD')},
    'CONTRIBUINTE_7': {'login': os.getenv('CONTRIBUINTE_7_LOGIN'), 'password': os.getenv('CONTRIBUINTE_7_PASSWORD')},
    'CONTRIBUINTE_8': {'login': os.getenv('CONTRIBUINTE_8_LOGIN'), 'password': os.getenv('CONTRIBUINTE_8_PASSWORD')},
}

# Configuração do driver (navegador Firefox)
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Clicar no elemento, função geral
def clicar_elemento_se_existir(driver, xpath):
    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        elemento.click()
        return True
    except:
        return False
# Fazer login
def fazer_login(login,password):
    # Acessando o site e maximizando a janela
    driver.get("https://iss.fortaleza.ce.gov.br/")
    driver.maximize_window()
    # Localizando o input de login utilizando CPF
    login_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='login:username']"))
    )

    # Dando o foco no input e incluindo o CPF
    login_element.click()
    login_element.send_keys(login)

    # Localizando o input de senha
    password_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='login:password']"))
    )

    # Dando o foco no input e incluindo a senha
    password_element.click()
    password_element.send_keys(password)

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
# Acessar contribuinte
def acessar_contribuinte_por_linha(numero_linha):
    xpath_contribuinte = f"//a[@id='alteraInscricaoForm:empresaDataTable:{numero_linha}:linkNome']"
    contribuinte = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_contribuinte))
    )
    contribuinte.click()
# Clicar no botão de escrituração
def clicar_botao_escrituracao():
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "alteraInscricaoForm:confirmaAlteraInscricaoAtualModalDiv"))
    )
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "alteraInscricaoModalDiv"))
    )
    botao_escrituracao = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='nav navbar-nav']/li[6]"))
    ) 
    botao_escrituracao.click()
# Clicar no botão de manter escrituração
def clicar_botao_manter_escrituracao():
    botao_manter_escrituracao = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='nav navbar-nav']/li[6]/ul/li[1]"))
    )
    botao_manter_escrituracao.click()
# Mudar o mês da escrituração
def mudar_mes_apuracao():
    botao_mes_inicial = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='rich-calendar-tool-btn']"))
    )
    botao_mes_inicial.click()
    mes_fechamento = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f"//div[text()='{mes_anterior_nome}']"))
    )
    mes_fechamento.click()
    botao_ok = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='manterEscrituracaoForm:dataInicialDateEditorButtonOk']"))
    )
    botao_ok.click()
    botao_consultar = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='manterEscrituracaoForm:btnConsultar']"))
    )
    botao_consultar.click()
# Mudar de contribuinte
def mudar_contribuinte(numero_linha):
    mudar_contribuintes = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div//a[@title='Alterar Inscrição Atual']"))
    )
    mudar_contribuintes.click()  
    xpath_contribuinte = f"//a[@id='alteraInscricaoForm:empresaDataTable:{numero_linha}:linkNome']"
    
    contribuinte = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_contribuinte))
    )
    contribuinte.click() 
    aceitar_troca = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='alteraInscricaoForm:botaoOk']"))
    )
    driver.execute_script("arguments[0].click();", aceitar_troca)
    print("Aceitei troca")

    clicar_botao_escrituracao()
    clicar_botao_manter_escrituracao()
    mudar_mes_apuracao()
# Mudar de página
def mudar_pagina(numero_linha,numero_pagina):
    print(numero_linha, 'dentro da função mudar_pagina, anter de mudar a pagina de fato')
    mudar_contribuintes = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div//a[@title='Alterar Inscrição Atual']"))
    )
    mudar_contribuintes.click()  

    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div[2]/div/div[2]/span/table/tfoot/tr/td/div/table/tbody/tr/td[{numero_pagina}]"))
    ).click()

    xpath_contribuinte = f"//a[@id='alteraInscricaoForm:empresaDataTable:{numero_linha}:linkNome']"
    
    contribuinte = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_contribuinte))
    )
    contribuinte.click() 
    aceitar_troca = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='alteraInscricaoForm:botaoOk']"))
    )
    driver.execute_script("arguments[0].click();", aceitar_troca)
    print("Aceitei troca")

    clicar_botao_escrituracao()
    clicar_botao_manter_escrituracao()
    mudar_mes_apuracao()
# Entrar na apuração
def entrar_apuracao():
    for numero_linha in range(48):

        # Localizar o elemento tbody com a classe rich-table-row
        situacao_escrituracao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//td[@id='manterEscrituracaoForm:dataTable:1:situacao']"))
        )

        # Localizar o segundo td dentro do tbody
        elemento_td = situacao_escrituracao.find_element(By.XPATH, f".//span[@id='manterEscrituracaoForm:dataTable:1:textoSituacao']")

        # Obter o texto do elemento td
        texto_td = elemento_td.text.strip().lower()
        print(texto_td)

        # Tomar ação com base no texto
        if "aberta - normal" in texto_td:
            # Relocar o elemento antes de clicar
            entrar_escrituracao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@id='manterEscrituracaoForm:dataTable:1:linkEscriturar']"))
            )
            driver.execute_script("arguments[0].click();", entrar_escrituracao)
        elif 19 > numero_linha > 8 and texto_td != "aberta - normal":
            
            print("Mudar para pagina 2")
            print(numero_linha, 'dentro da função entrar_apuracao, antes de mudar a página de fato')
            mudar_pagina(numero_linha + 1, 5)

        elif 29 > numero_linha > 18 and texto_td != "aberta - normal":
        
            print("Mudar para pagina 3")
            print(numero_linha, 'dentro da função entrar_apuracao, antes de mudar a página de fato')
            mudar_pagina(numero_linha + 1, 6)
            
        else:
            print("Deu ruim. Mudando contribuinte.")
            mudar_contribuinte(numero_linha + 1)
# Aceitar serviços pendentes
def aceitar_servicos_pendentes():
    time.sleep(2)

    # Aguardar até que o modal de progresso esteja invisível
    WebDriverWait(driver, 50).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[@id='mpProgressoDiv']"))
    )

    # Aguardar até que o modal esteja invisível
    WebDriverWait(driver, 50).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[@id='modalAlertaCarregamentoDadosDiv']"))
    )

    # Clicar no botão de serviços pendentes usando JavaScript
    botao_servicos_pendentes = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//td[@id='aba_servicos_pendentes_lbl']"))
    )
    
    # Executar o clique usando JavaScript
    driver.execute_script("arguments[0].click();", botao_servicos_pendentes)
    try:
        # Aguarda até que o elemento obscuro desapareça
        WebDriverWait(driver, 50).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@id='modalAlertaCarregamentoDadosDiv']"))
        )

        # Tenta localizar e clicar no botão original após o elemento obscuro desaparecer
        botao_aceitar_todos = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='servicos_pendentes_form:idLinkaceitarDocTomados']"))
        ) #servicos_pendentes_form:idLinkaceitarDocPrestados
        botao_aceitar_todos.click()
        botao_confirmar_aceitar_todos = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='aceite_todos_doc_tomados_modal_panel_form:btnSim']"))
        )
        botao_confirmar_aceitar_todos.click()   
        time.sleep(4)     

    except:
        print("Botão 'aceitarDocTomados' não encontrado. Verificando 'aceitarDocPrestados'.")

        try:
            # Tenta localizar e clicar no botão DocPrestados após o elemento obscuro desaparecer
            botao_aceitar_doc_prestados = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@id='servicos_pendentes_form:idLinkaceitarDocPrestados']"))
            )
            # Executar o clique usando JavaScript
            driver.execute_script("arguments[0].click();", botao_aceitar_doc_prestados)

            botao_confirmar_aceitar_todos = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='aceite_todos_doc_prestados_modal_panel_form:btnSim']"))
            )
            botao_confirmar_aceitar_todos.click()  
            time.sleep(4)

        except:
            # Trata a exceção se o botão DocPrestados também não estiver presente
            print("Nenhum dos botões 'aceitarDocTomados' ou 'aceitarDocPrestados' encontrado.")
# Encerrar escrituração
def encerrar_escrituracao():

    time.sleep(3)
    botao_encerramento = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//td[@id='abaEncerramento_lbl']"))
    )
    botao_encerramento.click()  

    # Aguarda até que o novo elemento obscuro desapareça
    WebDriverWait(driver, 50).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[@id='mpProgressoDiv']"))
    )
    WebDriverWait(driver, 50).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[@id='modalAlertaCarregamentoDadosDiv']"))
    )

    # Execute um clique usando JavaScript para contornar possíveis problemas de sobreposição
    botao_encerrar = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='abaEncerramentoForm:btnEncerrarEscrituracao']"))
    )
    driver.execute_script("arguments[0].click();", botao_encerrar)
    botao_confirmar_encerramento = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='formEncerramento:btnSim']"))
    )
    botao_confirmar_encerramento.click()  
    botao_certificado_encerramento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Certificado de Encerramento da Escrituração']"))
    )
    botao_certificado_encerramento.click()    
# Pegar o certificado de encerramento
def certificado_encerramento():
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write('teste bot')
    time.sleep(1)
    pyautogui.press('enter')

    elemento_xpath = "/html/body/div[1]/div[2]/div[3]/div[2]/table[4]/tbody/tr[2]/td[6]"
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, elemento_xpath))
    )

    # Obter o texto do elemento
    texto_elemento = elemento.text.strip()

    # Tomar ação com base no valor do texto
    if texto_elemento == '0,00':
        print("O valor é igual a '0,00'. Não há ISS retido")
        
    else:
        print(f"Há ISS Retido no valor de: {texto_elemento}, indo baixar o DAM...")

        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div/div/div[2]/ul/li[7]/a'))
        ).click()
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="formMenuTopo:menuRecolhimento:j_id93"]'))
        ).click()

        elemento_select = driver.find_element_by_id("comboImposto")
        seletor = Select(elemento_select)
        seletor.select_by_visible_text("ISS retido - Substituição Tributária")
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@id="btnConsultar"]'))
        ).click()
# Pegar serviços tomados e prestados
def pegar_xml_servicos():
    quantidade_servicos_tomados = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/table[3]/tfoot/tr/th[2]'))
    )
    if quantidade_servicos_tomados > 0:
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div/div/div[2]/ul/li[5]/a'))
        ).click()
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formMenuTopo:menuNfse:j_id58"]'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:opTipoRelatorio:1"]'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:abaPorCompetenciaTomador_tab_lbl"]'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[3]/div/table[1]/tbody/tr[2]/td/table/tbody/tr/td/div[1]/div/div[1]/table/tbody/tr[1]/td/label/div'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, f"//table[@id='consultarnfseForm:competenciaTomadorDateEditorLayout']//td[text()='{mes_anterior_nome}']"))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[3]/div/table[1]/tbody/tr[2]/td/table/tbody/tr/td/div[1]/div/div[1]/table[2]/tbody/tr/td/div/table/tbody/tr[7]/td[1]/div/span"))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='consultarnfseForm:j_id311']"))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='consultarnfseForm:j_id318']"))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/div/div[1]/input[3]"))
        ).click

        # Ver se tem uma segunda pagina de XML
        xpath_segunda_pagina = '/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/table/tfoot/tr/td/div/table/tbody/tr/td[5]'

        if clicar_elemento_se_existir(driver, xpath_segunda_pagina):
            WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/table/tfoot/tr/td/div/table/tbody/tr/td[5]"))
            ).click
            WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='consultarnfseForm:j_id318']"))
            ).click
            WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/div/div[1]/input[3]"))
            ).click      
            pass  
    quantidade_servicos_prestados = WebDriverWait(10,driver).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/table[2]/tfoot/tr/th[2]'))
    )     
    if quantidade_servicos_prestados > 0:
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div/div/div[2]/ul/li[5]/a'))
        ).click()
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formMenuTopo:menuNfse:j_id58"]'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:opTipoRelatorio:0"]'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:periodo_prestador_tab_lbl"]'))
        ).click
        periodo_inicial = WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:dataInicialInputDate"]'))
        )
        periodo_inicial.click
        periodo_inicial.send_keys(data_formatada)
        periodo_final = WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:dataFinalInputDate"]'))
        )
        periodo_final.click()
        periodo_final.send_keys(data_final_formatada)
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:j_id231"]'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="consultarnfseForm:j_id318"]'))
        ).click
        WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/div/div[1]/input[3]'))
        ).click
        
        # Ver se tem uma segunda pagina de XML
        xpath_segunda_pagina = '/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/table/tfoot/tr/td/div/table/tbody/tr/td[5]'

        if clicar_elemento_se_existir(driver, xpath_segunda_pagina):
            WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/table/tfoot/tr/td/div/table/tbody/tr/td[5]"))
            ).click
            WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='consultarnfseForm:j_id318']"))
            ).click
            WebDriverWait(10,driver).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[4]/div/div/div[1]/input[3]"))
            ).click      
            pass  
   

for contribuinte, credenciais in contribuintes.items():
    fazer_login(credenciais['login'], credenciais['password'])
    acessar_contribuinte_por_linha(0)
    clicar_botao_escrituracao()
    clicar_botao_manter_escrituracao()
    mudar_mes_apuracao()
    entrar_apuracao()
    aceitar_servicos_pendentes()
    encerrar_escrituracao()
    certificado_encerramento()
    pegar_xml_servicos()




