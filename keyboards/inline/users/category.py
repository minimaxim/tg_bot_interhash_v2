from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Category
from .general import UserCallbackData


async def category_paginator_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:
    categories = await Category.all(is_published=True)
    categories_iter = iter(categories)
    categories = list(zip_longest(*([categories_iter] * 5)))
    categories_page = list(filter(lambda x: x, categories[callback_data.category_page]))
    buttons = [
        [
            InlineKeyboardButton(
                text=category.name.upper(),
                callback_data=UserCallbackData(**callback_data.dict() | {
                    'target': 'brand',
                    'action': 'get',
                    'category_id': category.id
                }).pack()
            )
        ]
        for category in categories_page
    ]
    buttons += [
        [
            InlineKeyboardButton(
                text='🔙',
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'start',
                        'action': 'all',
                    }
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
