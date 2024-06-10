from aiogram import F, Bot, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ..database.user_methods import add_user, get_balance

from ..keyboards.inlineKeyboards import (
    starting_keyboard,
    main_menu_keyboard,
    shop_list_build,
    balance_menu_keyboard,
    support_menu,
    answers_menu_keyboard,
)
from ..states.userStates import UserStates
from .shop_handler import router_shop
from .balance_handler import router_balance
from .feedbacks_handler import router_answers
from .support_handler import router_support

import app.keyboards.callbacks.callbacks as cb


router_main = Router()
router_main.include_routers(router_shop, router_answers, router_balance, router_support)


# Starting!!!
@router_main.message(CommandStart())
async def start_msg(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(UserStates.started)

    if not await add_user(message.chat.id):
        pass

    await message.answer(
        text="Привет, это сервис искусственного интеллекта разработанный для Wildberries @iiwbbot ✌️\n\n"
        + "Я работаю на основе Искусственного интеллекта и умею полностью автономно отвечать на отзывы и вопросы покупателей и публиковать их🔥\n\n"
        + "Я умею сглаживать конфликты и мои ответы совершенно не отличаются от ответов человека😎\n\n"
        + "Для автоматических ответов добавьте магазин",
        reply_markup=starting_keyboard,
    )


# Main menu
@router_main.callback_query(F.data == cb.main_menu)
async def main_menu(callback_query: CallbackQuery, state: FSMContext):

    if callback_query.message.document:
        await callback_query.message.answer(
            text="Выберите один из пунктов главного меню:",
            reply_markup=main_menu_keyboard,
        )
    else:
        await callback_query.message.edit_text(
            text="Выберите один из пунктов главного меню:",
            reply_markup=main_menu_keyboard,
        )

    await state.set_state(UserStates.menu)
    await state.clear()
    await callback_query.answer()


# List of stores
@router_main.callback_query(F.data == cb.shop_list)
async def shop_list(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.shop_list)

    await callback_query.message.edit_text(
        text="Ваши магазины:",
        reply_markup=await shop_list_build(callback_query.from_user.id),
    )
    await callback_query.answer()


# BOT Answers
@router_main.callback_query(F.data == cb.answers)
async def answers_menu(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.answers_menu)

    await callback_query.message.edit_text(
        text="Здесь вы можете посмотреть архивные и неотвеченные отзывы. Что хотите посмотреть?",
        reply_markup=answers_menu_keyboard,
    )

    await callback_query.answer()


# Balance menu
@router_main.callback_query(F.data == cb.balance)
async def balance_menu(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.balance_menu)

    balance = await get_balance(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=f"Вам доступно <b>{balance}</b> токенов на отзывы и вопросы.",
        reply_markup=balance_menu_keyboard,
        parse_mode="HTML",
    )

    await callback_query.answer()


# Support message
@router_main.callback_query(F.data == cb.support)
async def support_msg(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.support_menu)
    await callback_query.answer()

    await callback_query.message.edit_text(
        text="Выберите пункт меню", reply_markup=support_menu
    )


# @router_main.message(Command("getAllUsers"))
# async def getUsersList(message: Message):

#     list_of_users = await get_users()
#     print(list_of_users)

#     if len(list_of_users) == 0:
#         await message.answer(text="Список пользователей пуст, что очень странно...")

#     await message.answer(text="Список пользователей:\n\n"+
#                          "\n".join(list_of_users))
