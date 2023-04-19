from aiogram import Router

from .main_panel import user_main_router
from .start import user_start_router

user_router = Router(name='users')
user_router.include_router(router=user_main_router)
user_router.include_router(router=user_start_router)


__all__: list[str] = [
    'user_router'
]