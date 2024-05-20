import aiohttp
import asyncio

from api.wb.wb_init import url, params


async def get_feedback(api_key: str) -> None:
    
    headers = {
        'Authorization': api_key
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            if resp.status != 200:
                print("ОШИБКА ПРИ ЗАПРОСЕ!!!", resp.status)
                return None
            
            res = await resp.json()
            
            if res['data']['countUnanswered'] == 0:
                print("У пользователя нет отзывов")
                return None
            
            return res
        
        
