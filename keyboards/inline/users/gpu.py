from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .general import UserCallbackData


async def all_list_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:

    buttons = [
        [
            InlineKeyboardButton(
                text='🔙',
                callback_data=UserCallbackData(
                    **callback_data.dict() | {
                        'target': 'start',
                        'action': 'all',
                    }
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)