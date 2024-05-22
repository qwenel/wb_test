import aiohttp

from api.wb.wb_init import url, params


async def get_feedbacks(api_key: str) -> dict | None:
    
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


async def answer_feedback(fb_id:str, ans_text:str, api_key:str) -> bool:
    
    headers = {
        'Authorization': api_key
    }
    
    data = {
        "id": fb_id,
        "text": ans_text 
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=data, headers=headers) as resp:
            if resp.status != 200:
                res = await resp.json()
                print("Ошибка при отправке PATCH запроса.", 
                      resp.status, "\n", res)                
                return False
            
            res = await resp.json()
            print("200 PATCH: ", res)
            
            return True
    