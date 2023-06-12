from itertools import zip_longest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models import Category
from .general import UserCallbackData


async def category_ikb() -> InlineKeyboardMarkup:
    categories = await Category.all(is_published=True)
    categories_iter = iter(categories)
    categories_iter = map(list, zip_longest(*([categories_iter] * 1)))
    buttons = [
        [
            InlineKeyboardButton(
                text=category.name.upper(),
                callback_data=UserCallbackData(
                    target='brand',
                    action='get',
                    category_id=category.id
                ).pack()
            )
            for category in line
            if category
        ]
        for line in categories_iter
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
