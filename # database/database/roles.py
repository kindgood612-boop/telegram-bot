# database/roles.py

from database.connection import get_db


async def get_user_role(chat_id: int, user_id: int) -> str:
    db = await get_db()

    async with db.execute(
        "SELECT role FROM roles WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    ) as cursor:
        row = await cursor.fetchone()

    await db.close()
    return row[0] if row else "member"
