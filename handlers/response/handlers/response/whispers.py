# handlers/response/whispers.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import random

router = Router()

# ---------- همسات المستخدمين ----------
WHISPERS = {}  # user_id: list من همسات

# قائمة همسات عامة ذكية
SMART_WHISPERS = [
    "بتوحشني 😢",
    "عامل ايه النهاردة؟ 😎",
    "خليك مبسوط 😁",
    "هاااي 🌸",
    "حبيت أجي اسلم عليك 😇",
    "تفائل بالخير 👌"
]

# أمر عمل همسة لشخص بالرد
@router.message(Command("همسه"))
async def whisper_user(message: Message):
    if not message.reply_to_message:
        return await message.reply("اعمل رد على الشخص اللي عايز تعمل له همسة")

    target = message.reply_to_message.from_user
    text = message.text.split(maxsplit=1)
    
    if len(text) < 2:
        return await message.reply("اكتب نص الهمسة بعد الامر")

    whisper_text = text[1]

    if target.id not in WHISPERS:
        WHISPERS[target.id] = []

    WHISPERS[target.id].append(whisper_text)
    await message.reply(f"تمام! همسة اتبعتت لـ {target.first_name} 💌")

# أمر لجعل البوت يهمس لك تلقائي من همساتك أو من الذكاء العام
@router.message(Command("اهمسلي"))
async def whisper_me(message: Message):
    user_id = message.from_user.id
    all_whispers = WHISPERS.get(user_id, []) + SMART_WHISPERS
    whisper_text = random.choice(all_whispers)
    await message.reply(f"همسة ليك: {whisper_text} 💌")

# أمر همسة عشوائية لشخص آخر
@router.message(Command("زاجل"))
async def random_whisper(message: Message):
    users = list(WHISPERS.keys())
    if not users:
        whisper_text = random.choice(SMART_WHISPERS)
        return await message.reply(f"زاجل ذكي: {whisper_text} ✨")

    target_id = random.choice(users)
    target_whispers = WHISPERS.get(target_id, []) + SMART_WHISPERS
    whisper_text = random.choice(target_whispers)
    await message.reply(f"زاجل: {whisper_text} 💌")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
