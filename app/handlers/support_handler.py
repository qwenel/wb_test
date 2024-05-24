from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
)

from app.keyboards.callbacks import callbacks as cb
from app.states.userStates import UserStates


router_support = Router()


@router_support.callback_query(UserStates.support_menu, F.data == cb.get_support)
async def get_support(callback_query: CallbackQuery):
    await callback_query.answer()

    await callback_query.message.edit_text(
        text="По вопросам обращайтесь в поддержку (тут будет ссылка)",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад ↩️", callback_data=cb.support)],
                [
                    InlineKeyboardButton(
                        text="Главное меню 🏠", callback_data=cb.main_menu
                    )
                ],
            ]
        ),
    )


@router_support.callback_query(UserStates.support_menu, F.data == cb.offerta)
async def get_offerta(callback_query: CallbackQuery):
    await callback_query.answer()

    oferta = FSInputFile("res/docs/oferta_122500000350.docx")

    await callback_query.message.answer(
        text="Привет!\n\n@iiwbbot помогает продавцам на маркетплейсах отвечать на отзывы и вопросы с помощью технологий искусственного интеллекта."
        + " Каждый отзыв и вопрос вызывает у нейросети генерацию уникального ответа, который невозможно отличить от человеческого.\n\n"
        + "Этот сервис способен автоматически реагировать на все ваши отзывы и запросы, полностью заменяя потребность в сотруднике. "
        + "Он также позволяет отвечать в режиме полуавтоматики, где вы можете просмотреть и отредактировать ответ по необходимости, а также в ручном режиме.\n\n"
        + "Мы ценим ваше время и стремимся сделать эту задачу как можно более легкой и быстрой. Присоединяйтесь к боту и оцените его возможности!\n"
        + "1 токен = 1 ответу на отзыв или вопрос.\nВ скобках указана стоимость 1 токена для каждого пакета.\n"
        + "499 р - 100 ответов (1 токен=4,99 р)\n1390 р - 500 ответов (1 токен = 2,78 р)\n2490 р - 1000 ответов (1 токен = 2,49 р)\n\n"
        + "1 токен = 1 ответу на отзыв или вопрос.\nВ скобках указана стоимость 1 токена для каждого пакета.\n499 р - 100 ответов (1 токен=4,99 р)\n"
        + "1390 р - 500 ответов (1 токен = 2,78 р)\n2490 р - 1000 ответов (1 токен = 2,49 р)\n\n"
        + "Полное наименование: Алексеев Сергей Владиславович\nИНН: 122500000350\nОГРН/ОГРНИП: 320121500004811\nКонтактный телефон: +7 927 887-13-16\n"
        + "Контактный e-mail: serga29121995@mail.ru",
    )

    await callback_query.message.answer_document(
        document=oferta,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Главное меню 🏠", callback_data=cb.main_menu
                    )
                ]
            ]
        ),
    )
