from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from keyboards.inline.users import promo_ikb, send_promo_ikb
from keyboards.inline.users.general import UserCallbackData
from keyboards.reply.users import main_panel
from parser.connection import connect_to_db

user_power_router = Router(name='user_power')


class Powerbank(StatesGroup):
    choice = State()
    answer = State()


@user_power_router.callback_query(UserCallbackData.filter((F.target == 'power') & (F.action == 'get')))
async def power(callback: CallbackQuery, callback_data: UserCallbackData, state: FSMContext):
    connect_to_db()

    user = callback.from_user.id
    power = callback_data.power_id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""SELECT name FROM start WHERE id = (%s)""", (power,))
    power_name = cur.fetchall()[0][0]
    conn.commit()

    cur.execute("""UPDATE users SET power = (%s) WHERE id = (%s)""", (power_name, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(choice=callback_data.power_id)

    if callback_data.power_id == 1:
        await callback.message.edit_text(
            text='Вашей мощности недостаточно для индивидуальных условий, но мы предоставляем Вам промокод для скидки',
            reply_markup=await promo_ikb()
        )


    elif callback_data.power_id == 2:
        await callback.message.edit_text(
            text='Вашей мощности достаточно для индивидуальных условий. Пожалуйста, укажите удобный способ для связи',
        )

        await state.set_state(Powerbank.answer)


@user_power_router.message(Powerbank.answer)
async def answer(message: Message, state: FSMContext):
    connect_to_db()

    data = message.text
    user = message.from_user.id
    date = datetime.now()

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET call_me = (%s) WHERE id = (%s)""", (data, user))
    conn.commit()

    cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(answer=message.text)

    await message.answer(
        text='Спасибо, скоро с Вами свяжется менеджер',
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


@user_power_router.callback_query(UserCallbackData.filter((F.target == 'promo') & (F.action == 'get')))
async def promo(callback: CallbackQuery, callback_data: UserCallbackData) -> None:
    if callback_data.promo_id == 1:
        await callback.message.edit_text(
            text='Ваш персональный промокод: 533030',
            reply_markup=await send_promo_ikb()
        )


@user_power_router.callback_query(UserCallbackData.filter((F.target == 'final') & (F.action == 'get')))
async def promo(callback: CallbackQuery, callback_data: UserCallbackData) -> None:
    if callback_data.app_id == 1:
        await callback.message.answer(
            text='Спасибо за заявку, скоро с Вами свяжется менеджер Interhash',
        )

        connect_to_db()

        date = str(datetime.now())
        user = callback.from_user.id
        promo = 'да'

        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("""UPDATE users SET promo = (%s) WHERE id = (%s)""", (promo, user))
        conn.commit()

        cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
        conn.commit()

        cur.close()
        conn.close()
