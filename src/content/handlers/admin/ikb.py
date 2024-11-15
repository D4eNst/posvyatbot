from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить администратора", callback_data="admin_add_superuser"),
        ],
        [
            InlineKeyboardButton(text="Сообщения бота", callback_data="admin_messages page_1"),
            InlineKeyboardButton(text="Кодовые слова", callback_data="admin_stations page_1"),
        ]
    ])
    return ikb


def admin_back_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отменить", callback_data="admin_main_menu")]]
    )
    return ikb
