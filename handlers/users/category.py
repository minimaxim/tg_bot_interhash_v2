from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from handlers.users.formilize import Form
from keyboards.inline.users import category_ikb, cur_ikb, power_ikb
from keyboards.inline.users.general import UserCallbackData
from keyboards.reply.users import main_panel
from parser.connection import connect_to_db

user_category_router = Router(name='user_category')


class Category(StatesGroup):
    star = State()
    thanks = State()

@user_category_router.callback_query(UserCallbackData.filter((F.target == 'category') & (F.action == 'get')))
async def paginate_categories(callback: CallbackQuery, callback_data: UserCallbackData, state: FSMContext) -> None:

    connect_to_db()

    user = callback.from_user.id
    start = callback_data.start_id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""SELECT name FROM start WHERE id = (%s)""", (start,))
    start_name = cur.fetchall()[0][0]
    conn.commit()

    cur.execute("""UPDATE users SET start_name = (%s) WHERE id = (%s)""", (start_name, user))
    conn.commit()

    cur.close()
    conn.close()


    if callback_data.start_id == 2:
        await callback.message.edit_text(
            text='Укажите Вашу мощность',
            reply_markup=await power_ikb()
        )

    elif callback_data.start_id == 3:

        await callback.message.edit_text(
            text='Укажите для вас удобный способ связи',
        )

        connect_to_db()

        date = str(datetime.now())
        user = callback.from_user.id

        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
        conn.commit()

        cur.close()
        conn.close()

        await state.update_data(star=callback_data.start_id)
        await state.set_state(Category.thanks)

    elif callback_data.start_id == 4:
        await state.set_state(Form.coin)
        await callback.message.edit_text(
            text='Выберите валюту для рассчета',
            reply_markup=await cur_ikb()
        )

    else:
        await callback.message.edit_text(
            text='Знаете ли вы какое оборудование вам необходимо?',
            reply_markup=await category_ikb()
        )


@user_category_router.message(Category.thanks)
async def get_contact(message: Message, state: FSMContext):

    connect_to_db()

    connect = message.text

    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET call_me = (%s) WHERE id = (%s)""", (connect, user))
    conn.commit()

    cur.close()
    conn.close()

    await message.answer(
        text='Cпасибо за обращение, наш менеджер свяжется с вами в ближайшее время',
        reply_markup=main_panel
    )

    connect_to_db()

    date = str(datetime.now())

    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.clear()
