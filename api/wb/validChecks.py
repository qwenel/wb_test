import aiohttp
from datetime import datetime, timedelta

async def is_valid_api_key(api_key: str) -> bool:
    
    dateFrom = int((datetime.now() - timedelta(days=90)).timestamp())
    dateTo = int(datetime.now().timestamp())
    
    url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'
    params = {
        'isAnswered': "false",
        'take': 1,
        'skip': 0,
        'order': 'dateDesc',
        'dateFrom': dateFrom,
        'dateTo': dateTo
    }
    headers = {
        'Authorization': api_key
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers, params=params)
    
    if response.status == 200: 
        return True
    else: 
        return False