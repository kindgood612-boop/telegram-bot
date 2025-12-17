# middlewares/permissions.py

from aiogram import BaseMiddleware
from aiogram.types import Message
from database.roles import get_user_role


class PermissionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if not event.from_user or not event.chat:
            return await handler(event, data)

        data["user_role"] = await get_user_role(
            event.chat.id,
            event.from_user.id
        )

        return await handler(event, data)
