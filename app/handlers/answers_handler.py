from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.callbacks.callbacks as cb
from ..states.userStates import UserStates

from app.database.answer_methods import get_unanswered_fb_list


router_answers = Router()


@router_answers.callback_query(F.data==cb.unanswered)
async def show_last_answers(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.show_last_answers)
    
    await callback_query.answer()
    
    unanswered_feedbacks = await get_unanswered_fb_list(callback_query.from_user.id)
    
    if unanswered_feedbacks == False:
        await callback_query.message.answer(text="увы нет отзывов")
        await state.set_state(UserStates.menu)
        await state.clear()
        return
    
    await callback_query.message.answer(text="ОТЗЫВ\n\n"+
                                        f"Оценка: {unanswered_feedbacks[0][0]}\n"+
                                        f"Магазин: {unanswered_feedbacks[0][1]}\n"+
                                        f"Товар: {unanswered_feedbacks[0][2]}\n"+
                                        f"Текст:\n{unanswered_feedbacks[0][3]}")


@router_answers.callback_query(F.data==cb.archive_fb)
async def show_more_answers(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.show_more_answers)
    
    await callback_query.answer()