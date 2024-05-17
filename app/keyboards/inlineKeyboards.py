from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.keyboards.callbacks.callbacks as cb
import app.database.shop_methods as db_shop


decide_auto_ans_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Автоматически", callback_data=cb.yes_auto)],
    [InlineKeyboardButton(text='В ручном режиме', callback_data=cb.no_auto)]
])

go_back_from_balance_replenishment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Главное меню", callback_data=cb.main_menu)],
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.balance)]
])

balance_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пополнить картой", callback_data=cb.balance_replenishment)],
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.main_menu)]
])

answers_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Список последних 5", callback_data=cb.last_5_answers)],
    [InlineKeyboardButton(text="Загрузить ещё", callback_data=cb.show_more)],
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.main_menu)]
])

go_to_main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Главное меню", callback_data=cb.main_menu)]
])

go_back_from_delete_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.delete_shop)],
    [InlineKeyboardButton(text="Главное меню", callback_data=cb.main_menu)]
])

starting_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить магазин", callback_data=cb.add_shop)],
    [InlineKeyboardButton(text="Главное меню", callback_data=cb.main_menu)]
])

setting_ratings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="На все отзывы", callback_data=cb.select_all_ratings)],
    [InlineKeyboardButton(text="Отзывы выше 2*(2-5)", callback_data=cb.select_gt2_ratings)],
    [InlineKeyboardButton(text="Отзывы выше 3*(3-5)", callback_data=cb.select_gt3_ratings)],
    [InlineKeyboardButton(text="Отзывы выше 4*(4-5)", callback_data=cb.select_gt4_ratings)],
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.shop_list)]
])

go_back_from_support = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.main_menu)]
])

go_back_from_shop_name_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.add_shop)]
])

main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мои кабинеты", callback_data=cb.shop_list)],
    [InlineKeyboardButton(text="Ответы", callback_data=cb.answers)],
    [InlineKeyboardButton(text="Баланс", callback_data=cb.balance)],
    [InlineKeyboardButton(text="Поддержка", callback_data=cb.support)],
])

chosen_shop_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сменить фильтр рейтинга", callback_data=cb.switch_rating)],
    [InlineKeyboardButton(text="Сменить режим обработки отзывов", callback_data=cb.setting_auto)],
    [InlineKeyboardButton(text="Удалить магазин", callback_data=cb.delete_shop)],
    [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.shop_list)],
    [InlineKeyboardButton(text="Главное меню", callback_data=cb.main_menu)]
])

async def shop_list_build(telegram_id: int) -> InlineKeyboardMarkup:
    got_list = await db_shop.get_shops_list(telegram_id)
    
    builder = InlineKeyboardBuilder()
    
    for shop in got_list:
        builder.button(text=shop, callback_data=cb.settings+shop)
        
    builder.button(text="Добавить магазин", callback_data=cb.add_shop)
    
    builder.button(text="Назад ↩️", callback_data=cb.main_menu)
    
    builder.adjust(1, True)
    
    return builder.as_markup()