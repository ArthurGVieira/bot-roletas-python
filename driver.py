from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import re
from config import login, senha
from bs4 import BeautifulSoup

# URLS de acesso da Betfair
url = 'https://www.betfair.com/exchange/plus/'
url2 = 'https://bit.ly/3IsglH8'

# Caminhos xpath do selenium
xpath_login = "//div[@class='ssc-lifg']//input[@name='username']"
xpath_password = "//*[@id='ssc-lipw']"
xpath_elementos = "//div[@class='lobby-table__wrapper']"
xpath_elementos2 = "//div[@class='lobby-table__wrapper lobby-table__wrapper_active']"
xpath_anti_afk = '//*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div[3]/div'
xpath_opcoes_lobby = '/html/body/div/div/div[3]/div[1]/div/div[1]/div/div/div[1]/div[1]/ul/li[1]'
xpath_lobby = '/html/body/div/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div[4]/div/div/div[1]/div/div/ul[1]/li[1]/span'
xpath_timer = '//*[@data-automation-locator="element.Timer"]'
xpath_last_number = '//*[@data-automation-locator="field.lastHistoryItem"]'
xpath_duzia1 = '//*[@data-automation-locator="betPlace.dozen-1st12"]'
xpath_duzia2 = '//*[@data-automation-locator="betPlace.dozen-2nd12"]'
xpath_duzia3 = '//*[@data-automation-locator="betPlace.dozen-3rd12"]'
xpath_col1 = '//*[@data-automation-locator="betPlace.column-1"]'
xpath_col2 = '//*[@data-automation-locator="betPlace.column-2"]'
xpath_col3 = '//*[@data-automation-locator="betPlace.column-3"]'
xpath_red = '//*[@data-automation-locator="betPlace.spots50x50-red"]'
xpath_black = '//*[@data-automation-locator="betPlace.spots50x50-black"]'
xpath_par = '//*[@data-automation-locator="betPlace.spots50x50-even"]'
xpath_impar = '//*[@data-automation-locator="betPlace.spots50x50-odd"]'
xpath_popup1 = '//*[@data-automation-locator="element.closePopup"]'
xpath_num_roleta = '/html/body/div/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div[8]/div/div[2]'
xpath_lobby_2 = '/html/body/div/div/div[3]/div[1]/div[1]/div[2]/div[1]'
xpath_saldo = '//*[@data-automation-locator="footer.balance"]'

# Login e senha da Betfair
login = login
password = senha


