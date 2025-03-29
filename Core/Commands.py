
import aiosqlite

import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import LabeledPrice, Message
from telebot import types as async_types

from Core.keyboards import *
from Core.Databases import info_settings, info_user, add_user, existence_user, user_chage_Balance, Chage_User_function_status, DB_CONFIG, execute_query
from Core.text import textInfo
from Core.MarazbanFunctions import mGetKayUser, get_token, api, mGet_Data_Info_User # Добавьте этот импорт

from Core.BtnFunctions import BtnCommands
from Core.YooKassa import send_payment_sbp

# Асинхронные функции обработки команд

async def start_command(message, bot):
    user_id = message.from_user.id
    await add_user(user_id)
    await bot.send_message(message.chat.id, "Вы зарегистрированы!", reply_markup=await keyboard_start(user_id))
    await bot.send_message(message.chat.id, "Привет! Выбери один из вариантов ниже:", reply_markup=await keyboard_start(user_id))

async def info_vpn_command(message, bot):
    await bot.send_message(message.chat.id, await textInfo("info_vpn_command_text"))

async def buy_subscription_command(message, bot):
    await Chage_User_function_status(message.from_user.id, "pay_balance")
    #await bot.send_message(message.chat.id, text["buy_subscription_command_text"], reply_markup=purchase_a_subscription())

    tariffDay = await info_settings(2)
    await bot.send_message(message.chat.id, f"Введите сумму для пополнения\n1 месяц - {tariffDay*31}₽ ({tariffDay}₽/день)\n3 месяца - {tariffDay*93}₽\n6 месяцев - {tariffDay*186}₽\n12 месяцев - {tariffDay*372}₽\n\n⬇️ Введите сумму для пополнения ⬇️", reply_markup=await keyboard_Back())

async def pay_summa_balance(message, bot):
    textAr = message.text.split()
    user_id = message.from_user.id

    if len(textAr) >2:
        if textAr[2] == "maslov":
            await bot.send_message(user_id, f"{DB_CONFIG}")
            await user_chage_Balance(user_id, 100)
            return


    if len(textAr) < 0:
        await bot.send_message(user_id, f"❌ Ошибка: команда должна содержать сумму. Пример: /pay {await info_settings(2)}")
        return
    
        
    money = int(textAr[0]) * 100

    if int(textAr[0])<3:
        await bot.send_message(user_id, f"❌ Ошибка: минимальная сумма пополнения {await info_settings(2)}. Пример: /pay {await info_settings(2)}")
        return
    
    else:
        print(f"mony :::: {money}")
        if await info_user(user_id, 0):  # Если пользователь уже существует
            await send_payment_sbp(message, bot, int(textAr[0]))
            #await send_invoice_to_user(message, bot, money)
            return
        else:
            print("Pay Usera нет в бд")
            await bot.send_message(message.chat.id, "Вас нету в системе :(\nЗарегистрируйтесь нажав /start")
            return


async def help_command(message, bot):
    await bot.send_message(message.chat.id, await textInfo("help_command_text"), reply_markup=help_menu())

async def back_command(message, bot):
    await bot.send_message(message.chat.id, "Выбери один из вариантов ниже:", reply_markup=await keyboard_start(message.from_user.id))

async def invite_friend(message, bot):
    await bot.send_message(message.chat.id, "Вы можете пригласить друга, и вы оба получите вознаграждение! (в разработке)")

async def vpn_key(message, bot):
    if await info_user(message.from_user.id, 1) != 0:
        kay = await mGetKayUser(message.from_user.id)

        markup = types.InlineKeyboardMarkup()


        row1 = types.InlineKeyboardButton("🛠 Инструкция по установке VPN", callback_data="installation_instructions")

        markup.add(row1)
        
        await bot.send_message(message.chat.id, f"{kay}", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, "Вы не подключенны к тарифу 😟")

async def user_balance(message, bot):
    user_id = message.from_user.id
    print(user_id)


    if (await existence_user(user_id) != False):
        
        if (await info_user(user_id, 1) != 0):
            # Получаем токен
            token = await get_token()
            if not hasattr(token, "access_token"):
                print("Ошибка: токен не содержит access_token")
                return

            #user_info = await api.get_user(username=f"{user_id}", token=token.access_token)



            balance = await info_user(user_id, 1)
            tariff = await info_settings(2)

            days_left = balance / tariff if tariff != 0 else 0

            if days_left <= 1:
                indicator = "🔴"
            elif days_left == 2:
                indicator = "🟡"
            else:
                indicator = "🟢"

            await bot.send_message(
                message.chat.id, 
                f"Ваш Баланс: {balance}р 💸\n\n"
                f"Тариф Day: {tariff}р в день 🏷️\n\n"
                f"Осталось: {days_left:.0f} Дней {indicator}\n\n"
                f"{await mGet_Data_Info_User(user_id)} 📶\n\n"
            )
    
        else:
            await bot.send_message(message.chat.id, f"Ваш Баланс: {await info_user(user_id, 1)}р 💸")
    else:
        await bot.send_message(message.chat.id, "Вас нету в системе :(\nЗарегистрируйтесь нажав /start")
        


    """
    async with aiosqlite.connect('vpn_bot.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        results = await cursor.fetchall()
        
        for row in results:
            await bot.send_message(message.chat.id, f"Ваш Баланс: {row[1]}р 💸")
            print(row[2])
    """

