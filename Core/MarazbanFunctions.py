import asyncio
from marzban import MarzbanAPI, UserCreate, ProxySettings
from Core.Databases import add_logs, info_settings, info_user


# Инициализация API
api = MarzbanAPI(base_url="https://fin-01.kadtale.site")

# Получение токена
async def get_token():
    token = await api.get_token(username="mtadmin", password="jQrtP4bzaDfCXosJ8q3MX5wLHasesj8")
    return token

# Добавление пользователя
async def mAddUser(user_id):
    try:
        # Получаем токен
        token = await get_token()
        if not hasattr(token, "access_token"):
            print("Ошибка: токен не содержит access_token")
            return



        new_user = UserCreate(
            username=f"{user_id}",  # Уникальное имя пользователя
            proxies={
                "vless": ProxySettings(flow="xtls-rprx-vision"),  # Настройки прокси
            },
            status="active",  # Статус пользователя (например, "active" или "disabled")
            data_limit=0,  # Лимит данных (0 — без лимита)
            expire=0,  # Срок действия (0 — бессрочно)
            data_limit_reset_strategy="no_reset",  # Стратегия сброса лимита данных
            inbounds={"vless": ["VLESS TCP REALITY"]},  # Входящие подключения
        )

        # Добавляем пользователя
        added_user = await api.add_user(user=new_user, token=token.access_token)
        print("Добавленный пользователь:", added_user)
        await add_logs("Marzban_Registration", f"user_id: {user_id}, добавлен в Marzban, Balance: {await info_user(user_id, 1)}")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")





# Удаление пользователя
async def mDelUser(user_id):
    try:
        # Получаем токен
        token = await get_token()
        if not hasattr(token, "access_token"):
            print("Ошибка: токен не содержит access_token")
            return
        
        # Добавляем пользователя
        await api.remove_user(username=f"{user_id}", token=token.access_token)
        print("Пользователь удалён.")
        await add_logs("Marzban_Delete", f"user_id: {user_id}, удалён из Marzban, Balance: {await info_user(user_id, 1)}")

    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")

async def mGetKayUser(user_id):
    try:
        # Получаем токен
        token = await get_token()
        if not hasattr(token, "access_token"):
            print("Ошибка: токен не содержит access_token")
            return

        user_info = await api.get_user(username=f"{user_id}", token=token.access_token)

        return f"Ваш ключ 🔑\n{await info_settings(3)}{user_info.subscription_url}"
    except:    
        print("Пользователя не существует")
        return "Вы не подключенны к тарифу 😟"


async def mChangeStatusUser(user_id):
    try:
        # Получаем токен
        token = await get_token()
        if not hasattr(token, "access_token"):
            print("Ошибка: токен не содержит access_token")
            return

        # Создаем нового пользователя
        new_user = UserCreate(
            username=f"{user_id}",
            proxies={"vless": ProxySettings(flow="xtls-rprx-vision")}
        )

        # Добавляем пользователя
        added_user = await api.add_user(user=new_user, token=token.access_token)
        print("Добавленный пользователь:", added_user)
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")

async def mGet_Data_Info_User(user_id):
        # Получаем токен
        token = await get_token()
        if not hasattr(token, "access_token"):
            print("Ошибка: токен не содержит access_token")
            return

        user_info = await api.get_user(username=f"{user_id}", token=token.access_token)

        user_UseData = round(user_info.used_traffic / 1073741824, 2)

        print(user_info.data_limit)

        if user_info.data_limit is None:
            user_DataLimit = "∞"
            
        else:
            print(user_info.data_limit)
            user_DataLimit = round(user_info.data_limit / 1073741824, 2)

        return f"Вы потратили: {user_UseData} GB из {user_DataLimit} GB"


#asyncio.run(mAddUser("1324016724"))
#asyncio.run(mDelUser("1324016724"))
#print(asyncio.run(mGetKayUser("1324016724")))
#print(asyncio.run(mGet_Data_Info_User("1324016724")))

