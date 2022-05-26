import telegram
from typing import Dict

from telegram import Update, BotCommand, Bot
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler, PollAnswerHandler,
)

from main.settings import TELEGRAM_TOKEN
from tgbot.handlers.login import tg_login


def setup_dispatcher(dp):
    # регистрируете ваши функции
    dp.add_handler(CommandHandler("start", tg_login.start_and_auth))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling(timeout=123)
    updater.idle()


def set_up_commands(bot_instance: Bot) -> None:
    bot_commands = {
        'ru': {
            'balance': 'Мой баланс',
            'my_order': 'Мои заказы',
            'order': 'Показать действующие заказы️',
            'info': 'Информация о профиле',
        }
    }
    bot_instance.delete_my_commands()
    bot_instance.set_my_commands(
        commands=[
            BotCommand(command, description) for command, description in bot_commands["ru"].items()
        ]
    )


bot = telegram.Bot(TELEGRAM_TOKEN)
set_up_commands(bot)
# bot.setWebhook(url=) # вставить в url https:// Ngrok или путь с протоколом https + telegram-bot/cleaning-serice-bot/update/
# n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=1, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]