import telebot
from telebot import types
from Core.keyboards import *
from Core.Commands import CommandProcessing  # Правильный импорт функции

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"

bot = telebot.TeleBot(token)


# Обработчик нажатий на все кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    CommandProcessing(message, bot)

bot.polling(none_stop=True)