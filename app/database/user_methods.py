from app.database.vars import path
from ..database.connection import create_connection


async def add_user(telegram_id: int, db=path) -> bool:
    if await get_user(telegram_id, db) != -1:
        return False
    
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("INSERT INTO users (tg_id) VALUES (?)", (telegram_id, ))
    
    await cursor.close()
    await conn.commit()
    await conn.close()

    return True
    
    
async def get_users(db=path) -> list | None:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT tg_id FROM users")
    got_users = await cursor.fetchall()
        
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_users is None:
        return None
    
    list_of_users = [user[0] for user in got_users]
    
    return list_of_users
    
    
async def get_user(telegram_id: int, db=path) -> int:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT tg_id FROM users WHERE tg_id=?", (telegram_id, ))
    got_telegram_id = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_telegram_id is None:
        return -1
    
    return got_telegram_id[0]


async def get_users_with_balance(db=path) -> dict[:int, :int] | None:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT tg_id, balance FROM users WHERE balance > 0")
    got_balance_users = await cursor.fetchall()
        
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_balance_users is None:
        return None
    
    users_with_balance = [{user[0], user[1]} for user in got_balance_users]
    
    return users_with_balance


async def get_balance(telegram_id: int, db=path) -> int | None:
    conn = await create_connection(db)
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT balance FROM users WHERE tg_id=?", (telegram_id, ))
    got_balance = await cursor.fetchone()
    
    await cursor.close()
    await conn.commit()
    await conn.close()
    
    if got_balance is None:
        return None
    return got_balance[0]