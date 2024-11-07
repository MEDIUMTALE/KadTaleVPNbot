import telebot
from telebot import types

def guide_iphone(message):
    # подгрузка фотографий
    in_appstore_photo = open("ViewModels/resourse/img/guides/iphone/in_appstore.jpg", "rb")
    add_profile_photo = open("ViewModels/resourse/img/guides/iphone/add_profile.jpg", "rb")
    import_at_bufer_photo = open("ViewModels/resourse/img/guides/iphone/import_at_bufer.jpg", "rb")
    profile_choice_photo = open("ViewModels/resourse/img/guides/iphone/profile_choice.jpg", "rb")
    activate_photo = open("ViewModels/resourse/img/guides/iphone/activate.jpg", "rb")

    # шаг 1
    bot.send_message(message.chat.id,
                     "Шаг 1:\n    Для запуска нашего VPN на Iphone, необходимо приложение клиент, в нашем случаее рекомендую 'Streisand':")
    bot.send_photo(message.chat.id, in_appstore_photo)

    # шаг 2
    bot.send_message(message.chat.id,
                     "Шаг 2:\n    Предварительно скопировав выданный ключ, зайдя в приложение нажмите на плюсик в верхнем правом углу экрана:")
    bot.send_photo(message.chat.id, add_profile_photo)

    # шаг 3
    bot.send_message(message.chat.id, "Шаг 3:\n    Нажмите на кнопку 'Добавить из буфера':")
    bot.send_photo(message.chat.id, import_at_bufer_photo)

    # шаг 4
    bot.send_message(message.chat.id, "Шаг 4:\n    Выберите добавленный профиль нажав на него:")
    bot.send_photo(message.chat.id, profile_choice_photo)

    # шаг 5
    bot.send_message(message.chat.id, "Шаг 5:\n    Включите VPN:")
    bot.send_photo(message.chat.id, activate_photo)