from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.models import Discont
from .general import UserCallbackData


async def discont_ikb() -> InlineKeyboardMarkup:
    disconts = await Discont.all(is_published=True)
    disconts_iter = iter(disconts)
    disconts_iter = map(list, zip_longest(*([disconts_iter] * 2)))
    buttons = [
        [
            InlineKeyboardButton(
                text=discont.name.upper(),
                callback_data=UserCallbackData(
                    target='discont',
                    action='get',
                    discont_id=discont.id
                ).pack()
            )
            for discont in line
            if discont
        ]
        for line in disconts_iter
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
