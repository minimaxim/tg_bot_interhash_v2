from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputFile, FSInputFile
from keyboards.inline.users import start_ikb
from keyboards.inline.users.general import UserCallbackData
from parser.connection import connect_to_db
from openpyxl import Workbook

user_start_router = Router(name='user_start')


@user_start_router.message(F.text == 'НАЖМИТЕ СЮДА 🏦')
async def send_start_ikb(message: Message):
    await message.delete()
    await message.answer(
        text='👋 Привет, '
             
             'Мы компания Interhash, Занимаемся предоставлением комплексных услуг для майнинга. Мы на рынке с 2017 года и являемся официальным представителями майнинг-пула ViaBTC в Европе и странах СНГ.',
        reply_markup=await start_ikb()
    )

@user_start_router.message(F.text == '/password')
async def get_text_message(message: Message):

    workbook = Workbook()

    sheet = workbook.active

    conn = connect_to_db()

    cur = conn.cursor()

    cur.execute("""SELECT * FROM users""")
    rows = cur.fetchall()

    headers = ['id ', 'name', 'start_name', 'category_name', 'brand_name', 'model_name', 'currency',
               'cost_electricity ', 'hash', 'potreb', 'komm', 'coin']

    sheet.append(headers)

    for row in rows:
        sheet.append(row)

    workbook.save(fr"C:\Users\37533\PycharmProjects\parser\userlist\users.xlsx")

    filename = fr"C:\Users\37533\PycharmProjects\parser\userlist\users.xlsx"

    cur.close()
    conn.close()

    await message.answer_document(document=FSInputFile(filename))

@user_start_router.callback_query(UserCallbackData.filter(F.action == 'all'))
async def start_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        text='👋 Привет, '

             'Мы компания Interhash, Занимаемся предоставлением комплексных услуг для майнинга. Мы на рынке с 2017 года и являемся официальным представителями майнинг-пула ViaBTC в Европе и странах СНГ.',
        reply_markup=await start_ikb()
    )
