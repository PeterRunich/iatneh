from ._base_keyboard_pagination import BaseKeyboardPagination, BaseKeyboardPaginationExtension, BasePaginationControls
from aiogram.types import InlineKeyboardButton
from ...database.db import Sqlite
import math
"""Создаёт и возвращает inline панель с жанрами и pagination"""

async def filter_kb_builder(current_page_number, last_page_num, limit, genre_ids=[]):
    offset = (current_page_number - 1) * limit
    data = Sqlite().get_genres(limit, offset)
    callback_id = 'cq1'

    return BaseKeyboardPagination(last_page_num,
                                  callback_id,
                                  current_page_number,
                                  [GenreFilters(data, genre_ids), BasePaginationControls(), GenresFilterControls()]).kb

class GenreFilters(BaseKeyboardPaginationExtension):
    def __init__(self, all_genres, selected_genre_ids):
        self.selected_genre_ids = selected_genre_ids
        self.all_genres = all_genres

    def _extender(self):
        for genre in self.all_genres:
            genre_id = genre[0]
            genre_name = genre[1]
            #мб стоит вынести логичку отсюда
            if str(genre_id) in self.selected_genre_ids:
                genre_name += ' ✅'
                action = 'remove_from_filter'
            else:
                action = 'add_to_filter'
            #мб стоит вынести логичку отсюда
            if len(genre_name) > 15:
                self.pgn.kb.row_width = 1
                self.pgn.kb.row(InlineKeyboardButton(genre_name, callback_data=f'{self.pgn.callback_id}:{action}:{genre_id}'))
            else:
                self.pgn.kb.insert(InlineKeyboardButton(genre_name, callback_data=f'{self.pgn.callback_id}:{action}:{genre_id}'))
                self.pgn.kb.row_width = 3

class GenresFilterControls(BaseKeyboardPaginationExtension):
    def _extender(self):
        self.pgn.kb.add(InlineKeyboardButton('Перейти на страницу по номеру', callback_data="cq1:ask_page_to_go:"),
                        InlineKeyboardButton('Поиск жанра по названию', callback_data="cq1:find_genre_by_name:"),
                        InlineKeyboardButton('Показать выбраные жанры', callback_data="cq1:show_selected_genres:"),
                        InlineKeyboardButton('Поиск 🔎', callback_data="cq1:search:"))
