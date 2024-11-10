from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сообщения бота", callback_data="bot_messages page_1"),
            InlineKeyboardButton(text="Кодовые слова", callback_data="admin_stations page_1"),
        ]
    ])
    return ikb
