from aiogram import Router, F
from aiogram.types import Message

user_kolvo_router = Router(name='user_kolvo')

@user_kolvo_router.message(F.text == '1')
async def choose_num(message: Message):
    await message.answer(
        text='На данный момент бот не может obaka'
    )