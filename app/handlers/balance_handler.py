import asyncio
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from api.robocassa.robocassa import create_pay_link
import app.keyboards.callbacks.callbacks as cb
from ..keyboards.inlineKeyboards import (
    balance_replenish_by_card_keyboard,
    balance_replenish_web_app_keyboard,
    go_to_main_menu_keyboard,
)
from ..states.userStates import UserStates


router_balance = Router()


# Balance replenishment
@router_balance.callback_query(F.data == cb.balance_replenishment)
async def balance_replenishment(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.balance_replenishment)

    link1 = create_pay_link(1, "тестовая покупка")
    link100 = create_pay_link(499, "покупка+100+токенов")
    link500 = create_pay_link(1390, "покупка+500+токенов")
    link1000 = create_pay_link(2490, "покупка+1000+токенов")

    await callback_query.message.edit_text(
        text="Выбери сумму пополнения",
        reply_markup=await balance_replenish_web_app_keyboard(
            link1, link100, link500, link1000
        ),
    )

    await callback_query.answer()


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
