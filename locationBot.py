from asyncio.log import logger
from asyncore import dispatcher
import logging
from tracemalloc import start

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackContext)

from dotenv import load_dotenv
import os
load_dotenv()
CHAVE = os.getenv('CHAVE_API')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
PHOTO, LOCATION, BIO = range(3)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("O nome do usuário é %s", user.first_name)
    update.message.reply_text("Me mande uma foto sua para que possamos registrá-lo, ou mande /skip se você deseja pular", reply_markup=ReplyKeyboardRemove(),)
    return PHOTO

def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("A foto de %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text("Perfeito, quase terminando. Agora me mande a sua localização, ou mande /skip se você deseja pular")

    return LOCATION

def skip_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("O usuário %s não mandou a foto.", user.first_name)
    update.message.reply_text("Oh, sem problema! Agora, me mande a sua localização ou mande /skip para pular")

    return LOCATION

def location(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Localização do usuário %s: %s / %s", user.first_name, user_location.latitude, user_location.longitude)
    update.message.reply_text("Ok, obrigado por mandar sua localização")

    return BIO

def skip_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Usuário %s não mandou a localização.", user.first_name)
    update.message.reply_text("Ok, sem problema. Mande /start para recomeçar")
    return ConversationHandler.END

def bio(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Mensagem de %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Obrigado! Até a próxima. Mande /start para recomeçar")
    return ConversationHandler.END

def cancel (update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Usuário %s cancelou a conversa", user.first_name)
    update.message.reply_text("Entre em contato se tiver alguma dúvida", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    updater = Updater(CHAVE)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


main()
