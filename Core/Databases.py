import sqlite3
from datetime import datetime

now = datetime.now()
day = now.day
mon = now.month
year = now.year
h = now.hour
m = now.minute

def add_user(user_id):
    conn = sqlite3.connect('vpn_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    conn.close()
    # Проверяем, есть ли результаты
    if results:  # Если список не пуст
        print("User Есть в бд")
        return
    else:
        conn = sqlite3.connect('vpn_bot.db')
        cursor = conn.cursor()

        # Вставляем пользователя, если его еще нет
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, has_trial, balance)
            VALUES (?, ?, ?)
        ''', (user_id, False, 0))
        conn.commit()
        cursor.execute('''
            INSERT OR IGNORE INTO logs (type, text, date)
            VALUES (?, ?, ?)
        ''', ("Registration", f"user_id: {user_id}, user_id: '{user_id}' зарегистрировался", f"{day}.{mon}.{year}-{h}:{m}"))
        conn.commit()

    conn.close()

def info_user(user_id, cal):
    connection = sqlite3.connect('vpn_bot.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    connection.close()
    # Проверяем, есть ли результаты
    if results:  # Если список не пуст
        for row in results:
            return row[cal]
