import telebot
from config import chave_api, id_grupo

# Definições do BOT do Telegram
CHAVE_API = chave_api
ID_GRUPO = id_grupo


class Bot:
    def __init__(self):
        self.bot = telebot.TeleBot(CHAVE_API)

    def mandar_msg_green(self, tipo, nome_roleta, saldo, quant_gale):
        mensagem = self.bot.send_message(ID_GRUPO,
                                     "\U00002705\U00002705  RESULTADO  \U00002705\U00002705\n\n "
                                     "\U0001F4B0 Repetição na {TIPO} \U0001F4B0\n\n"
                                     " \U0001F3B0  {ROLETA}  \U0001F3B0\n\n"
                                     "  SALDO: {SALDO}\n\n"
                                     "  QUANTIDADE DE GALES: {GALE}\n\n"
                                     "  \U00002705\U00002705   GREEN!!   \U00002705\U00002705"
                                     "".format(TIPO=tipo, ROLETA=nome_roleta,
                                               SALDO=saldo, GALE=quant_gale))
        return mensagem.id

    def mandar_msg_red(self, tipo, nome_roleta, saldo, quant_gale):
        mensagem2 = self.bot.send_message(ID_GRUPO,
                                     "\U0001F534\U0001F534  RESULTADO  \U0001F534\U0001F534\n\n "
                                     "\U0001F4B0 Repetição {TIPO} \U0001F4B0\n\n"
                                     " \U0001F3B0  {ROLETA}  \U0001F3B0\n\n"
                                     "  SALDO: {SALDO}\n\n"
                                     "  QUANTIDADE DE GALES: {GALE}\n\n"
                                     "   \U0001F534\U0001F534    RED    \U0001F534\U0001F534"
                                     "".format(TIPO=tipo, ROLETA=nome_roleta,
                                               SALDO=saldo, GALE=quant_gale))
        return mensagem2.id

    def apagar_msg(self, id_msg):
        self.bot.delete_message(ID_GRUPO, id_msg)
