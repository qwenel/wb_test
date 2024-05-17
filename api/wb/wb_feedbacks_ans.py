# import aiohttp
# import asyncio

# from api.wb.wb_init import url, params


# async def get_feedback(api_key: str) -> None | dict[dict][list][int][str]:
    
#     headers = {
#         'Authorization': api_key
#     }
    
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, params=params, headers=headers) as resp:
#             res = await resp.json()

#             print(res)


# asyncio.run(get_feedback())