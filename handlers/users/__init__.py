from aiogram import Router
from .formilize import user_fromilize_router
from .main_panel import user_main_router
from .power import user_power_router
from .start import user_start_router
from .category import user_category_router
from .brand import user_brand_router
from .viabtc import user_viabtc_router
from .password import user_password_router
from .query import user_admin_router


user_router = Router(name='users')
user_router.include_router(router=user_main_router)
user_router.include_router(router=user_start_router)
user_router.include_router(router=user_admin_router)
user_router.include_router(router=user_password_router)
user_router.include_router(router=user_category_router)
user_router.include_router(router=user_brand_router)
user_router.include_router(router=user_fromilize_router)
user_router.include_router(router=user_viabtc_router)
user_router.include_router(router=user_power_router)


__all__: list[str] = [
    'user_router'
]