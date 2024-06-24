from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
from aiogram.fsm.context import FSMContext

from api.gpt.gpt_api import generate_answer
from api.wb.wb_feedbacks_ans import answer_feedback
from app.database.exec_methods.user_methods import (
    publish_cancelling,
    undo_user_props_after_generating,
)
from app.keyboards.inlineKeyboards import (
    publish,
    unanswered_last,
    go_to_main_menu_keyboard,
)
import app.keyboards.callbacks.callbacks as cb
from ...states.userStates import UserStates
from loguru import logger
from app.database.exec_methods.answer_methods import (
    get_answer_by_feedback_id,
    get_api_key_by_feedback_id,
    get_feedback_to_generate_answer,
    get_unanswered_fb_list,
    get_feedback,
    update_answer_text,
)


router_unanswered = Router()


@router_unanswered.callback_query(F.data == cb.unanswered)
async def show_unanswered(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.unanswered)

    await callback_query.answer()

    unanswered_feedbacks = await get_unanswered_fb_list(callback_query.from_user.id)

    if not unanswered_feedbacks:
        await callback_query.message.edit_text(
            text="увы нет новых или неотвеченных отзывов",
            reply_markup=go_to_main_menu_keyboard,
        )

        await state.set_state(UserStates.menu)
        await state.clear()
        return

    feedbacks_to_show = 5
    less_than_five = False

    if len(unanswered_feedbacks) <= feedbacks_to_show:
        feedbacks_to_show = len(unanswered_feedbacks)
        less_than_five = True

    await callback_query.message.answer(
        text="⬇️Ниже вы видите список отзывов, которые ждут ответов!⬇️"
    )

    for i in range(feedbacks_to_show):

        if i != feedbacks_to_show - 1:
            await callback_query.message.answer(
                text="ОТЗЫВ\n\n"
                + f"Оценка: {unanswered_feedbacks[i][0]}\n"
                + f"Магазин: {unanswered_feedbacks[i][1]}\n"
                + f"Товар: {unanswered_feedbacks[i][2]}\n"
                + f"Текст:\n{unanswered_feedbacks[i][3]}",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Сгенерировать 🤖",
                                callback_data=cb.generate + unanswered_feedbacks[i][4],
                            )
                        ]
                    ]
                ),
            )
            continue

        await callback_query.message.answer(
            text="ОТЗЫВ\n\n"
            + f"Оценка: {unanswered_feedbacks[i][0]}\n"
            + f"Магазин: {unanswered_feedbacks[i][1]}\n"
            + f"Товар: {unanswered_feedbacks[i][2]}\n"
            + f"Текст:\n{unanswered_feedbacks[i][3]}",
            reply_markup=await unanswered_last(
                unanswered_feedbacks[i][4], less_than_five
            ),
        )

    not_shown_fbs = []
    if not less_than_five:
        not_shown_fbs = unanswered_feedbacks[5:]
        await state.update_data(last_to_show=not_shown_fbs)


@router_unanswered.callback_query(UserStates.unanswered, F.data == cb.show_more)
async def show_more(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    data = await state.get_data()

    unanswered_feedbacks = data["last_to_show"]

    feedbacks_to_show = 5
    less_than_five = False

    if len(unanswered_feedbacks) < feedbacks_to_show:
        feedbacks_to_show = len(unanswered_feedbacks)
        less_than_five = True

    await callback_query.message.answer(text="Список последних отвеченных отзывов:")
    for i in range(feedbacks_to_show):

        if i != feedbacks_to_show - 1:
            await callback_query.message.answer(
                text="ОТЗЫВ\n\n"
                + f"Оценка: {unanswered_feedbacks[i][0]}\n"
                + f"Магазин: {unanswered_feedbacks[i][1]}\n"
                + f"Товар: {unanswered_feedbacks[i][2]}\n"
                + f"Текст:\n{unanswered_feedbacks[i][3]}",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Сгенерировать 🤖",
                                callback_data=cb.generate + unanswered_feedbacks[i][4],
                            )
                        ]
                    ]
                ),
            )
            continue

        await callback_query.message.answer(
            text="ОТЗЫВ\n\n"
            + f"Оценка: {unanswered_feedbacks[i][0]}\n"
            + f"Магазин: {unanswered_feedbacks[i][1]}\n"
            + f"Товар: {unanswered_feedbacks[i][2]}\n"
            + f"Текст:\n{unanswered_feedbacks[i][3]}",
            reply_markup=await unanswered_last(
                unanswered_feedbacks[i][4], less_than_five
            ),
        )

    not_shown_fbs = []
    if not less_than_five:
        not_shown_fbs = unanswered_feedbacks[5:]
        await state.update_data(last_to_show=not_shown_fbs)
        return

    await state.clear()
    await state.set_state(UserStates.unanswered)


