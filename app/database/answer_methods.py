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


async def fill_unanswered_feedback(fb_id: str, fb_rating:int, fb_shop_wb:str, fb_product_wb:str, fb_text:str, fk_api_key:str, db=path) -> bool:
    if await get_feedback_id(fb_id) != False:
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("INSERT INTO feedbacks (fb_id, fb_rating, fb_shop_wb, fb_product_wb, fb_text, fk_api_key) VALUES (?, ?, ?, ?, ?, ?)",
                         (fb_id, fb_rating, fb_shop_wb, fb_product_wb, fb_text, fk_api_key))
    
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


async def get_feedback_to_generate_answer(fb_id:str, db=path) -> bool | list:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fb_text, fk_api_key FROM feedbacks WHERE fb_id=?", (fb_id, ))
    
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
    
    await cursor.execute("SELECT fb.fb_rating, fb.fb_shop_wb, fb.fb_product_wb, fb.fb_text, fb.fb_id FROM feedbacks fb LEFT JOIN shops sh on sh.api_key=fb.fk_api_key LEFT JOIN users u on u.tg_id=sh.fk_tg_id WHERE u.tg_id=? AND fb.fb_answer IS NULL", (telegram_id, ))
    
    list_of_fb = await cursor.fetchall()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if len(list_of_fb) == 0:
        return False

    return list_of_fb


async def get_answer(telegram_id:int, shop_name:str, db=path) -> str | bool:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fb.fb_answer FROM feedbacks fb LEFT JOIN shops sh on sh.api_key=fb.fk_api_key LEFT JOIN users u on u.tg_id=sh.fk_tg_id WHERE u.tg_id=? AND sh.shop_name=?", (telegram_id, shop_name))
    
    got_answer = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_answer is None:
        return False

    return got_answer[0]


async def get_answer_by_feedback_id(fb_id: str, db=path) -> str | bool:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fb_answer FROM feedbacks WHERE fb_id=?", (fb_id, ))
    
    got_answer = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_answer is None:
        return False

    return got_answer[0]


async def get_api_key_by_feedback_id(fb_id: str, db=path) -> str | bool:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fk_api_key FROM feedbacks WHERE fb_id=?", (fb_id, ))
    
    got_api = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_api is None:
        return False

    return got_api[0]


async def get_not_null_answer_feedbacks_list(telegram_id:int, db=path) -> list | bool:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT fb.fb_rating, fb.fb_shop_wb, fb.fb_product_wb, fb.fb_text, fb.fb_answer, fb.fb_id FROM feedbacks fb LEFT JOIN shops sh on sh.api_key=fb.fk_api_key LEFT JOIN users u on u.tg_id=sh.fk_tg_id WHERE u.tg_id=? AND fb.fb_answer IS NOT NULL", (telegram_id, ))
    
    list_of_feedbacks = await cursor.fetchall()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if len(list_of_feedbacks) == 0:
        return False

    return list_of_feedbacks


async def update_answer_text(fb_id:str, ans_text:str, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    if ans_text == "null":
        await cursor.execute("UPDATE feedbacks SET fb_answer=NULL WHERE fb_id=?", (fb_id, ))
        print("поставил нул")
    else:
        await cursor.execute("UPDATE feedbacks SET fb_answer=? WHERE fb_id=?", (ans_text, fb_id))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    
async def mark_shown_feedback(fb_id: str, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()

    await cursor.execute("UPDATE feedbacks SET show_date=datetime('now', '+3 hours') WHERE fb_id=? AND show_date=0", (fb_id, ))
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    
async def delete_old_shown_feedback(db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()

    await cursor.execute("DELETE FROM feedbacks WHERE datetime('now', '+3 hours') > datetime(show_date, '+24 hours') AND show_date != 0")
    
    await cursor.close()
    await conn.commit()
    await conn.close()