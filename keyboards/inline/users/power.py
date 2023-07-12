from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.models import Power
from .general import UserCallbackData


async def power_ikb() -> InlineKeyboardMarkup:
    powers = await Power.all(is_published=True)
    powers_iter = iter(powers)
    powers_iter = map(list, zip_longest(*([powers_iter] * 2)))
    buttons = [
        [
            InlineKeyboardButton(
                text=power.name.upper(),
                callback_data=UserCallbackData(
                    target='power',
                    action='get',
                    power_id=power.id
                ).pack()
            )
            for power in line
            if power
        ]
        for line in powers_iter
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
