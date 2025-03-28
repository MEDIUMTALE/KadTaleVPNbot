import asyncio
import aiosqlite
from datetime import datetime
from yookassa import Payment

async def check_add(check_id, amount, user_id, date, status):
    async with aiosqlite.connect('vpn_bot.db') as conn:
        cursor = await conn.cursor()
        
        # Добавляем Чек
        
        await cursor.execute('''
            INSERT OR IGNORE INTO checks (check_id, user_id, amount, status, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (check_id, user_id, float(amount), status, date))
        
        await conn.commit()
        
        # Асинхронный вызов функции добавления пользователя


