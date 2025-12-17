# handlers/admin/roles.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.roles import set_role, remove_role, get_user_role, has_permission

router = Router()

# الرتب اللي ممكن ترفع بيها
ROLES = ["ادمن", "مدير", "مالك"]

# دالة تجيب الشخص اللي هيترفع أو يتنزل
def get_target_user(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    if message.entities:
        for e in message.entities:
            if e.type == "text_mention":
                return e.user
    return None


@router.message(Command("رفع"))
async def promote_user(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("اكتب الرتبة اللي عايز ترفع الشخص ليها")

    role = parts[1]
    if role not in ROLES:
        return await message.reply("الرتبة دي مش موجودة")

    # صلاحية صاحب الامر لازم تكون مالك
    if not await has_permission(message.chat.id, message.from_user.id, "مالك"):
        return await message.reply("معاكش صلاحية تعمل ده")

    target = get_target_user(message)
    if not target:
        return await message.reply("اعمل رد على الشخص اللي عايز ترفعه")

    await set_role(message.chat.id, target.id, role)
    await message.reply(f"تمام! {target.first_name} اترفع → {role}")


@router.message(Command("تنزيل"))
async def demote_user(message: Message):
    if not await has_permission(message.chat.id, message.from_user.id, "مالك"):
        return await message.reply("معاكش صلاحية تعمل ده")

    target = get_target_user(message)
    if not target:
        return await message.reply("اعمل رد على الشخص اللي عايز تنزله")

    await remove_role(message.chat.id, target.id)
    await message.reply(f"{target.first_name} اتنزل للعضو العادي")


@router.message(Command("رتبتي"))
async def my_role(message: Message):
    role = await get_user_role(message.chat.id, message.from_user.id)
    await message.reply(f"رتبتك دلوقتي: {role}")


# تسجيل الرتر
def register(dp):
    dp.include_router(router)
