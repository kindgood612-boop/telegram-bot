# handlers/response/replies.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# ---------- الردود العادية ----------
REPLIES = {
    "سلام": "وعليكم السلام 😎",
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته 🌹",
    "ازيك": "تمام الحمدلله، وانت؟",
    "باي": "باي باي 👋",
    "صباح الخير": "صباح النور يا جميل ☀️",
    "مساء الخير": "مساء الفل 😁",
    "شكرا": "العفو 🙏",
    "تمام": "كويس 😎",
    "هاى": "هاي يا باشا 😁",
    "ايه الاخبار": "الحمدلله كله تمام، وانت؟",
    "حب": "الحب في الهوا 😍",
    "وحشتني": "وانت كمان 😢",
    "هوا الجو": "يااا سلام 🌤",
    "ضحك": "ههههه 😂",
    "معلش": "ولا يهمك 🙏",
    "فينك": "أنا هنا 😎",
    "طبعا": "طبعا يا باشا 😉",
    "معاك": "دايمًا معاك 👍",
    "كويس": "الحمدلله 😁",
    "ايوة": "تمام ✔️",
    "مش فاهم": "ممكن تشرحلي تاني؟ 🤔"
}

# ---------- الردود المخصصة ----------
CUSTOM_REPLIES = {}  # ممكن نضيفها من الأوامر

# ---------- همسات ----------
WHISPERS = {}  # user_id: list من همسات

# ---------- الردود العامة ----------
@router.message()
async def auto_reply(message: Message):
    text = message.text.lower()

    # ردود عادية
    if text in REPLIES:
        await message.reply(REPLIES[text])
        return

    # ردود مخصصة
    if text in CUSTOM_REPLIES:
        await message.reply(CUSTOM_REPLIES[text])
        return

# ---------- أوامر الردود المخصصة ----------
@router.message(Command("اضف_رد"))
async def add_custom_reply(message: Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        return await message.reply("اكتب الكلمة + الرد اللي عايز تضيفه")

    key = parts[1]
    value = parts[2]
    CUSTOM_REPLIES[key] = value
    await message.reply(f"تمام! الرد اتضاف على الكلمة: {key}")

@router.message(Command("مسح_رد"))
async def delete_custom_reply(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("اكتب الكلمة اللي عايز تمسح ردها")

    key = parts[1]
    if key in CUSTOM_REPLIES:
        del CUSTOM_REPLIES[key]
        await message.reply(f"تمام! الرد اتشال على الكلمة: {key}")
    else:
        await message.reply("الكلمة مش موجودة في الردود")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
