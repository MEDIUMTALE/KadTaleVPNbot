import telebot
from Core.Commands import CommandProcessing  # Правильный импорт функции
import sqlite3
from datetime import datetime
import asyncio
import threading
from Core.Databases import *

# вызов функции для инициализации базы данных и создания таблиц
#init_db()

token = "7622209066:AAFoZZanqTXQZdK8fwXHqngmcOUAiUHZxpc"
bot = telebot.TeleBot(token)

# Обработчик нажатий на все кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    CommandProcessing(message, bot)  # передаем message

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    CommandProcessing(callback=callback, bot=bot)  # передаем callback

def fetch_data():
    connection = sqlite3.connect('vpn_bot.db')
    cursor = connection.cursor()
    cursor.execute("SELECT date FROM settings WHERE id = ?", (0,))
    results = cursor.fetchall()
    connection.close()
    # Проверяем, есть ли результаты
    if results:  # Если список не пуст
        for row in results:
            now = datetime.now()
            day = now.day
            mon = now.month
            year = now.year
            h = now.hour
            m = now.minute

            if row[0] != day:
                connection = sqlite3.connect('vpn_bot.db')
                cursor = connection.cursor()
                cursor.execute("UPDATE settings SET date = ? WHERE id = 0", (day,))
                connection.commit()
                connection.close()
                print("День изменён")

                
                connection = sqlite3.connect('vpn_bot.db')
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id IS NOT NULL")
                results = cursor.fetchall()
                connection.close()
                
                if results:  # Если список не пуст
                    for row in results:
                        print(row[1])

                        balance = row[1] - 3

                        if balance<=0:
                            balance=0

                        connection = sqlite3.connect('vpn_bot.db')
                        cursor = connection.cursor()
                        cursor.execute('''
                            INSERT OR IGNORE INTO logs (type, text, date)
                            VALUES (?, ?, ?)
                        ''', ("NewDayMinusMoney", f"user_id: {row[0]}, Money {row[1]} - 3 = {balance}", f"{day}.{mon}.{year}-{h}:{m}"))
                        connection.commit()
                        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance ,row[0]))
                        connection.commit()
                        connection.close()

            else:
                print("День Софподает")
                
    else:
        print("Нет данных для id = 0")


async def run_periodically():
    while True:
        fetch_data()  # Выполняем действие
        await asyncio.sleep(60)  # Ждём 60 секунд


def run_bot():
    bot.polling(none_stop=True)


# Основная асинхронная функция
async def main():
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Запускаем периодическую задачу
    await run_periodically()  # Используем await для вызова корутины

if __name__ == "__main__":
    asyncio.run(main())  # Запускаем асинхронный цикл