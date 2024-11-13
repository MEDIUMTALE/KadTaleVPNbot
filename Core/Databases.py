import sqlite3


def init_db():
    conn = sqlite3.connect('vpn_bot.db')
    cursor = conn.cursor()

    # Создаём таблицу пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            has_trial BOOLEAN,
            active_until DATE
        )
    ''')

    # Создаём таблицу подписок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            key TEXT,
            region TEXT,
            protocol TEXT,
            active_until DATE,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('vpn_bot.db')
    cursor = conn.cursor()

    # Вставляем пользователя, если его еще нет
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, has_trial, active_until)
        VALUES (?, ?, ?)
    ''', (user_id, False, None))

    conn.commit()
    conn.close()