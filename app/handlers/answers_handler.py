from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext

from app.keyboards.inlineKeyboards import unanswered_last, generated_answer_keyboard, go_to_main_menu_keyboard
import app.keyboards.callbacks.callbacks as cb
from ..states.userStates import UserStates

from app.database.answer_methods import get_unanswered_fb_list, get_feedback, update_answer_text


router_answers = Router()


@router_answers.callback_query(F.data==cb.unanswered)
async def show_unanswered(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.unanswered)
    
    await callback_query.answer()
    
    unanswered_feedbacks = await get_unanswered_fb_list(callback_query.from_user.id)
    
    if unanswered_feedbacks == False:
        await callback_query.message.answer(text="увы нет новых или неотвеченных отзывов",
                                            reply_markup=go_to_main_menu_keyboard)
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
                                            reply_markup=await unanswered_last(unanswered_feedbacks[i][4]))
        

@router_answers.callback_query(UserStates.unanswered, F.data[:4] == cb.generate)
async def generate(callback_query: CallbackQuery, state: FSMContext):
    
    await state.update_data(fb_id=callback_query.data[4:])
    await state.update_data(answer="Сгенерировал ответ!")
    
    await callback_query.answer()
    
    await callback_query.message.edit_text(text=callback_query.message.text + 
                                           f"\n\nОтвет:\n<code>Сгенерировал ответ!</code>",
                                           parse_mode='HTML',
                                           reply_markup=generated_answer_keyboard)
    
    
@router_answers.callback_query(UserStates.unanswered, F.data==cb.edit_generated)
async def edit_generated(callback_query:CallbackQuery, state: FSMContext):
    
    await callback_query.answer()
    
    await callback_query.message.answer(text="Для редактирования полученного отзыва:\n\n"+
                                        "\t • Нажмите в поле ответа для его копирования.\n"+
                                        "\t • Вставьте скопированный текст в поле для ввода\n"+
                                        "\t • Отредактируйте отзыв и отправьте его мне!")
    
@router_answers.message(UserStates.editing)
async def check_edited(message: Message, state: FSMContext):
    
    await state.update_data(answer=message.text)
    
    data = await state.get_data()

    feedback = await get_feedback(data['fb_id'])
    
    await message.answer(text="ОТЗЫВ\n\n"+
                        f"Оценка: {feedback[0]}\n"+
                        f"Магазин: {feedback[1]}\n"+
                        f"Товар: {feedback[2]}\n"+
                        f"Текст:\n{feedback[3]}"+
                        f"\n\nОтвет:\n<code>{message.text}</code>",
                        parse_mode='HTML',
                        reply_markup=generated_answer_keyboard)


@router_answers.callback_query(UserStates.unanswered, F.data==cb.publish)
async def publishing(callback_query:CallbackQuery, state:FSMContext):
    await callback_query.answer()
    
    data = await state.get_data()

    feedback = data['fb_id']
    answer = data['answer']
    
    await update_answer_text(feedback, answer)
    
    await callback_query.message.answer(text="Отлично, работаю над публикацией, спасибо за доверие!",
                                        reply_markup=go_to_main_menu_keyboard)
    
    # TODO: вызов функции ответа на отзыв
    
    await state.clear()
    await state.set_state(UserStates.menu)
    

@router_answers.callback_query(F.data==cb.archive_fb)
async def show_more_answers(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.show_more_answers)
    
    await callback_query.answer()