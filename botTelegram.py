
from telegram import *
from telegram.ext import *
from dotenv import load_dotenv
import os


load_dotenv()
CHAVE = os.getenv('CHAVE_API')

CADASTRAR, MENSAGEM, LOCATION, FINALIZAR = range(4)
updater = Updater(CHAVE)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Cancelar")], [KeyboardButton("Cadastrar")]]
    update.message.reply_text(
        "Olá, seja bem vindo ao Bot da Báh", reply_markup=ReplyKeyboardMarkup(buttons))
    return MENSAGEM

def senha(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Cadastrar Localização")], [KeyboardButton("Finalizar")]]
    print("Salvar a senha e o user")
    update.message.reply_text("O usuário %s foi cadastrado com a senha %s" % (
        update.message.from_user.first_name, update.message.text))
    update.message.reply_text("Deseja cadastrar a localização também?", reply_markup=ReplyKeyboardMarkup(buttons))
    return MENSAGEM


def cadastrar(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Para ser cadastrado, digite uma senha", reply_markup=ReplyKeyboardRemove())
    # dispatcher.add_handler(MessageHandler(Filters.all, senha))
    return CADASTRAR

def finalizar( update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Iniciar")]]
    update.message.reply_text("Operação finalizada", reply_markup=ReplyKeyboardMarkup(buttons))
    return ConversationHandler.END

def cancelar(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Iniciar")]]
    update.message.reply_text("O usuário %s cancelou a conversa" % (
        update.message.from_user.first_name), reply_markup=ReplyKeyboardMarkup(buttons))
    return ConversationHandler.END

def localizacaoPedir(update: Update, context: CallbackContext):
    update.message.reply_text("Mande a sua localização", reply_markup=ReplyKeyboardRemove())
    return LOCATION

def localizacao(update: Update, context: CallbackContext):
    localicazaoUser = update.message.location
    nameUser = update.message.from_user.first_name
    update.message.reply_text("Sua localização é longitude: %s e latitude: %s" % 
    (localicazaoUser.longitude, localicazaoUser.latitude))
    return finalizar(update, context)


def mensagens(update: Update, context: CallbackContext):
    if "Cadastrar" == update.message.text:
        return cadastrar(update, context)
    if "Cancelar" == update.message.text:
        cancelar(update, context)
        return cancelar(update, context)
    if "Finalizar" == update.message.text:
        return finalizar(update, context)
    if "Cadastrar Localização" == update.message.text:
        return localizacaoPedir(update, context)


# dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(MessageHandler(Filters.text, mensagens))
dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(~Filters.command, start)],
    states={
        CADASTRAR: [MessageHandler(Filters.all, senha)],
        MENSAGEM: [MessageHandler(Filters.text, mensagens)],
        LOCATION: [MessageHandler(Filters.location, localizacao)]
    },
    fallbacks=[ConversationHandler.END]))

updater.start_polling()
