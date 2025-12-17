# handlers/admin/locks.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.roles import has_permission

router = Router()

# الحاجات اللي ممكن نقفلها
LOCKABLES = [
    "صور",
    "فيديو",
    "ملصقات",
    "استيكر",
    "رابط",
    "كلايش",
    "الشات",
    "شتائم"
]

# ---------- قفل ----------
@router.message(Command("قفل"))
async def lock_stuff(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("اكتب ايه اللي عايز تقفله")

    thing = parts[1]

    if thing not in LOCKABLES:
        return await message.reply(f"مش قادر اقفله، الحاجات اللي اقدر اقفلها: {', '.join(LOCKABLES)}")

    if not await has_permission(message.chat.id, message.from_user.id, "مدير"):
        return await message.reply("معاكش صلاحية تعمل ده")

    # هنا ممكن تضيف القفل الفعلي لكل حاجة في المستقبل
    await message.reply(f"تمام! {thing} اتقفلت دلوقتي")


# ---------- فتح ----------
@router.message(Command("فتح"))
async def unlock_stuff(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("اكتب ايه اللي عايز تفتحه")

    thing = parts[1]

    if thing not in LOCKABLES:
        return await message.reply(f"مش قادر افتحه، الحاجات اللي اقدر افتحها: {', '.join(LOCKABLES)}")

    if not await has_permission(message.chat.id, message.from_user.id, "مدير"):
        return await message.reply("معاكش صلاحية تعمل ده")

    # هنا ممكن تضيف الفتح الفعلي لكل حاجة في المستقبل
    await message.reply(f"تمام! {thing} اتفتحت دلوقتي")


# تسجيل الريتر
def register(dp):
    dp.include_router(router)
