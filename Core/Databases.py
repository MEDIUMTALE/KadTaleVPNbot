import asyncio
import aiomysql
from datetime import datetime
from pymysql.err import OperationalError

DB_CONFIG = {
    "host": "109.120.132.222",
    #"host": "127.0.0.1",
    "port": 3306,
    "user": "admin",
    #"user": "root",
    "password": "password",
    #"password": "",
    "db": "vpn_bot",
    "autocommit": True,
    "minsize": 1,
    "maxsize": 10,
    "connect_timeout": 10,
    "pool_recycle": 3600
}


pool = None

#print(DB_CONFIG)

async def create_pool():
    global pool
    while True:
        try:
            pool = await aiomysql.create_pool(**DB_CONFIG)
            print("Успешное подключение к базе данных")
            return pool
        except OperationalError as e:
            print(f"Ошибка подключения: {e}. Повторная попытка через 5 секунд...")
            await asyncio.sleep(5)

async def get_connection():
    """Получает соединение из пула с обработкой ошибок"""
    global pool
    if pool is None:
        await create_pool()
    
    try:
        return await pool.acquire()
    except OperationalError:
        # Если соединение разорвано, пересоздаем пул
        await create_pool()
        return await pool.acquire()

async def execute_query(query, args=None, retries=3):
    """Выполняет SQL запрос с автоматическим переподключением"""
    for attempt in range(retries):
        conn = None
        cursor = None
        try:
            conn = await get_connection()
            cursor = await conn.cursor()
            await cursor.execute(query, args or ())
            if query.strip().upper().startswith('SELECT'):
                return await cursor.fetchall()
            return True
        except OperationalError as e:
            print(f"Ошибка запроса (попытка {attempt + 1}): {e}")
            if attempt == retries - 1:
                raise
            await asyncio.sleep(1)
        finally:
            if cursor:
                await cursor.close()
            if conn:
                pool.release(conn)

async def add_user(user_id):
    from Core.MarazbanFunctions import mAddUser
    
    now = datetime.now()
    
    try:
        # Проверяем существование пользователя
        results = await execute_query(
            "SELECT * FROM users WHERE user_id = %s", 
            (user_id,)
        )
        
        if results:
            print("User уже есть в бд")
            return
        
        # Добавляем пользователя
        await execute_query(
            "INSERT IGNORE INTO users (user_id, balance) VALUES (%s, %s)",
            (user_id, await info_settings(5))
        )

        # Логируем действие
        await execute_query(
            "INSERT IGNORE INTO logs (type, text) VALUES (%s, %s)",
            ("Registration", f"user_id: '{user_id}' зарегистрировался")
        )
        
        await mAddUser(user_id)
    except Exception as e:
        print(f"Ошибка в add_user: {e}")

async def Chage_User_function_status(user_id, value):
    await execute_query(
        "UPDATE users SET functin_status = %s WHERE user_id = %s",
        (value, user_id)
    )

async def info_user(user_id, cal):
    results = await execute_query(
        "SELECT * FROM users WHERE user_id = %s", 
        (user_id,)
    )
    return results[0][cal] if results else None

async def existence_user(user_id):
    results = await execute_query(
        "SELECT * FROM users WHERE user_id = %s", 
        (user_id,)
    )
    return bool(results)

async def info_settings(cal):
    results = await execute_query(
        "SELECT * FROM settings WHERE id = %s", 
        (0,)
    )
    return results[0][cal] if results else None

async def add_logs(log_type, text):
    
    await execute_query(
        "INSERT IGNORE INTO logs (type, text) VALUES (%s, %s)",
        (log_type, text)
    )

async def user_chage_Balance(user_id, value):
    xpay = await info_settings(4)

    b = await info_user(user_id,1)
    await execute_query(
        "UPDATE users SET balance = %s WHERE user_id = %s",
        (value * xpay if xpay else value, user_id)
    )
    
    balance = await info_user(user_id,1) + value
    await execute_query(
        "INSERT IGNORE INTO logs (type, text) VALUES (%s, %s)",
        ("Balance_Add", f"user_id: {await info_user(user_id,0)}, Money: {b} + {value} = {balance}")
    )
async def user_chage_Referrer_Id(user_id, value):
    await execute_query(
        "UPDATE users SET referrer_id = %s WHERE user_id = %s",
        (value, user_id)
    )

