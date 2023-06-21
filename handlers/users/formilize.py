from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, CallbackQuery

from handlers.users.math import math
from keyboards.inline.users import coin_ikb
from keyboards.inline.users.general import UserCallbackData
from keyboards.reply.users import main_panel
from parser.connection import connect_to_db

user_fromilize_router = Router(name='user_formilize')


class Form(StatesGroup):
    user = State()
    currency = State()
    coin = State()
    cost_electr = State()
    hash_rate = State()
    potr_electr = State()
    comm_pull = State()
    finish = State()


@user_fromilize_router.callback_query(UserCallbackData.filter((F.target == 'curs') & (F.action == 'get')))
async def get_coin(callback: CallbackQuery, state: FSMContext, callback_data: UserCallbackData):
    connect_to_db()

    if callback_data.currency_id == 1:
        val = 'RUB ₽'
    else:
        val = 'USD $'

    user = callback.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET currency = (%s) WHERE id = (%s)""", (val, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(currency=callback_data.currency_id)
    await state.set_state(Form.cost_electr)

    await callback.message.edit_text(
        text='Выберите монету',
        reply_markup=await coin_ikb()
    )


@user_fromilize_router.callback_query(UserCallbackData.filter((F.target == 'coins') & (F.action == 'get')))
async def get_cost(callback: CallbackQuery, state: FSMContext, callback_data: UserCallbackData):
    connect_to_db()

    if callback_data.coin_id == 1:
        coin = 'bitcoin'
    elif callback_data.coin_id == 2:
        coin = 'bitcoin-cash'
    elif callback_data.coin_id == 3:
        coin = 'litecoin'
    elif callback_data.coin_id == 4:
        coin = 'ethereum-classic'
    elif callback_data.coin_id == 5:
        coin = 'zcash'
    elif callback_data.coin_id == 6:
        coin = 'dash'

    user = callback.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET coin = (%s) WHERE id = (%s)""", (coin, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(coin=callback_data.coin_id)
    await state.set_state(Form.hash_rate)

    await callback.message.answer(
        text='Укажите цену на электричество (кВт/ч):',
        reply_markup=main_panel
    )


@user_fromilize_router.message(Form.hash_rate)
async def get_hash(message: Message, state: FSMContext):
    connect_to_db()

    tip = message.text

    if tip.isdecimal():

        if message.text < '0':
            await message.answer(
                text='Укажите цену на электричество (кВт/ч) больше 0.1:',
                reply_markup=main_panel
            )
        else:
            cost = message.text

            user = message.from_user.id

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET cost_electricity = (%s) WHERE id = (%s)""", (cost, user))
            conn.commit()

            cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))

            coin_type = cur.fetchall()[0][0]

            cur.close()
            conn.close()

            await state.update_data(cost_electr=message.text)
            await state.set_state(Form.potr_electr)

            if coin_type == "bitcoin" or coin_type == "bitcoin-cash":

                await message.answer(
                    text='Укажите хешрейт (Th/s):',
                    reply_markup=main_panel
                )

            elif coin_type == "litecoin" or coin_type == "dash":
                await message.answer(
                    text='Укажите хешрейт (Gh/s):',
                    reply_markup=main_panel
                )

            elif coin_type == "ethereum-classic":
                await message.answer(
                    text='Укажите хешрейт (Mh/s):',
                    reply_markup=main_panel
                )

            elif coin_type == "zcash":
                await message.answer(
                    text='Укажите хешрейт (kh/s):',
                    reply_markup=main_panel
                )
    else:
        try:
            float(tip)

            if message.text < '0.1':
                await message.answer(
                    text='Укажите цену на электричество (кВт/ч) больше 0.1:',
                    reply_markup=main_panel
                )
            else:
                cost = message.text

                user = message.from_user.id

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET cost_electricity = (%s) WHERE id = (%s)""", (cost, user))
                conn.commit()

                cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))

                coin_type = cur.fetchall()[0][0]

                cur.close()
                conn.close()

                await state.update_data(cost_electr=message.text)
                await state.set_state(Form.potr_electr)

                if coin_type == "bitcoin" or coin_type == "bitcoin-cash":

                    await message.answer(
                        text='Укажите хешрейт (Th/s):',
                        reply_markup=main_panel
                    )

                elif coin_type == "litecoin" or coin_type == "dash":
                    await message.answer(
                        text='Укажите хешрейт (Gh/s):',
                        reply_markup=main_panel
                    )

                elif coin_type == "ethereum-classic":
                    await message.answer(
                        text='Укажите хешрейт (Mh/s):',
                        reply_markup=main_panel
                    )

                elif coin_type == "zcash":
                    await message.answer(
                        text='Укажите хешрейт (kh/s):',
                        reply_markup=main_panel
                    )

        except ValueError:
            await message.answer(
                text='Укажите цену на электричество (кВт/ч) числом:',
                reply_markup=main_panel
            )


