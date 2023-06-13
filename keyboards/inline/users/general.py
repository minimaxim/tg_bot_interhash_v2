from aiogram.filters.callback_data import CallbackData


class UserCallbackData(CallbackData, prefix='user'):
    target: str
    action: str
    start_id: int = None
    category_id: int = None
    coin_id: int = None
    currency_id: int = None
    power_id: int = None
    discont_id: int = None
    promo_id: int = None
    app_id: int = None