async def fetch_data(bot):
    from Core.MarazbanFunctions import mDelUser
    try:
        results = await execute_query("SELECT date FROM settings WHERE id = %s", (0,))
        
        if results:
            now = datetime.now()

            date_str = now.strftime('%Y-%m-%d')
            print(date_str)
            print(results[0][0])
            if str(results[0][0]) != str(date_str):
                await execute_query("UPDATE settings SET date = %s WHERE id = 0", (f"{date_str}",))
                print("День изменён")

                user_results = await execute_query("SELECT * FROM users WHERE user_id IS NOT NULL")

                for user_row in user_results:
                    tariffDay = await info_settings(2)
                    balance = max(user_row[1] - tariffDay, 0)

                    await execute_query(
                        "INSERT IGNORE INTO logs (type, text) VALUES (%s, %s)",
                        ("NewDayMinusMoney", f"user_id: {user_row[0]}, Money {user_row[1]} - {tariffDay} = {balance}")
                    )

                    await execute_query(
                        "UPDATE users SET balance = %s WHERE user_id = %s",
                        (balance, user_row[0])
                    )

                    # Уведомления
                    balance = await info_user(user_row[0], 1)
                    tariff = await info_settings(2)
                    days_left = balance / tariff if tariff != 0 else 0

                    if days_left == 1:
                        await bot.send_message(user_row[0], 
                            f"❗❗ У вас остался {days_left:.0f} день ❗❗\n\n🚨 Не забудьте продлить тариф 🚨")
                    elif days_left == 0:
                        await bot.send_message(user_row[0], 
                            f"❗❗ У вас закончился тариф ❗❗\n\n🚨 Продлите тариф 🚨")

                    if await info_user(user_row[0], 1) == 0:
                        await mDelUser(user_row[0])
                        print(f"User id Dell {user_row[0]}")
            else:
                print("День совпадает")
        else:
            print("Нет данных для id = 0")
    except Exception as e:
        print(f"Ошибка в fetch_data: {e}")


#ТЕКСТ
async def info_text(name):
    results = await execute_query(
        "SELECT * FROM text WHERE name = %s", 
        (name,)
    )
    return results[0][2].replace("\\n", "\n") if results else None


#ЧЕКИ

async def check_add(check_id, amount, user_id, date, status):
    if(await check_exists(check_id) != True):
        await execute_query(
            "INSERT IGNORE INTO checks (check_id, user_id, amount, status, date) VALUES (%s, %s, %s, %s, %s)",
            (check_id, user_id, float(amount), status, date)
        )

async def check_exists(check_id):
    results = await execute_query(
        "SELECT * FROM checks WHERE check_id = %s", 
        (check_id,)
    )
    return bool(results)
#ЧЕКИ КОНЕЦ

#ВЫВОД ИНФОРАМАЦИИ О КОЛИЧЕСТВЕ ТВОИХ РЕФЕРАЛОВ

async def Referrer_Count(user_id):
    user_results = await execute_query("SELECT * FROM users WHERE referrer_id = %s", (user_id))
    return len(user_results)


#ВЫВОД ИНФОРАМАЦИИ О КОЛИЧЕСТВЕ ТВОИХ РЕФЕРАЛОВ КОНЕЦ


#АДМИН СБОР СТАТИСТИКИ

async def bInfo_Stats_Users():
    from Core.MarazbanFunctions import mGet_Data_Info_Stats_User
    user_results = await execute_query("SELECT * FROM users WHERE user_id IS NOT NULL")

    active_count = 0
    diseible_count = 0

    for user_row in user_results:
        try:
            id = user_row[0]
            Data = await mGet_Data_Info_Stats_User(id)
            print(f"Data = {Data}")
            if float(Data) > 0.1:
                active_count = active_count + 1
        except Exception as e:
            print(f"Error - {e}")
    
    diseible_count = len(user_results) - active_count
    
    return f"Активных пользователей: {active_count}\nМёртвых пользователей: {diseible_count}"

#АДМИН СБОР СТАТИСТИКИ КОНЕЦ

#ДЕНЬГИ ЗА МЕСЯЦ
async def bMonth_finance():
    now = datetime.now()
    date_pattern = f"%{now.year}-{now.month:02d}%"
    amaut_check = await execute_query(
        "SELECT * FROM checks WHERE status = 'succeeded' AND date LIKE %s",
        (date_pattern,)
    )

    summa = 0
    for amaut in amaut_check:
        try:
            print(f"MOOBY: {int(amaut[3])}")
            summa +=  int(amaut[3])
        except:
            return False
    return f"{summa}"
#ДЕНЬГИ ЗА МЕСЯЦ КОНЕЦ

#ДЕНЬГИ ЗА ДЕНЬ
async def bDay_finance():
    now = datetime.now()
    date_pattern = f"%{now.year}-{now.month:02d}-{now.day:02d}%"
    amaut_check = await execute_query(
        "SELECT * FROM checks WHERE status = 'succeeded' AND date LIKE %s",
        (date_pattern,)
    )

    summa = 0
    for amaut in amaut_check:
        try:
            print(f"MOOBY: {int(amaut[3])}")
            summa +=  int(amaut[3])
        except:
            return False
    return f"{summa}"
#ДЕНЬГИ ЗА МЕСЯЦ КОНЕЦ


async def close_pool():
    """Закрывает пул соединений"""
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None