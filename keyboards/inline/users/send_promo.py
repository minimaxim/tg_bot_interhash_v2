from itertools import zip_longest

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.models import Application
from .general import UserCallbackData


async def send_promo_ikb() -> InlineKeyboardMarkup:
    button = [
        [
            InlineKeyboardButton(
                text="Зарегистрироваться",
                url="https://www.viabtc.net/signup?refer=533030"
                )
        ]
    ]
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=button)
