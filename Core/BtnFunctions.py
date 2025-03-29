from Core.Databases import info_settings, info_user, add_user, existence_user, user_chage_Balance, Chage_User_function_status, DB_CONFIG, execute_query, add_logs
from Core.keyboards import *

# Храним данные для каждого пользователя отдельно
user_b_id = {}  # Формат: {user_id: target_user_id}
amout_b = {}    # Формат: {user_id: amount}

async def BtnCommands(message, bot, user_id):
    from Core.Commands import back, pay_summa_balance

    function_status = await info_user(user_id, 3)
    
    if message.text == "Назад 🔙":
        await back(message, bot)

    # Пополнение баланса
    elif function_status == "pay_balance":
        if message.text.isdigit():
            await Chage_User_function_status(user_id, None)
            await pay_summa_balance(message, bot)
        else:
            await bot.send_message(user_id, f"Неверное число")

    # Рассылка сообщений
    elif function_status == "send_message_all":
        user_results = await execute_query("SELECT * FROM users WHERE user_id IS NOT NULL")
        for user_row in user_results:
            await bot.send_message(user_row[0], f"{str(message.text)}")
        await Chage_User_function_status(user_id, None)
        await add_logs("Admin_Send_All_Message", f"user_id: {user_id}, сделал рассылку всем пользователям с текстом: '{str(message.text)}'")

    # Изменение баланса (Админка)
    elif function_status == "change_balance_user_id":
        try:
            # Сохраняем введённый ID пользователя в словарь с ключом user_id
            user_b_id[user_id] = message.text  # user_id (админа) -> target_user_id (кого меняем)
            
            if await existence_user(user_b_id[user_id]):
                await bot.send_message(user_id, "Укажите желаемый баланс")
                await Chage_User_function_status(user_id, "change_balance_user_amout")
            else:
                await bot.send_message(user_id, "Неверный ID")
        except Exception as e:
            print(f"Ошибка в change_balance_user_id: {e}")
            await back(message, bot)

    elif function_status == "change_balance_user_amout":
        try:
            # Сохраняем сумму для данного user_id (админа)
            amout_b[user_id] = message.text
            
            print(f"user_b_id: {user_b_id}")
            print(f"amout_b: {amout_b}")
            
            if amout_b[user_id].isdigit():
                # Меняем баланс target_user_id (user_b_id[user_id]) на amout_b[user_id]
                await user_chage_Balance(int(user_b_id[user_id]), int(amout_b[user_id]))
                await bot.send_message(
                    user_id,
                    f"Пользователю {user_b_id[user_id]} установлен баланс: {amout_b[user_id]}",
                    reply_markup=await keyboard_start(user_id)
                )
                await Chage_User_function_status(user_id, None)
                await add_logs("Admin_Change_Balance_User", f"user_id: {user_id}, установил пользователю {user_b_id[user_id]} баланс: {amout_b[user_id]}")
                
                # Очищаем данные после выполнения
                user_b_id.pop(user_id, None)
                amout_b.pop(user_id, None)
            else:
                await bot.send_message(user_id, "Неверное число")
        except Exception as e:
            print(f"Ошибка в change_balance_user_amout: {e}")
            await back(message, bot)