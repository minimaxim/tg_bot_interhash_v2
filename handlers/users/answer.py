import os

import psycopg2
from aiogram import Router, F
from aiogram.types import Message

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


@user_answer_router.message(F.text)
async def handle_message_click(message: Message):

    all_units = get_list()

    if message.text in all_units:
        x = message.text

        await message.answer(text='Укажите количество:',
                             reply_markup=kol_vo)

    elif message.text in list(str(range(1, 10))):
        await message.answer(text='Укажите количествоdsaddas:',
                             reply_markup=kol_vo)


