import logging

from aiogram import types, Router
from aiogram.filters import StateFilter
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from repository.crud.stations import StationRepo

router = Router()

logger = logging.getLogger(__name__)


@router.message(StateFilter(None))
async def get_station(message: types.Message, session: AsyncSession) -> None:
    code = message.text.strip()
    try:
        station = await StationRepo(session).get(code=code)
    except NoResultFound:
        await message.reply("Кажется, код неверный!")
        return

    await message.answer(station.text)
