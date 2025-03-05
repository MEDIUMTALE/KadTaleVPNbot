import telebot
from telebot import types
from Core.keyboards import *  # Импорт клавиатур
from Core.Databases import add_user  # Добавление пользователей

# Текст информации о VPN
info_about_vpn_text = "⚔️ KadTaleVPN ⚔️\n\n🔹 Мгновенный и удобный VPN прямо в Telegram\n\n✅ Доступ к Instagram, YouTube, TikTok и др.\n\n🚀 Высокая скорость без рекламы\n\n🛜 Стабильное соединение\n\n💳 Оплата картами РФ и СБП\n\n⚡️ Шифрование трафика и скрытие IP"

### 🔹 Функции обработки команд
def start_command(message, bot):
    user_id = message.from_user.id
    add_user(user_id)
    bot.send_message(message.chat.id, "Вы зарегистрированы!", reply_markup=keyboard_start())
    bot.send_message(message.chat.id, "Привет! Выбери один из вариантов ниже:", reply_markup=keyboard_start())

def info_vpn_command(message, bot):
    bot.send_message(message.chat.id, info_about_vpn_text)

def buy_subscription_command(message, bot):
    bot.send_message(message.chat.id, "Выберите вариант подписки:", reply_markup=purchase_a_subscription())

def help_command(message, bot):
    bot.send_message(message.chat.id, "Меню помощи:\n\nВ случае если вы не нашли ответ на вопрос здесь, можете написать в нашу поддержку, которая вам с радостью поможет!", reply_markup=help_menu())

def back_command(message, bot):
    bot.send_message(message.chat.id, "Привет! Выбери один из вариантов ниже:", reply_markup=keyboard_start())

def language_command(message, bot):
    bot.send_message(message.chat.id, "Пожалуйста, выберите язык:", reply_markup=language_choice())

def invite_friend(message, bot):
    bot.send_message(message.chat.id, "Вы можете пригласить друга, и вы оба получите вознаграждение! (в разработке)")
# Словарь команд
COMMANDS = {
    "/start": start_command,
    "Информация о VPN 📜": info_vpn_command,
    "Пополнить баланс ⚔️": buy_subscription_command,
    "Помощь 🛟": help_command,
    "Назад ⏪": back_command,
    "Язык 🗺️": language_command,
    "Партнерка 🤝" : invite_friend
}

### 🔹 Функции обработки callback-кнопок
def help_faq(callback, bot):
    bot.send_message(callback.message.chat.id, "В разработке...")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_install(callback, bot):
    bot.send_message(callback.message.chat.id, "Выберите ОС:", reply_markup=guide_menu())
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_android(callback, bot):
    bot.send_message(callback.message.chat.id, "В разработке...")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_iphone(callback, bot):
    bot.send_message(callback.message.chat.id, "В разработке...")

    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_pc(callback, bot):
    bot.send_message(callback.message.chat.id, "В разработке...")

    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_tv(callback, bot):
    bot.send_message(callback.message.chat.id, "В разработке...")

    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_support(callback, bot):
    bot.send_message(callback.message.chat.id, "Переходим на страницу поддержки")

    bot.delete_message(callback.message.chat.id, callback.message.message_id)
def language_ru(callback, bot):
    bot.send_message(callback.message.chat.id, "Локализация в процессе")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def language_en(callback, bot):
    bot.send_message(callback.message.chat.id, "Локализация в процессе")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

# словарь callback-кнопок
CALLBACKS = {
    "frequent_questions": help_faq, # часто задавемые вопросы
    "installation_instructions": help_install, # инструкция по установке
    "help_android": help_android, # помощь клиентам андроид
    "help_iphone": help_iphone, # помощь клиентам apple (iphone, macOS, iPad)
    "help_pc": help_pc, # помощь клиентам PC (windows)
    "help_tv": help_tv, # помощь клиентам TV (Android TV)
    "contact_support": help_support, # связь с поддержкой
    "language_ru": language_ru, # смена языка на русский
    "language_en": language_en, # смена языка на английский
}

### 🔹 Основная обработка команд и callback-кнопок
def CommandProcessing(message=None, bot=None, callback=None):
    if message:
        command_function = COMMANDS.get(message.text)
        if command_function:
            command_function(message, bot)
        else:
            bot.send_message(message.chat.id, "В разработке...")

    elif callback and callback.message:
        callback_function = CALLBACKS.get(callback.data)
        if callback_function:
            callback_function(callback, bot)
        else:
            bot.send_message(callback.message.chat.id, "В разработке...")