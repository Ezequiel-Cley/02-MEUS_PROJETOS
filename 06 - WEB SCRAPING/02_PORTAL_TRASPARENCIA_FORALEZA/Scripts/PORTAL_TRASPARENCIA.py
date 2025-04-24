from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge import options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException
from time import sleep

# Realizado a instalação do Gerenciamento do EDGE DRIVER para não ter preocupação com a versão do EDGE instalada atual
service = Service(EdgeChromiumDriverManager().install())

# Configurar as opções do Edge
options = webdriver.EdgeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": r'C:\Users\ezequ\Scripts\01 - Python\02 - MEUS_PROJETOS\06 - WEB SCRAPING\02_PORTAL_TRASPARENCIA_FORALEZA\Datasets',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True})
options.add_argument("--headles")

# Iniciar o navegador Chrome
print("Abrindo Navegador")
navegador = webdriver.Edge(service=service, options=options)

# Entrando no Portal da transparencia de Fortaleza
navegador.get("https://transparencia.fortaleza.ce.gov.br")
# Maximizado o Navegador para melhor gerenciamento
navegador.maximize_window()
sleep(2)

# Clicando na opação de realizar de "Despesas Detalhadas do Portal da Trasparencia"
navegador.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/a[3]").click()
# Atrasar o códgio em 5 segundos para da tempo da pagina carregar
sleep(5)

# Agora, role para baixo usando JavaScript
navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# Clicando no botão de "Consultar" para carregar as informações desejadas
navegador.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/form[2]/div[3]/input").click()
# Atrasar o códgio em 5 segundos para da tempo da pagina carregar
sleep(5)

# Clicando no botão de "Dowload" para realizar Dowload do arquivo para alimentar o dashboard
navegador.find_element(By.ID, "download").click()
sleep(15)

# Finalizando a conexão com site
navegador.quit()