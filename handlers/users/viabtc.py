from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards.reply.users import main_panel
from parser.connection import connect_to_db

user_viabtc_router = Router(name='user_viabtc')


class Via(StatesGroup):
    user = State()
    model = State()
    kolvo = State()
    connect = State()


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
        text='Оставьте удобный для вас способ связи, либо свяжитесь с нашим менеджером: @interhash_manager',
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
