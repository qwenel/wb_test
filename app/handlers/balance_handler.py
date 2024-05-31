from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from api.robocassa.robocassa import create_pay_link
import app.keyboards.callbacks.callbacks as cb
from ..keyboards.inlineKeyboards import balance_replenish_by_card_keyboard
from ..states.userStates import UserStates


router_balance = Router()


# Balance replenishment
@router_balance.callback_query(F.data == cb.balance_replenishment)
async def balance_replenishment(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.balance_replenishment)

    link100 = create_pay_link(499, "покупка+100+токенов")
    link500 = create_pay_link(1390, "покупка+500+токенов")
    link1000 = create_pay_link(2490, "покупка+1000+токенов")

    await callback_query.message.edit_text(
        text=f"link100: {link100}\n\n"
        + f"link500 : {link500}\n\n"
        + f"link1000 : {link1000}"
    )

    # await callback_query.message.edit_text(
    #     text="Выбери сумму пополнения",
    #     reply_markup=await balance_replenish_by_card_keyboard(
    #         link100, link500, link1000
    #     ),
    # )

    await callback_query.answer()
    await state.clear()
    await state.set_state(UserStates.menu)
