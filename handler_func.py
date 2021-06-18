from json import dumps, loads
from telegram.ext import DispatcherHandlerStop

from config import USERS
from sql_executor import sp_telegram_wrap
from jsonExport import json_to_txt


def check_user(func):
    def wrapper(*args, **kwargs):
        username = args[0].message.from_user.username
        if username in USERS:
            func(*args, **kwargs, username=username)
        else:
            raise DispatcherHandlerStop
    return wrapper


@check_user
def start(update, context, **kwargs):
    msg = f'{kwargs["username"]}\nREADME /help'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@check_user
def unknown(update, context, **kwargs):
    username = kwargs['username']
    data = [username, *update.message.text[1:].split()]  # get list [username, cmd, v1, v2]
    result = sp_telegram_wrap(data)
    if result:
        if len(result) <= 4096:
            result = dumps(loads(result), indent=1)  # prettify
            msg = f'{username}\n{result}'  # add username
            for x in range(0, len(msg), 4096):
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg[x:x+4096])
        else:
            filename = f'{update.message.text[1:].replace(" ", "_")}.txt'
            context.bot.send_message(chat_id=update.effective_chat.id, text=username)
            context.bot.sendDocument(chat_id=update.effective_chat.id,
                                     filename=filename,
                                     document=json_to_txt(result))


@check_user
def ping(update, context, **kwargs):
    msg = f'{kwargs["username"]}\npong'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@check_user
def caps(update, context, **kwargs):
    msg = kwargs["username"] + '\n' + ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


'''    
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)
'''
