from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from repository.models import Message


def admin_messages_ikb(messages: Sequence[Message], page: int, page_cnt: int) -> InlineKeyboardMarkup:
    messages_list_btns = [
        [InlineKeyboardButton(text=message.name, callback_data=f"admin_message {message.id} {page}")]
        for message in messages
    ]
    messages_list_btns.extend([
        [
            InlineKeyboardButton(text="⬅", callback_data=f"admin_messages page_{max(page - 1, 1)}"),
            InlineKeyboardButton(text=f"{page}/{max(1, page_cnt)}", callback_data="None"),
            InlineKeyboardButton(text="➡", callback_data=f"admin_messages page_{min(page_cnt + 1, page_cnt)}")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="admin_main_menu"),
            InlineKeyboardButton(text="Добавить", callback_data="admin_add_message")
        ]
    ])
    ikb = InlineKeyboardMarkup(inline_keyboard=messages_list_btns)
    return ikb


def admin_back_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отменить", callback_data="admin_main_menu")]]
    )
    return ikb


def admin_edit_message_ikb(message: Message, current_page: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Удалить", callback_data=f"admin_delete_message {message.id}"),
        InlineKeyboardButton(text="Назад", callback_data=f"admin_messages page_{current_page}"),
    ]])
    return ikb
