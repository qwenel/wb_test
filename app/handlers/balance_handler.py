from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.callbacks.callbacks as cb
from ..keyboards.inlineKeyboards import go_back_from_balance_replenishment
from ..states.userStates import UserStates


router_balance = Router()


# Balance replenishment
@router_balance.callback_query(F.data==cb.balance_replenishment)
async def balance_replenishment(callback_query : CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.balance_replenishment)
    
    await callback_query.message.edit_text(text="Здесь ты должен увидеть успешное пополнение баланса!",
                                           reply_markup=go_back_from_balance_replenishment)
    
    await callback_query.answer()
    await state.clear()
    await state.set_state(None)