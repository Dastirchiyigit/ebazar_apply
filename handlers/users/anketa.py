from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from states.personalData import PersonalData1

import logging

from aiogram import Dispatcher

from data.config import ADMINS


# /form komandasi uchun handler yaratamiz. Bu yerda foydalanuvchi hech qanday holatda emas, state=None
@dp.message_handler(CommandStart())
async def enter_test(message: types.Message):
    await message.answer(f"👋Salom, {message.from_user.full_name}!\n🤖Bot orqali mahsulotlarimizga buyurma berishinggiz mumkin")
    await message.answer("🫡Hurmatli mijoz!\nTo'liq ismingizni kiriting✏️")
    await PersonalData1.fullName.set()


@dp.message_handler(state=PersonalData1.fullName)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    await state.update_data(
        {"name": fullname}
    )

    await message.answer("Yashash manzil yoki\nbuyurtmani yitkazib berish manzilini kiriting🚀")

    # await PersonalData.email.set()
    await PersonalData1.next()

@dp.message_handler(state=PersonalData1.manzil)
async def answer_email(message: types.Message, state: FSMContext):
    manzil = message.text

    await state.update_data(
        {"email": manzil}
    )

    await message.answer("Sizga bog'lanishimiz uchun Telefon raqam kiriting📲")

    await PersonalData1.next()


@dp.message_handler(state=PersonalData1.phoneNum )
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.text

    await state.update_data(
        {"phone": phone}
    )
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    msg = "Quyidai ma`lumotlar qabul qilindi‼️:\n\n"
    msg += f"Username - @{message.from_user.username}\n"
    msg += f"Nikname - {message.from_user.full_name}\n"
    msg += f"Botga bergan malumoti\n\nIsmi - {name}\n"
    msg += f"Manzil - {email}\n"
    msg += f"Telefon: - {phone}"
    await message.answer("✨Buyurtma qabul qilindi!,Agar malumotlarni to'g'ri kiritgan bo'lsanggiz,"
                         "🛂Adminlar sizga yaqin Daqiqalar⏱ichida bog'lanishadilar\n"
                         "📝Malumotlariz xato bo'lsa  /START  tugmasini bosin va qayta to'ldiring")

    # State dan chiqaramiz
    # 1-variant
    await state.finish()

    # 2-variant
    # await state.reset_state()

    # 3-variant. Ma`lumotlarni saqlab qolgan holda
    await state.reset_state(with_data=False)
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, msg)

        except Exception as err:
            logging.exception(err)
