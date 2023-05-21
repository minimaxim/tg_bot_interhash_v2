import time

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from keyboards.inline.users import brand_paginator_ikb
from keyboards.inline.users.general import UserCallbackData
from keyboards.reply.users import main_panel
from parser.connection import connect_to_db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


user_fromilize_router = Router(name='user_formilize')

class Form(StatesGroup):
    user = State()
    currency = State()
    cost_electr = State()
    hash_rate = State()
    potr_electr = State()
    comm_pull = State()
    finish = State()


@user_fromilize_router.message(Form.cost_electr)
async def get_cost(message: Message, state: FSMContext) -> None:

    connect_to_db()

    if message.text == 'RUS🇷🇺':
        val = 'RUS'
    else:
        val = 'USA'

    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET currency = (%s) WHERE id = (%s)""", (val, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(currency=message.from_user.id)
    await state.update_data(currency=message.text)
    await state.set_state(Form.hash_rate)

    await message.answer(
    text='Укажите цену на электричество (кВт/ч):',
    reply_markup=main_panel
)

@user_fromilize_router.message(Form.hash_rate)
async def get_hash(message: Message, state: FSMContext) -> None:

    connect_to_db()

    cost = message.text
    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET cost_electricity = (%s) WHERE id = (%s)""", (cost, user))
    conn.commit()

    cur.close()
    conn.close()

    await state.update_data(cost_electr=message.text)
    await state.set_state(Form.potr_electr)

    await message.answer(
            text='Укажите хешрейт (Th/s):',
            reply_markup=main_panel
        )

@user_fromilize_router.message(Form.potr_electr)
async def get_potr(message: Message, state: FSMContext) -> None:

    connect_to_db()

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

@user_fromilize_router.message(Form.comm_pull)
async def get_comm(message: Message, state: FSMContext) -> None:

    connect_to_db()

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


@user_fromilize_router.message(Form.finish)
async def get_final(message: Message, state: FSMContext) -> None:

    connect_to_db()

    com = message.text
    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET komm = (%s) WHERE id = (%s)""", (com, user))
    conn.commit()

    cur.close()
    conn.close()
    await state.update_data(potr_electr=message.text)

    await message.answer(
        text='Происходит расчет, пожалуйста, подождите...',
        reply_markup=main_panel
    )

    await get_all(message=message,)


@user_fromilize_router.message()
async def get_all(message: Message, callback_data: UserCallbackData):

    connect_to_db()

    user = message.from_user.id
    user_name = message.from_user.username

    conn = connect_to_db()
    cur = conn.cursor()

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

    cur.close()
    conn.close()


    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://ultramining.com/crypto-calc/bitcoin/")

    if currency == 'USA':
        driver.find_element(By.CLASS_NAME, 'input-group-append').click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//*[@id='content']/div[2]/div[2]/div[1]/div/div/div/div[1]").click()
        time.sleep(1)
    else:
        pass

    price = driver.find_element(By.XPATH, "//*[@id='input-electricity']", )
    price.clear()
    price.send_keys(cost_electricity)

    price = driver.find_element(By.XPATH, "//*[@id='input-electricity']", )
    price.clear()
    price.send_keys(cost_electricity)

    price = driver.find_element(By.XPATH, "//*[@id='input-hashrate']")
    price.clear()
    price.send_keys(hash)

    price = driver.find_element(By.XPATH, "//*[@id='input-consumption']")
    price.clear()
    price.send_keys(potreb)

    price = driver.find_element(By.XPATH, "//*[@id='input-commission']")
    price.clear()
    price.send_keys(komm)

    time.sleep(3)

    rows = driver.find_element(By.CLASS_NAME, 'dataTables_scrollBody')

    row_body = rows.find_element(By.TAG_NAME, 'tbody')
    row_name = row_body.find_elements(By.TAG_NAME, 'tr')

    bable = []

    for row in row_name:
        row_text = row.text
        median_text = row_text.split()
        pre_fi = [median_text[0] + ' ' + median_text[1], median_text[2] + ' ' +
                  median_text[3], median_text[4], median_text[5] + median_text[6], median_text[7]]
        bable.append(pre_fi)

    df = pd.DataFrame(bable, columns=['Период', 'Награда', 'Доход', 'Расходы', 'Прибыль'])

    columns = ['Период', 'Награда', 'Доход', 'Расходы', 'Прибыль']
    data = df[columns].values.tolist()

    font = ImageFont.truetype('arial.ttf', 22)
    cell_size = (250, 120)

    num_rows = len(data)
    num_cols = len(columns)
    table_size = (num_cols * cell_size[0], (num_rows + 1) * cell_size[1])

    im = Image.new('RGB', table_size, (255, 255, 255))
    draw = ImageDraw.Draw(im)

    for i, col in enumerate(columns):
        draw.rectangle((i * cell_size[0] + 100, 100, (i + 1) * cell_size[0] + 100, cell_size[1] + 100),
                       fill=(255, 255, 255), outline=(255, 255, 255))
        draw.text((i * cell_size[0] + 48, 90), col, font=font, fill=(0, 0, 0))

    for i in range(num_rows):
        for j in range(num_cols):
            draw.rectangle(
                ((j * cell_size[0], (i + 1) * cell_size[1]), ((j + 1) * cell_size[0], (i + 2) * cell_size[1])),
                fill=(255, 255, 255), outline=(255, 255, 255))
            draw.text((j * cell_size[0] + 50, (i + 1) * cell_size[1] + 50), str(data[i][j]), font=font, fill=(0, 0, 0))

    filename = r"C:\Users\37533\PycharmProjects\parser\parser\logo_new.png"

    with Image.open(filename) as img:
        img.load()
    im.paste(img, (10, 10), mask=img.convert('RGBA'))
    im.save(fr"C:\Users\37533\PycharmProjects\parser\photos\{user_name}.png")

    driver.quit()

    filename = fr"C:\Users\37533\PycharmProjects\parser\photos\{user_name}.png"

    await message.answer_photo(photo=FSInputFile(filename))

