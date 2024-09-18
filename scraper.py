import os
import time

from bs4 import BeautifulSoup
import re
from config import quantidade_numeros, STRATEGY

quantidade_numeros = quantidade_numeros
atributo_nomes = {"class": "lobby-table__name-container"}
atributo_numeros = {"class": "roulette-history-item__value-text--siwxW"}
lista_ref = ['Dúzia 1', 'Dúzia 2', 'Dúzia 3', 'Linha 1', 'Linha 2', 'Linha 3']
lista_ref2 = ['Vermelho', 'Preto']
lista_ref3 = ['Par', 'Impar']
lista_conf = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36], [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
                [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35], [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]]
lista_conf2 = [[1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
               [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]]
lista_conf3 = [[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36],
               [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]]
lista_null = [0]
roletas_repetidas = ['Football French Roulette', 'Bucharest French Roulette', 'French Roulette', 'Spread Bet Roulette',
                     'Age Of The Gods Bonus Roulette']
STRATEGY = STRATEGY

# (0, 1) - DUZIA 1 E DUZIA 2
# (1, 2) - DUZIA 2 E DUZIA 3 - VERMELHO - PAR
# (0, 2) - DUZIA 1 E DUZIA 3 - PRETO - IMPAR
# (3, 4) - COL 1 E COL 2
# (4, 5) - COL 2 E COL 3
# (3, 5) - COL 1 E COL 3
tipos_apostas = [(1, 2), (0, 2), (0, 1), (4, 5), (3, 5), (3, 4)]


class Scraper:

    def __init__(self, html):
        self.html_roletas = html
        self.lista_nomes = []
        self.lista_numeros = []
        self.db = []

    def get_names(self):
        self.lista_nomes = []
        for x in self.html_roletas:
            soup = BeautifulSoup(x, 'html.parser')
            nome_raw = soup.find('div', atributo_nomes)
            self.lista_nomes.append(nome_raw.string)

    def get_numbers(self):
        self.lista_numeros = []
        resultados = []
        for x in self.html_roletas:
            soup = BeautifulSoup(x, 'html.parser')
            results_raw = soup.find_all('div', atributo_numeros)
            for i in results_raw:
                if i.string is None:
                    resultados.append(0)
                else:
                    resultados.append(int(i.string))
            self.lista_numeros.append(resultados)
            resultados = []

    def estrategia_duz_col(self):
        lista_true_false = []
        for k in range(6):
            for x in self.db:
                try:
                    for y in range(quantidade_numeros):
                        if x[y] in lista_conf[k]:
                            lista_true_false.append(True)
                        else:
                            lista_true_false.append(False)
                    if all(lista_true_false) and self.lista_nomes[self.db.index(x)] not in roletas_repetidas:
                        print('ESTRATEGIA ACONTECEU')
                        return lista_ref[k], self.lista_numeros[self.db.index(x)], \
                    self.lista_nomes[self.db.index(x)], k, self.db.index(x), tipos_apostas[k]
                    lista_true_false = []
                except IndexError:
                    continue

    def estrategia_cor(self):
        lista_true_false = []
        for k in range(2):
            for x in self.db:
                try:
                    for y in range(quantidade_numeros):
                        if x[y] in lista_conf2[k]:
                            lista_true_false.append(True)
                        else:
                            lista_true_false.append(False)
                    if all(lista_true_false) and self.lista_nomes[self.db.index(x)] not in roletas_repetidas:
                        print('ESTRATEGIA ACONTECEU')
                        return lista_ref2[k], self.lista_numeros[self.db.index(x)],\
                    self.lista_nomes[self.db.index(x)], k, self.db.index(x), tipos_apostas[k]
                    lista_true_false = []
                except IndexError:
                    continue

    def estrategia_par_impar(self):
        lista_true_false = []
        for k in range(2):
            for x in self.db:
                try:
                    for y in range(quantidade_numeros):
                        if x[y] in lista_conf3[k]:
                            lista_true_false.append(True)
                        else:
                            lista_true_false.append(False)
                    if all(lista_true_false) and self.lista_nomes[self.db.index(x)] not in roletas_repetidas:
                        print('ESTRATEGIA ACONTECEU')
                        return lista_ref3[k], self.lista_numeros[self.db.index(x)], \
                    self.lista_nomes[self.db.index(x)], k, self.db.index(x), tipos_apostas[k]
                    lista_true_false = []
                except IndexError:
                    continue

    @staticmethod
    def green_red(num, k):
        soup = BeautifulSoup(num, 'html.parser')
        numero = int(soup.string)
        if STRATEGY == 0:
            if numero in lista_conf[k] or numero in lista_null:
                return 0
            else:
                return 1
        if STRATEGY == 1:
            if numero in lista_conf2[k] or numero in lista_null:
                return 0
            else:
                return 1
        if STRATEGY == 2:
            if numero in lista_conf3[k] or numero in lista_null:
                return 0
            else:
                return 1

    def database(self):
        lista_num = []
        lista_num_temp = []
        if not self.db:
            self.db = self.lista_numeros
        for y in self.db:
            for i in range(10):
                lista_num_temp.append(y[i])
            lista_num.append(lista_num_temp)
            lista_num_temp = []
        for x in range(len(self.lista_numeros)):
            if self.lista_nomes[x] not in roletas_repetidas:
                if self.lista_numeros[x] != lista_num[x]:
                    self.db[x].insert(0, self.lista_numeros[x][0])

    def limpar_database(self):
        self.db = []
