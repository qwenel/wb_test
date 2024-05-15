from aiosqlite import connect, Connection
from app.database.vars import path, creation


async def create_connection(db=path) -> Connection:
    conn = await connect(db)
    cursor = await conn.cursor()
    
    await cursor.executescript(creation)
    
    await cursor.close()
    await conn.commit()
    
    return conn