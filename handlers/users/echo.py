from aiogram import types

from loader import dp


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("Hurmatli foydalanavchi Siz bu botdan faqat buyurtma berish uchun foydalana olasiz")
