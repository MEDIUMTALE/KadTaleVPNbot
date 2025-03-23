import asyncio
from marzban import MarzbanAPI, UserCreate, ProxySettings

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
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")

async def mGetInfoStatusUser(user_id):
    try:
        # Получаем токен
        token = await get_token()
        if not hasattr(token, "access_token"):
            print("Ошибка: токен не содержит access_token")
            return

        user_info = await api.get_user(username=f"{user_id}", token=token.access_token)
        #print("Информация о пользователе:", user_info)
        print(user_info)
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")




#asyncio.run(mGetInfoStatusUser(1324016724))
#asyncio.run(mAddUser(42))
#asyncio.run(mDelUser("roma"))