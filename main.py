import asyncio
from datetime import datetime
import aiosqlite  # Асинхронная замена для sqlite3
from telebot.async_telebot import AsyncTeleBot  # Асинхронная версия telebot

from Core.Commands import CommandProcessing
from Core.Databases import *
from Core.MarazbanFunctions import *

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"
bot = AsyncTeleBot(token)

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

<<<<<<< HEAD
                            balance = user_row[1] - tariffDay
                            balance = max(balance, 0)  # Заменяем if balance<=0: balance=0
=======
                        connection = sqlite3.connect('vpn_bot.db')
                        cursor = connection.cursor()
                        cursor.execute('''
                            INSERT OR IGNORE INTO logs (type, text, date)
                            VALUES (?, ?, ?)
                        ''', ("NewDayMinusMoney", f"user_id: {row[0]}, Money {row[1]} - 3 = {balance}", f"{day}.{mon}.{year}-{h}:{m}"))
                        connection.commit()
                        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance ,row[0]))
                        connection.commit()
>>>>>>> parent of 9b12d4e (fix)

                            await cursor.execute('''
                                INSERT OR IGNORE INTO logs (type, text, date)
                                VALUES (?, ?, ?)
                            ''', ("NewDayMinusMoney", f"user_id: {user_row[0]}, Money {user_row[1]} - {tariffDay} = {balance}", f"{day}.{mon}.{year}-{h}:{m}"))
                            await connection.commit()
                            
                            await cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_row[0]))
                            await connection.commit()

                            if await info_user(user_row[0], 1) == 0:
                                #await mDelUser(user_row[0])
                                print(f"User id Dell {user_row[0]}")

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