import telebot
from telebot import types

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"

bot = telebot.TeleBot(token)

text1 = "KadTaleVPN был сделан неравнодушными людьми, которым не всеравно на проблему свободного интернета в стране."


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = types.KeyboardButton("Информация о VPN 📜")
    button_tarif = types.KeyboardButton("Тарифы 📚")
    button_givekey = types.KeyboardButton("Получить ключ 🔑")
    button_guide = types.KeyboardButton("Инструкция 📝")
    markup.add(button_info) # добавление кнопки об информации
    markup.add(button_tarif, button_givekey, button_guide) # добавление 3-ех других кнопок

    bot.send_message(
        message.chat.id,
        "Привет! Выбери один из вариантов ниже, чтобы получить информацию.",
        reply_markup=markup
    )


# Обработчик нажатий на все кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # обработка основных кнопок
    if message.text == "Информация о VPN 📜":
        bot.send_message(message.chat.id, text1)
    elif message.text == "Тарифы 📚":
        tarif_photo = open("./tarif.png", "rb")
        bot.send_photo(message.chat.id, tarif_photo)
    elif message.text == "Получить ключ 🔑":
        tarif_menu(message)
    elif message.text == "Инструкция 📝":
        guide_menu(message)


    # обработка кнопки назад
    elif message.text == "Назад ⏪":
        start(message)


    # обработка нажатий на дополнительные кнопки поддержки
    elif message.text == "Тариф Free":
        bot.send_message(message.chat.id, "В разработке...")
    elif message.text == "Тариф Lite":
        bot.send_message(message.chat.id, "В разработке...")
    elif message.text == "Тариф Basic":
        bot.send_message(message.chat.id, "В разработке...")
    elif message.text == "Тариф Maxi":
        bot.send_message(message.chat.id, "В разработке...")

    # инструкции
    elif message.text == "Для Android 🤖":
        bot.send_message(message.chat.id, "в разработке...")
    elif message.text == "Для Iphone 🍎":
        bot.send_message(message.chat.id, "в разработке...")

    else:
        bot.send_message(message.chat.id, "Я не понимаю, выберите нужный пункт снизу.")


# меню с тарифами
def tarif_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_free = types.KeyboardButton("Тариф Free")
    button_lite = types.KeyboardButton("Тариф Lite")
    button_basic = types.KeyboardButton("Тариф Basic")
    button_maxi = types.KeyboardButton("Тариф Maxi")
    button_back_to_start = types.KeyboardButton("Назад ⏪")

    markup.add(button_free, button_lite)
    markup.add(button_basic, button_maxi)
    markup.add(button_back_to_start)

    bot.send_message(message.chat.id, "Выверите интересующий вас тариф, или вернитесь в меню.", reply_markup=markup)

# меню с гайдами по установке
def guide_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_guide_android = types.KeyboardButton("Для Android 🤖")
    button_guide_ios = types.KeyboardButton("Для Iphone 🍎")
    button_back_to_tarif = types.KeyboardButton("Назад ⏪")

    markup.add(button_guide_android, button_guide_ios)
    markup.add(button_back_to_tarif)

    bot.send_message(message.chat.id, "Выверите инструкцию подходящую под ваше устройство, или вернитесь в меню.", reply_markup=markup)

bot.polling(none_stop=True)