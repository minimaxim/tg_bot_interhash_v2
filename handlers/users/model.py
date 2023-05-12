from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline.users import model_paginator_ikb
from keyboards.inline.users.general import UserCallbackData

user_model_router = Router(name='user_model')



@user_model_router.callback_query(UserCallbackData.filter((F.target == 'model') & (F.action == 'get')))
async def get_model(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.edit_text(
        text='Нужна ли вам скидка на подключение к майнинг-пулу?',
        reply_markup=await model_paginator_ikb(callback_data=callback_data)
    )
    if callback_data.model_id == 1 or callback_data.model_id == 2:
        await callback.message.edit_text(
            text='Спасибо за ответ! К вам подключится специалист для обсуждения всех условий ☺',
        )

