import os
import time

import psycopg2
from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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
    x = range(1, 100000)

    return list(x)


@user_answer_router.message(Text(text=get_list(), ignore_case=True))
async def handle_message_click(message: Message):
    x = message.text.split('/')
    user = message.from_user.id
    algo = x[1]

    if message.text in ['/SHA256', '/Sia', '/Blake14r', '/Kadena', '/Handsnake']:
        await message.answer(
            text='Укажите хэшрейт (Th/s):',
        )
    elif message.text in ['/Scrypt', '/X11', '/Quark', '/Qubit', '/MyrGroestl', '/Skein', '/LBRY', '/Lyra2REv2', '/Keccak',
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

    cur.execute("""SELECT asic_name FROM users WHERE id = (%s)""", (user,))
    asic = cur.fetchall()[0][0]
    conn.commit()

    cur.close()
    conn.close()

    chrome_options = Options()
    # chrome_options.add_argument()

    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    url = 'https://whattomine.com/asic'

    driver.get(url)

    time.sleep(2)

    if asic == 'SHA256':

        asic_element = driver.find_element(By.NAME, "factor[sha256_hr]")
        asic_element.clear()
        asic_element.send_keys(f"{kolvo}\n")
        driver.quit()



        # elif asic == 'Scrypt':
        #     asic_element = driver.find_element(By.NAME, "factor[scrypt_hash_rate]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'X11':
        #     asic_element = driver.find_element(By.NAME, "factor[x11_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Sia':
        #     asic_element = driver.find_element(By.NAME, "factor[sia_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Quark':
        #     asic_element = driver.find_element(By.NAME, "factor[qk_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Qubit':
        #     asic_element = driver.find_element(By.NAME, "factor[qb_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Myr':
        #     asic_element = driver.find_element(By.NAME, "factor[mg_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Skein':
        #     asic_element = driver.find_element(By.NAME, "factor[sk_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'LBRY':
        #     asic_element = driver.find_element(By.NAME, "factor[lbry_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Blake':
        #     asic_element = driver.find_element(By.NAME, "factor[bk14_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'CryptoNight':
        #     asic_element = driver.find_element(By.NAME, "factor[cn_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'CryptoNightSTC':
        #     asic_element = driver.find_element(By.NAME, "factor[cst_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Equihash':
        #     asic_element = driver.find_element(By.NAME, "factor[eq_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Lyra2REv2':
        #     asic_element = driver.find_element(By.NAME, "factor[lrev2_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'BCD':
        #     asic_element = driver.find_element(By.NAME, "factor[bcd_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Lyra2z':
        #     asic_element = driver.find_element(By.NAME, "factor[l2z_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Keccak':
        #     asic_element = driver.find_element(By.NAME, "factor[kec_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Groestl':
        #     asic_element = driver.find_element(By.NAME, "factor[gro_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Eaglesong':
        #     asic_element = driver.find_element(By.NAME, "factor[esg_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Cuckatoo31':
        #     asic_element = driver.find_element(By.NAME, "factor[ct31_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Cuckatoo32':
        #     asic_element = driver.find_element(By.NAME, "factor[ct32_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Kadena':
        #     asic_element = driver.find_element(By.NAME, "factor[kd_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'Handshake':
        #     asic_element = driver.find_element(By.NAME, "factor[hk_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()
        #
        #
        # elif asic == 'RandomX':
        #     asic_element = driver.find_element(By.NAME, "factor[rmx_hr]")
        #     asic_element.clear()
        #     asic_element.send_keys(f"{kolvo}\n")
        #     time.sleep(2)
        #
        #     driver.quit()


