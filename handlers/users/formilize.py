import time
from datetime import datetime

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, CallbackQuery
from keyboards.inline.users import coin_ikb
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
    coin = State()
    cost_electr = State()
    hash_rate = State()
    potr_electr = State()
    comm_pull = State()
    finish = State()
    finish2 = State()


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


@user_fromilize_router.message(Form.potr_electr)
async def get_potr(message: Message, state: FSMContext):

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
async def get_comm(message: Message, state: FSMContext):

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
async def get_final(message: Message, state: FSMContext):

    com = message.text
    user = message.from_user.id

    connect_to_db()

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET komm = (%s) WHERE id = (%s)""", (com, user))
    conn.commit()


    await state.update_data(comm_pull=message.text)
    await state.update_data(finish='done')

    await message.answer(
        text='Происходит расчет, пожалуйста, подождите...',
        reply_markup=main_panel
    )


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

    cur.execute("""SELECT coin FROM users WHERE id = (%s)""", (user,))
    conn.commit()
    coin = cur.fetchall()[0][0]

    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://ultramining.com/crypto-calc/{coin}/")

    if currency == 'USD $':
        driver.find_element(By.CLASS_NAME, 'input-group-append').click()
        time.sleep(1)
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

    time.sleep(1)

    rows = driver.find_element(By.CLASS_NAME, 'dataTables_scrollBody')

    row_body = rows.find_element(By.TAG_NAME, 'tbody')
    row_name = row_body.find_elements(By.TAG_NAME, 'tr')

    bable = []

    for row in row_name:
        row_text = row.text
        median_text = row_text.split()
        median_text[2] = str("{0:.10f}".format(float(median_text[2])))
        pre_fi = [median_text[0] + ' ' + median_text[1], median_text[2] + ' ' +
                  median_text[3], median_text[4], median_text[5] + median_text[6], median_text[7]]
        bable.append(pre_fi)

    df = pd.DataFrame(bable, columns=['Period', 'Reward', 'Income', 'Expenses', 'Profit'])

    columns = ['Period', 'Reward', 'Income', 'Expenses', 'Profit']
    data = df[columns].values.tolist()

    font = ImageFont.truetype('arial.ttf', 22)
    cell_size = (270, 130)

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

    filename = fr"C:\Users\37533\PycharmProjects\parser-v2\logo_new.png"

    with Image.open(filename) as img:
        img.load()
    im.paste(img, (10, 10), mask=img.convert('RGBA'))
    im.save(fr"C:\Users\37533\PycharmProjects\parser-v2\photos\{user_name}.png")

    driver.quit()

    filename = fr"C:\Users\37533\PycharmProjects\parser-v2\photos\{user_name}.png"

    await message.answer_photo(photo=FSInputFile(filename))

    date = str(datetime.now())
    user = message.from_user.id

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""UPDATE users SET date = (%s) WHERE id = (%s)""", (date, user))
    conn.commit()

    await state.clear()

    cur.close()
    conn.close()

