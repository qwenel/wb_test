from app.database.vars import path
from ..database.connection import create_connection


async def add_shop(telegram_id : int, shop_name : str, db=path) -> bool:
    if len(shop_name) > 32:
        return False
    
    if await get_shop_id(telegram_id, shop_name=shop_name, db=db):
        return False
        
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("INSERT INTO shops (shop_name, fk_tg_id) VALUES (?, ?)", (shop_name, telegram_id))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True
    

async def get_shop_id(telegram_id:int, api_key="", shop_name="", db=path) -> int | bool:
    conn = await create_connection(db)
    cursor = await conn.cursor()

    if shop_name == "":
        await cursor.execute("SELECT id FROM shops WHERE fk_tg_id=? AND api_key=?", (telegram_id, api_key))
    else:
        await cursor.execute("SELECT id FROM shops WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
        
    found_id = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if found_id is None:
        return False
    
    return found_id
    
    
async def delete_shop(telegram_id:int, api_key="", shop_name="", db=path) -> bool:
    if await get_shop_id(telegram_id, shop_name=shop_name, db=db) == False:
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    if shop_name == "":
        await cursor.execute("DELETE FROM shops WHERE api_key=? AND fk_tg_id=?", (api_key, telegram_id))
    else:
        await cursor.execute("DELETE FROM shops WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True


async def delete_all_shops(telegram_id : int, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("DELETE FROM shops WHERE fk_tg_id=?", (telegram_id, ))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    
async def delete_shop_if_null(telegram_id:int, db=path): 
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("DELETE FROM shops WHERE fk_tg_id=? AND api_key IS NULL", (telegram_id, ))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    
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
        
    return got_api_key[0]
    
    
async def get_shops_list(telegram_id: int, db=path) -> list:
  
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT shop_name FROM shops WHERE fk_tg_id=?", (telegram_id, ))
    
    list_of_shops = await cursor.fetchall()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if list_of_shops is None:
        return None
    
    formatted_list = [shop_cortage[0] for shop_cortage in list_of_shops]
    
    return formatted_list


async def get_apis_list(telegram_id: int, db=path) -> list[:str] | None:
  
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT api_key FROM shops WHERE fk_tg_id=?", (telegram_id, ))
    
    list_of_apis = await cursor.fetchall()
    
    print(list_of_apis)
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if len(list_of_apis) == 0:
        return None
    
    formatted_list = [api_cortage[0] for api_cortage in list_of_apis]
    
    return formatted_list


async def toggle_auto_ans(telegram_id:int, shop_name:str, db=path) -> bool:
    if not await get_shop_id(telegram_id, shop_name=shop_name, db=db):
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("UPDATE shops SET auto_ans=1 WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True


async def toggle_manual_ans(telegram_id:int, shop_name:str, db=path) -> bool:
    if not await get_shop_id(telegram_id, shop_name=shop_name, db=db):
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("UPDATE shops SET auto_ans=0 WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True


async def get_status_auto_ans(telegram_id:int, shop_name:str, db=path) -> bool:
    if not await get_shop_id(telegram_id, shop_name=shop_name, db=db):
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT auto_ans FROM shops WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    got_status = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_status is None:
        return False
    
    return got_status[0] * True