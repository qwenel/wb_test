from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext

from api.gpt.gpt_api import generate_answer
from app.keyboards.inlineKeyboards import unanswered_last, generated_answer_keyboard, go_to_main_menu_keyboard
import app.keyboards.callbacks.callbacks as cb
from ..states.userStates import UserStates

from app.database.answer_methods import get_feedback_to_generate_answer, get_unanswered_fb_list, get_feedback, update_answer_text
from .unanswered_feedbacks.unanswered_handler import router_unanswered



router_answers = Router()

router_answers.include_router(
    router_unanswered
)

    

@router_answers.callback_query(F.data==cb.archive_fb)
async def show_archive(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.show_more_answers)
    
    await callback_query.answer()