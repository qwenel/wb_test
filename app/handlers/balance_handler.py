import asyncio
from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from api.robocassa.robocassa import create_pay_link
from app.database.payments_method import get_last_payment_id, new_payment
from app.database.user_methods import inc_balance
import app.keyboards.callbacks.callbacks as cb
from ..keyboards.inlineKeyboards import (
    balance_replenish_web_app_keyboard,
    after_payment_keyboard,
)
from main import logger
from ..states.userStates import UserStates


tokens = {
    499: 100,
    1390: 500,
    2490: 1000,
}


router_balance = Router()


# Balance replenishment
@router_balance.callback_query(F.data == cb.balance_replenishment)
async def balance_replenishment(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.balance_replenishment)

    await new_payment(callback_query.from_user.id)
    get_invId = get_last_payment_id(callback_query.from_user.id)

    if get_invId is None:
        await callback_query.message.edit_text(
            text="Упс... Произошла непредвиденная ошибка.\n\n"
            + "Простите за предоставленные неудобства, пожалуйста, повторите попытку позднее 😔",
            reply_markup=after_payment_keyboard,
        )
        return

    link1 = create_pay_link(1, get_invId, "тестовая+покупка")
    link100 = create_pay_link(499, get_invId, "покупка+100+токенов")
    link500 = create_pay_link(1390, get_invId, "покупка+500+токенов")
    link1000 = create_pay_link(2490, get_invId, "покупка+1000+токенов")

    await callback_query.message.edit_text(
        text="Выбери сумму пополнения",
        reply_markup=await balance_replenish_web_app_keyboard(
            link1, link100, link500, link1000
        ),
    )

    await callback_query.answer()


async def payment_status_success(
    bot: Bot, user_id: int, out_sum: int, state: FSMContext
):
    await state.set_state(UserStates.menu)

    await bot.send_message(
        user_id,
        text=f"Отлично! Покупка на сумму <b>{out_sum} RUB</b> прошла успешно!"
        + f"\n\nВаш баланс пополнен на <b>{tokens[out_sum]} токенов</b>!",
        parse_mode="HTML",
        reply_markup=after_payment_keyboard,
    )


async def payment_status_success(
    bot: Bot, user_id: int, out_sum: int, state: FSMContext
):
    await state.set_state(UserStates.menu)

    tokens = {
        499: 100,
        1390: 500,
        2490: 1000,
    }

    await inc_balance(user_id, tokens[out_sum])

    await bot.send_message(
        user_id,
        text=f"Отлично! Покупка на сумму <b>{out_sum} RUB</b> прошла успешно!"
        + f"\n\nВаш баланс пополнен на <b>{tokens[out_sum]} токенов</b>!",
        parse_mode="HTML",
        reply_markup=after_payment_keyboard,
    )


async def payment_status_failure(
    bot: Bot, user_id: int, out_sum: int, state: FSMContext
):
    await state.set_state(UserStates.menu)

    await bot.send_message(
        user_id,
        text=f"Произошла ошибка! Покупка на сумму <b>{out_sum} RUB</b> не осуществлена!"
        + f"\n\nПопробуйте ещё раз...",
        parse_mode="HTML",
        reply_markup=after_payment_keyboard,
    )


# @router_balance.message(content_type=['web_app_data'])
# async def getRequest(request: Message):


# @router_balance.callback_query(
#     UserStates.balance_replenishment, F.data == cb.link_pressed
# )
# async def process_pressed_link(callback_query: CallbackQuery, state: FSMContext):

#     tokens = callback_query.data[len(cb.link_pressed) :]

#     out_sum = {"1": 1, "100": 499, "500": 1390, "1000": 2490}

#     link = create_pay_link(out_sum[tokens], f"Покупка+{tokens}+токенов")

#     await callback_query.message.edit_text(text=f"Ваша ссылка на оплату:\n\n{link}")

#     await callback_query.answer()

#     asyncio.sleep(2)

#     await callback_query.message.edit_text(
#         text=f"Оплата прошла успешно!\n\nБаланс пополнен на {callback_query.data[len(cb.link_pressed):]}",
#         reply_markup=go_to_main_menu_keyboard,
#     )
