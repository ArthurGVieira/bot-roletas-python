import sys
from configparser import ConfigParser
import time

estrategias = ['duz_e_col', 'cores', 'par_impar']

try:
    config = ConfigParser()
    config.read('config\config.ini')
    config_data = config['DEFAULT']

    quantidade_numeros = int(config_data['quantidade_numeros'])
    quantidade_gale = int(config_data['quantidade_gale'])
    valor_ficha = config_data['valor_ficha']
    login = config_data['login']
    senha = config_data['senha']
    chave_api = config_data['chave_api']
    id_grupo = int(config_data['id_grupo'])
    estrategia = config_data['estrategia']
    STRATEGY = estrategias.index(estrategia)
    parar_no_red = config_data['parar_no_red']
except KeyError:
    print('ERRO AO LER CONFIGS')
    time.sleep(5)
    sys.exit()

if estrategia not in estrategias:
    print('ESTRATEGIA INVALIDA')
    time.sleep(5)
    sys.exit()
if quantidade_numeros < 5:
    print('QUANTIDADE DE NUMEROS MUITO BAIXA')
    time.sleep(5)
    sys.exit()
if estrategia == 'duz_e_col' and (quantidade_gale < 1 or quantidade_gale > 3):
    print('QUANTIDADE GALE INVALIDA')
    time.sleep(5)
    sys.exit()
if estrategia != 'duz_e_col' and (quantidade_gale < 1 or quantidade_gale > 5):
    print('QUANTIDADE GALE INVALIDA')
    time.sleep(5)
    sys.exit()
if parar_no_red != 's' and parar_no_red != 'n':
    print('OPCAO INVALIDA NO PARAR_NO_RED')
    time.sleep(5)
    sys.exit()
