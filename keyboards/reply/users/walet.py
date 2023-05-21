from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


walet_panel = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='RUS🇷🇺'
            ),
            KeyboardButton(
                text='USA🇱🇷'
            )
        ]
    ]
)