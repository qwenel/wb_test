from app.database.vars import path
from ..database.connection import create_connection


async def fill_unanswered_feedbacks(fb_text:str, shop_id:int, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("INSERT INTO feedbacks (fb_text, fk_shop_id) VALUES (?, ?, ?)", (fb_text, shop_id))
    
    await cursor.close()
    await conn.commit()
    await conn.close()