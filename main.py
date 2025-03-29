import asyncio
from datetime import datetime
import aiosqlite
from telebot.async_telebot import AsyncTeleBot 
from telebot.types import LabeledPrice, Message
from telebot import types

from Core.Commands import CommandProcessing
from Core.keyboards import keyboard_start

from Core.Databases import *
from Core.MarazbanFunctions import *

from Core.YooKassa import check_payment_status
from yookassa import Payment

token = "7662636396:AAGcWhdrmXkbYFKWkOWYCweQ5WDgsI622W4"
#token = "6120629335:AAF8ERXPC7rCzWccZbKwi1WxODAzqBPObx8"
bot = AsyncTeleBot(token)





#обработчик облаты
@bot.callback_query_handler(func=lambda call: call.data.startswith('check_'))
async def check_payment_callback(call: types.CallbackQuery):
    """Обработчик проверки платежа"""
    try:
        if not call or not call.message:
            return

        payment_id = call.data.split('_')[1]
        chat_id = call.message.chat.id
        #user_id = call.message.from_user.id
        
        payment = Payment.find_one(payment_id)

        amout = payment.amount.value
        
        #metadata = getattr(payment, 'metadata', None)  # Безопасное получение metadata

        user_id = payment.metadata.get('user_id')

        # Отвечаем на callback
        await bot.answer_callback_query(call.id)

        # Проверяем статус
        status = await check_payment_status(payment_id)
        
        print(user_id)

        if status == "succeeded":
            # Удаляем исходное сообщение
            await bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            
            await check_add(payment.id, amout, user_id, payment.created_at, status)

            markup = await keyboard_start(user_id)


            row1 = types.InlineKeyboardButton("🛠 Инструкция по установке VPN", callback_data="installation_instructions")

            markup.add(row1)

            await bot.send_message(
                chat_id,
                "✅ Платеж успешно завершен! Баланс пополнен.",
                reply_markup=markup
            )

            balance = await info_user(user_id, 1) + int(amout)

            await add_logs("Pay_Balance", f"user_id: {user_id}, amount: {int(amout)}р, payment.id: {payment.id}")

            await user_chage_Balance(user_id, balance)
            
            if await mGetKayUser(user_id) == "Вы не подключенны к тарифу 😟":
                await mAddUser(user_id)
            
            
        elif status == "pending":
            await bot.send_message(
                chat_id,
                "⌛ Платеж еще обрабатывается. Попробуйте позже.",
                reply_markup= await keyboard_start(user_id)
            )


        else:
            await check_add(payment.id, amout, user_id, payment.created_at, status)

            await bot.send_message(
                chat_id,
                "❌ Платеж не был завершен или произошла ошибка.",
                reply_markup=keyboard_start(user_id)
            )
        print(f"chat_id: {chat_id}\namout: {amout}\nuser_id: {user_id}\npayment.created_at: {payment.created_at}")
    
    except Exception as e:
        print(f"Ошибка в обработчике callback: {e}")
        try:
            await bot.send_message(
                chat_id,
                "⚠️ Произошла ошибка при проверке платежа."
            )
        except:
            pass






# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
async def handle_buttons(message):
    await CommandProcessing(message, bot)

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda callback: True)
async def callback_message(callback):
    await CommandProcessing(callback=callback, bot=bot)

async def run_periodically():
    while True:
        await fetch_data(bot)
        await asyncio.sleep(60)

async def run_bot():
    await bot.polling(none_stop=True)

async def main():
    # Создаем задачи для одновременного выполнения
    bot_task = asyncio.create_task(run_bot())
    periodic_task = asyncio.create_task(run_periodically())
    
    # Ожидаем завершения обеих задач (хотя они бесконечные)
    await asyncio.gather(bot_task, periodic_task)

if __name__ == "__main__":
    # Инициализация базы данных (если нужно)
    # await init_db()  # Убедитесь, что init_db тоже асинхронная
    
    # Запускаем асинхронное приложение
    asyncio.run(main())
