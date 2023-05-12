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

    await message.answer(
        text='Укажите количество:',
        reply_markup=kol_vo
    )


@user_answer_router.message(Text(text=get_kol_vo(), ignore_case=True))
async def choose_num(message: Message):
    await message.answer(
        text='Отлично, теперь ты точно знаешь, какое оборудование тебе необходимо. Перейдем к следкющему шагу.',
        reply_markup=main_panel
    )