@router_unanswered.callback_query(UserStates.unanswered, F.data[:4] == cb.generate)
async def generate(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await state.update_data(fb_id=callback_query.data[4:])

    got_feedback = await get_feedback_to_generate_answer(callback_query.data[4:])

    if got_feedback == False:
        logger.error("Не нашел отзыв перед генерацией")
        return

    answer = await generate_answer(
        callback_query.from_user.id,
        callback_query.data[4:],
        got_feedback[0],
        got_feedback[1],
        got_feedback[2],
        False,
    )

    if answer == False:
        logger.error("Непредвиденная ошибка при генерации ответа на отзыв...")
        return

    await update_answer_text(callback_query.data[4:], answer)

    await callback_query.message.edit_text(
        text=callback_query.message.text + f"\n\nОтвет:\n<code>{answer}</code>",
        parse_mode="HTML",
        reply_markup=await publish(callback_query.data[4:]),
    )


@router_unanswered.callback_query(
    UserStates.unanswered, F.data[:4] == cb.edit_generated
)
async def edit_generated(callback_query: CallbackQuery, state: FSMContext):

    await state.update_data(fb_id=callback_query.data[4:])

    await update_answer_text(callback_query.data[4:], "null")

    await callback_query.answer()

    await callback_query.message.answer(
        text="Для редактирования полученного отзыва:\n\n"
        + "\t • Нажмите в поле ответа для его копирования.\n"
        + "\t • Вставьте скопированный текст в поле для ввода\n"
        + "\t • Отредактируйте отзыв и отправьте его мне!"
    )


@router_unanswered.message(UserStates.unanswered)
async def check_edited(message: Message, state: FSMContext):

    await state.update_data(answer=message.text)

    data = await state.get_data()

    feedback = await get_feedback(data["fb_id"])

    await update_answer_text(data["fb_id"], message.text)

    await message.answer(
        text="ОТЗЫВ\n\n"
        + f"Оценка: {feedback[0]}\n"
        + f"Магазин: {feedback[1]}\n"
        + f"Товар: {feedback[2]}\n"
        + f"Текст:\n{feedback[3]}"
        + f"\n\nОтвет:\n<code>{message.text}</code>",
        parse_mode="HTML",
        reply_markup=await publish(data["fb_id"]),
    )


@router_unanswered.callback_query(UserStates.unanswered, F.data[:7] == cb.publish)
async def publishing(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.answer(
        text="Отлично, работаю над публикацией. . .\n\n"
        + "Спасибо за использование наших инструментов!",
        reply_markup=go_to_main_menu_keyboard,
    )

    feedback_id = callback_query.data[7:]
    answer = await get_answer_by_feedback_id(feedback_id)
    api_key = await get_api_key_by_feedback_id(feedback_id)

    if not await answer_feedback(feedback_id, answer, api_key):
        await undo_user_props_after_generating(callback_query.from_user.id)
        await update_answer_text(feedback_id, "null")
        await callback_query.message.answer(
            text="Ошибка при публикации. . .\n\n" + "Отзыв не опубликован!",
            reply_markup=go_to_main_menu_keyboard,
        )


@router_unanswered.callback_query(UserStates.unanswered, F.data[:10] == cb.undo)
async def no_publish(callback_query: CallbackQuery):
    await callback_query.answer()

    await callback_query.message.answer(
        text="Отменяю публикацию. . .",
        reply_markup=go_to_main_menu_keyboard,
    )

    feedback_id = callback_query.data[10:]

    await publish_cancelling(callback_query.from_user.id)

    await update_answer_text(feedback_id, "null")
