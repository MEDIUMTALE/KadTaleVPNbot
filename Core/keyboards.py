from telebot import types as async_types

async def keyboard_start():
    markup = async_types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    buttons = [
        async_types.KeyboardButton("Информация о VPN 📜"),
        async_types.KeyboardButton("Получить Ключ 🔑"),
        async_types.KeyboardButton("Пополнить баланс 💰️"),
        async_types.KeyboardButton("Баланс 🏦"),
        async_types.KeyboardButton("Помощь 🛟"),
        async_types.KeyboardButton("Партнерка 🤝")
    ]
    
    # Добавляем кнопки с четким распределением по строкам
    markup.add(buttons[0])  # Первая кнопка в отдельной строке
    markup.add(buttons[1])  # Вторая кнопка в отдельной строке
    markup.add(buttons[2], buttons[3])  # Две кнопки в одной строке
    markup.add(buttons[4])  # Помощь
    markup.add(buttons[5])  # Партнерка
    
    return markup

async def keyboard_balance():
    markup = async_types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    buttons = [
        async_types.KeyboardButton("Пополнить баланс ⚔️"),
        async_types.KeyboardButton("Пригласить друга"),
        async_types.KeyboardButton("⏪ Назад")
    ]
    
    markup.add(buttons[0], buttons[1])  # Две кнопки в одной строке
    markup.add(buttons[2])  # Назад в отдельной строке
    
    return markup