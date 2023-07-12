from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def send_promo_ikb() -> InlineKeyboardMarkup:
    button = [
        [
            InlineKeyboardButton(
                text="Зарегистрироваться",
                url="https://www.viabtc.net/signup?refer=533030"
            )
        ]
    ]
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=button)