@user_fromilize_router.message(Form.potr_electr)
async def get_potr(message: Message, state: FSMContext):
    connect_to_db()

    tip = message.text

    if tip.isdecimal():
        if message.text < '0':
            await message.answer(
                text='Укажите хешрейт больше 0.1:',
                reply_markup=main_panel
            )
        else:
            hash = message.text

            user = message.from_user.id

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET hash = (%s) WHERE id = (%s)""", (hash, user))
            conn.commit()

            cur.close()
            conn.close()

            await state.update_data(hash_rate=message.text)
            await state.set_state(Form.comm_pull)

            await message.answer(
                text='Укажите потребление (Ватт):',
                reply_markup=main_panel
            )
    else:
        try:
            float(tip)

            if message.text < '0.1':
                await message.answer(
                    text='Укажите хешрейт больше 0.1:',
                    reply_markup=main_panel
                )

            else:
                hash = message.text

                user = message.from_user.id

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET hash = (%s) WHERE id = (%s)""", (hash, user))
                conn.commit()

                cur.close()
                conn.close()

                await state.update_data(hash_rate=message.text)
                await state.set_state(Form.comm_pull)

                await message.answer(
                    text='Укажите потребление (Ватт):',
                    reply_markup=main_panel
                )

        except ValueError:
            await message.answer(
                text='Укажите хешрейт числом:',
                reply_markup=main_panel
            )


@user_fromilize_router.message(Form.comm_pull)
async def get_comm(message: Message, state: FSMContext):
    connect_to_db()

    tip = message.text

    if tip.isdecimal():
        if message.text < '0':
            await message.answer(
                text='Укажите потребление (Ватт) больше 0.1:',
                reply_markup=main_panel
            )
        else:
            potr = message.text
            user = message.from_user.id

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET potreb = (%s) WHERE id = (%s)""", (potr, user))
            conn.commit()

            cur.close()
            conn.close()

            await state.update_data(potr_electr=message.text)
            await state.set_state(Form.finish)

            await message.answer(
                text='Укажите комиссию пула (%):',
                reply_markup=main_panel
            )
    else:
        try:
            float(tip)

            if message.text < '0.1':
                await message.answer(
                    text='Укажите потребление (Ватт) больше 0.1:',
                    reply_markup=main_panel
                )
            else:
                potr = message.text
                user = message.from_user.id

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET potreb = (%s) WHERE id = (%s)""", (potr, user))
                conn.commit()

                cur.close()
                conn.close()

                await state.update_data(potr_electr=message.text)
                await state.set_state(Form.finish)

                await message.answer(
                    text='Укажите комиссию пула (%):',
                    reply_markup=main_panel
                )

        except ValueError:
            await message.answer(
                text='Укажите потребление (Ватт) числом:',
                reply_markup=main_panel
            )


@user_fromilize_router.message(Form.finish)
async def get_final(message: Message, state: FSMContext):
    tip = message.text

    if tip.isdecimal():
        if message.text < '0':
            await message.answer(
                text='Укажите комиссию пула (%) больше 0.1:',
                reply_markup=main_panel
            )

        else:
            await state.update_data(comm_pull=message.text)
            await state.update_data(finish='done')

            await message.answer(
                text='Происходит расчет, пожалуйста, подождите...',
                reply_markup=main_panel
            )

            com = message.text
            user = message.from_user.id

            connect_to_db()

            conn = connect_to_db()
            cur = conn.cursor()

            cur.execute("""UPDATE users SET komm = (%s) WHERE id = (%s)""", (com, user))
            conn.commit()

            user = message.from_user.id
            user_name = message.from_user.username

            cur.execute("""SELECT currency FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            currency = cur.fetchall()[0][0]

            cur.execute("""SELECT cost_electricity FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            cost_electricity = cur.fetchall()[0][0]

            cur.execute("""SELECT hash FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            hash = cur.fetchall()[0][0]

            cur.execute("""SELECT potreb FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            potreb = cur.fetchall()[0][0]

            cur.execute("""SELECT komm FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            komm = cur.fetchall()[0][0]

            cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))
            conn.commit()
            coin = cur.fetchall()[0][0]

            await message.answer_photo(photo=FSInputFile(math(user_name, currency, cost_electricity, hash, potreb,
                                                              komm, coin)))

            date = str(datetime.now())
            user = message.from_user.id

            cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
            conn.commit()

            await state.clear()

            cur.close()
            conn.close()

    else:
        try:
            float(tip)

            if message.text < '0.1':
                await message.answer(
                    text='Укажите комиссию пула (%) больше 0.1:',
                    reply_markup=main_panel
                )
            else:
                await state.update_data(comm_pull=message.text)
                await state.update_data(finish='done')

                await message.answer(
                    text='Происходит расчет, пожалуйста, подождите...',
                    reply_markup=main_panel
                )

                com = message.text
                user = message.from_user.id

                connect_to_db()

                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""UPDATE users SET komm = (%s) WHERE id = (%s)""", (com, user))
                conn.commit()

                user = message.from_user.id
                user_name = message.from_user.username

                cur.execute("""SELECT currency FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                currency = cur.fetchall()[0][0]

                cur.execute("""SELECT cost_electricity FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                cost_electricity = cur.fetchall()[0][0]

                cur.execute("""SELECT hash FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                hash = cur.fetchall()[0][0]

                cur.execute("""SELECT potreb FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                potreb = cur.fetchall()[0][0]

                cur.execute("""SELECT komm FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                komm = cur.fetchall()[0][0]

                cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))
                conn.commit()
                coin = cur.fetchall()[0][0]

                await message.answer_photo(photo=FSInputFile(math(user_name, currency, cost_electricity, hash, potreb,
                                                                  komm, coin)))

                date = str(datetime.now())
                user = message.from_user.id

                cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
                conn.commit()

                await state.clear()

                cur.close()
                conn.close()

        except ValueError:
            await message.answer(
                text='Укажите комиссию пула (%) числом:',
                reply_markup=main_panel
            )

        await state.clear()