class Driver:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.roletas = []
        self.roletas_html = []
        self.numero_atual_roletas = 0
        self.last_number = []
        self.last_number_html = []
        self.saldo_atual = 0
        self.acesso_bet()
        self.atualizar_roletas()

    def acesso_bet(self):
        self.driver.get(url)
        time.sleep(10)
        self.driver.find_element(By.XPATH, value=xpath_login).send_keys(login)
        time.sleep(1)
        self.driver.find_element(By.XPATH, value=xpath_password).send_keys(password + Keys.ENTER)
        time.sleep(5)
        self.driver.get(url2)
        time.sleep(10)
        self.driver.maximize_window()
        time.sleep(20)

    def anti_afk(self, x):
        element = self.driver.find_element(By.XPATH, value=xpath_anti_afk)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.drag_and_drop_by_offset(element, 0, x)
        action.perform()

    def atualizar_saldo(self):
        try:
            elemento_saldo = self.driver.find_element(By.XPATH, value=xpath_saldo).get_attribute('outerHTML')
            soup = BeautifulSoup(elemento_saldo, 'html.parser')
            saldo = soup.find('div', {'class': 'fit-container__contentl2noRBpTnyQVMFpTYsrN'}).string
            self.saldo_atual = saldo
        except:
            pass

    def fechar_driver(self):
        print('RESETANDO DRIVER')
        self.driver.close()
        self.driver.quit()
        time.sleep(2)
        self.roletas = []
        self.roletas_html = []
        self.numero_atual_roletas = 0
        self.last_number = []
        self.last_number_html = []

    def atualizar_roletas(self):
        while True:
            try:
                self.roletas = []
                self.roletas_html = []
                elementos_roletas = self.driver.find_elements(By.XPATH, value=xpath_elementos)
                elementos_roletas2 = self.driver.find_elements(By.XPATH, value=xpath_elementos2)
                for x in elementos_roletas:
                    self.roletas.append(x)
                for x in elementos_roletas2:
                    self.roletas.append(x)
                self.html_roletas()
                if len(self.roletas) != self.numero_atual_roletas:
                    self.numero_atual_roletas = len(self.roletas)
                    return 1
                break
            except:
                continue

    def html_roletas(self):
        for x in self.roletas:
            self.roletas_html.append(x.get_attribute('outerHTML'))

    def timer_tela(self):
        try:
            timer = self.driver.find_element(By.XPATH, value=xpath_timer)
            if timer:
                return 1
        except:
            return 0

    def acessar_roleta(self, i):
        tempo = 0
        self.driver.execute_script("arguments[0].scrollIntoView();", self.roletas[i])
        self.roletas[i].click()
        while True:
            timer = self.timer_tela()
            if timer:
                self.atualizar_last_number()
                print('DEU TEMPO DE APOSTAR')
                break
            elif tempo == 7:
                print('SEM TEMPO PARA APOSTAR')
                self.voltar_lobby()
                return 1
            else:
                tempo += 1
                time.sleep(1)
                continue

    def acessar_roleta_sair(self, i):
        self.roletas[i].click()
        time.sleep(3)
        self.voltar_lobby()

    def atualizar_last_number(self):
        self.last_number = self.driver.find_element(By.XPATH, value=xpath_last_number)
        self.last_number_html = self.last_number.get_attribute('outerHTML')

    def verificar_popup(self):
        try:
            self.driver.find_element(By.XPATH, value=xpath_popup1).click()
        except:
            pass

    def saiu_numero(self):
        numero = self.driver.find_element(By.XPATH, value=xpath_last_number)
        if numero == self.last_number:
            return 0
        else:
            self.last_number = numero
            self.last_number_html = numero.get_attribute('outerHTML')
            return 1

    def voltar_lobby(self):
        tempo = 0
        print('VOLTANDO AO LOBBY')
        while True:
            if tempo == 15:
                break
            try:
                self.driver.find_element(By.XPATH, value=xpath_lobby_2)
                self.atualizar_roletas()
                break
            except:
                pass
            try:
                self.verificar_popup()
                self.driver.find_element(By.XPATH, value=xpath_opcoes_lobby).click()
                time.sleep(1)
                element = self.driver.find_element(By.XPATH, value=xpath_lobby)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                element.click()
                time.sleep(5)
                self.atualizar_roletas()
                break
            except:
                time.sleep(1)
                tempo += 1
                continue

    def escolher_ficha(self, valor):
        fichas = self.driver.find_elements(By.CLASS_NAME, value='chip__label')
        lista_fichas = []
        for x in fichas:
            html = x.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            if 'K' not in soup.string:
                lista_fichas.append(soup.string)
        if valor in lista_fichas:
            while True:
                try:
                    fichas[lista_fichas.index(valor)].click()
                    print('A aposta pode ser realizada')
                    return 1
                except:
                    continue
        else:
            print('A aposta NAO pode ser realizada')
            self.voltar_lobby()
            return 0

    def bet_duz_col(self, tipo, gale):
        aposta1 = tipo[0]
        aposta2 = tipo[1]
        duzias_colunas = []
        while True:
            try:
                duzias_colunas.append(self.driver.find_element(By.XPATH, value=xpath_duzia1))
                duzias_colunas.append(self.driver.find_element(By.XPATH, value=xpath_duzia2))
                duzias_colunas.append(self.driver.find_element(By.XPATH, value=xpath_duzia3))
                duzias_colunas.append(self.driver.find_element(By.XPATH, value=xpath_col1))
                duzias_colunas.append(self.driver.find_element(By.XPATH, value=xpath_col2))
                duzias_colunas.append(self.driver.find_element(By.XPATH, value=xpath_col3))
                break
            except:
                duzias_colunas = []
                continue
        try:
            for g in range(gale):
                duzias_colunas[aposta1].click()
                time.sleep(0.005)
                duzias_colunas[aposta2].click()
                time.sleep(0.005)
            print('APOSTA REALIZADA')
            return 1
        except:
            print('FALHA AO REALIZAR A APOSTA')
            self.voltar_lobby()
            return 0

    def bet_cor(self, tipo, gale):
        aposta1 = None
        if tipo != (1, 2) and tipo != (0, 2):
            print('FALHA AO REALIZAR A APOSTA')
            self.voltar_lobby()
            return 0
        if tipo == (0, 2):
            aposta1 = 0
        if tipo == (1, 2):
            aposta1 = 1
        vermelho_e_preto = []
        while True:
            try:
                vermelho_e_preto.append(self.driver.find_element(By.XPATH, value=xpath_red))
                vermelho_e_preto.append(self.driver.find_element(By.XPATH, value=xpath_black))
                break
            except:
                vermelho_e_preto = []
                continue
        try:
            for g in range(gale):
                vermelho_e_preto[aposta1].click()
                time.sleep(0.005)
            print('APOSTA REALIZADA')
            return 1
        except:
            print('FALHA AO REALIZAR A APOSTA')
            self.voltar_lobby()
            return 0

    def bet_par_impar(self, tipo, gale):
        aposta1 = None
        if tipo != (1, 2) and tipo != (0, 2):
            print('FALHA AO REALIZAR A APOSTA')
            self.voltar_lobby()
            return 0
        if tipo == (0, 2):
            aposta1 = 0
        if tipo == (1, 2):
            aposta1 = 1
        par_e_impar = []
        while True:
            try:
                par_e_impar.append(self.driver.find_element(By.XPATH, value=xpath_par))
                par_e_impar.append(self.driver.find_element(By.XPATH, value=xpath_impar))
                break
            except:
                par_e_impar = []
                continue
        try:
            for g in range(gale):
                par_e_impar[aposta1].click()
                time.sleep(0.005)
            print('APOSTA REALIZADA')
            return 1
        except:
            print('FALHA AO REALIZAR A APOSTA')
            self.voltar_lobby()
            return 0

    def pre_bet(self, last_numbers):
        try:
            lista_num = []
            numeros_html = self.driver.find_element(By.XPATH, value=xpath_num_roleta).get_attribute('outerHTML')
            timer_html = self.driver.find_element(By.XPATH, value=xpath_timer).get_attribute('outerHTML')
            soup = BeautifulSoup(numeros_html, 'html.parser')
            soup_raw = soup.find_all('div', {"class": "roulette-history-item__value-text--siwxW"})
            soup2 = BeautifulSoup(timer_html, 'html.parser')
            tag_timer = soup2.find('path')
            string = tag_timer['style']
            tempo_atual = float(re.search('.*: (.*)px', string).group(1))
            for i in range(10):
                if soup_raw[i].string is None:
                    lista_num.append(0)
                else:
                    lista_num.append(int(soup_raw[i].string))
            if last_numbers == lista_num and tempo_atual < 590:
                print('APOSTA AUTORIZADA')
                return 1
            else:
                print('APOSTA NAAAO AUTORIZADA')
                self.voltar_lobby()
                return 0
        except:
            print('excepcion')
            print('APOSTA NAAAO AUTORIZADA')
            self.voltar_lobby()
            return 0
