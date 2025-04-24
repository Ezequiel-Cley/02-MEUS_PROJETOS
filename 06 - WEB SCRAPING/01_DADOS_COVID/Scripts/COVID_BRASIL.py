# IMPORTANDO TODAS AS BIBLIOTECAS NECESSARIAS PARA MANIPULAÇÃO DOS DADOS WEB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge import options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException
# IMPORTANDO TODAS AS BIBLIOTECAS PARA CONTROLA O TEMPO DE EXECUÇÃO DO CÓDIGO
from time import sleep

# Realizado a instalação do Gerenciamento do EDGE DRIVER para não ter preocupação com a versão do EDGE instalada atual
service = Service(EdgeChromiumDriverManager().install())

# Configurar as opções do Edge
options = webdriver.EdgeOptions()
options.add_experimental_option("prefs", {
    # Manipulando o local que vai ser armazenado o local de dowloads
    "download.default_directory": r'C:\Users\ezequ\Scripts\01 - Python\02 - MEUS_PROJETOS\06 - WEB SCRAPING\01_DADOS_COVID\Datasets',
    # Desativar a opção de confirmação de Dowload para realizar o download sem solicitar confirmação
    "download.prompt_for_download": False,
    # Desativado atualizações para evitar erros de versões divergentes
    "download.directory_upgrade": True,
    # Ativando proteção de navegação para evitar pup's indesejados
    "safebrowsing.enabled": True})
    # Realizado leitura de forma visual para executar de forma invisivel trocar para "--headless" 
options.add_argument("--headless")

# Iniciar o navegador Chrome
print("Abrindo Navegador")
navegador = webdriver.Edge(service=service, options=options)

# Entrando no site da GOV com os dados do Covid para extrair dados 
navegador.get("https://infoms.saude.gov.br/extensions/covid-19_html/covid-19_html.html")
# Maximizado o Navegador para melhor gerenciamento
navegador.maximize_window()
sleep(10)

sleep(1)
# Clicando no botão de painel para limpar todas as seleções"
navegador.find_element(By.ID, "clear-selections").click()
# Atrasar o códgio em 1 segundos para da tempo dos recursos abrir
sleep(2)

sleep(1)
# Rola até o final da página
navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

sleep(1)
# Realizado o Dowload do arquivo"
navegador.find_element(By.ID, "exportar-dados-Tab-01").click()

# Finalizando a conexão com site
navegador.quit()

print("Arquivos extraídos com sucesso!")