from json import load
import telebot
from dotenv import load_dotenv
import os
load_dotenv()
CHAVE = os.getenv('CHAVE_API')
bot = telebot.TeleBot(CHAVE)

@bot.message_handler(commands=["beijo"])
def beijo(mensagem):
    bot.send_message(mensagem.chat.id, "Um beijão para você")

@bot.message_handler(commands=["abraco"])
def beijo(mensagem):
    bot.send_message(mensagem.chat.id, "Um abração para você")

@bot.message_handler(commands=["massagem"])
def beijo(mensagem):
    bot.send_message(mensagem.chat.id, "Sem massagens hoje /menu")

@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    texto="""
    O que você deseja?
        /beijo
        /abraco
        /massagem
    """
    bot.reply_to(mensagem, texto)

@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    bot.send_message(mensagem.chat.id, "A Báh também te ama")

@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    bot.send_message(mensagem.chat.id, "Para fazer uma reclamação, mande um email para reclamacao@blablabla.com")

@bot.message_handler(commands=["opcao4"])
def opcao4(mensagem):
    bot.send_message(mensagem.chat.id, mensagem)

#função geral que responde qualquer msg
def verificar(mensagem):
    return True

@bot.message_handler(func=verificar) #diz qnd def responder deve ser executado
def responder(mensagem):
    texto = """
    Oie! Eu sou o Chat da Báh! O que você quer fazer? (Clique no item):
        /opcao1 Fazer um pedido
        /opcao2 Falar que me ama
        /opcao3 Fazer uma reclamação
        /opcao4 Teste Localização
    """
    bot.reply_to(mensagem, texto)



bot.polling() #looping infinito do telegram para ficar escutando
