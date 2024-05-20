import aiohttp
import asyncio

from api.wb.wb_init import url, params


async def get_feedback(api_key: str) -> None:
    
    headers = {
        'Authorization': api_key
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            res = await resp.json()
            
            print("Это должно вылезать каждые 10 секунд!\n", res, "\n\n")
            
    return None