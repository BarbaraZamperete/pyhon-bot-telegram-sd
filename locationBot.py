from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackContext)

from dotenv import load_dotenv
import os
load_dotenv()
CHAVE = os.getenv('CHAVE_API')

PHOTO, LOCATION, BIO = range(3)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    print("O nome do usuário é %s" % user.first_name)
    update.message.reply_text("Olá, %s!" % user.first_name)
    update.message.reply_text("Me mande uma foto sua para que possamos registrá-lo.\nDigite /cancel para terminar a conversa", reply_markup=ReplyKeyboardRemove(),)
    return PHOTO

def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(user.first_name + '_photo.jpg')
    print("A foto de %s: %s" % (user.first_name, user.first_name + '_photo.jpg'))
    update.message.reply_text("Perfeito, quase terminando. Agora me mande a sua localização.\nDigite /cancel para terminar a conversa")

    return LOCATION

def location(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location
    print("Localização do usuário %s: %s / %s" % (user.first_name, user_location.latitude, user_location.longitude))
    update.message.reply_text("Você foi registrado com sucesso!")
    update.message.reply_text("O usuário %s se encontra na latitude: %s e longitude: %s." %(user.first_name, user_location.latitude, user_location.longitude ))

    return BIO

def bio(update: Update, context: CallbackContext):
    user = update.message.from_user
    print("Mensagem de %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text("Obrigado! Até a próxima. Mande /start para recomeçar")
    return ConversationHandler.END

def cancel (update: Update, context: CallbackContext):
    user = update.message.from_user
    print("Usuário %s cancelou a conversa" % user.first_name)
    update.message.reply_text("Usuário %s cancelou a conversa" % user.first_name)
    update.message.reply_text("Entre em contato se tiver alguma dúvida. Mande /start para recomeçar", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    updater = Updater(CHAVE)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(~Filters.command, start), CommandHandler("start", start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[MessageHandler(~Filters.command, cancel), CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


main()
