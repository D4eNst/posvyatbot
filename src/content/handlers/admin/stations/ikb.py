from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from repository.models import Station


def admin_stations_ikb(stations: Sequence[Station], page: int, page_cnt: int) -> InlineKeyboardMarkup:
    stations_list_btns = [
        [InlineKeyboardButton(text=station.name, callback_data=f"admin_station {station.id} {page}")]
        for station in stations
    ]
    stations_list_btns.extend([
        [
            InlineKeyboardButton(text="⬅", callback_data=f"admin_stations page_{max(page - 1, 1)}"),
            InlineKeyboardButton(text=f"{page}/{max(1, page_cnt)}", callback_data="None"),
            InlineKeyboardButton(text="➡", callback_data=f"admin_stations page_{min(page_cnt + 1, page_cnt)}")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="admin_main_menu"),
            InlineKeyboardButton(text="Добавить", callback_data="admin_add_station")
        ]
    ])
    ikb = InlineKeyboardMarkup(inline_keyboard=stations_list_btns)
    return ikb


def admin_back_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отменить", callback_data="admin_main_menu")]]
    )
    return ikb


def admin_edit_station_ikb(station: Station, current_page: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Удалить", callback_data=f"admin_delete_station {station.id}"),
        InlineKeyboardButton(text="Назад", callback_data=f"admin_stations page_{current_page}"),
    ]])
    return ikb
