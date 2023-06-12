from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.models import Application
from .general import UserCallbackData


async def send_promo_ikb() -> InlineKeyboardMarkup:
    apps = await Application.all(is_published=True)
    apps_iter = iter(apps)
    apps_iter = map(list, zip_longest(*([apps_iter] * 2)))
    buttons = [
        [
            InlineKeyboardButton(
                text=app.name.upper(),
                callback_data=UserCallbackData(
                    target='final',
                    action='get',
                    app_id=app.id
                ).pack()
            )
            for app in line
            if app
        ]
        for line in apps_iter
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)