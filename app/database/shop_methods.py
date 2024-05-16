from app.database.vars import path
from ..database.connection import create_connection


async def add_shop(telegram_id : int, shop_name : str, db=path) -> bool:
    if len(shop_name) > 32:
        return False
    
    if await get_shop_id(telegram_id, shop_name, db) is not None:
        return False
        
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("INSERT INTO shops (shop_name, fk_tg_id) VALUES (?, ?)", (shop_name, telegram_id))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True
    
    
async def get_shop_name(telegram_id:int, db=path) -> str:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT shop_name FROM shops WHERE fk_tg_id=? AND api_key IS NULL", (telegram_id, ))
    found_name = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return found_name[0]


async def get_shop_name_rating(telegram_id:int, db=path) -> str:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT shop_name FROM shops WHERE fk_tg_id=? AND rating IS NULL", (telegram_id, ))
    found_name = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if found_name is None:
        return None
    
    return found_name[0]


async def get_shop_id(telegram_id:int, shop_name:str, db=path) -> int:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT id FROM shops WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    found_id = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return found_id


async def get_shop_id_by_api(telegram_id: int, api_key: str, db=path) -> int:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT id FROM shops WHERE fk_tg_id=? AND api_key=?", (telegram_id, api_key))
    
    found_id = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if found_id is None:
        return None
    
    return found_id[0]
    
    
async def new_name_shop(telegram_id : int, old_shop_name : str, new_shop_name : str, db=path) -> bool:
    
    # new name is too long
    if len(new_shop_name) > 32:
        return False
    
    # new name isn't unique for the user
    if await get_shop_id(telegram_id, new_shop_name, db) is not None:
        return False
    
    # the shop isn't exists
    if await get_shop_id(telegram_id, old_shop_name, db) is None:
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()

    await cursor.execute("UPDATE shops SET shop_name=? WHERE fk_tg_id=? AND shop_name=?", (new_shop_name, telegram_id, old_shop_name))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True
    
    
async def delete_shop(telegram_id:int, shop_name:str, db=path) -> bool:
    if await get_shop_id(telegram_id, shop_name, db) is None:
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("DELETE FROM shops WHERE shop_name=? AND fk_tg_id=?", (shop_name, telegram_id))
    
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
    
    
async def is_empty_list(telegram_id:int, db=path) -> bool:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT COUNT(shop_name) FROM shops WHERE fk_tg_id=?", (telegram_id, ))
    count = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if count[0] == 0:
        return True
    
    return False
    
    
async def get_api_key(telegram_id:int, shop_name:str, db=path) -> str:
    if await get_shop_id(telegram_id, shop_name, db) is None:
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
    formatted_list = [shop_cortage[0] for shop_cortage in list_of_shops]
    # print("Магазины:", formatted_list)
    
    # list_of_apis = [await get_api_key(telegram_id, shop_name) for shop_name in formatted_list]
    # print("Их ключи: ", list_of_apis)
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return formatted_list


async def toggle_auto_ans(telegram_id:int, shop_name:str, db=path) -> bool:
    if await get_shop_id(telegram_id, shop_name) == -1:
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("UPDATE shops SET auto_ans=(1-auto_ans) WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True


async def get_status_auto_ans(telegram_id:int, shop_name:str, db=path) -> bool | None:
    if await get_shop_id(telegram_id, shop_name) == -1:
        return None
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT auto_ans FROM shops WHERE fk_tg_id=? AND shop_name=?", (telegram_id, shop_name))
    
    got_status = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_status is None:
        return None
    
    if got_status[0] == 1:
        return True
    return False