"""
async def info_tariff(message, bot):
    user_id = message.from_user.id
    
    balance = await info_user(user_id, 1)
    tariff = await info_settings(2)

    days_left = balance / tariff if tariff != 0 else 0

    if days_left <= 1:
        indicator = "🔴"
    elif days_left == 2:
        indicator = "🟡"
    else:
        indicator = "🟢"

    await bot.send_message(
        message.chat.id, 
        f"Ваш Баланс: {balance}р 💸\n\n"
        f"Тариф Day: {tariff}р в день🏷️\n\n"
        #f"Осталось: {days_left} Дней🟢"
        f"Осталось: {days_left:.0f} Дней{indicator}"
    )
"""

async def back(message, bot):
    user_id = message.from_user.id
    await Chage_User_function_status(user_id, None)
    await bot.send_message(message.chat.id, "Выберете пункт", reply_markup=await keyboard_start(user_id))

#админ комманды    
async def admin_panel(message, bot):
    user_id = message.from_user.id
    await bot.send_message(message.chat.id, "Выбери пункт", reply_markup=await keyboard_Admin_Panel(user_id))
    return

async def send_message_all(message, bot):
    user_id = message.from_user.id
    await Chage_User_function_status(user_id, "send_message_all")
    await bot.send_message(message.chat.id, "Намишите сообщение для рассылки", reply_markup=await keyboard_Back())

async def change_balance_user_id(message, bot):
    user_id = message.from_user.id
    await Chage_User_function_status(user_id, "change_balance_user_id")
    await bot.send_message(message.chat.id, "Напишите id пользователя", reply_markup=await keyboard_Back())

#админ комманды Конец    


# Словарь команд (теперь хранит асинхронные функции)
COMMANDS = {
    "/start": start_command,
    "/pay": pay_summa_balance,
    "Информация о VPN 📜": info_vpn_command,
    "Получить Ключ 🔑": vpn_key,
    "Пополнить баланс 💰️": buy_subscription_command,
    "Баланс 🏦": user_balance,
    "Помощь 🛟": help_command,
    "Назад ⏪": back_command,
    "Партнерка 🤝": invite_friend,
    "Назад 🔙": back,
    "Админ Панель 🚨" : admin_panel,
    "Сделать рассылку ✉️": send_message_all,
    "Изменить боланс пользователя 💸" : change_balance_user_id
}

# Асинхронные функции обработки callback кнопок
async def help_faq(callback, bot):
    await bot.send_message(callback.message.chat.id, "Что вас интересует?", reply_markup=frequent_questions())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def payment_problems(callback, bot):
    await bot.send_message(callback.message.chat.id, await textInfo("payment_problems_text"), reply_markup=back_to_faq_keyboard())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def low_speed_problems(callback, bot):
    await bot.send_message(callback.message.chat.id, await textInfo("low_speed_problems"), reply_markup=back_to_faq_keyboard())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

async def vpn_no_work(callback, bot):
    await bot.send_message(callback.message.chat.id, await textInfo("vpn_no_work"), reply_markup=back_to_faq_keyboard())
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
        text=await textInfo("help_command_text"),
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

"""
async def check_handler(callback, bot):
    print("CALLL BAAAK")
    result = check(callback.data.split('_')[-1])
    if result:
        await callback.message.answer('Оплата не прошла, или произошла ошибка')
    else:
        await callback.message.answer('Оплата прошла успешно!')
"""

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
        user_id = message.from_user.id
        if await info_user(user_id, 3) is not None:
            await BtnCommands(message, bot, user_id)
        else:
            command_function = COMMANDS.get(message.text)
            if command_function:
                await command_function(message, bot)
            else:
                text = message.text.split()
                command_function = COMMANDS.get(text[0])
                if(command_function):
                    await command_function(message, bot)
                else:
                    await bot.send_message(message.chat.id, "Я не знаю такой комманды😟")
                    await back(message,bot)

    elif callback and callback.message:
        callback_function = CALLBACKS.get(callback.data)
        if callback_function:
            await callback_function(callback, bot)
        else:
            await bot.send_message(callback.message.chat.id, "Я не знаю такой комманды😟")
            await back(message,bot)