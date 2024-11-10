import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from content.handlers.admin import ikb as admin_ikb
from repository.crud.users import UserRepo

from .stations.handlers import router as admin_stations_router

router = Router()
router.include_routers(
    admin_stations_router,
)

logger = logging.getLogger(__name__)


@router.message(Command("admin"))
async def cmd_start(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    user = await UserRepo(session).get(telegram_id=message.from_user.id)
    if not user.is_superuser:
        return

    await message.answer("Админ панель", reply_markup=admin_ikb.admin_menu_ikb())
    await state.clear()
