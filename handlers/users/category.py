from aiogram import Router, F, types
from aiogram.types import CallbackQuery, message

from keyboards.inline.users import category_paginator_ikb, all_list_ikb
from keyboards.inline.users.general import UserCallbackData
from models.models import Asic
from parser.test_par import parse_and_save, connect_to_db

user_category_router = Router(name='user_category')


@user_category_router.callback_query(UserCallbackData.filter((F.target == 'category') & (F.action == 'get')))
async def paginate_categories(callback: CallbackQuery, callback_data: UserCallbackData):

    connect_to_db()

    user = callback.from_user.id
    start = callback_data.start_id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""UPDATE users SET start_id = (%s) WHERE id = (%s)""", (start, user))
    conn.commit()

    cur.close()
    conn.close()


    if callback_data.start_id == 3:
        await callback.message.edit_text(
            text='Спасибо за ответ! К вам подключится специалист... Напишите пожалуйста свой вопрос ☺',
        )
    elif callback_data.start_id == 4:

        parse_and_save()

        asics = await Asic.all()

        text = '\n\nASIC алгоритмы:\n'
        for asic in asics:
            text += f'/{asic.name} '

        await callback.message.edit_text(
            text=text.strip(),
            reply_markup= await all_list_ikb(callback_data=callback_data)
        )
    else:
        await callback.message.edit_text(
            text='Знаете ли вы какое оборудование вам необходимо?',
            reply_markup=await category_paginator_ikb(callback_data=callback_data)
        )


