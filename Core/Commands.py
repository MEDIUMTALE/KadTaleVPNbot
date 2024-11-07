import telebot
from telebot import types
from Core.keyboards import *
from main import *

def CommandProcessing(message, bot):

    # обработка основных кнопок
    if message.text == "Информация о VPN 📜":
        bot.send_message(message.chat.id, "KadTaleVPN был сделан неравнодушными людьми, которым не всеравно на проблему свободного интернета в стране.")
    elif message.text == "Тарифы 📚":
        tarif_photo = open("ViewModels/resourse/img/tarif.png", "rb")
        bot.send_photo(message.chat.id, tarif_photo)
    elif message.text == "Получить ключ 🔑":
        keyboard_tariff(message)
    elif message.text == "Инструкция 📝":
        keyboard_Manual(message)


    # обработка кнопки назад
    elif message.text == "Назад ⏪":
        bot.send_message(
        message.chat.id,
        "Привет! Выбери один из вариантов ниже, чтобы получить информацию.",
        reply_markup=keyboard_start()
    )






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
        # шаг 1
        bot.send_message(message.chat.id,
                        "Шаг 1:\n    Для запуска нашего VPN на Iphone, необходимо приложение клиент, в нашем случаее рекомендую 'Streisand':")
        bot.send_photo(message.chat.id, open("ViewModels/resourse/img/guides/iphone/in_appstore.jpg", "rb"))

        # шаг 2
        bot.send_message(message.chat.id,
                        "Шаг 2:\n    Предварительно скопировав выданный ключ, зайдя в приложение нажмите на плюсик в верхнем правом углу экрана:")
        bot.send_photo(message.chat.id, open("ViewModels/resourse/img/guides/iphone/add_profile.jpg", "rb"))

        # шаг 3
        bot.send_message(message.chat.id, "Шаг 3:\n    Нажмите на кнопку 'Добавить из буфера':")
        bot.send_photo(message.chat.id, open("ViewModels/resourse/img/guides/iphone/import_at_bufer.jpg", "rb"))

        # шаг 4
        bot.send_message(message.chat.id, "Шаг 4:\n    Выберите добавленный профиль нажав на него:")
        bot.send_photo(message.chat.id, open("ViewModels/resourse/img/guides/iphone/profile_choice.jpg", "rb"))

        # шаг 5
        bot.send_message(message.chat.id, "Шаг 5:\n    Включите VPN:")
        bot.send_photo(message.chat.id, open("ViewModels/resourse/img/guides/iphone/activate.jpg", "rb"))

        bot.send_message(message.chat.id, "Выверите инструкцию подходящую под ваше устройство, или вернитесь в меню.")
    else:
        bot.send_message(message.chat.id, "Я не понимаю, выберите нужный пункт снизу.")
