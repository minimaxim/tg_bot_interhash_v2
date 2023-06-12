from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from parser.connection import connect_to_db
from openpyxl import Workbook

user_admin_router = Router(name='user_admin_panel')


@user_admin_router.message(F.text == 'Проверить пользователей🥳')
async def send_start_ikb(message: Message):

    workbook = Workbook()

    sheet = workbook.active

    conn = connect_to_db()

    cur = conn.cursor()

    cur.execute("""SELECT * FROM users""")
    rows = cur.fetchall()

    headers = ['id ', 'name', 'username', 'start_name', 'category_name', 'model_name', 'kolvo', 'call_me', 'discont',
               'power', 'currency', 'coin', 'cost_electricity', 'hash', 'potreb', 'komm', 'promo', 'date']

    sheet.append(headers)

    for row in rows:
        sheet.append(row)

    workbook.save(fr"C:\Users\37533\PycharmProjects\parser-v2\userlist\users.xlsx")

    filename = fr"C:\Users\37533\PycharmProjects\parser-v2\userlist\users.xlsx"

    cur.close()
    conn.close()

    await message.answer_document(document=FSInputFile(filename))
