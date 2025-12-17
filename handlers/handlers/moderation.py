from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# ---------- قوائم الحظر والكتم والتقييد ----------
BANNED_USERS = set()
MUTED_USERS = set()
RESTRICTED_USERS = set()

# ---------- حظر المستخدم ----------
@router.message(Command("حظر"))
async def ban_user(message: Message):
    args = message.text.split(" ",1)
    if len(args) < 2:
        return await message.reply("اكتب يوزر الشخص أو الايدي، مثال: حظر @username")
    user = args[1].strip()
    BANNED_USERS.add(user)
    await message.reply(f"🚫 تم حظر {user} بنجاح!")

# ---------- فك الحظر ----------
@router.message(Command("الغاء_حظر"))
async def unban_user(message: Message):
    args = message.text.split(" ",1)
    if len(args) < 2:
        return await message.reply("اكتب يوزر الشخص أو الايدي")
    user = args[1].strip()
    BANNED_USERS.discard(user)
    await message.reply(f"✅ تم الغاء الحظر عن {user}")

# ---------- كتم المستخدم ----------
@router.message(Command("كتم"))
async def mute_user(message: Message):
    args = message.text.split(" ",1)
    if len(args) < 2:
