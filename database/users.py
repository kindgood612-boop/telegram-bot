# database/users.py

import time
from database.connection import get_db


async def create_users_table():
    db = await get_db()
    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER,
            chat_id     INTEGER,
            username    TEXT,
            first_name  TEXT,
            messages    INTEGER DEFAULT 0,
            points      INTEGER DEFAULT 0,
            last_active INTEGER,
            joined_at   INTEGER,
            PRIMARY KEY (user_id, chat_id)
        )
    """)
    await db.commit()
    await db.close()


async def add_or_update_user(chat_id: int, user):
    db = await get_db()
    now = int(time.time())

    await db.execute("""
        INSERT INTO users (user_id, chat_id, username, first_name, last_active, joined_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, chat_id) DO UPDATE SET
            username=excluded.username,
            first_name=excluded.first_name,
            last_active=excluded.last_active
    """, (
        user.id,
        chat_id,
        user.username,
        user.first_name,
        now,
        now
    ))

    await db.commit()
    await db.close()


async def increase_messages(chat_id: int, user_id: int, count: int = 1):
    db = await get_db()
    await db.execute("""
        UPDATE users
        SET messages = messages + ?
        WHERE chat_id=? AND user_id=?
    """, (count, chat_id, user_id))
    await db.commit()
    await db.close()


async def add_points(chat_id: int, user_id: int, points: int):
    db = await get_db()
    await db.execute("""
        UPDATE users
        SET points = points + ?
        WHERE chat_id=? AND user_id=?
    """, (points, chat_id, user_id))
    await db.commit()
    await db.close()


async def get_user(chat_id: int, user_id: int):
    db = await get_db()
    async with db.execute("""
        SELECT * FROM users
        WHERE chat_id=? AND user_id=?
    """, (chat_id, user_id)) as cursor:
        row = await cursor.fetchone()
    await db.close()
    return row


async def get_top_messages(chat_id: int, limit: int = 10):
    db = await get_db()
    async with db.execute("""
        SELECT user_id, messages
        FROM users
        WHERE chat_id=?
        ORDER BY messages DESC
        LIMIT ?
    """, (chat_id, limit)) as cursor:
        rows = await cursor.fetchall()
    await db.close()
    return rows


async def reset_chat_users(chat_id: int):
    db = await get_db()
    await db.execute("""
        DELETE FROM users WHERE chat_id=?
    """, (chat_id,))
    await db.commit()
    await db.close()
