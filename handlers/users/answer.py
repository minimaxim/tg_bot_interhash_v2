import os

import psycopg2
from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

from keyboards.reply.users import main_panel

user_answer_router = Router(name='user_answer')


def connect_to_db():

    conn = psycopg2.connect(
        host=f'{os.getenv("DATABASE_HOST")}',
        database=f'{os.getenv("DATABASE_NAME")}',
        user=f'{os.getenv("DATABASE_USERNAME")}',
        password=f'{os.getenv("DATABASE_PASSWORD")}'
    )
    return conn

def get_list():

    all_lists = []

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""SELECT * from asics""")
    asic_in_db = cur.fetchall()

    second_elements_asic = [row[1] for row in asic_in_db]

    for asic in second_elements_asic:
        all_lists.append(f'/{asic}')

    cur.close()
    conn.close()

    return all_lists


def get_kol_vo():

    x = range(1,100000)

    return list(x)


@user_answer_router.message(Text(text=get_list(), ignore_case=True))
async def handle_message_click(message: Message):

    x = message.text.split('/')
    user = message.from_user.id
    algo = x[1]

    if message.text in ['/SHA', '/Sia', '/Blake', '/Kadena', '/Handsnake']:
        await message.answer(
            text='Укажите хэшрейт (Th/s):',
        )
    elif message.text in ['/Scrypt', '/X11', '/Quark', '/Qubit', '/Myr', '/Skein', '/LBRY', '/Lyra2REv2', '/Keccak',
                          '/Groestl', '/Eaglesong']:
        await message.answer(
            text='Укажите хэшрейт (Gh/s):',
        )
    elif message.text in ['/CryptoNight', '/CryptoNightSTC', '/Equihash', '/RandomX']:
        await message.answer(
            text='Укажите хэшрейт (kh/s):',
        )
    elif message.text in ['/BCD', '/Lyra2z']:
        await message.answer(
            text='Укажите хэшрейт (Mh/s):',
        )
    elif message.text in ['/Cuckatoo31', '/Cuckatoo32']:
        await message.answer(
            text='Укажите хэшрейт (h/s):',
        )
    else:
        await message.answer(
            text='Укажите хэшрейт:',
        )

    connect_to_db()

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET asic_name = (%s) WHERE id = (%s)""", (algo, user))
    conn.commit()

    cur.close()
    conn.close()


@user_answer_router.message(Text(text=get_kol_vo(), ignore_case=True))
async def choose_num(message: Message):
    await message.answer(
        text='Отлично, теперь ты точно знаешь, какое оборудование тебе необходимо. Перейдем к следующему шагу.',
        reply_markup=main_panel
    )

    user = message.from_user.id
    kolvo = message.text

    connect_to_db()

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET kolvo = (%s) WHERE id = (%s)""", (kolvo, user))
    conn.commit()

    cur.close()
    conn.close()
