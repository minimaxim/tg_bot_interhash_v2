from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.models import Promo
from .general import UserCallbackData


async def promo_ikb() -> InlineKeyboardMarkup:
    promos = await Promo.all(is_published=True)
    promos_iter = iter(promos)
    promos_iter = map(list, zip_longest(*([promos_iter] * 2)))
    buttons = [
        [
            InlineKeyboardButton(
                text=promo.name.upper(),
                callback_data=UserCallbackData(
                    target='promo',
                    action='get',
                    promo_id=promo.id
                ).pack()
            )
            for promo in line
            if promo
        ]
        for line in promos_iter
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
