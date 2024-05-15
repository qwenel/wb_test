from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.callbacks.callbacks as cb
from ..keyboards.inlineKeyboards import go_back_from_balance_replenishment
from ..states.userStates import UserStates

router_answers = Router()


@router_answers.callback_query(F.data==cb.last_5_answers)
async def show_last_answers(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.show_last_answers)

    await callback_query.answer()


@router_answers.callback_query(F.data==cb.example)
async def show_example(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.example_answer)
    
    await callback_query.answer()


@router_answers.callback_query(F.data==cb.show_more)
async def show_more_answers(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.show_more_answers)
    
    await callback_query.answer()