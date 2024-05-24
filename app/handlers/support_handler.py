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
                [InlineKeyboardButton(text="Назад", callback_data=cb.support)],
                [InlineKeyboardButton(text="Главное меню", callback_data=cb.main_menu)],
            ]
        ),
    )


@router_support.callback_query(UserStates.support_menu, F.data == cb.offerta)
async def get_offerta(callback_query: CallbackQuery):
    await callback_query.answer()

    oferta = FSInputFile("res/docs/oferta_122500000350.docx")

    await callback_query.message.answer_document(
        document=oferta,
        caption="Наше пользовательское соглашение",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Главное меню", callback_data=cb.main_menu)]
            ]
        ),
    )
