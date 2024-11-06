from aiogram.fsm.state import StatesGroup, State


class StartState(StatesGroup):
    GET_USER_GROUP = State()
    GET_USER_READY = State()
