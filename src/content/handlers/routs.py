from aiogram import Router

from .basic.handlers import router as basic_router
from .stations.handlers import router as stations_router

main_router = Router()
main_router.include_routers(
    basic_router,
    stations_router,

)
