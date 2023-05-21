from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


finish_panel = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='НАЖМИТЕ СЮДА 🏦'
            )
        ],
        [
            KeyboardButton(
                text='РАССЧИТАТЬ 🏁'
            )
        ],
    ]
)