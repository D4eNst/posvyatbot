from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from content.handlers.admin.stations.ikb import admin_stations_ikb
from repository.crud.stations import StationRepo

router = Router()


@router.callback_query(StateFilter(None), F.data.startswith("admin_stations"))
async def admin_stations_list(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    # getting page from callback data like "admin_stations page_1"
    page = int(callback_query.data.split()[1].split("_")[1])
    page_size = 5

    cnt, stations = await StationRepo(session).get_page(page_size, page)
    page_cnt = (cnt - 1) // page_size + 1
    try:
        await callback_query.message.edit_text("Список", reply_markup=admin_stations_ikb(stations, page, page_cnt))
    except TelegramBadRequest:
        pass
