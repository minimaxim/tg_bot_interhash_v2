from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline.users import brand_paginator_ikb, all_list_ikb
from keyboards.inline.users.general import UserCallbackData
from parser.connection import connect_to_db

user_brand_router = Router(name='user_brand')


@user_brand_router.callback_query(UserCallbackData.filter((F.target == 'brand') & (F.action == 'get')))
async def get_brand(callback: CallbackQuery, callback_data: UserCallbackData):

    connect_to_db()

    user = callback.from_user.id
    category = callback_data.category_id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""SELECT name FROM categories WHERE id = (%s)""", (category,))
    category_name = cur.fetchall()[0][0]
    conn.commit()

    cur.execute(f"""UPDATE users SET category_name = (%s) WHERE id = (%s)""", (category_name, user))
    conn.commit()

    cur.close()
    conn.close()

    if callback_data.category_id == 1:

        asics = await Asic.all()

        text = '\n\nASIC алгоритмы:\n'
        for asic in asics:
            text += f'/{asic.name} '

        await callback.message.edit_text(
            text=text.strip(),
            reply_markup=await all_list_ikb(callback_data=callback_data)
        )
        
    elif callback_data.category_id == 2:
        await callback.message.edit_text(
            text='Спасибо за ответ! К вам подключится специалист для обсуждения всех условий ☺',
        )
    else:
        await callback.message.edit_text(
            text='Нужен ли вам хостинг?',
            reply_markup=await brand_paginator_ikb(callback_data=callback_data)
        )


