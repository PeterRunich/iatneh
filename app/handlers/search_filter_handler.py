from ..keyboards.anime_show_keyboard import anime_show_kb_builder
from aiogram.dispatcher.filters.state import State, StatesGroup
from ..keyboards.canel_keyboard import canel_kb_builder
from ..helpers.start_kb_helper import start_kb
from aiogram.dispatcher.filters import Text
from ...database.db import Sqlite
from ..bot import dispatcher
"""Обработчик поиска аниме по имени"""

class Search(StatesGroup): # отвечает за описание FSM маршрута
    waiting_for_name = State() # определяем возможный стейт

@dispatcher.message_handler(Text(equals="поиск", ignore_case=True), state="*")
async def search_by_name_dialog(msg):
    kb = await canel_kb_builder()
    await msg.answer('Напиши название, если хотите прервать поиск нажми кнопку', reply_markup=kb)
    await Search.waiting_for_name.set() # переходим на состояние waiting_for_name

@dispatcher.message_handler(state=Search.waiting_for_name) # обработчик состояния waiting_for_name
async def search(msg, state):
    if msg.text == '/canel': # если команда /canel то обнуляем состояние
        await state.finish() # обнуляем состояние т.к это конечное состояние
        await start_kb(msg) # возваращаем клавиатуру главного меню /start
        return True # прерываем функцию т.к пользователь не захотел идти дальше

    kb = await anime_show_kb_builder(Sqlite().find_anime_by_name(msg.text)) # строим клавиатуру из результатов метода find_anime_by_name из бд
    await state.finish() # обнуляем состояние т.к это конечное состояние
    await start_kb(msg) # возваращаем клавиатуру главного меню /start

    await msg.answer('Поиск по "' + msg.text + '"')
    await msg.answer('Результаты:', reply_markup=kb)