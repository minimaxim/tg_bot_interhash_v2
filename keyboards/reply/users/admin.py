from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='Проверить пользователей🥳'
            )
        ],
]
)
