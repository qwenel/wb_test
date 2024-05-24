from api.gpt.gpt_api import generate_answer
from app.database.shop_settings import get_rating
from app.database.user_methods import get_users_with_balance
from app.database.shop_methods import get_apis_list
from app.database.answer_methods import (
    delete_old_shown_feedback,
    fill_unanswered_feedback,
)
from api.wb.wb_feedbacks_ans import get_feedbacks


async def test_sched() -> None:
    print("Scheduler работает каждые 10 секунд")


async def scheduled_db_fill_job() -> bool:

    await delete_old_shown_feedback()

    users_with_balance = await get_users_with_balance()

    if users_with_balance is None:
        print("все пользователи без баланса")
        return None

    got_apis_for_user_id = {
        user_id: await get_apis_list(user_id) for user_id in users_with_balance
    }

    for user_id in users_with_balance:

        if got_apis_for_user_id[user_id] is None:
            print("по какой-то причине у пользователя нет магазинов")
            continue

        # Working with shop's api_key
        for api_key in got_apis_for_user_id[user_id]:

            got_rating_from_api = await get_rating(user_id, api_key=api_key)

            if got_rating_from_api == None:
                got_rating_from_api = "0"
                print("Не удалось вычислить рейтинг магазина: \n", api_key)

            got_feedback = await get_feedbacks(api_key)
            if got_feedback is None:
                continue

            # Working with loaded feedbacks from one API
            for i in range(got_feedback["data"]["countUnanswered"]):

                fb_id = got_feedback["data"]["feedbacks"][i]["id"]
                fb_rating = got_feedback["data"]["feedbacks"][i]["productValuation"]
                fb_shop_wb = got_feedback["data"]["feedbacks"][i]["productDetails"][
                    "brandName"
                ]
                fb_product_wb = got_feedback["data"]["feedbacks"][i]["productDetails"][
                    "productName"
                ]
                fb_text = got_feedback["data"]["feedbacks"][i]["text"]

                if not await fill_unanswered_feedback(
                    fb_id, fb_rating, fb_shop_wb, fb_product_wb, fb_text, api_key
                ):
                    print("пытаюсь пихнуть существующий в базе отзыв")
                    return False

                if got_rating_from_api != "0" or got_rating_from_api == "gt0":
                    await generate_answer(user_id, fb_id, fb_text, api_key, True)
                elif got_rating_from_api == "gt2" and fb_rating >= 2:
                    await generate_answer(user_id, fb_id, fb_text, api_key, True)
                elif got_rating_from_api == "gt3" and fb_rating >= 3:
                    await generate_answer(user_id, fb_id, fb_text, api_key, True)
                elif got_rating_from_api == "gt4" and fb_rating >= 4:
                    await generate_answer(user_id, fb_id, fb_text, api_key, True)

    return True
