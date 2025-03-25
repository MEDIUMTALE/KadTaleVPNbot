from telebot import types
import sqlite3

from Core.Databases import info_user

async def keyboard_start(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard=True аналогично C# ResizeKeyboard = true

    # добавляем строки кнопок
    row1 = [types.KeyboardButton("Информация о VPN 📜")]
    row2 = [types.KeyboardButton("Получить Ключ 🔑")]
    row3 = [
        types.KeyboardButton("Пополнить баланс 💰️"), types.KeyboardButton("Баланс 🏦")
    ]
    row4 = [
        types.KeyboardButton("Помощь 🛟")
    ]
    row5 = [types.KeyboardButton("Партнерка 🤝")]

    # добавляем строки в клавиатуру
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)
    markup.add(*row4)
    markup.add(*row5)

    return markup

def keyboard_balance(): # РАЗОБРАТЬСЯ С ЭТОХУЙ ХУЙНЕЙ
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # добавляем строки кнопок
    row1 = [types.KeyboardButton("Пополнить баланс ⚔️", callback_data="deposit_money"), types.KeyboardButton("Пригласить друга", callback_data="invite_friend")]
    row2 = [types.KeyboardButton("⏪ Назад")]    

    # добавляем строки в клавиатуру
    markup.add(*row1)
    markup.add(*row2)

    return markup

# помощь в установке vpn
def guide_menu():
    markup = types.InlineKeyboardMarkup()

    url_android = "https://telegra.ph/Nastrojka-KadTaleVPN-dlya-Android-03-07"
    url_pc = "https://telegra.ph/Nastrojka-KadTaleVPN-dlya-PK-03-07-2"

    # добавляем строки кнопок (аналог двумерного массива)
    row1 = [
        types.InlineKeyboardButton("🤖 Для Android", url = url_android, callback_data="help_android"),
            ]
    row2 = [types.InlineKeyboardButton("🍎 Для IOS (Iphone, IPad, MacOS)", callback_data="help_iphone")]
    row3 = [types.InlineKeyboardButton("💻 Для ПК (Windows)", url = url_pc, callback_data="help_pc")]
    row4 = [types.InlineKeyboardButton("⏪ Назад", callback_data="guide_back")]

    # добавляем строку в клавиатуру
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)
    markup.add(*row4)

    return markup

# разветление на apple
def apple_menu():
    markup = types.InlineKeyboardMarkup()

    url_iphone_and_ipad = "https://telegra.ph/Nastrojka-KadTaleVPN-dlya-IOS-IphoneIPad-03-06"
    url_macos = "https://telegra.ph/Nastrojka-KadTaleVPN-dlya-macOS-03-07"

    # добавляем строки кнопок (аналог двумерного массива)
    row1 = [types.InlineKeyboardButton("📱 Для Iphone/IPad", url=url_iphone_and_ipad, callback_data="help_for_iphone"),]
    row2 = [types.InlineKeyboardButton("🖥 Для MacOS", url=url_macos, callback_data="help_for_macos")]
    row3 = [types.InlineKeyboardButton("⏪ Назад", callback_data="help_back_apple")]


    # добавляем строку в клавиатуру
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)

    return markup
# меню преобрести подписку
def purchase_a_subscription():
    markup = types.InlineKeyboardMarkup()

    row1 = types.InlineKeyboardButton("Отменить", callback_data="pay_delete")

    markup.add(row1)

    return markup

# меню помощи пользователю
def help_menu():
    markup = types.InlineKeyboardMarkup()

    target_username = "kadtalevpn_support"
    profile_url = f"https://t.me/{target_username}"

    row1 = types.InlineKeyboardButton("📝 Часто задаваемые вопросы", callback_data="frequent_questions")
    row2 = types.InlineKeyboardButton("🛠 Инструкция по установке VPN", callback_data="installation_instructions")
    row3 = types.InlineKeyboardButton("💬 Обратиться в поддержку", url=profile_url, callback_data="contact_support") # прописан в этой функции

    markup.add(row1)
    markup.add(row2)
    markup.add(row3)

    return markup

# часто задаваемые вопрсосы
def frequent_questions():
    markup = types.InlineKeyboardMarkup()
    target_username = "kadtalevpn_support"
    profile_url = f"https://t.me/{target_username}"

    row1 = types.InlineKeyboardButton("💸 Проблема с платежом", callback_data="payment_problems")
    row2 = types.InlineKeyboardButton("🐌 VPN Лагает / Низкая скорость", callback_data="low_speed_problems")
    row3 = types.InlineKeyboardButton("🚫 VPN Не работает", callback_data="vpn_no_work")
    row4 = types.InlineKeyboardButton("💬 Другой вопрос (поддержка)", url=profile_url, callback_data="contact_support")
    row5 = types.InlineKeyboardButton("⏪ Назад", callback_data="guide_back")

    markup.add(row1)
    markup.add(row2)
    markup.add(row3)
    markup.add(row4)
    markup.add(row5)

    return markup

# возвращение из разделов помощи FAQ в FAQ
def back_to_faq_keyboard():
    markup = types.InlineKeyboardMarkup()

    target_username = "kadtalevpn_support"
    profile_url = f"https://t.me/{target_username}"

    row1 = types.InlineKeyboardButton("⏪ Назад", callback_data="faq_back")
    row2 = types.InlineKeyboardButton("💬 Обратиться в поддержку", url=profile_url, callback_data="contact_support")

    markup.add(row1)
    markup.add(row2)

    return markup