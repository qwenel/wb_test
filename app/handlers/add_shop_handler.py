from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from ..states.userStates import UserStates

import app.keyboards.inlineKeyboards as in_kb
import app.keyboards.callbacks.callbacks as cb

from ..database.shop_methods import (
    add_shop, delete_shop_if_null, delete_shop,
    toggle_auto_ans, get_status_auto_ans
)

from ..database.shop_settings import (
    set_api_key, set_rating
)
from .validChecks import is_valid_api_key


router_shop = Router()

# ======= GET SHOP NAME
@router_shop.callback_query(F.data == cb.add_shop)
async def ask_shop_name(callback_query: CallbackQuery, state: FSMContext): 
    await delete_shop_if_null(callback_query.from_user.id)
    
    await state.set_state(UserStates.awaiting_shop_name)
    
    await callback_query.message.edit_text(text="Введите название магазина",
                                           reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()
    

# ======= GET SHOP API KEY
@router_shop.message(UserStates.awaiting_shop_name)
async def got_shop_name(message : Message, state: FSMContext):
    await delete_shop_if_null(message.from_user.id)
    
    if not await add_shop(message.chat.id, message.text):
        await message.answer(text="Название магазина некорректно!\n"+
                       "\nПроверьте, пожалуйста, соблюдение следующих критериев:\n"+
                       "\t - Длина названия магазина должна быть не более 32 символов\n"+
                       "\t - Название вашего магазина не должно повторяться среди ваших других\n"+
                       "\n\nВведите новое название магазина:",
                       reply_markup=in_kb.go_to_main_menu_keyboard)
        return
    
    await state.update_data(shop_name=message.text)
    
    await state.set_state(UserStates.awaiting_api_key)
    
    photo = FSInputFile("res/images/get_api.jpg")
    
    await message.answer_photo(photo=photo,
                               caption=f"☝️Чтобы добавить актуальный токен в магазин \"{message.text}\", необходимо сделать несколько шагов:\n\n"+
                               "1. Зайдите на страницу Доступ к API - https://seller.wildberries.ru/supplier-settings/access-to-api"+
                               "\n\n2. Выберите Тип токена - «Вопросы и отзывы»\n\n"+
                               "3. НЕ ставьте галочку в опции «Только для чтения». Проверьте ее отсутствие\n\n"+
                               "4. Нажмите «Создать»\n\nПосле этого введите созданный токен в поле ниже ⬇️\n\n"+
                               "Все текущие настройки магазина сохранятся👌",
                               reply_markup=in_kb.go_back_from_api_keyboard)
    

# ======= GET SHOP AUTO ANSWER STATUS
@router_shop.message(UserStates.awaiting_api_key)
async def got_api_key(message : Message, state: FSMContext):

    if not await is_valid_api_key(message.text):
        await message.answer(text="API-ключ введён некорректно!\n\n"+
                             "Попробуйте ещё раз: ",
                             reply_markup=in_kb.go_back_from_api_keyboard)
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
    

# ======= GOT YES FOR AUTO ANSWERS
@router_shop.callback_query(UserStates.awaiting_auto_choose, F.data==cb.yes_auto)    
async def yes_auto_answer(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.awaiting_rating)
    
    data = await state.get_data()
    
    if not await toggle_auto_ans(callback_query.from_user.id, data["shop_name"]):
        callback_query.message.answer(text="Произошла непредвиденная ошибка.",
                                      reply_markup=in_kb.go_back_from_api_keyboard)
    
    await callback_query.message.edit_text(text="Отлично! Настройка сохранена.\n\n"+
                                           "Здесь же вы можете гибко настроить, как бот будет отвечать на ваши отзывы, в зависимости от их оценки.\n\n"+
                                            "Например\n\nВы можете выбрать, чтобы на все отзывы с оценкой 5 и 4 звезды бот отвечал в полностью автоматическом режиме.\n\n"+
                                            "На все остальные отзывы [с оценками 3, 2, 1 звезда] бот будет создавать ответ, но будет присылать вам на согласование.\n\n"+
                                            "Выберите на какие отзывы отвечать автоматически? ⤵️",
                                            reply_markup=in_kb.setting_ratings_keyboard)
    
    await callback_query.answer()    
    

# ======= GOT NO FOR AUTO ANSWERS
@router_shop.callback_query(UserStates.awaiting_auto_choose, F.data==cb.no_auto)    
async def no_auto_answer(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.awaiting_rating)
    
    await callback_query.message.edit_text(text="Отлично! Настройка сохранена.\n\n"+
                                           "Здесь же вы можете гибко настроить, как бот будет отвечать на ваши отзывы, в зависимости от их оценки.\n\n"+
                                            "Например\n\nВы можете выбрать, чтобы на все отзывы с оценкой 5 и 4 звезды бот отвечал в полностью автоматическом режиме.\n\n"+
                                            "На все остальные отзывы [с оценками 3, 2, 1 звезда] бот будет создавать ответ, но будет присылать вам на согласование.\n\n"+
                                            "Выберите на какие отзывы отвечать автоматически? ⤵️",
                                            reply_markup=in_kb.setting_ratings_keyboard)
    
    await callback_query.answer()       
    
    
# ======= CHOSEN SHOP MENU (SETTINGS : AUTO, FILTER, DELETE)    
@router_shop.callback_query(UserStates.shop_list, F.data[:5] == "shop_")    
async def shop_chosen(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.chosen_shop)
    
    _shop_name = callback_query.data[5:]
    
    await state.update_data(shop_name=_shop_name)
    
    await callback_query.message.edit_text(text=f"Выбран магазин => \"{_shop_name}\"",
                        reply_markup=in_kb.chosen_shop_menu_keyboard)
    
    await callback_query.answer()
    

# ======== GOT FILTER ALL RATINGS
@router_shop.callback_query(F.data == cb.select_all_ratings)
async def got_ratings_all(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_all_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!",
                                        reply_markup=in_kb.starting_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)
    

# ======== GOT FILTER GT2 RATINGS
@router_shop.callback_query(F.data == cb.select_gt2_ratings)
async def got_ratings_gt2(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_gt2_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!",
                                        reply_markup=in_kb.starting_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)
    
    
# ======== GOT FILTER GT3 RATINGS
@router_shop.callback_query(F.data == cb.select_gt3_ratings)
async def got_ratings_gt3(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_gt3_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!",
                                        reply_markup=in_kb.starting_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)
    

# ======== GOT FILTER GT4 RATINGS
@router_shop.callback_query(F.data == cb.select_gt4_ratings)
async def got_ratings_gt4(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    await set_rating(callback_query.from_user.id, data["shop_name"], cb.select_gt4_ratings)

    await callback_query.message.edit_text(text="Принято, Босс)\n\nПошел работать!",
                                        reply_markup=in_kb.starting_keyboard)
    await callback_query.answer()
    
    await state.clear()
    await state.set_state(UserStates.menu)
    

# ======== SETTING TOGGLING AUTO ANSWER
@router_shop.callback_query(UserStates.chosen_shop, F.data==cb.toggle_auto)
async def toggle_auto_answer(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    shop_to_toggle_auto = data["shop_name"]
    
    if not await toggle_auto_ans(callback_query.from_user.id, shop_to_toggle_auto):
        await callback_query.message.answer(text="По какой-то причине изменение невозможно\n\n"+
                                      "Извините за предоставленные неудобства, разбираемся...",
                                      reply_markup=in_kb.go_back_from_toggle_keyboard)
    
    await state.clear()
    await state.set_state(UserStates.menu)
    
    status_auto_ans = await get_status_auto_ans(callback_query.from_user.id, shop_to_toggle_auto)
    
    if status_auto_ans is True:
        status_auto_ans = "автоматически"
    else:
        status_auto_ans = "в ручном режиме"
    
    await callback_query.message.edit_text(text=f"Вы успешно изменили режим ответов бота на отзывы с магазина \"{shop_to_toggle_auto}\"!\n\n"+
                                           f"Теперь бот будет обрабатывать отзывы {status_auto_ans}",
                                           reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()
    
    
# ======== SETTING DELETING
@router_shop.callback_query(UserStates.chosen_shop, F.data==cb.delete_shop)
async def del_shop(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    shop_to_delete = data["shop_name"]
    
    if not await delete_shop(callback_query.from_user.id, shop_to_delete):
        await callback_query.message.answer(text="По какой-то причине удаление невозможно\n\n"+
                                      "Извините за предоставленные неудобства, разбираемся...",
                                      reply_markup=in_kb.go_back_from_delete_keyboard)
    
    await state.clear()
    await state.set_state(UserStates.menu)
    
    await callback_query.message.edit_text(text=f"Вы удалили магазин \"{shop_to_delete}\".",
                                           reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()