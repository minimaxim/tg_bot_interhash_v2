from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_panel = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='У МЕНЯ ЕСТЬ ВОПРОС 🏦'
            )
        ],
        # [
        #     KeyboardButton(
        #         text='КАЛЬКУЛЯТОР ДОХОДНОСТИ 🏦'
        #     )
        # ],
        # [
        #     KeyboardButton(
        #         text='ХОЧУ КУПИТЬ ОБОРУДОВАНИЕ 🏦'
        #     ),
        # ],
        # [
        #     KeyboardButton(
        #         text=' ИНДИВИДУАЛЬНАЯ КОНСУЛЬТАЦИЯ 🏦'
        #     )
        # ]
    ]
)
