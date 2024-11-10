import telebot
from telebot import types
from Core.keyboards import *  # Импорт клавиатур из Core.keyboards
# from main import *  # Этот импорт больше не нужен

def CommandProcessing(message, bot, callback = None):

    # обработка команды /start
    if message.text == "/start":
        bot.send_message(
            message.chat.id,
            "Привет! Выбери один из вариантов ниже, чтобы получить информацию.",
            reply_markup = keyboard_start()
        )


    # обработка основных кнопок
    elif message.text == "Информация о VPN 📜":
        bot.send_message(message.chat.id, "KadTaleVPN был сделан неравнодушными людьми, которым не всеравно на проблему свободного интернета в стране.")

    # получить ключ
    elif message.text == "Получить ключ 🔑":
        bot.send_message(
            message.chat.id,
            "Выверите интересующий вас тариф, или вернитесь в меню.",
            reply_markup = keyboard_tariff()
        )

    # преобрести подписку
    elif message.text == "Преобрести подписку ⚔️":
        bot.send_message(message.chat.id,
        "Выберите вариант подписки:",
        reply_markup = purchase_a_subscription()
        )

    # помощь
    elif message.text == "Помощь 🛟":
        bot.send_message(message.chat.id,
        "Чем вам помочь?:",
        reply_markup = help_menu()
        )

    elif callback:
        if callback.data == "help_two":
            bot.send_message(callback.message.chat.id, "Как установить VPN...")
        elif callback.data == "help_two":
            bot.send_message(callback.message.chat.id, "Как установить VPN...")

    # смена языка
    elif message.text == "Язык 🗺️":
        bot.send_message(message.chat.id,
        "Пожалуйста, выберите язык интерфейса:",
        reply_markup = language_choice()
        )

    # обработка кнопки назад
    elif message.text == "Назад ⏪":
        bot.send_message(
            message.chat.id,
            "Привет! Выбери один из вариантов ниже, чтобы получить информацию.",
            reply_markup = keyboard_start()
        )



    # инструкции
    elif message.text == "Для Android 🤖":
        bot.send_message(message.chat.id, "в разработке...")

    # инструкция для Iphone
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
