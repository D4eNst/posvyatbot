from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from content.handlers.admin.stations import ikb
from repository.crud.stations import StationRepo
from repository.models import Station
from .states import AdminAddStationState

router = Router()


@router.callback_query(StateFilter(None), F.data.startswith("admin_stations"))
async def admin_stations_list(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    await callback_query.answer()

    # getting page from callback data like "admin_stations page_1"
    page = int(callback_query.data.split()[1].split("_")[1])
    page_size = 5

    cnt, stations = await StationRepo(session).get_page(page_size, page)
    page_cnt = (cnt - 1) // page_size + 1
    try:
        await callback_query.message.edit_text(
            "Список",
            reply_markup=ikb.admin_stations_ikb(stations, page, page_cnt)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(StateFilter(None), F.data.startswith("admin_add_station"))
async def admin_add_station(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminAddStationState.GET_STATION_NAME)
    await callback_query.message.edit_text("Введите название:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddStationState.GET_STATION_NAME, F.text)
async def set_station_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(AdminAddStationState.GET_STATION_TEXT)
    await message.answer("Введите текст сообщения, который увидят участники:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddStationState.GET_STATION_NAME)
async def incorrect_station_name(message: types.Message) -> None:
    await message.answer("Произошла ошибка, введите название снова:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddStationState.GET_STATION_TEXT, F.text)
async def set_station_text(message: types.Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(AdminAddStationState.GET_STATION_GROUP)
    await message.answer("Введите группу, за которой будет закреплено кодовое слово:",
                         reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddStationState.GET_STATION_TEXT)
async def incorrect_station_text(message: types.Message) -> None:
    await message.answer("Произошла ошибка, введите текст снова:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddStationState.GET_STATION_GROUP, F.text)
async def set_station_group(message: types.Message, state: FSMContext) -> None:
    await state.update_data(group=message.text)
    await state.set_state(AdminAddStationState.GET_STATION_CODE)
    await message.answer("Введите кодовое слово:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddStationState.GET_STATION_GROUP)
async def incorrect_station_group(message: types.Message):
    await message.answer("Произошла ошибка, введите группу снова:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddStationState.GET_STATION_CODE, F.text)
async def set_station_code(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(code=message.text)
    data = await state.get_data()
    station_repo = StationRepo(session)

    try:
        station = await station_repo.create(**data)
        await message.answer(f"Сохранение \"{station.name}\" с кодовым словом {station.code}...")
    except Exception as e:
        await message.answer(f"Во время создания произошла ошибка: \n{e}")

    await state.clear()
    cnt, stations = await station_repo.get_page(5, 1)
    page_cnt = (cnt - 1) // 5 + 1
    await message.answer("Список", reply_markup=ikb.admin_stations_ikb(stations, 1, page_cnt))


@router.message(AdminAddStationState.GET_STATION_GROUP)
async def incorrect_station_code(message: types.Message) -> None:
    await message.answer("Произошла ошибка, введите кодовое слово снова:", reply_markup=ikb.admin_back_ikb())


@router.callback_query(StateFilter(None), F.data.startswith("admin_station"))
async def admin_station_info(callback_query: types.CallbackQuery, session: AsyncSession) -> None:
    try:
        station = await StationRepo(session).get(Station.id == int(callback_query.data.split()[1]))
    except NoResultFound:
        await callback_query.answer(text=f"Ошибка: не найдено", show_alert=True)
        return

    await callback_query.message.edit_text(
        f"<b>Название</b>: {station.name}\n"
        f"<b>Группа</b>: {station.group}\n"
        f"<b>Кодовое слово</b>: {station.code}\n"
        f"<b>Текст сообщения</b>: {station.text}",
        reply_markup=ikb.admin_edit_station_ikb(station, current_page=int(callback_query.data.split()[2]))
    )


@router.callback_query(StateFilter(None), F.data.startswith("admin_delete_station"))
async def admin_station_delete(callback_query: types.CallbackQuery, session: AsyncSession) -> None:
    station_repo = StationRepo(session)

    try:
        await station_repo.delete(Station.id == int(callback_query.data.split()[1]))
        await callback_query.answer("Удаление...")
    except Exception as e:
        await callback_query.answer(f"Ошибка: {e}", show_alert=True)

    cnt, stations = await station_repo.get_page(5, 1)
    page_cnt = (cnt - 1) // 5 + 1
    await callback_query.message.edit_text("Список",
                                           reply_markup=ikb.admin_stations_ikb(stations, 1, page_cnt))
