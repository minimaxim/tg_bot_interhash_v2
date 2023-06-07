from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.users.general import UserCallbackData
from models import Currency


async def cur_ikb() -> InlineKeyboardMarkup:
    currencies = await Currency.all(is_published=True)
    currencies_iter = iter(currencies)
    currencies_iter = map(list, zip_longest(*([currencies_iter]*2)))
    buttons = [
        [
            InlineKeyboardButton(
                text=currency.name.upper(),
                callback_data=UserCallbackData(
                    target='curs',
                    action='get',
                    currency_id=currency.id
                ).pack()
            )
            for currency in line
            if currency
        ]
        for line in currencies_iter
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)