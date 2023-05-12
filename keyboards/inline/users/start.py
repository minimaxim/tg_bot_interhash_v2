from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Start
from .general import UserCallbackData


async def start_ikb() -> InlineKeyboardMarkup:
    starts = await Start.all(is_published=True)
    starts_iter = iter(starts)
    starts_iter = map(list, zip_longest(*([starts_iter]*1)))
    buttons = [
        [
            InlineKeyboardButton(
                text=start.name.upper(),
                callback_data=UserCallbackData(
                    target='category',
                    action='get',
                    start_id=start.id
                ).pack()
            )
            for start in line
            if start
        ]
        for line in starts_iter
    ]
    # print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
