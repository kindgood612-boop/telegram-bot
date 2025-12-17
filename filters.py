# filters.py

from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.roles import get_user_role


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        role = await get_user_role(message.chat.id, message.from_user.id)
        return role in (
            "owner", "creator", "manager", "admin"
        )


class IsOwner(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        role = await get_user_role(message.chat.id, message.from_user.id)
        return role in (
            "owner", "creator"
        )
