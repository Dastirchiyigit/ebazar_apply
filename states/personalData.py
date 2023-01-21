from aiogram.dispatcher.filters.state import StatesGroup, State


# Shaxsiy ma'lumotlarni yig'sih uchun PersonalData holatdan yaratamiz
class PersonalData1(StatesGroup):
    # Foydalanuvchi buyerda 3 ta holatdan o'tishi kerak
    fullName = State() # ism
    manzil = State() # email
    phoneNum = State() # Tel raqami

