from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from keyboards.inline.users import discont_ikb
from keyboards.inline.users.general import UserCallbackData
from keyboards.reply.users import main_panel
from parser.connection import connect_to_db

user_viabtc_router = Router(name='user_viabtc')


class Via(StatesGroup):
    user = State()
    model = State()
    kolvo = State()
    connect = State()
    discont = State()


@user_viabtc_router.message(Via.model)
async def get_model(message: Message, state: FSMContext):

    connect_to_db()

    model = message.text
    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET model_name = (%s) WHERE id = (%s)""", (model, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(model=message.text)
    await state.set_state(Via.kolvo)

    await message.answer(
        text='Укажите количество',
        reply_markup=main_panel
        )


@user_viabtc_router.message(Via.kolvo)
async def get_kolvo(message: Message, state: FSMContext):

    connect_to_db()

    kolvo = message.text
    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET kolvo = (%s) WHERE id = (%s)""", (kolvo, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(kolvo=message.text)
    await state.set_state(Via.connect)

    await message.answer(
        text='Укажите контакный номер телефона и удобный способ для связи',
        reply_markup=main_panel
        )


@user_viabtc_router.message(Via.connect)
async def get_connect(message: Message, state: FSMContext):

    connect_to_db()

    connect = message.text
    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET call_me = (%s) WHERE id = (%s)""", (connect, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(kolvo=message.text)
    await state.set_state(Via.discont)

    await message.answer(
        text='Необходима скидка на подключение?',
        reply_markup= await discont_ikb()
    )


@user_viabtc_router.callback_query(UserCallbackData.filter((F.target == 'discont') & (F.action == 'get')))
async def get_connect(callback: CallbackQuery, state: FSMContext, callback_data: UserCallbackData):

    connect_to_db()

    if callback_data.discont_id == 1:
        discont = 'Да'
    else:
        discont = 'Нет'

    user = callback.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET discont = (%s) WHERE id = (%s)""", (discont, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(discont=discont)

    await callback.message.answer(
        text='Спасибо за заявку, скоро с Вами свяжется менеджер Interhash',
        reply_markup=main_panel
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

