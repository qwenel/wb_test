import random
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.answer_methods import fill_unanswered_feedback, get_not_null_answer_feedbacks_list
from app.database.user_methods import get_answers_counter
import app.keyboards.callbacks.callbacks as cb
from ..states.userStates import UserStates

from ..keyboards.inlineKeyboards import (
    archive_menu_keyboard, go_to_main_menu_keyboard,
    archive_menu_on_last_keyboard
)

from .unanswered_feedbacks.unanswered_handler import router_unanswered


router_answers = Router()

router_answers.include_router(
    router_unanswered
)


@router_answers.callback_query(F.data=="adder")
async def adder(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    id = random.randint(0, 100)
    
    await fill_unanswered_feedback(f"fb_id{id}", 3, "ViPi", f"did{id}", f"very like did{id}", "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyODY5OTY3NiwiaWQiOiIyOTQ4OGU1NC1mMTdmLTRiYjUtOTcwNi0xMzQ5ZmUwZTc1ZWMiLCJpaWQiOjEwOTU3MTQzMSwib2lkIjoxMjMxMzE0LCJzIjozODQsInNpZCI6Ijc2NjZjYTM4LTVkMWQtNDVlNS04YzNjLTg4NzFlZjdmZGUyYyIsInQiOmZhbHNlLCJ1aWQiOjEwOTU3MTQzMX0.HzNSNmTnnRVlAmIY7I_LPyFRTqX5xgAu6SQBN2JPxQLVnebumo6h88lrU30nhMSCsXUb35pqHhbJx6woEKl1sw")
    

@router_answers.callback_query(F.data==cb.archive_fb)
async def show_archive(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.archive)
    await callback_query.answer()
    
    got_counter = await get_answers_counter(callback_query.from_user.id)
    
    if got_counter is None:
        print("Ошибка! Не удалось получить count_ans у пользователя.")
        await state.clear()
        await state.set_state(UserStates.menu)
        return
    
    await callback_query.message.edit_text(text=f"Я ответили на {got_counter} отзывов! Все в порядке, я справляюсь, Босс)",
                                           reply_markup=archive_menu_keyboard)
        
        
@router_answers.callback_query(UserStates.archive, F.data==cb.archive_last_5)
async def show_last_5(callback_query: CallbackQuery, state: FSMContext):   
    await callback_query.answer()
    
    got_list_of_answered_fbs = await get_not_null_answer_feedbacks_list(callback_query.from_user.id)
    
    if got_list_of_answered_fbs is None:
        await callback_query.message.edit_text(text="увы нет отвеченных отзывов",
                                               reply_markup=go_to_main_menu_keyboard)
        return
    
    feedbacks_to_show = 5
    less_than_five = False
    
    if len(got_list_of_answered_fbs) <= feedbacks_to_show:
        feedbacks_to_show = len(got_list_of_answered_fbs)
        less_than_five = True
        
    await callback_query.message.answer(text="Список последних отвеченных отзывов:")    
    for i in range(feedbacks_to_show):
        
        if i != feedbacks_to_show - 1:
            await callback_query.message.answer(text="ОТЗЫВ\n\n"+
                                            f"Оценка: {got_list_of_answered_fbs[i][0]}\n"+
                                            f"Магазин: {got_list_of_answered_fbs[i][1]}\n"+
                                            f"Товар: {got_list_of_answered_fbs[i][2]}\n"+
                                            f"Текст:\n{got_list_of_answered_fbs[i][3]}\n\n"+
                                            f"Ответ:{got_list_of_answered_fbs[i][4]}")
            continue
        
        await callback_query.message.answer(text="ОТЗЫВ\n\n"+
                                        f"Оценка: {got_list_of_answered_fbs[i][0]}\n"+
                                        f"Магазин: {got_list_of_answered_fbs[i][1]}\n"+
                                        f"Товар: {got_list_of_answered_fbs[i][2]}\n"+
                                        f"Текст:\n{got_list_of_answered_fbs[i][3]}\n\n"+
                                        f"Ответ: {got_list_of_answered_fbs[i][4]}",
                                        reply_markup=await archive_menu_on_last_keyboard(less_than_five))
        
    not_shown_fbs = []   
    if not less_than_five:
        not_shown_fbs = got_list_of_answered_fbs[5:]
        await state.update_data(last_to_show=not_shown_fbs)
    
    
        
@router_answers.callback_query(UserStates.archive, F.data==cb.show_more)
async def show_more(callback_query: CallbackQuery, state: FSMContext): 
    await callback_query.answer()
    
    data = await state.get_data()
    
    got_list_of_answered_fbs = data["last_to_show"]
    
    feedbacks_to_show = 5
    less_than_five = False
    
    if len(got_list_of_answered_fbs) < feedbacks_to_show:
        feedbacks_to_show = len(got_list_of_answered_fbs)
        less_than_five = True
        
    await callback_query.message.answer(text="Список последних отвеченных отзывов:")    
    for i in range(feedbacks_to_show):
        
        if i != feedbacks_to_show - 1:
            await callback_query.message.answer(text="ОТЗЫВ\n\n"+
                                            f"Оценка: {got_list_of_answered_fbs[i][0]}\n"+
                                            f"Магазин: {got_list_of_answered_fbs[i][1]}\n"+
                                            f"Товар: {got_list_of_answered_fbs[i][2]}\n"+
                                            f"Текст:\n{got_list_of_answered_fbs[i][3]}\n\n"+
                                            f"Ответ:{got_list_of_answered_fbs[i][4]}")
            continue
        
        await callback_query.message.answer(text="ОТЗЫВ\n\n"+
                                            f"Оценка: {got_list_of_answered_fbs[i][0]}\n"+
                                            f"Магазин: {got_list_of_answered_fbs[i][1]}\n"+
                                            f"Товар: {got_list_of_answered_fbs[i][2]}\n"+
                                            f"Текст:\n{got_list_of_answered_fbs[i][3]}\n\n"+
                                            f"Ответ:{got_list_of_answered_fbs[i][4]}",
                                            reply_markup=await archive_menu_on_last_keyboard(less_than_five))
        
    not_shown_fbs = []   
    if not less_than_five:
        not_shown_fbs = got_list_of_answered_fbs[5:]
        await state.update_data(last_to_show=not_shown_fbs)
        return
            
    await state.clear()
    await state.set_state(UserStates.menu)