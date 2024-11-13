import telebot
from telebot import types
from Core.keyboards import *  # Импорт клавиатур из Core.keyboards
# from main import *  # Этот импорт больше не нужен
from Core.Databases import add_user

def CommandProcessing(message=None, bot=None, callback=None):
    # Если это сообщение
    if message:
        if message.text == "/start":
            user_id = message.from_user.id
            add_user(user_id)
            bot.send_message(
                message.chat.id,
                "Привет! Выбери один из вариантов ниже, чтобы получить информацию.",
                reply_markup=keyboard_start()
            )
        elif message.text == "Информация о VPN 📜":
            bot.send_message(message.chat.id, "KadTaleVPN был сделан неравнодушными людьми, которым не всеравно на проблему свободного интернета в стране.")
        elif message.text == "Получить ключ 🔑":
            bot.send_message(
                message.chat.id,
                "Выберите интересующий вас тариф, или вернитесь в меню.",
                reply_markup=keyboard_tariff()
            )
        elif message.text == "Преобрести подписку ⚔️":
            bot.send_message(
                message.chat.id,
                "Выберите вариант подписки:",
                reply_markup=purchase_a_subscription()
            )
        elif message.text == "Помощь 🛟":
            bot.send_message(message.chat.id, "Чем вам помочь?:", reply_markup=help_menu())

        elif message.text == "Назад ⏪":
            bot.send_message(
                message.chat.id,
                "Привет! Выбери один из вариантов ниже, чтобы получить информацию.",
                reply_markup=keyboard_start()
            )
        elif message.text == "Язык 🗺️":
            bot.send_message(message.chat.id, "Пожалуйста, выберите язык интерфейса:", reply_markup=language_choice())
        else:
            bot.send_message(message.chat.id, "В разработке...")

    # Если это callback
    elif callback:

        # кнопки помощи

        # часто задаваемые вопросы
        if callback.data == "help_one":
            bot.send_message(callback.message.chat.id, "В разработке...")
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) # удаление

        # установка vpn
        elif callback.data == "help_two":
            bot.send_message(callback.message.chat.id, "Пожалуйста, выберите операционную систему вашего телефона:", reply_markup=guide_menu())
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) # удаление

        # android
        elif callback.data == "help_android":
            bot.send_message(callback.message.chat.id, "В разработке...")
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)  # удаление

        # iphone
        elif callback.data == "help_iphone":
            bot.send_message(callback.message.chat.id, "В разработке...")
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)  # удаление

        # обратиться в поддержку
        elif callback.data == "help_three":
            bot.send_message(callback.message.chat.id, "В разработке...")
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

        # гайды на установку

        # Для других callback-ов можно добавить аналогичные условия
        else:
            bot.send_message(callback.message.chat.id, "В разработке...")