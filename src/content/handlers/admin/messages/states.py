from aiogram.fsm.state import StatesGroup, State


class AdminAddMessageState(StatesGroup):
    GET_MESSAGE_NAME = State()
    GET_MESSAGE_SLUG = State()
    GET_MESSAGE_TEXT = State()

