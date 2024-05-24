from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from api.wb.validChecks import is_valid_api_key
from app.database.shop_settings import set_api_key

from ..states.userStates import UserStates

import app.keyboards.inlineKeyboards as in_kb
import app.keyboards.callbacks.callbacks as cb

from ..database.shop_methods import (
    add_shop, delete_shop_if_null, delete_shop
)

from .setting_rating.rating_handler import router_rating
from .setting_answers.answers_handler import router_answers


router_shop = Router()
router_shop.include_routers(
    router_rating,
    router_answers
)


# ======= GET SHOP NAME
@router_shop.callback_query(F.data == cb.add_shop)
async def ask_shop_name(callback_query: CallbackQuery, state: FSMContext): 
    await delete_shop_if_null(callback_query.from_user.id)
    
    await state.set_state(UserStates.awaiting_shop_name)
    
    if callback_query.message.photo:
        await callback_query.message.delete()
        await callback_query.message.answer(text="Введите название магазина",
                                           reply_markup=in_kb.go_to_main_menu_keyboard)
    else:
        await callback_query.message.edit_text(text="Введите название магазина",
                                           reply_markup=in_kb.go_to_main_menu_keyboard)
    await callback_query.answer()
    

# ======= GET SHOP API KEY
@router_shop.message(UserStates.awaiting_shop_name)
async def got_shop_name(message : Message, state: FSMContext):
    await delete_shop_if_null(message.from_user.id)
    
    if not await add_shop(telegram_id=message.chat.id, shop_name=message.text):
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
                               reply_markup=in_kb.go_back_from_shop_name_keyboard)
       
       
@router_shop.message(UserStates.awaiting_api_key)      
async def setting_api_key(message: Message, state: FSMContext):
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

    
# ======= CHOSEN SHOP MENU (SETTINGS : AUTO, FILTER, DELETE)    
@router_shop.callback_query(UserStates.shop_list, F.data[:5] == cb.settings)    
async def shop_chosen(callback_query: CallbackQuery, state: FSMContext):
    
    await state.clear()
    await state.set_state(UserStates.chosen_shop)
    
    _shop_name = callback_query.data[5:]
    
    await state.update_data(shop_name=_shop_name)
    
    await callback_query.message.edit_text(text=f"Выбран магазин => \"{_shop_name}\"",
                        reply_markup=in_kb.chosen_shop_menu_keyboard)
    
    await callback_query.answer()
    
    
# ======== SETTING AUTO
@router_shop.callback_query(UserStates.chosen_shop, F.data==cb.setting_auto)    
async def setting_auto(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.awaiting_auto_choose)
    
    await callback_query.answer()
    
    await callback_query.message.edit_text(text="Здесь вы можете выбрать, отвечать на отзывы автоматически или вручную.\n\n"+
                        "А именно\n\nБот сможет автоматически публиковать ответы на отзывы с выбранными вами фильтрами.\n\n"+
                        "Либо же, робот будет присылать вам сгенерированные им ответы на одобрение, а вы будете решать, публиковать ответ или нет.\n\n"+
                        "Отвечать на ваши отзывы автоматически? ⤵️",
                        reply_markup=in_kb.decide_auto_ans_keyboard)
    
    
# ======== SETTING DELETING
@router_shop.callback_query(UserStates.chosen_shop, F.data==cb.setting_delete)
async def setting_delete(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    shop_to_delete = data["shop_name"]
    
    if not await delete_shop(callback_query.from_user.id, shop_name=shop_to_delete):
        await state.set_state(UserStates.shop_list)
        await callback_query.message.answer(text="По какой-то причине удаление невозможно\n\n"+
                                      "Извините за предоставленные неудобства, разбираемся...",
                                      reply_markup=await in_kb.go_back_from_settings_errors_kb(shop_to_delete))
    
    await state.clear()
    await state.set_state(UserStates.menu)
    await callback_query.answer()
    
    await callback_query.message.edit_text(text=f"Вы удалили магазин \"{shop_to_delete}\".",
                                           reply_markup=in_kb.go_to_main_menu_keyboard)
    
