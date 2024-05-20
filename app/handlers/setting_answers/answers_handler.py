from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from api.wb.validChecks import is_valid_api_key
from app.database.shop_methods import delete_shop_if_null, toggle_auto_ans, toggle_manual_ans
from app.database.shop_settings import set_api_key
from app.keyboards.callbacks import callbacks as cb
from app.keyboards import inlineKeyboards as in_kb
from app.states.userStates import UserStates


router_answers = Router()


# ======= GET SHOP AUTO ANSWER STATUS
@router_answers.message(UserStates.awaiting_api_key)
async def got_api_key(message : Message, state: FSMContext):

    if not await is_valid_api_key(message.text):
        await message.answer(text="API-ключ введён некорректно!\n\n"+
                             "Попробуйте ещё раз: ",
                             reply_markup=in_kb.go_back_from_shop_name_keyboard)
        return
    
    data = await state.get_data()
    
    if not await set_api_key(message.chat.id, data["shop_name"], message.text):
        await delete_shop_if_null(message.from_user.id)
        await message.answer(text="Произошла внутренняя ошибка при вводе api_key\n\n"+
                             "Вероятная причина ошибки: API-ключи уже зарегестрирован\n"+
                             "Извините за предоставленные неудобства, повторите позднее...",
                             reply_markup=in_kb.go_to_main_menu_keyboard)
        await state.clear()
        await state.set_state(UserStates.menu)
        return
    
    await state.update_data(api_key=message.text)
    await state.set_state(UserStates.awaiting_auto_choose)
    
    await message.answer(text=f"Ура, Магазин \"{data["shop_name"]}\" успешно добавлен🎉\n\n"+
                        "Здесь вы можете выбрать, отвечать на отзывы автоматически или вручную.\n\n"+
                        "А именно\n\nБот сможет автоматически публиковать ответы на отзывы с выбранными вами фильтрами.\n\n"+
                        "Либо же, робот будет присылать вам сгенерированные им ответы на одобрение, а вы будете решать, публиковать ответ или нет.\n\n"+
                        "Отвечать на ваши отзывы автоматически? ⤵️",
                        reply_markup=in_kb.decide_auto_ans_keyboard)    
    

# ======= GOT AUTO FOR AUTO ANSWERS
@router_answers.callback_query(UserStates.awaiting_auto_choose, F.data==cb.yes_auto)    
async def yes_auto_answer(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.awaiting_rating)
    
    data = await state.get_data()
    
    await callback_query.answer()
    
    if not await toggle_auto_ans(callback_query.from_user.id, data["shop_name"]):
        callback_query.message.answer(text="Произошла непредвиденная ошибка.",
                                      reply_markup=in_kb.go_to_main_menu_keyboard)
        await state.set_state(UserStates.menu)
        await state.clear()
    
    await callback_query.message.edit_text(text="Отлично! Настройка сохранена.\n\n"+
                                           "Здесь же вы можете гибко настроить, как бот будет отвечать на ваши отзывы, в зависимости от их оценки.\n\n"+
                                            "Например\n\nВы можете выбрать, чтобы на все отзывы с оценкой 5 и 4 звезды бот отвечал в полностью автоматическом режиме.\n\n"+
                                            "На все остальные отзывы [с оценками 3, 2, 1 звезда] бот будет создавать ответ, но будет присылать вам на согласование.\n\n"+
                                            "В каком формате отвечать на ваши отзывы? ⤵️",
                                            reply_markup=in_kb.setting_ratings_keyboard)
    
# ------- UNIVERSAL FOR BOTH SETTING AND ADDING NEW SHOP
# ======= GOT MANUAL FOR AUTO ANSWERS
@router_answers.callback_query(F.data==cb.no_auto)    
async def no_auto_answer(callback_query: CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    await state.set_state(UserStates.menu)
    await state.clear()
    await callback_query.answer()
    
    if not await toggle_manual_ans(callback_query.from_user.id, data["shop_name"]):
        callback_query.message.answer(text="Произошла непредвиденная ошибка.",
                                      reply_markup=await in_kb.go_back_from_settings_errors_kb(data["shop_name"]))
    
    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!\n\n"+
                                           "Я буду отвечать на отзывы в РУЧНОМ режиме",
                                        reply_markup=in_kb.go_to_main_menu_keyboard)
    
    
    
# ======= GET SETTING AUTO STATUS
@router_answers.callback_query(UserStates.chosen_shop, F.data==cb.setting_auto)
async def set_new_auto(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.toggle_auto)

    data = await state.get_data()
    
    await callback_query.message.edit_text(text=f"Здесь для магазина \"{data["shop_name"]}\" вы можете выбрать, отвечать на отзывы автоматически или вручную.\n\n"+
                        "А именно\n\nБот сможет автоматически публиковать ответы на отзывы с выбранными вами фильтрами.\n\n"+
                        "Либо же, робот будет присылать вам сгенерированные им ответы на одобрение, а вы будете решать, публиковать ответ или нет.\n\n"+
                        "В каком формате отвечать на ваши отзывы? ⤵️",
                        reply_markup=in_kb.decide_auto_ans_keyboard)
    
    await callback_query.answer()
    

# ======= GOT AUTO FOR AUTO ANSWERS
@router_answers.callback_query(UserStates.toggle_auto, F.data==cb.yes_auto)    
async def toggle_to_auto(callback_query: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    
    await callback_query.answer()
    await state.set_state(UserStates.menu)
    await state.clear()
    
    if not await toggle_auto_ans(callback_query.from_user.id, data["shop_name"]):
        await callback_query.message.answer(text="Произошла непредвиденная ошибка.",
                                      reply_markup=await in_kb.go_back_from_settings_errors_kb(data["shop_name"]))        
    
    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!\n\n"+
                                           "Я будет отвечать на отзывы в АВТОМАТИЧЕСКОМ режиме",
                                        reply_markup=in_kb.go_to_main_menu_keyboard)