import asyncio
import aiohttp
from loguru import logger

from api.wb.wb_init import url, params
from app.database.answer_methods import delete_feedback


async def get_feedbacks(api_key: str) -> dict | None:

    headers = {"Authorization": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            response = await resp.json()

            if resp.status != 200:
                logger.error(f"GET list error: {response}")
                return None

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


async def answer_feedback(fb_id: str, ans_text: str, api_key: str) -> bool:

    headers = {"Authorization": api_key}

    data = {"id": fb_id, "text": ans_text}

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=data, headers=headers) as resp:
            response = await resp.json()

            if resp.status != 200:
                logger.error(f"PATCH error: couldn't answer feedback: {response}")
                return False

            logger.info(f"successfully send PATCH query: {response}")
            return True


async def delete_if_answered_feedback(fb_id: str, api_key: str) -> bool:

    headers = {"Authorization": api_key}

    params = {"id": fb_id}

    url = "https://feedbacks-api.wildberries.ru/api/v1/feedback"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            response = await resp.json()

            if resp.status != 200:
                logger.error(f"GET id error: {response}")
                return False

            if response["data"]["answer"] is not None:
                await delete_feedback(fb_id)
                logger.info(
                    "GET id query success: \n"
                    + f'\t id: {response["data"]["id"]}\n'
                    + f'\t rating: {response["data"]["productValuation"]}\n'
                    + f'\t shop: {response["data"]["productDetails"]["brandName"]}\n'
                    + f'\t product: {response["data"]["productDetails"]["productName"]}\n'
                    + f'\t text: {response["data"]["text"]}'
                    + f'\t date: {response["data"]["createdDate"]}'
                )
                return True
