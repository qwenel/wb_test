from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)


register_shop = KeyboardButton(text="Добавить магазин 🛍")
menu_start = ReplyKeyboardMarkup([
    [register_shop]
    ], resize_keyboard=True)


cancel_button_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text='Отмена ❌')]
], resize_keyboard=True)