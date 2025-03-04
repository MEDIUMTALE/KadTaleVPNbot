from telebot import types
import sqlite3


def keyboard_start():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard=True аналогично C# ResizeKeyboard = true

    # Добавляем строки кнопок (аналог двумерного массива)
    row1 = [types.KeyboardButton("Информация о VPN 📜")]
    # row2 = [types.KeyboardButton("Тарифы 📚"), types.KeyboardButton("Получить ключ 🔑"), types.KeyboardButton("Инструкция 📝")]
    row2 = [types.KeyboardButton("Пополнить баланс⚔️")]
    row3 = [types.KeyboardButton("Помощь 🛟"), types.KeyboardButton("Язык 🗺️")]
    # row4 = [types.KeyboardButton("Поменять локацию 🌍"), types.KeyboardButton("Поменять протокол ⛓")]
    row5 = [types.KeyboardButton("Пригласить 👥"), types.KeyboardButton("Партнерская промграмма 🤝")]

    # Добавляем строки в клавиатуру
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)
#    markup.add(*row4)
    markup.add(*row5)

    return markup

def keyboard_balance():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard=True аналогично C# ResizeKeyboard = true



    # Добавляем строки кнопок (аналог двумерного массива)
    row1 = [types.KeyboardButton("Пополнить баланс ⚔️", callback_data="deposit_money"), types.KeyboardButton("Пригласить друга", callback_data="invite_friend")]
    row2 = [types.KeyboardButton("Назад ⏪")]

    # Добавляем строки в клавиатуру
    markup.add(*row1)
    markup.add(*row2)

    return markup

# помощь в установке vpn
def guide_menu():
    markup = types.InlineKeyboardMarkup()

    # добавляем строки кнопок (аналог двумерного массива)
    row1 = [
        types.InlineKeyboardButton("Для Android 🤖", callback_data="help_android"),
        types.InlineKeyboardButton("Для IOS (Iphone, IPad, MacOS) 🍎", callback_data="help_iphone"),
            ]
    row2 = [
        types.InlineKeyboardButton("Для ПК (Windows) 💻", callback_data="help_pc"),
        types.InlineKeyboardButton("Для TV (Android TV) 📺", callback_data="help_tv")
    ]

    # добавляем строку в клавиатуру
    markup.add(*row1)
    markup.add(*row2)

    return markup

# меню преобрести подписку
def purchase_a_subscription():
    markup = types.InlineKeyboardMarkup()



    return markup

# меню помощи пользователю
def help_menu():
    markup = types.InlineKeyboardMarkup()

    row1 = types.InlineKeyboardButton("Часто задаваемые вопросы", callback_data="help_one")
    row2 = types.InlineKeyboardButton("Установка VPN", callback_data="help_two")
    row3 = types.InlineKeyboardButton("Обратиться в поддержку", callback_data="help_three")

    markup.add(row1)
    markup.add(row2)
    markup.add(row3)

    return markup

def language_choice():
    markup = types.InlineKeyboardMarkup()

    row1 = [types.InlineKeyboardButton("🇷🇺", callback_data="language_ru"), types.InlineKeyboardButton("🇬🇧 / 🇺🇸", callback_data="language_us")]

    markup.add(*row1)

    return markup

