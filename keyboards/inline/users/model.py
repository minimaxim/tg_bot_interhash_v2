from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Model
from .general import UserCallbackData


async def model_paginator_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:
    models = await Model.all(is_published=True)
    models_iter = iter(models)
    models = list(zip_longest(*([models_iter] * 5)))
    models_page = list(filter(lambda x: x, models[callback_data.model_page]))
    buttons = [
        [
            InlineKeyboardButton(
                text=model.name.upper(),
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'model',
                        'action': 'get',
                        'model_id': model.id
                    }
                ).pack()
            )
        ]
        for model in models_page
    ]
    buttons += [
        [
            InlineKeyboardButton(
                text='🔙',
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'brand',
                        'action': 'get',
                    }
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
