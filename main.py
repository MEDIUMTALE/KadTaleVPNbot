import asyncio
from datetime import datetime
import aiosqlite  # Асинхронная замена для sqlite3

from telebot.async_telebot import AsyncTeleBot  # Асинхронная версия telebot
from telebot.types import LabeledPrice, Message
from telebot import types

from Core.Commands import CommandProcessing
from Core.Databases import *
from Core.MarazbanFunctions import *

from Core.YooKassa import check_payment_status
from yookassa import Payment

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"
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

            await bot.send_message(
                chat_id,
                "✅ Платеж успешно завершен! Баланс пополнен."
            )


            balance = await info_user(user_id, 1) + int(amout)

            await user_chage_Balance(user_id, balance)

            if await mGetKayUser(user_id) == "Вы не подключенны к тарифу😟":
                await mAddUser(user_id)
            
        elif status == "pending":
            await bot.send_message(
                chat_id,
                "⌛ Платеж еще обрабатывается. Попробуйте позже."
            )
        else:
            await bot.send_message(
                chat_id,
                "❌ Платеж не был завершен или произошла ошибка."
            )

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

async def fetch_data():
    async with aiosqlite.connect('vpn_bot.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute("SELECT date FROM settings WHERE id = ?", (0,))
        results = await cursor.fetchall()
        
        if results:
            for row in results:
                now = datetime.now()
                day = now.day
                mon = now.month
                year = now.year
                h = now.hour
                m = now.minute


                if row[0] != day:
                    await cursor.execute("UPDATE settings SET date = ? WHERE id = 0", (day,))
                    await connection.commit()
                    print("День изменён")

                    await cursor.execute("SELECT * FROM users WHERE user_id IS NOT NULL")
                    user_results = await cursor.fetchall()
                    
                    if user_results:
                        for user_row in user_results:
                            print(user_row[1])

                            print(await info_settings(2))

                            tariffDay = await info_settings(2)

                            balance = user_row[1] - tariffDay
                            balance = max(balance, 0)  # Заменяем if balance<=0: balance=0

                            await cursor.execute('''
                                INSERT OR IGNORE INTO logs (type, text, date)
                                VALUES (?, ?, ?)
                            ''', ("NewDayMinusMoney", f"user_id: {user_row[0]}, Money {user_row[1]} - {tariffDay} = {balance}", f"{day}.{mon}.{year}-{h}:{m}"))
                            await connection.commit()
                            
                            await cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_row[0]))
                            await connection.commit()


                            if await info_user(user_row[0], 1) == 0:
                                await mDelUser(user_row[0])
                                print(f"User id Dell {user_row[0]}")
                            
                                #Уведомления
                                balance = await info_user(user_row[0], 1)
                                tariff = await info_settings(2)

                                days_left = balance / tariff if tariff != 0 else 0
                                                
                                print(f"days_left {days_left}")

                                if days_left >= 1 and days_left!=0:
                                    print(f"Message To Id{user_row[0]}")
                                    await bot.send_message(user_row[0], f"❗❗ У вас осталось {days_left:.0f} дней ❗❗\n\n🚨 Не забудьте продлить тариф 🚨")
                                elif days_left==0:
                                    print(f"ЫMessage To Id{user_row[0]}")
                                    await bot.send_message(user_row[0], f"❗❗ У вас осталось закончился тариф ❗❗\n\n🚨 Продлейте тариф 🚨")
                                #

                else:
                    print("День совпадает")
        else:
            print("Нет данных для id = 0")

async def run_periodically():
    while True:
        await fetch_data()
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
