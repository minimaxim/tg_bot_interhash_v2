import os

import psycopg2
from aiogram import Router, F
from aiogram.filters import Text
from aiogram.types import Message

from keyboards.reply.users import main_panel
from keyboards.reply.users.qurry import kol_vo

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

    x = range(1,10)

    return list(x)


@user_answer_router.message(Text(text=get_list(), ignore_case=True))
async def handle_message_click(message: Message):

    x = message.text.split('/')
    user = message.from_user.id
    algo = x[1]


    await message.answer(
        text='Укажите количество:',
        reply_markup=kol_vo
    )

    connect_to_db()

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""SELECT id FROM asics where name = (%s)""", (algo,))
    algo_id = cur.fetchall()[0][0]
    conn.commit()

    cur.execute("""SELECT user_id from calculators""")
    us_in_db = cur.fetchall()
    true_id = [row[0] for row in us_in_db]
    conn.commit()

    if user in true_id:
        cur.execute("""UPDATE calculators SET asic_id = (%s) WHERE user_id = (%s)""",
                    (algo_id, user))
        conn.commit()
    else:
        cur.execute("""INSERT INTO calculators (asic_id, user_id) VALUES (%s, %s)""", (algo_id, user))
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

    cur.execute("""UPDATE calculators SET kolvo = (%s) WHERE user_id = (%s)""",
                (kolvo, user))
    conn.commit()

    cur.execute("""SELECT id FROM calculators WHERE user_id = (%s)""", (user,))
    calculate_id = cur.fetchall()[0][0]
    conn.commit()

    cur.execute("""UPDATE users SET calculator_id = (%s) WHERE users.id = (%s)""",
                (calculate_id, user))
    conn.commit()

    cur.close()
    conn.close()
