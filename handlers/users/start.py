from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards.inline.users import start_ikb
from keyboards.inline.users.general import UserCallbackData

user_start_router = Router(name='user_start')


@user_start_router.message(F.text == 'НАЖМИТЕ СЮДА 🔥')
async def start_panel_1(message: Message):
    await message.delete()
    await message.answer(
        text='Выберите один из предложенных вариантов:',
        reply_markup=await start_ikb()
    )


@user_start_router.callback_query(UserCallbackData.filter(F.action == 'all'))
async def start_panel_2(callback: CallbackQuery):
    await callback.message.edit_text(
        text= 'Выберите один из предложенных вариантов:',
        reply_markup=await start_ikb()
    )
