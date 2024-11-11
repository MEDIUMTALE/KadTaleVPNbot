import telebot
from telebot import types
from Core.keyboards import *
from Core.Commands import CommandProcessing  # Правильный импорт функции

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"
bot = telebot.TeleBot(token)

# Обработчик нажатий на все кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    CommandProcessing(message, bot)  # передаем message

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    CommandProcessing(callback=callback, bot=bot)  # передаем callback

bot.polling(none_stop=True)