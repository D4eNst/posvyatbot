from aiogram import Router

from .basic.handlers import router as basic_router
from .stations.handlers import router as stations_router
from .admin.handlers import router as admin_router

main_router = Router()
main_router.include_routers(
    basic_router,
    admin_router,
    stations_router,

)
