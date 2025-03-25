from telebot import types
from telebot.types import LabeledPrice, Message
from telebot.async_telebot import AsyncTeleBot
import asyncio

payment_status = {}

async def send_invoice_to_user(message, bot, money):
    provider_token = '390540012:LIVE:67574'
    #provider_token = '1744374395:TEST:dac3822bb9afd4c099e4'
    prices = [
        LabeledPrice(label='Пополнение баланса VPN', amount=money),
    ]
    
    try:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Пополнение баланса VPN',
            description='Пополнение баланса VPN',
            invoice_payload='add_bolance',
            provider_token=provider_token,
            currency='rub',
            prices=prices,
            is_flexible=False,
            start_parameter='add_bolance'
        )
        print("Инвойс отправлен. Ожидаем оплату...")
        
        # Ждем подтверждения оплаты (таймаут 15 минут)
        for _ in range(90):
            await asyncio.sleep(10)
            if payment_status.get(message.chat.id, False):
                return True
        return False
        
    except Exception as e:
        print(f"Ошибка при отправке инвойса: {e}")
        return False