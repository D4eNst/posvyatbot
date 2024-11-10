from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from repository.models import Station


def admin_stations_ikb(stations: Sequence[Station], page_num: int, page_cnt: int) -> InlineKeyboardMarkup:
    stations_list_btns = [
        [InlineKeyboardButton(text=station.name, callback_data=f"admin_station {station.id}")] for station in stations
    ]
    stations_list_btns.append([
        InlineKeyboardButton(text="⬅", callback_data=f"admin_stations page_{max(page_num - 1, 1)}"),
        InlineKeyboardButton(text=f"{page_num}/{page_cnt}", callback_data="None"),
        InlineKeyboardButton(text="➡", callback_data=f"admin_stations page_{min(page_cnt + 1, page_cnt)}")
    ])
    ikb = InlineKeyboardMarkup(inline_keyboard=stations_list_btns)
    return ikb
