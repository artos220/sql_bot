import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import TOKEN
import handler_func as h

# TODO logs inside sql sp: datetime, user, rtype, value, result

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

handlers = [
            CommandHandler('start', h.start),
            CommandHandler('ping', h.ping),
            CommandHandler('caps', h.caps),
            # MessageHandler(Filters.text & (~Filters.command), h.echo),
            # InlineQueryHandler(h.inline_caps),
            MessageHandler(Filters.command, h.unknown),
            ]

for handler in handlers:
    dispatcher.add_handler(handler)

try:
    while True:
        updater.start_polling()
finally:
    updater.stop()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

