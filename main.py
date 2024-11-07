import telebot
from telebot import types
from Core.keyboards import *
from Core.Commands import *

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"

bot = telebot.TeleBot(token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Выбери один из вариантов ниже, чтобы получить информацию.",
        reply_markup=keyboard_start()
    )


# Обработчик нажатий на все кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    CommandProcessing(message, bot)

bot.polling(none_stop=True)



