import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from content.handlers.basic import kb
from content.handlers.basic.states import StartState
from data.config import settings
from repository.crud.messages import MessageRepo
from repository.crud.stations import StationRepo
from repository.crud.users import UserRepo
from repository.models import User

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()

    user_repo = UserRepo(session)
    try:
        await user_repo.get(telegram_id=message.from_user.id)
    except NoResultFound:
        await user_repo.create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            is_superuser=message.from_user.id == settings.ADMIN_ID,
        )

    message_repo = MessageRepo(session)
    start_message = await message_repo.get_or_none(slug="start")

    start_message_text = (
        "Стартовое сообщение не задано. Администратор должен добавить стартовое сообщение, используя slug \"start\""
    ) if start_message is None else start_message.text

    await message.answer(start_message_text, reply_markup=kb.get_reply_kb("ГОТОВ"))
    await state.set_state(StartState.GET_USER_READY)


@router.message(StartState.GET_USER_READY, F.text.lower() == "готов")
async def user_ready(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    message_repo = MessageRepo(session)
    user_ready_message = await message_repo.get_or_none(slug="user_ready")

    user_ready_message_text = (
        "Сообщение не задано. Администратор должен добавить стартовое сообщение, используя slug \"user_ready\""
    ) if user_ready_message is None else user_ready_message.text

    await message.answer(user_ready_message_text)
    await state.set_state(StartState.GET_USER_GROUP)


@router.message(StartState.GET_USER_READY)
async def user_not_ready(message: types.Message) -> None:
    await message.answer("Для продолжения напиши \"ГОТОВ\" "
                         "или воспользоваться соответствующей кнопкой")


@router.message(StartState.GET_USER_GROUP, F.text.regexp(r'[A-Za-zА-Яа-я0-9]+'))
async def user_set_group(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    user_repo = UserRepo(session)
    await user_repo.update(User.telegram_id == message.from_user.id, group=message.text)
    await state.clear()

    first_station = await StationRepo(session).get_or_none(group=message.text)
    if first_station is not None:
        await message.answer(first_station.text)
    else:
        await message.answer(f"Для продолжения введите кодовое слово или убедитесь, что правильно указали номер группы."
                             f" Чтобы изменить группу, воспользуйтесь командой /start")


@router.message(StartState.GET_USER_GROUP)
async def invalid_user_group(message: types.Message) -> None:
    await message.answer("Для продолжения необходимо указать номер группы")
