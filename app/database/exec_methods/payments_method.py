from app.database.vars import path
from ...database.connection import create_connection


async def new_payment(tg_id: int, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()

    await cursor.execute("INSERT INTO payments (fk_tg_id) VALUES (?)", (tg_id,))

    await cursor.close()
    await conn.commit()
    await conn.close()


async def get_payment_id(tg_id: int, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()

    await cursor.execute("SELECT id FROM payments WHERE fk_tg_id=?", (tg_id,))

    got_id = await cursor.fetchall()

    await cursor.close()
    await conn.commit()
    await conn.close()

    if len(got_id) == 0:
        return None
    return got_id


async def get_last_payment_id(tg_id: int, db=path):
    got_id = await get_payment_id(tg_id)

    if got_id is None:
        return None

    return got_id[-1][0]


async def get_user_id_by_payment_id(invId: int, db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()

    await cursor.execute("SELECT fk_tg_id FROM payments WHERE id=?", (invId,))

    got_id = await cursor.fetchone()

    await cursor.close()
    await conn.commit()
    await conn.close()

    if got_id is None:
        return None
    return got_id
