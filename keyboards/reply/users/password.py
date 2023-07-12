from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

pass_panel = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='Проверим кто ты?'
            )
        ],
    ]
)
