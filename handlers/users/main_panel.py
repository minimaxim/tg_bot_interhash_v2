from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from keyboards.reply.users import main_panel
from models import User

user_main_router = Router(name='user_main_panel')


@user_main_router.message(F.text == '/start')
async def command_start(message: Message):
    await message.delete()
    if await User.get(pk=message.from_user.id):

        filename = fr"C:\Users\37533\PycharmProjects\parser-v2\photos\start_im.jpg"

        await message.answer_photo(
            photo=FSInputFile(filename),
            caption='👋 Привет, '

                    'Мы компания Interhash, Занимаемся предоставлением комплексных услуг для майнинга. '
                    'Мы на рынке с 2017 года и являемся официальным представителями майнинг-пула ViaBTC'
                    ' в Европе и странах СНГ.',
            reply_markup=main_panel
        )

    else:
        user = User(id=message.from_user.id, name=message.from_user.full_name, username=f'@{message.from_user.username}')
        await user.save()

        filename = fr"C:\Users\37533\PycharmProjects\parser-v2\photos\start_im.jpg"

        await message.answer_photo(
            photo=FSInputFile(filename),
            caption='👋 Привет, '

                 'Мы компания Interhash, Занимаемся предоставлением комплексных услуг для майнинга. '
                 'Мы на рынке с 2017 года и являемся официальным представителями майнинг-пула ViaBTC'
                 ' в Европе и странах СНГ.',
            reply_markup=main_panel
        )

