# handlers/admin/moderation.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.roles import has_permission
from database.users import get_user_role

router = Router()

# تجيب الشخص اللي هنعمله حظر أو كتم أو طرد
def get_target_user(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    if message.entities:
        for e in message.entities:
            if e.type == "text_mention":
                return e.user
    return None

# ---------- حظر ----------
@router.message(Command("حظر"))
async def ban_user(message: Message):
    if not await has_permission(message.chat.id, message.from_user.id, "مدير"):
        return await message.reply("معاكش صلاحية تعمل ده")

    target = get_target_user(message)
    if not target:
        return await message.reply("اعمل رد على الشخص اللي عايز تحظره")

    try:
        await message.chat.kick(user_id=target.id)
        await message.reply(f"{target.first_name} اتحظر من الجروب")
    except Exception as e:
        await message.reply(f"حصل غلط: {e}")

# ---------- فك الحظر ----------
@router.message(Command("فك_الحظر"))
async def unban_user(message: Message):
    if not await has_permission(message.chat.id, message.from_user.id, "مدير"):
        return await message.reply("معاكش صلاحية تعمل ده")

    target = get_target_user(message)
    if not target:
        return await message.reply("اعمل رد على الشخص اللي عايز تفك عنه الحظر")

    try:
        await message.chat.unban(user_id=target.id)
        await message.reply(f"{target.first_name} اتفك عنه الحظر")
    except Exception as e:
        await message.reply(f"حصل غلط: {e}")

# ---------- كتم ----------
@router.message(Command("كتم"))
async def mute_user(message: Message):
    if not await has_permission(message.chat.id, message.from_user.id, "مدير"):
        return await message.reply("معاكش صلاحية تعمل ده")

    target = get_target_user(message)
    if not target:
        return await message.reply("اعمل رد على الشخص اللي عايز تكتمه")

    try:
        await message.chat.restrict(user_id=target.id, can_send_messages=False)
        await message.reply(f"{target.first_name} اتكتم")
    except Exception as e:
        await message.reply(f"حصل غلط: {e}")

# ---------- فك الكتم ----------
@router.message(Command("فك_الكتم"))
async def unmute_user(message: Message):
    if not await has_permission(message.chat.id, message.from_user.id, "مدير"):
        return await message.reply("معاكش صلاحية تعمل ده")

    target = get_target_user(message)
    if not target:
        return await message.reply("اعمل رد على الشخص اللي عايز تفك عنه الكتم")

    try:
        await message.chat.restrict(user_id=target.id, can_send_messages=True)
        await message.reply(f"{target.first_name} اتفك عنه الكتم")
    except Exception as e:
        await message.reply(f"حصل غلط: {e}")


# تسجيل الريتر
def register(dp):
    dp.include_router(router)
