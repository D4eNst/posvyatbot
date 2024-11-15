from aiogram.fsm.state import StatesGroup, State


class AdminAddSuperuser(StatesGroup):
    GET_USERNAME = State()
