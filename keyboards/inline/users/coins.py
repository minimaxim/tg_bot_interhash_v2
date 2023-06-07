from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.users.general import UserCallbackData
from models import Coin


async def coin_ikb() -> InlineKeyboardMarkup:
    coins = await Coin.all(is_published=True)
    coins_iter = iter(coins)
    coins_iter = map(list, zip_longest(*([coins_iter]*2)))
    buttons = [
        [
            InlineKeyboardButton(
                text=coin.name.upper(),
                callback_data=UserCallbackData(
                    target='coins',
                    action='get',
                    coin_id=coin.id
                ).pack()
            )
            for coin in line
            if coin
        ]
        for line in coins_iter
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)