from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


qurry = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text=' ХОЧУ КУПИТЬ ОБОРУДОВАНИЕ 🏦'
            )
        ]
    ]
)
