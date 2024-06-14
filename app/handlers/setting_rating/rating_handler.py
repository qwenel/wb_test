from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.exec_methods.shop_settings import set_rating
from app.keyboards.callbacks import callbacks as cb
from app.keyboards import inlineKeyboards as in_kb
from app.states.userStates import UserStates

router_rating = Router()


# ======== GOT FILTER ALL RATINGS
@router_rating.callback_query(UserStates.awaiting_rating, F.data == cb.select_all_ratings)
async def got_ratings_all(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_all_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!\n\n"+
                                            "Теперь бот будет отвечать на отзывы с <b>любыми оценками</b>!",
                                            parse_mode='HTML',
                                            reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)
    

# ======== GOT FILTER GT2 RATINGS
@router_rating.callback_query(UserStates.awaiting_rating, F.data == cb.select_gt2_ratings)
async def got_ratings_gt2(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_gt2_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!\n\n"+
                                            "Теперь бот будет отвечать на отзывы с <b>оценками выше 2</b>!",
                                            parse_mode='HTML',
                                            reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)
    
    
# ======== GOT FILTER GT3 RATINGS
@router_rating.callback_query(UserStates.awaiting_rating, F.data == cb.select_gt3_ratings)
async def got_ratings_gt3(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_gt3_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!\n\n"+
                                            "Теперь бот будет отвечать на отзывы с <b>оценками выше 3</b>!",
                                            parse_mode='HTML',
                                            reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)
    

# ======== GOT FILTER GT4 RATINGS
@router_rating.callback_query(UserStates.awaiting_rating, F.data == cb.select_gt4_ratings)
async def got_ratings_gt4(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_gt4_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!\n\n"+
                                            "Теперь бот будет отвечать на отзывы с <b>оценками выше 4</b>!",
                                            parse_mode='HTML',
                                            reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)