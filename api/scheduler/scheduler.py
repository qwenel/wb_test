import asyncio
from loguru import logger

from api.gpt.gpt_api import generate_answer
from app.database.shop_settings import get_rating
from app.database.user_methods import get_users, get_users_with_balance
from app.database.shop_methods import get_apis_list
from app.database.answer_methods import (
    delete_old_shown_feedback,
    fill_unanswered_feedback,
    get_unanswered_fb_list,
)
from api.wb.wb_feedbacks_ans import delete_if_answered_feedback, get_feedbacks


db_fill_job_lock = asyncio.Lock()
process_unanswered_job_lock = asyncio.Lock()
clear_old_shown_feedbacks_job_lock = asyncio.Lock()


async def clear_old_shown_feedbacks_job():
    async with clear_old_shown_feedbacks_job_lock:
        await delete_old_shown_feedback()


# Working with unanswered feedbacks in DB
async def process_unanswered_job():

    async with process_unanswered_job_lock:
        list_of_user_ids = await get_users()

        for user_id in list_of_user_ids:
            unanswered_feedbacks = await get_unanswered_fb_list(user_id)

            if unanswered_feedbacks != False:
                for unanswered_feedback in unanswered_feedbacks:

                    await delete_if_answered_feedback(
                        unanswered_feedback[4], unanswered_feedback[5]
                    )

                    rating_filter = await get_rating(
                        user_id, api_key=unanswered_feedback[5]
                    )

                    await auto_answer(
                        user_id,
                        unanswered_feedback[4],
                        unanswered_feedback[0],
                        unanswered_feedback[3],
                        unanswered_feedback[5],
                        rating_filter,
                    )


async def db_fill_job():

    async with db_fill_job_lock:

        users_with_balance = await get_users_with_balance()

        if users_with_balance is None:
            logger.error("all user have empty balance")
            return

        got_apis_for_user_id = {
            user_id: await get_apis_list(user_id) for user_id in users_with_balance
        }

        for user_id in users_with_balance:

            if got_apis_for_user_id[user_id] is None:
                logger.info(f"user {user_id} don't have any API-keys...")
                continue

            # Working with shop's api_key
            for api_key in got_apis_for_user_id[user_id]:

                got_rating_from_api = await get_rating(user_id, api_key=api_key)

                if got_rating_from_api == None:
                    got_rating_from_api = "0"
                    logger.error(
                        f"couldn't get Rating from user {user_id} with API: {api_key}"
                    )

                await asyncio.sleep(0.7)
                got_feedback = await get_feedbacks(api_key)

                if got_feedback is None:
                    continue

                # Working with loaded feedbacks from one API
                for i in range(got_feedback["data"]["countUnanswered"]):
                    await fill_unanswered_feedback(
                        got_feedback["data"]["feedbacks"][i]["id"],
                        got_feedback["data"]["feedbacks"][i]["productValuation"],
                        got_feedback["data"]["feedbacks"][i]["productDetails"][
                            "brandName"
                        ],
                        got_feedback["data"]["feedbacks"][i]["productDetails"][
                            "productName"
                        ],
                        got_feedback["data"]["feedbacks"][i]["text"],
                        api_key,
                    )


async def auto_answer(
    tg_id: str,
    fb_id: str,
    fb_rating: int,
    fb_text: str,
    api_key: str,
    rating_filter: str,
):

    if rating_filter == "gt0":
        await generate_answer(tg_id, fb_id, fb_text, api_key, True)
    elif rating_filter == "gt2" and fb_rating >= 2:
        await generate_answer(tg_id, fb_id, fb_text, api_key, True)
    elif rating_filter == "gt3" and fb_rating >= 3:
        await generate_answer(tg_id, fb_id, fb_text, api_key, True)
    elif rating_filter == "gt4" and fb_rating >= 4:
        await generate_answer(tg_id, fb_id, fb_text, api_key, True)
