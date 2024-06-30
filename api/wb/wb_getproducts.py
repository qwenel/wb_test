import asyncio
import aiohttp
from loguru import logger


async def get_product_list(api_key: str):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    headers = {"Authorization": api_key}
    params = {"limit": "1000"}
    
    async with aiohttp.ClientSession() as session:
        delay = 1
        for attempt in range(5):
            try:
                async with session.get(url, params=params, headers=headers) as resp:
                    response = await resp.json()
                    
                    if response["error"]:
                        logger.error(response["errorText"])
                        asyncio.sleep(delay)
                        delay *= 2
                    else:
                        logger.info("got list of products")
                        return response
                    
            except aiohttp.ClientError as e:
                logger.error(f"error sending request {e}")
                return None

        logger.error("couldn't get products after 5 attempts")
        return None


async def inc_discount_on_products(products, api_key: str):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/upload/task"
    headers = {"Authorization": api_key}
    data = {"data": products}
    
    async with aiohttp.ClientSession() as session:
        delay = 1
        for attempt in range(5):
            try:
                async with session.post(url, json=data, headers=headers) as resp:
                    response = await resp.json()
                    #TODO: finish post request

            except aiohttp.ClientError as e:
                logger.error(f"error sending request {e}")
                return None

        logger.error("couldn't get data after 5 attempts")
        return None
    
if __name__ == "__main__":
    asyncio.run(get_product_list("eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyODY5OTY3NiwiaWQiOiIyOTQ4OGU1NC1mMTdmLTRiYjUtOTcwNi0xMzQ5ZmUwZTc1ZWMiLCJpaWQiOjEwOTU3MTQzMSwib2lkIjoxMjMxMzE0LCJzIjozODQsInNpZCI6Ijc2NjZjYTM4LTVkMWQtNDVlNS04YzNjLTg4NzFlZjdmZGUyYyIsInQiOmZhbHNlLCJ1aWQiOjEwOTU3MTQzMX0.HzNSNmTnnRVlAmIY7I_LPyFRTqX5xgAu6SQBN2JPxQLVnebumo6h88lrU30nhMSCsXUb35pqHhbJx6woEKl1sw"))