import asyncio
from yookassa import Payment, Configuration
import uuid
from telebot import types
from telebot.async_telebot import AsyncTeleBot

# Настройки ЮKassa
YOOKASSA_SHOP_ID = "1046269"
YOOKASSA_SECRET_KEY = "live_HMstD4JMz_kYwfQr6u3r7MCeUXhV-Off_QdVHXwiEug"
Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY

async def send_payment_sbp(message: types.Message, bot: AsyncTeleBot, amount: float):
    """Создание платежа через СБП"""
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id  # Добавляем user_id для metadata
        
        # Создаем платеж
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": f"{amount:.2f}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/rozkomvpn_bot"
            },
            "capture": True,
            "description": "Пополнение баланса",
            "metadata": {
                "chat_id": chat_id,
                "user_id": user_id  # Добавляем user_id
            }
        }, idempotence_key)

        # Создаем кнопки
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton(
                text="💳 Оплатить",
                url=payment.confirmation.confirmation_url
            )
        )
        markup.row(
            types.InlineKeyboardButton(
                text="🔄 Проверить оплату",
                callback_data=f"check_{payment.id}"
            )
        )

        await bot.send_message(
            chat_id=chat_id,
            text=f"После полаты бязательно нажмите \"🔄 Проверить оплату\" ❗️\n✅ Для оплаты {amount} руб. нажмите кнопку ниже:",
            reply_markup=markup
        )

        return payment

    except Exception as e:
        print(f"Ошибка при создании платежа: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Произошла ошибка при создании платежа. Попробуйте позже."
        )
        return None

async def check_payment_status(payment_id: str) -> str:
    """Проверка статуса платежа"""
    try:
        payment = Payment.find_one(payment_id)
        return payment.status
    except Exception as e:
        print(f"Ошибка проверки платежа: {e}")
        return None