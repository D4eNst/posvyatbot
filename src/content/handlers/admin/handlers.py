import logging

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from content.handlers.admin import ikb as admin_ikb
from repository.crud.users import UserRepo
from repository.models import User
from .messages.handlers import router as admin_messages_router
from .states import AdminAddSuperuser
from .stations.handlers import router as admin_stations_router

router = Router()
router.include_routers(
    admin_stations_router,
    admin_messages_router
)

logger = logging.getLogger(__name__)


@router.message(Command("admin"))
async def admin_main_menu(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    user = await UserRepo(session).get(telegram_id=message.from_user.id)
    if not user.is_superuser:
        return

    await message.answer("Админ панель", reply_markup=admin_ikb.admin_menu_ikb())


@router.callback_query(F.data.startswith("admin_main_menu"))
async def admin_stations_list(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    await callback_query.answer()

    user = await UserRepo(session).get(telegram_id=callback_query.from_user.id)
    if not user.is_superuser:
        return

    await callback_query.message.edit_text("Админ панель", reply_markup=admin_ikb.admin_menu_ikb())


@router.callback_query(F.data.startswith("admin_add_superuser"))
async def admin_stations_list(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminAddSuperuser.GET_USERNAME)
    await callback_query.message.edit_text(
        "Введите username пользователя (то, что используется в телеграм после @):",
        reply_markup=admin_ikb.admin_back_ikb()
    )


@router.message(AdminAddSuperuser.GET_USERNAME, F.text)
async def admin_main_menu(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    user_repo = UserRepo(session)

    current_user = await user_repo.get(telegram_id=message.from_user.id)
    if not current_user.is_superuser:
        return

    try:
        await user_repo.update(User.username == message.text, is_superuser=True)
        await message.answer("Успешно добавлен")
    except NoResultFound:
        await message.answer(f"Пользователя с username {message.text} не найдено")

    await state.clear()
    await message.answer("Админ панель", reply_markup=admin_ikb.admin_menu_ikb())


@router.message(AdminAddSuperuser.GET_USERNAME)
async def incorrect_station_code(message: types.Message) -> None:
    await message.answer("Произошла ошибка, введите username снова:", reply_markup=admin_ikb.admin_back_ikb())
