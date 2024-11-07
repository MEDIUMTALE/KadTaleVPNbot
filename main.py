import telebot
from telebot import types

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"

bot = telebot.TeleBot(token)

text1 = "KadTaleVPN был сделан неравнодушными людьми, которым не всеравно на проблему свободного интернета в стране."
text2 = "В разработке"
text3 = "В разработке"


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = types.KeyboardButton("Информация о VPN 📜")
    button_tarif = types.KeyboardButton("Тарифы 📚")
    button_givekey = types.KeyboardButton("Получить ключ 🔑")
    markup.add(button_info, button_tarif, button_givekey)

    bot.send_message(
        message.chat.id,
        "Привет! Выберите один из вариантов ниже, чтобы получить информацию.",
        reply_markup=markup
    )


# Обработчик нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "Информация о VPN 📜":
        bot.send_message(message.chat.id, text1)
    elif message.text == "Тарифы 📚":
        tarif_photo = open("./tarif.png", "rb")
        bot.send_photo(message.chat.id, tarif_photo)
    elif message.text == "Получить ключ 🔑":
        tarif_menu(message)

    # обработка кнопки назад
    elif message.text == "Назад":
        start(message)

    # обработка нажатий на дополнительные кнопки поддержки
    elif message.text == "Тариф Free":
        bot.send_message(message.chat.id, "работаем братья")
    elif message.text == "Тариф Lite":
        bot.send_message(message.chat.id, "работаем братья")
    elif message.text == "Тариф Basic":
        bot.send_message(message.chat.id, "работаем братья")
    elif message.text == "Тариф Maxi":
        bot.send_message(message.chat.id, "работаем братья")

    # запрос номера телефона

    else:
        bot.send_message(message.chat.id, "не работаем братья")


def tarif_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_free = types.KeyboardButton("Тариф Free")
    button_lite = types.KeyboardButton("Тариф Lite")
    button_basic = types.KeyboardButton("Тариф Basic")
    button_maxi = types.KeyboardButton("Тариф Maxi")
    button_back = types.KeyboardButton("Назад")

    markup.add(button_free, button_lite)
    markup.add(button_basic, button_maxi)
    markup.add(button_back)

    bot.send_message(message.chat.id, "Выверите интересующий вас тариф, или вернитесь в меню.", reply_markup=markup)

bot.polling(none_stop=True)