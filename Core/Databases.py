import aiosqlite
from datetime import datetime

async def add_user(user_id):
    from Core.MarazbanFunctions import mAddUser
    
    now = datetime.now()
    date_str = f"{now.day}.{now.month}.{now.year}-{now.hour}:{now.minute}"
    
    async with aiosqlite.connect('vpn_bot.db') as conn:
        cursor = await conn.cursor()
        
        # Проверяем существование пользователя
        await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        results = await cursor.fetchall()
        
        if results:  # Если пользователь уже существует
            print("User Есть в бд")
            return
        else:
            # Добавляем нового пользователя
            await cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, balance)
                VALUES (?, ?)
            ''', (user_id, 15))
            
            await cursor.execute('''
                INSERT OR IGNORE INTO logs (type, text, date)
                VALUES (?, ?, ?)
            ''', ("Registration", f"user_id: {user_id}, user_id: '{user_id}' зарегистрировался", date_str))
            
            await conn.commit()
            
            # Асинхронный вызов функции добавления пользователя
            await mAddUser(user_id)

async def info_user(user_id, cal):
    async with aiosqlite.connect('vpn_bot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        results = await cursor.fetchall()
        
        if results:  # Если пользователь найден
            return results[0][cal]  # Возвращаем запрошенное поле
        return None  # Или можно вызвать исключение, если пользователь не найден
    
async def info_settings(cal):
    async with aiosqlite.connect('vpn_bot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM settings WHERE id = ?", (0,))
        results = await cursor.fetchall()
        
        if results:  # Если пользователь найден
            return results[0][cal]  # Возвращаем запрошенное поле
        return None  # Или можно вызвать исключение, если пользователь не найден
    
async def add_logs(type, text):
    now = datetime.now()
    date_str = f"{now.day}.{now.month}.{now.year}-{now.hour}:{now.minute}"

    async with aiosqlite.connect('vpn_bot.db') as conn:
        cursor = await conn.cursor()

        await cursor.execute('''
                INSERT OR IGNORE INTO logs (type, text, date)
                VALUES (?, ?, ?)
            ''', (f"{type}", f"{text}", date_str))
            
        await conn.commit()


async def user_chage_Balance(user_id, value):
    async with aiosqlite.connect('vpn_bot.db') as conn:
        cursor = await conn.cursor()
        #await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        await cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (value, user_id))
        await conn.commit()