from aiogram.fsm.state import StatesGroup, State


class AdminAddStationState(StatesGroup):
    GET_STATION_NAME = State()
    GET_STATION_TEXT = State()
    GET_STATION_CODE = State()
    GET_STATION_GROUP = State()
