from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

BdCotasB3_URL = os.getenv('BdCotasB3_URL')

class ColetaB3:
   
    def __init__(self, driver=None, timeout: int = 10):
        self.driver = driver or self.get_new_driver()
        self.timeout = timeout

    def get_new_driver(self):
        """Método para configurar e retornar uma nova instância do WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')  # Maximiza a janela
        service = Service(ChromeDriverManager().install())  # Instala e configura o ChromeDriver automaticamente
        return webdriver.Chrome(service=service, options=options)

    def open(self, url):
        """Abre uma URL no navegador."""
        self.driver.get(url)
        print(f"Abrindo a URL: {url}")

    def switch_to_iframe(self, iframe):
        try:
            # Troca o foco para o iframe com ID ou nome 'e1menuAppIframe'
            iframe_element = self.find_element(By.ID, iframe)
            self.driver.switch_to.frame(iframe_element)
            print("Foco trocado para o iframe.")
        except TimeoutException:
            print("Erro: Iframe não encontrado.")

    def switch_to_default_content(self):
        """Retorna o foco para o conteúdo principal da página."""
        self.driver.switch_to.default_content()
        print("Foco trocado de volta para o conteúdo principal.")

    def find_element(self, by, value, timeout: int = None):
        """Encontra um elemento na página com base em seu localizador."""
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))
        except TimeoutException:
            print(f"Elemento {value} não encontrado")
            raise

    def execute_script(self, script):
        """Executa um código JavaScript na página atual."""
        return self.driver.execute_script(script)

    def navega(self):
        try:
            # Aceitar todos os cookies
            self.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']").click()
            print('Click Aceitar todos os Cookies efetuado')
            
            # Troca para o iframe onde o elemento está localizado
            self.switch_to_iframe("e1menuAppIframe")
            
            # Clica no elemento localizado pelo XPath
            self.find_element(By.XPATH, "//*[@id='tabelaBDI']/a").click()
            print('Clique realizado no elemento da tabela BDI.')

        except TimeoutException:
            print('Falha ao tentar navegar elemento.')
        finally:
            # Retorna ao conteúdo principal após a navegação
            self.switch_to_default_content()


    def close(self):
        """Fecha o navegador."""
        self.driver.quit()
        print("Navegador fechado")

BDCotasB3 = ColetaB3()              # Cria uma instância da página
BDCotasB3.open(BdCotasB3_URL)       # Abre a URL
BDCotasB3.navega()                  # Navega para a pagina de download dos itens
BDCotasB3.close()                   # Fecha a sessão aberta para o procedimento no chrome
