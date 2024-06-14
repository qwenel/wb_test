import asyncio
from datetime import datetime, timedelta
import aiohttp
from loguru import logger

from app.database.exec_methods.answer_methods import delete_feedback


async def get_feedbacks(api_key: str) -> dict | None:

    headers = {"Authorization": api_key}
    url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"

    dateFrom = int((datetime.now() - timedelta(days=90)).timestamp())
    dateTo = int(datetime.now().timestamp())

    params = {
        "isAnswered": "false",
        "take": 100,
        "skip": 0,
        "order": "dateDesc",
        "dateFrom": dateFrom,
        "dateTo": dateTo,
    }

    async with aiohttp.ClientSession() as session:
        delay = 1
        for attempt in range(5):
            try:

                async with session.get(url, params=params, headers=headers) as resp:
                    response = await resp.json()

                    if resp.status == 200:
                        if response["data"]["countUnanswered"] == 0:
                            return None

                        logger.info("GET list query success:")
                        for i in range(response["data"]["countUnanswered"]):
                            logger.info(
                                f'\n\t id: {response["data"]["feedbacks"][i]["id"]}\n'
                                + f'\t rating: {response["data"]["feedbacks"][i]["productValuation"]}\n'
                                + f'\t shop: {response["data"]["feedbacks"][i]["productDetails"]["brandName"]}\n'
                                + f'\t product: {response["data"]["feedbacks"][i]["productDetails"]["productName"]}\n'
                                + f'\t text: {response["data"]["feedbacks"][i]["text"]}'
                            )
                        return response

                    elif resp.status == 503:
                        logger.warning(f"GET list: {response}\nattempt: {attempt}")
                        await asyncio.sleep(delay)
                        delay *= 2
                    else:
                        logger.error(f"GET list error: {response}")
                        return None

            except aiohttp.ClientError as e:
                logger.error(f"error sending request {e}")
                return None

        logger.error("couldn't get data after 5 attempts")
        return None


async def answer_feedback(fb_id: str, ans_text: str, api_key: str) -> bool:

    headers = {"Authorization": api_key}
    url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
    data = {"id": fb_id, "text": ans_text}

    async with aiohttp.ClientSession() as session:
        delay = 1
        for attempt in range(5):
            try:
                logger.info(
                    f"sending request: PATCH {url}\nbody: {data}\n headers: {headers}"
                )
                async with session.patch(url, json=data, headers=headers) as resp:
                    response = await resp.json()

                    if resp.status == 200:
                        logger.info(f"successfully send PATCH query: {response}")
                        return True
                    elif resp.status == 503:
                        logger.warning(
                            f"PATCH: couldn't answer feedback: {response}\nattempt: {attempt}"
                        )
                        await asyncio.sleep(delay)
                        delay *= 2
                    else:
                        logger.error(f"PATCH error: {response}")
                        return False

            except aiohttp.ClientError as e:
                logger.error(f"couldn't patch {e}")
                return False

        logger.error("couldn't patch in 5 attempts")
        return False


async def delete_if_answered_feedback(fb_id: str, api_key: str) -> bool:

    headers = {"Authorization": api_key}

    params = {"id": fb_id}

    url = "https://feedbacks-api.wildberries.ru/api/v1/feedback"

    delay = 1

    async with aiohttp.ClientSession() as session:

        for attempt in range(5):
            try:
                logger.info(
                    f"sending request GET id {url}\nparams: {params}\nheaders: {headers}"
                )
                async with session.get(url, params=params, headers=headers) as resp:
                    response = await resp.json()
                    if resp.status == 200:
                        logger.info(
                            "GET id query success: \n"
                            + f'\t id: {response["data"]["id"]}\n'
                            + f'\t rating: {response["data"]["productValuation"]}\n'
                            + f'\t shop: {response["data"]["productDetails"]["brandName"]}\n'
                            + f'\t product: {response["data"]["productDetails"]["productName"]}\n'
                            + f'\t text: {response["data"]["text"]}'
                            + f'\t date: {response["data"]["createdDate"]}'
                        )

                        if response["data"]["answer"] is not None:
                            await delete_feedback(fb_id)
                            return True
                        else:
                            return False
                    elif resp.status == 503:
                        logger.warning(
                            f"GET id: couldn't answer feedback: {response}\nattempt: {attempt}"
                        )
                        await asyncio.sleep(delay)
                        delay *= 2
                    else:
                        logger.error(f"GET id error: {response}")
                        return False
            except aiohttp.clientError as e:
                logger.error(f"couldn't get feedback by id: {fb_id}")
                return False

        logger.error("couldn't get id in 5 attempts")
        return False
