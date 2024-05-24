from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.keyboards.callbacks.callbacks as cb
import app.database.shop_methods as db_shop


decide_auto_ans_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Автоматически 🤖", callback_data=cb.yes_auto)],
        [InlineKeyboardButton(text="В ручном режиме 📝", callback_data=cb.no_auto)],
    ]
)

go_back_from_balance_replenishment = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Главное меню 🏠", callback_data=cb.main_menu)],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.balance)],
    ]
)

balance_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Пополнить картой 💳", callback_data=cb.balance_replenishment
            )
        ],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.main_menu)],
    ]
)

answers_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Архивные 🗄", callback_data=cb.archive_fb)],
        [
            InlineKeyboardButton(
                text="Отзывы без ответов 🆕", callback_data=cb.unanswered
            )
        ],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.main_menu)],
    ]
)

go_to_main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Главное меню 🏠", callback_data=cb.main_menu)]
    ]
)

starting_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить магазин ➕", callback_data=cb.add_shop)],
        [InlineKeyboardButton(text="Главное меню 🏠", callback_data=cb.main_menu)],
    ]
)

setting_ratings_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="На все отзывы ↕️", callback_data=cb.select_all_ratings
            )
        ],
        [
            InlineKeyboardButton(
                text="Отзывы выше 2*(2-5) ⭐️⭐️", callback_data=cb.select_gt2_ratings
            )
        ],
        [
            InlineKeyboardButton(
                text="Отзывы выше 3*(3-5) ⭐️⭐️⭐️", callback_data=cb.select_gt3_ratings
            )
        ],
        [
            InlineKeyboardButton(
                text="Отзывы выше 4*(4-5) ⭐️⭐️⭐️⭐️", callback_data=cb.select_gt4_ratings
            )
        ],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.shop_list)],
    ]
)

support_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Пользовательское соглашение 📄", callback_data=cb.offerta
            )
        ],
        [
            InlineKeyboardButton(
                text="Обратиться в поддержку 🆘", callback_data=cb.get_support
            )
        ],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.main_menu)],
    ]
)

go_back_from_shop_name_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад ↩️", callback_data=cb.add_shop)]]
)

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои кабинеты 💼", callback_data=cb.shop_list)],
        [InlineKeyboardButton(text="Ответы 📝", callback_data=cb.answers)],
        [InlineKeyboardButton(text="Баланс 💰", callback_data=cb.balance)],
        [InlineKeyboardButton(text="Поддержка 🆘", callback_data=cb.support)],
    ]
)

chosen_shop_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Режим обработки ответов и фильтры оценок ⚙️",
                callback_data=cb.setting_auto,
            )
        ],
        [
            InlineKeyboardButton(
                text="Удалить магазин ❌", callback_data=cb.setting_delete
            )
        ],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.shop_list)],
        [InlineKeyboardButton(text="Главное меню 🏠", callback_data=cb.main_menu)],
    ]
)

archive_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Список последних 5 👇", callback_data=cb.archive_last_5
            )
        ],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.answers)],
        [InlineKeyboardButton(text="Главное меню 🏠", callback_data=cb.main_menu)],
    ]
)

archive_menu_on_last_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Загрузить ещё 👇", callback_data=cb.show_more)],
        [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.archive_fb)],
        [InlineKeyboardButton(text="Главное меню 🏠", callback_data=cb.main_menu)],
    ]
)


async def archive_menu_on_last_keyboard(less_than_five: bool) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    if not less_than_five:
        builder.button(text="Загрузить ещё 👇", callback_data=cb.show_more)

    builder.button(text="Назад ↩️", callback_data=cb.archive_fb)

    builder.button(text="Главное меню 🏠", callback_data=cb.main_menu)

    builder.adjust(1, True)

    return builder.as_markup()


async def shop_list_build(telegram_id: int) -> InlineKeyboardMarkup:
    got_list = await db_shop.get_shops_list(telegram_id)

    builder = InlineKeyboardBuilder()

    for shop in got_list:
        builder.button(text=shop, callback_data=cb.settings + shop)

    builder.button(text="Добавить магазин ➕", callback_data=cb.add_shop)

    builder.button(text="Назад ↩️", callback_data=cb.main_menu)

    builder.adjust(1, True)

    return builder.as_markup()


async def go_back_from_settings_errors_kb(shop_name: str) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(text="Назад ↩️", callback_data=cb.settings + shop_name)
    builder.button(text="Главное меню 🏠", callback_data=cb.main_menu)

    builder.adjust(1, True)

    return builder.as_markup()


async def unanswered_last(fb_id: str, less_than_five: bool) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(text="Сгенерировать 🤖", callback_data=cb.generate + fb_id)

    if not less_than_five:
        builder.button(text="Загрузить ещё 👇", callback_data=cb.show_more)

    builder.button(text="Назад ↩️", callback_data=cb.answers)
    builder.button(text="Главное меню 🏠", callback_data=cb.main_menu)

    builder.adjust(1, True)

    return builder.as_markup()


async def publish(fb_id: str) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(text="Опубликовать ответ 🌐", callback_data=cb.publish + fb_id)
    builder.button(text="Редактировать ✍️", callback_data=cb.edit_generated + fb_id)

    builder.adjust(1, True)

    return builder.as_markup()
