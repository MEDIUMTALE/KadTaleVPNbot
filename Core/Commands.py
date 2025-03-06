from Core.keyboards import *  # импорт клавиатур
from Core.Databases import add_user  # добавление пользователей
from Core.text import text # импорт текстового массива

# функции обработки команд
def start_command(message, bot):
    user_id = message.from_user.id
    add_user(user_id)
    bot.send_message(message.chat.id, "Вы зарегистрированы!", reply_markup=keyboard_start())
    bot.send_message(message.chat.id, "Привет! Выбери один из вариантов ниже:", reply_markup=keyboard_start())

def info_vpn_command(message, bot):
    bot.send_message(message.chat.id, text["info_vpn_command_text"])

def buy_subscription_command(message, bot):
    bot.send_message(message.chat.id, text["buy_subscription_command_text"], reply_markup=purchase_a_subscription())

def help_command(message, bot):
    bot.send_message(message.chat.id, text["help_command_text"], reply_markup=help_menu())

def back_command(message, bot):
    bot.send_message(message.chat.id, "Выбери один из вариантов ниже:", reply_markup=keyboard_start())

def invite_friend(message, bot):
    bot.send_message(message.chat.id, "Вы можете пригласить друга, и вы оба получите вознаграждение! (в разработке)")

# словарь команд
COMMANDS = {
    "/start": start_command,
    "Информация о VPN 📜": info_vpn_command,
    "Пополнить баланс 💰️": buy_subscription_command,
    "Помощь 🛟": help_command,
    "Назад ⏪": back_command,
    "Партнерка 🤝" : invite_friend
}

# функции обработки callback кнопок
def help_faq(callback, bot): # часто задаваемые вопросы (faq)
    bot.send_message(callback.message.chat.id, "Что вас интересует?", reply_markup = frequent_questions())
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def payment_problems(callback, bot): # faq - проблемы с платежами
    bot.send_message(callback.message.chat.id, text["payment_problems_text"], reply_markup=back_to_faq_keyboard())  # Исправленное имя функции
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def low_speed_problems(callback, bot): # faq - низкая скорость
    bot.send_message(callback.message.chat.id, text["low_speed_problems"], reply_markup=back_to_faq_keyboard())
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def vpn_no_work(callback, bot): # faq - впн не работает
    bot.send_message(callback.message.chat.id, text["vpn_no_work"], reply_markup=back_to_faq_keyboard())
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


# гайд меню по установке vpn на разные устройства
def help_install(callback, bot): # меню выбора помощи по установке
    bot.send_message(callback.message.chat.id, "Выберите вашу ОС:", reply_markup = guide_menu())
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_android(callback, bot): # инструкция по устройствам android
    bot.send_message(callback.message.chat.id, "В разработке...")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_apple(callback, bot): # инструкции по устройствам apple
    bot.send_message(callback.message.chat.id, "Выберите ваше устройство Apple:", reply_markup=apple_menu())
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_pc(callback, bot): # инструкции по компьютеру
    bot.send_message(callback.message.chat.id, "В разработке...")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_tv(callback, bot): # инструкция по android TV
    bot.send_message(callback.message.chat.id, "В разработке...")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_support(callback, bot):
    bot.send_message(callback.message.chat.id, "Переходим на страницу поддержки")
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

def help_back(callback, bot): # возвращение из часто задаваемых вопросов в меню помощи
    bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= text["help_command_text"],reply_markup=help_menu())  # главное меню помощи

def back_to_faq(callback, bot): # возвращение из пунктов faq в faq
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Что вас интересует?", reply_markup=frequent_questions())

def help_back_apple(callback, bot): # возвращение из меню выбора устроиств apple в полное меню выбора устройств
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Выберите вашу ОС:", reply_markup=guide_menu()) # главное меню помощи

def pay_delete(callback, bot): # удаление визуального сообщения для пополнения (временно)
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

# словарь callback-кнопок
CALLBACKS = {
    "frequent_questions": help_faq, # faq - часто задаваемые вопросы
    "payment_problems": payment_problems, # faq - проблемы с платежом
    "low_speed_problems" : low_speed_problems, # faq - низкая скорость vpn
    "vpn_no_work": vpn_no_work,  # faq - vpn не работает

    "installation_instructions": help_install, # инструкция по установке
    "help_android": help_android, # помощь клиентам андроид
    "help_iphone": help_apple, # помощь клиентам apple (iphone, macOS, iPad)
    "help_pc": help_pc, # помощь клиентам PC (windows)
    "help_tv": help_tv, # помощь клиентам TV (Android TV)
    "contact_support": help_support, # связь с поддержкой
    "guide_back": help_back, # возвращение назад
    "faq_back": back_to_faq, # возвращение в меню faq
    "help_back_apple": help_back_apple, # возвращение назад из меню устройств apple

    "pay_delete": pay_delete, # удаление платежа (временно)
}



# основная обработка команд и callback кнопок
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