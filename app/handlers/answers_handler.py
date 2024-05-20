from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

import app.keyboards.callbacks.callbacks as cb
from ..states.userStates import UserStates

from app.database.answer_methods import get_unanswered_fb_list


router_answers = Router()


@router_answers.callback_query(F.data==cb.unanswered)
async def show_unanswered(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.unanswered)
    
    await callback_query.answer()
    
    unanswered_feedbacks = await get_unanswered_fb_list(callback_query.from_user.id)
    
    if unanswered_feedbacks == False:
        await callback_query.message.answer(text="увы нет отзывов")
        await state.set_state(UserStates.menu)
        await state.clear()
        return
    
    for i in range(len(unanswered_feedbacks)):
        if i != len(unanswered_feedbacks) - 1:
            await callback_query.message.answer(text="ОТЗЫВ\n\n"+
                                            f"Оценка: {unanswered_feedbacks[i][0]}\n"+
                                            f"Магазин: {unanswered_feedbacks[i][1]}\n"+
                                            f"Товар: {unanswered_feedbacks[i][2]}\n"+
                                            f"Текст:\n{unanswered_feedbacks[i][3]}",
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                [InlineKeyboardButton(text="Сгенерировать", callback_data=cb.generate+unanswered_feedbacks[0][4])]
                                            ]))
            continue
        await callback_query.message.answer(text="ОТЗЫВ\n\n"+
                                            f"Оценка: {unanswered_feedbacks[i][0]}\n"+
                                            f"Магазин: {unanswered_feedbacks[i][1]}\n"+
                                            f"Товар: {unanswered_feedbacks[i][2]}\n"+
                                            f"Текст:\n{unanswered_feedbacks[i][3]}",
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                [InlineKeyboardButton(text="Сгенерировать", callback_data=cb.generate+unanswered_feedbacks[0][4])]
                                            ]))
        
        


# @router_answers.callback_query(UserStates.show_last_answers, F.data[:4] == cb.generate)


@router_answers.callback_query(F.data==cb.archive_fb)
async def show_more_answers(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.show_more_answers)
    
    await callback_query.answer()