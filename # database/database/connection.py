# database/connection.py

import aiosqlite
from config import DATABASE_PATH


async def get_db():
    return await aiosqlite.connect(DATABASE_PATH)
