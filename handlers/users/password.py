import json
import psycopg2

from aiogram import F, Router
from aiogram.types import Message
from aiohttp import connector

from models import Admin, User
from keyboards.reply.users import admin, main_panel, pass_panel

user_password_router = Router(name='user_password_router')


@user_password_router.message(F.text == '/password')
async def get_text_message(message: Message):
    await message.answer('Привет, нажми на кнопку', reply_markup=pass_panel)


@user_password_router.message(F.text == 'Проверим кто ты?')
async def proporty(message: Message):
    await message.delete()
    if await Admin.get(pk=message.from_user.id):
        await message.answer(text=f'Снова зравствуйте, {message.from_user.full_name}😎', reply_markup=admin)
    else:
        await message.answer(text='доступ закрыт ')