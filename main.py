import sys

from driver import Driver
from scraper import Scraper
from bot import Bot
import time
from config import quantidade_gale, valor_ficha, STRATEGY, parar_no_red


driver = Driver()
scraper = Scraper(driver.roletas_html)
bot = Bot()
i = 0
contador_gale = 0
gale = quantidade_gale
quantidade_aposta = 1
STRATEGY = STRATEGY
nomes_funcoes_scraper = ['scraper.estrategia_duz_col', 'scraper.estrategia_cor', 'scraper.estrategia_par_impar']
nomes_funcoes_driver = ['driver.bet_duz_col', 'driver.bet_cor', 'driver.bet_par_impar']

while True:
    atualizar = driver.atualizar_roletas()
    if atualizar:
        print('LIMPANDO DATABASE')
        scraper.limpar_database()
    scraper.html_roletas = driver.roletas_html
    scraper.get_names()
    scraper.get_numbers()
    scraper.database()
    # Return da estrategia: 0 - tipo de repeticao, 1 - lista dos ultimos numeros
    # 2 - nome da roleta, 3 - index para lista_ref, 4 - index da roleta, 5 - tipo da aposta
    estrategia = eval(nomes_funcoes_scraper[STRATEGY] + "()")
    if estrategia:
        print(scraper.db[estrategia[4]])
        # Estrategia aconteceu
        print(estrategia)
        acessar = driver.acessar_roleta(estrategia[4])
        time.sleep(1)
        driver.verificar_popup()
        if not acessar:
            ficha = driver.escolher_ficha(valor_ficha)
            time.sleep(0.2)
            pre_bet = 0
            if ficha:
                pre_bet = driver.pre_bet(estrategia[1])
            if ficha and pre_bet:
                while True:
                    if contador_gale == gale:
                        print('DEU RED')
                        if parar_no_red == 's':
                            bot.mandar_msg_red(estrategia[0], estrategia[2], driver.saldo_atual, contador_gale - 1)
                            sys.exit()
                        time.sleep(5)
                        driver.atualizar_saldo()
                        bot.mandar_msg_red(estrategia[0], estrategia[2], driver.saldo_atual, contador_gale - 1)
                        driver.voltar_lobby()
                        time.sleep(120)
                        scraper.limpar_database()
                        driver.last_number = []
                        driver.last_number_html = []
                        quantidade_aposta = 1
                        contador_gale = 0
                        break
                    aposta = eval(nomes_funcoes_driver[STRATEGY] + '(estrategia[5], quantidade_aposta)')
                    contador_gale += 1
                    if aposta:
                        while True:
                            saiu_num = driver.saiu_numero()
                            if saiu_num:
                                break
                            time.sleep(0.2)
                        green_red = scraper.green_red(driver.last_number_html, estrategia[3])
                        if green_red:
                            print('DEU GREEN')
                            time.sleep(5)
                            driver.atualizar_saldo()
                            bot.mandar_msg_green(estrategia[0], estrategia[2], driver.saldo_atual, contador_gale - 1)
                            driver.voltar_lobby()
                            time.sleep(30)
                            scraper.limpar_database()
                            driver.last_number = []
                            driver.last_number_html = []
                            quantidade_aposta = 1
                            contador_gale = 0
                            break
                        if not green_red:
                            while True:
                                timer = driver.timer_tela()
                                if timer:
                                    time.sleep(1)
                                    break
                            if STRATEGY == 0:
                                quantidade_aposta = quantidade_aposta * 3
                            if STRATEGY == 1 or STRATEGY == 2:
                                quantidade_aposta = quantidade_aposta * 2
                            driver.atualizar_last_number()
                            continue
                    if not aposta:
                        contador_gale = 0
                        quantidade_aposta = 1
                        time.sleep(30)
                        scraper.limpar_database()
                        break
            else:
                driver.last_number = []
                driver.last_number_html = []
                quantidade_aposta = 1
                contador_gale = 0
                time.sleep(30)
                scraper.limpar_database()
        if acessar:
            driver.last_number = []
            driver.last_number_html = []
            contador_gale = 0
            quantidade_aposta = 1
            time.sleep(30)
            scraper.limpar_database()

    i += 1
    if i % 5 == 0:
        print(i)
    if i == 500:
        i = 0
        while True:
            # try:
            driver.fechar_driver()
            driver = Driver()
            scraper.limpar_database()
            break
            # except:
            #     continue
