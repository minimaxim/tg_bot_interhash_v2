from aiogram.filters.callback_data import CallbackData


class UserCallbackData(CallbackData, prefix='user'):
    target: str
    action: str
    start_id: int = None
    brand_id: int = None
    model_id: int = None
    category_id: int = None
    product_id: int = None
    size_id: int = None
    videocard_id: int = None
    videohash_id: int = None
    asic_id: int = None
    brand_page: int = 0
    category_page: int = 0
    videocard_page: int = 0
    model_page: int = 0
