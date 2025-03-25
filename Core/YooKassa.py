from telebot import types
from telebot.types import LabeledPrice, Message
from telebot.async_telebot import AsyncTeleBot
import asyncio

payment_status = {}

async def send_invoice_to_user(message, bot, amount_rub):
    provider_token = '390540012:LIVE:67574'  # Замените на реальный!
    prices = [LabeledPrice(label="Пополнение баланса", amount=int(amount_rub))]

    try:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Пополнение баланса VPN',
            description=f'Пополнение на {amount_rub} руб',
            invoice_payload=f'balance_{message.from_user.id}',
            provider_token=provider_token,
            currency='rub',
            prices=prices,
            is_flexible=False,
            start_parameter=f'balance_{amount_rub}'
        )
        print(f"Инвойс отправлен для {message.from_user.id}")
        return True
    except Exception as e:
        error_text = (
            "⚠️ Не удалось создать платёж. "
            "Попробуйте позже или свяжитесь с поддержкой."
        )
        await bot.send_message(message.chat.id, error_text)
        print(f"Ошибка платежа: {e}")
        return False