from app.database.vars import path
from ..database.connection import create_connection

from .shop_methods import get_shop_id


async def set_api_key(telegram_id:int, shop_name:str, api_key:str, db=path) -> bool:
    if await get_shop_id(telegram_id, api_key=api_key, db=db):
        return False
     
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("UPDATE shops SET api_key=? WHERE fk_tg_id=? AND shop_name=?", (api_key, telegram_id, shop_name))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
        
    return True


async def set_rating(telegram_id:int, shop_name:str, rating:str, db=path) -> bool:
    if not await get_shop_id(telegram_id, shop_name=shop_name, db=db):
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("UPDATE shops SET rating=? WHERE fk_tg_id=? AND shop_name=?", (rating, telegram_id, shop_name))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
        
    return True


async def get_api_key(telegram_id:int, shop_name:str, db=path) -> str:
    if not await get_shop_id(telegram_id, shop_name=shop_name, db=db):
        return None
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT api_key FROM shops WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    got_api_key = await cursor.fetchone()   
        
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_api_key is None:
        return None    
    return got_api_key[0]


async def get_rating(telegram_id:int, shop_name='', api_key='', db=path) -> str:
    if not await get_shop_id(telegram_id, shop_name=shop_name, api_key=api_key, db=db):
        return None
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    if shop_name=='':
        await cursor.execute("SELECT rating FROM shops WHERE fk_tg_id=? AND api_key=?", (telegram_id, api_key))
    else:
        await cursor.execute("SELECT rating FROM shops WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    got_rating = await cursor.fetchone()
        
    await cursor.close()
    await conn.commit()
    await conn.close()
        
    if got_rating is None:
        return None    
        
    return got_rating[0]