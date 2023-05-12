from aiogram import Router


from .main_panel import user_main_router
from .start import user_start_router
from .category import user_category_router
from .brand import user_brand_router
from .model import user_model_router
from .answer import user_answer_router
from .kol_vo import user_kolvo_router


user_router = Router(name='users')
user_router.include_router(router=user_main_router)
user_router.include_router(router=user_start_router)
user_router.include_router(router=user_category_router)
user_router.include_router(router=user_brand_router)
user_router.include_router(router=user_model_router)
user_router.include_router(router=user_answer_router)
user_router.include_router(router=user_kolvo_router)


__all__: list[str] = [
    'user_router'
]