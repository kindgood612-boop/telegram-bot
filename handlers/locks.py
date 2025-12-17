from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# ---------- حالة القفل لكل ميزة ----------
LOCKS = {
    "روابط": False,
    "صور": False,
    "الشات": False,
    "ملصقات": False,
    "فيديو": False
}

# ---------- أوامر القفل ----------
@router.message(Command("قفل"))
async def lock_feature(message: Message):
    args = message.text.split(" ",1)
    if len(args) < 2:
        return await message.reply("اكتب اسم الحاجة اللي عايز تقفلها، مثال: قفل روابط")
    feature = args[1].strip()
    if feature not in LOCKS:
        return await message.reply("الميزة مش موجودة 😅")
    LOCKS[feature] = True
    await message.reply(f"✅ تم قفل {feature} بنجاح!")

# ---------- أوامر الفتح ----------
@router.message(Command("فتح"))
async def unlock_feature(message: Message):
    args = message.text.split(" ",1)
    if len(args) < 2:
        return await message.reply("اكتب اسم الحاجة اللي عايز تفتحها، مثال: فتح روابط")
    feature = args[1].strip()
    if feature not in LOCKS:
        return await message.reply("الميزة مش موجودة 😅")
    LOCKS[feature] = False
    await message.reply(f"✅ تم فتح {feature} بنجاح!")

# ---------- التحقق من الرسائل ----------
@router.message()
async def check_locked_features(message: Message):
    text = message.text.lower()
    user = message.from_user
    # مثال: قفل روابط
    if LOCKS["روابط"] and ("http" in text or "www." in text):
        await message.delete()
        return await message.answer(f"🚫 {user.first_name}، الروابط مقفولة هنا!")
    # مثال: قفل الصور
    if LOCKS["صور"] and message.photo:
        await message.delete()
        return await message.answer(f"🚫 {user.first_name}، الصور مقفولة هنا!")
    # مثال: قفل الشات
    if LOCKS["الشات"] and text:
        await message.delete()
        return await message.answer(f"🚫 {user.first_name}، الشات مقفول الآن!")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
