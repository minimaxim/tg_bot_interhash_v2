from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message

from loader import CHAT_ID, bot

user_chat_router = Router(name='user_chat')


@user_chat_router.message(F.chat.type == ChatType.PRIVATE)
async def forward(message: Message):

    await message.forward(chat_id=CHAT_ID,)

    username = message.from_user.username

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"Сообщение от пользователя @{username}"
    )


@user_chat_router.message(F.chat.type == ChatType.SUPERGROUP, F.reply_to_message)
async def answer(message: Message):
    await bot.send_message(
        chat_id=message.reply_to_message.forward_from.id,
        text=message.text,
    )
