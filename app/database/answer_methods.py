from app.database.vars import path
from app.database.shop_methods import get_shop_id
from ..database.connection import create_connection


async def get_feedback_id(fb_id:str, db=path) -> int | bool:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fb_id FROM feedbacks WHERE fb_id=?", (fb_id, ))
    
    got_id = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_id is None:
        return False
    
    return got_id[0]


async def fill_unanswered_feedback(fb_id: str, fb_rating:int, fb_shop_wb:str, fb_product_wb:str, fb_text:str, api_key:str, db=path) -> bool:
    if await get_feedback_id(fb_id) != False:
        return False
    
    fk_shop_id = await get_shop_id(api_key=api_key)
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("INSERT INTO feedbacks (fb_id, fb_rating, fb_shop_wb, fb_product_wb, fb_text, fk_shop_id) VALUES (?, ?, ?, ?, ?, ?)",
                         (fb_id, fb_rating, fb_shop_wb, fb_product_wb, fb_text, fk_shop_id))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    return True


async def get_feedback(fb_id:str, db=path) -> bool | list:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fb_rating, fb_shop_wb, fb_product_wb, fb_text FROM feedbacks WHERE fb_id=?", (fb_id, ))
    
    got_feedback = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_feedback is None:
        return False

    return got_feedback


async def get_unanswered_fb_list(telegram_id:int, db=path) -> bool | list:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fb.fb_rating, fb.fb_shop_wb, fb.fb_product_wb, fb.fb_text, fb.fb_id FROM feedbacks fb LEFT JOIN shops sh on sh.id=fb.fk_shop_id LEFT JOIN users u on u.tg_id=sh.fk_tg_id WHERE u.tg_id=?", (telegram_id, ))
    
    list_of_fb = await cursor.fetchall()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if list_of_fb is None:
        return False

    return list_of_fb