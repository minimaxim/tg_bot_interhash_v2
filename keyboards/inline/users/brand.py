from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Brand
from .general import UserCallbackData


async def brand_paginator_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:
    brands = await Brand.all(is_published=True)
    brands_iter = iter(brands)
    brands = list(zip_longest(*([brands_iter] * 5)))
    brands_page = list(filter(lambda x: x, brands[callback_data.brand_page]))
    buttons = [
        [
            InlineKeyboardButton(
                text=brand.name.upper(),
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'model',
                        'action': 'get',
                        'brand_id': brand.id
                    }
                ).pack()
            )
        ]
        for brand in brands_page
    ]
    buttons += [
        [
            InlineKeyboardButton(
                text='🔙',
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'category',
                        'action': 'all',
                    }
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)