from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.shop_settings import set_rating
from app.keyboards.callbacks import callbacks as cb
from app.keyboards import inlineKeyboards as in_kb
from app.states.userStates import UserStates


router_answers = Router()
    

# ======= GOT AUTO FOR AUTO ANSWERS
@router_answers.callback_query(UserStates.awaiting_auto_choose, F.data==cb.yes_auto)    
async def yes_auto_answer(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.awaiting_rating)
    
    await callback_query.answer()
    
    await callback_query.message.edit_text(text="<b>Автоматический режим</b> - выбор профессионалов)\n\n"+
                                            "Здесь вы можете гибко настроить, как бот будет отвечать на ваши отзывы, в зависимости от их оценки.\n\n"+
                                            "Например\n\nВы можете выбрать, чтобы на все отзывы с оценкой 5 и 4 звезды бот отвечал в полностью автоматическом режиме.\n\n"+
                                            "На все остальные отзывы [с оценками 3, 2, 1 звезда] бот будет создавать ответ, но будет присылать вам на согласование.\n\n"+
                                            "Выберите на какие отзывы отвечать автоматически?⤵️",
                                            parse_mode='HTML',
                                            reply_markup=in_kb.setting_ratings_keyboard)
    
    
# ======= GOT MANUAL FOR AUTO ANSWERS
@router_answers.callback_query(UserStates.awaiting_auto_choose, F.data==cb.no_auto)    
async def no_auto_answer(callback_query: CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    await state.set_state(UserStates.menu)
    await state.clear()
    await callback_query.answer()
    
    if not await set_rating(callback_query.from_user.id, data["shop_name"], "0"):
        callback_query.message.answer(text="Произошла непредвиденная ошибка.",
                                      reply_markup=await in_kb.go_back_from_settings_errors_kb(data["shop_name"]))
    
    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!\n\n"+
                                            "Я буду отвечать на отзывы в <b>ручном</b> режиме",
                                            parse_mode='HTML',
                                            reply_markup=in_kb.go_to_main_menu_keyboard)
