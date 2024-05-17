from app.database.vars import path
from ..database.connection import create_connection


async def fill_unanswered_feedbacks(fb_text:str, answer:str, shop_id:int, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("INSERT INTO feedbacks (fb_text, answer, fk_shop_id) VALUES (?, ?, ?)", (fb_text, answer, shop_id))
    
    await cursor.close()
    await conn.commit()
    await conn.close()