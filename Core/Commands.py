import aiosqlite
from telebot.async_telebot import AsyncTeleBot
from Core.keyboards import *
from Core.Databases import *
from Core.text import text
from Core.MarazbanFunctions import mGetKayUser  # Добавьте этот импорт

from telebot import types as async_types

# Асинхронные функции обработки команд

async def start_command(message, bot):
    user_id = message.from_user.id
    await add_user(user_id)
    await bot.send_message(message.chat.id, "Вы зарегистрированы!", reply_markup=keyboard_start())
    await bot.send_message(message.chat.id, "Привет! Выбери один из вариантов ниже:", reply_markup=keyboard_start())

async def info_vpn_command(message, bot):
    await bot.send_message(message.chat.id, text["info_vpn_command_text"])

async def buy_subscription_command(message, bot):
    await bot.send_message(message.chat.id, text["buy_subscription_command_text"], reply_markup=purchase_a_subscription())

async def help_command(message, bot):
    await bot.send_message(message.chat.id, text["help_command_text"], reply_markup=help_menu())

async def back_command(message, bot):
    await bot.send_message(message.chat.id, "Выбери один из вариантов ниже:", reply_markup=keyboard_start())

async def invite_friend(message, bot):
    await bot.send_message(message.chat.id, "Вы можете пригласить друга, и вы оба получите вознаграждение! (в разработке)")

async def vpn_key(message, bot):
    if await info_user(message.from_user.id, 1) != 0:
        kay = await mGetKayUser(message.from_user.id)
        await bot.send_message(message.chat.id, f"{message.from_user.id}     {kay}")
    else:
        await bot.send_message(message.chat.id, "Вы не подключены")

async def user_balance(message, bot):
    user_id = message.from_user.id
    print(user_id)
    async with aiosqlite.connect('vpn_bot.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        results = await cursor.fetchall()
        
        for row in results:
            await bot.send_message(message.chat.id, f"Ваш Баланс: {row[1]}р 💸")
            print(row[2])

# Словарь команд (теперь хранит асинхронные функции)
COMMANDS = {
    "/start": start_command,
    "Информация о VPN 📜": info_vpn_command,
    "Получить Ключ 🔑": vpn_key,
    "Пополнить баланс 💰️": buy_subscription_command,
    "Баланс 🏦": user_balance,
    "Помощь 🛟": help_command,
    "Назад ⏪": back_command,
    "Партнерка 🤝": invite_friend
}

# Асинхронные функции обработки callback кнопок
async def help_faq(callback, bot):
    await bot.send_message(callback.message.chat.id, "Что вас интересует?", reply_markup=frequent_questions())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def payment_problems(callback, bot):
    await bot.send_message(callback.message.chat.id, text["payment_problems_text"], reply_markup=back_to_faq_keyboard())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def low_speed_problems(callback, bot):
    await bot.send_message(callback.message.chat.id, text["low_speed_problems"], reply_markup=back_to_faq_keyboard())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def vpn_no_work(callback, bot):
    await bot.send_message(callback.message.chat.id, text["vpn_no_work"], reply_markup=back_to_faq_keyboard())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def help_install(callback, bot):
    await bot.send_message(callback.message.chat.id, "Выберите вашу ОС:", reply_markup=guide_menu())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def help_android(callback, bot):
    await bot.send_message(callback.message.chat.id, "В разработке...")
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def help_apple(callback, bot):
    await bot.send_message(callback.message.chat.id, "Выберите ваше устройство Apple:", reply_markup=apple_menu())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def help_pc(callback, bot):
    await bot.send_message(callback.message.chat.id, "В разработке...")
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def help_support(callback, bot):
    await bot.send_message(callback.message.chat.id, "Переходим на страницу поддержки")
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def help_back(callback, bot):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text["help_command_text"],
        reply_markup=help_menu()
    )

async def back_to_faq(callback, bot):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Что вас интересует?",
        reply_markup=frequent_questions()
    )

async def help_back_apple(callback, bot):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выберите вашу ОС:",
        reply_markup=guide_menu()
    )

async def pay_delete(callback, bot):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

# Словарь callback-кнопок (теперь хранит асинхронные функции)
CALLBACKS = {
    "frequent_questions": help_faq,
    "payment_problems": payment_problems,
    "low_speed_problems": low_speed_problems,
    "vpn_no_work": vpn_no_work,
    "installation_instructions": help_install,
    "help_android": help_android,
    "help_iphone": help_apple,
    "help_pc": help_pc,
    "contact_support": help_support,
    "guide_back": help_back,
    "faq_back": back_to_faq,
    "help_back_apple": help_back_apple,
    "pay_delete": pay_delete,
}

# Основная асинхронная обработка команд и callback кнопок
async def CommandProcessing(message=None, bot=None, callback=None):
    if message:
        command_function = COMMANDS.get(message.text)
        if command_function:
            await command_function(message, bot)
        else:
            await bot.send_message(message.chat.id, "В разработке...")

    elif callback and callback.message:
        callback_function = CALLBACKS.get(callback.data)
        if callback_function:
            await callback_function(callback, bot)
        else:
            await bot.send_message(callback.message.chat.id, "В разработке...")