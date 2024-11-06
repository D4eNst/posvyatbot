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


@router.message()
async def get_station(message: types.Message, session: AsyncSession) -> None:
    code = message.text.strip().lower()
    try:
        station = await StationRepo(session).get(code=code)
    except NoResultFound:
        await message.reply("Кажется, код неверный!")
        return

    await message.answer(station.text)
