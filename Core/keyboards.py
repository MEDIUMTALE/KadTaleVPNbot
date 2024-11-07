from telebot import types

"""
def  create_keyboard(srt = []):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for text in srt:
        markup.add(types.KeyboardButton(text)) # добавление кнопки об информации
        
    return markup
"""




def keyboard_start():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard=True аналогично C# ResizeKeyboard = true

    # Добавляем строки кнопок (аналог двумерного массива)
    row1 = [types.KeyboardButton("Информация о VPN 📜")]
    row2 = [types.KeyboardButton("Тарифы 📚"), types.KeyboardButton("Получить ключ 🔑"), types.KeyboardButton("Инструкция 📝")]

    # Добавляем строки в клавиатуру
    markup.add(*row1)  # Добавляем первую строку
    markup.add(*row2)  # Добавляем вторую строку

    return markup

def keyboard_tariff():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard=True аналогично C# ResizeKeyboard = true

    # Добавляем строки кнопок (аналог двумерного массива)
    row1 = [types.KeyboardButton("Тариф Free"), types.KeyboardButton("Тариф Lite")]
    row2 = [types.KeyboardButton("Тариф Basic"), types.KeyboardButton("Тариф Maxi")]
    row3 = [types.KeyboardButton("Назад ⏪")]

    # Добавляем строки в клавиатуру
    markup.add(*row1)  # Добавляем первую строку
    markup.add(*row2)  # Добавляем вторую строку
    markup.add(*row3)  # Добавляем вторую строку

    return markup

def keyboard_Manual():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard=True аналогично C# ResizeKeyboard = true

    # Добавляем строки кнопок (аналог двумерного массива)
    row1 = [types.KeyboardButton("Для Android 🤖"), types.KeyboardButton("Для Iphone 🍎")]
    row2 = [types.KeyboardButton("Назад ⏪")]

    # Добавляем строки в клавиатуру
    markup.add(*row1)  # Добавляем первую строку
    markup.add(*row2)  # Добавляем вторую строку

    return markup