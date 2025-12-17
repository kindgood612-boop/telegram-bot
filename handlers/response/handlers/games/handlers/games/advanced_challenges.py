# handlers/games/advanced_challenges.py

from aiogram import Router
from aiogram.types import Message, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import random

router = Router()

# ---------- نقاط اللاعبين ----------
PLAYER_POINTS = {}  # user_id: points

# ---------- ألغاز متقدمة ----------
PUZZLES = [
    {"q": "انا شيء، كلما أخذت مني زاد لديك. ما أنا؟ 🤔", "answer": "ثقب"},
    {"q": "شيء إذا كسرت اسمه يصبح أطول؟", "answer": "العصا"},
    {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "answer": "القلم"},
]

# ---------- تحديات ممتعة ----------
CHALLENGES = [
    "اعمل صورة لرسم قلب في الهواء وصورني 🙌",
    "اعمل لي تحدي سريع: قول لي 3 أشياء بتحبها دلوقتي ❤️",
    "اعمل تحدي: جرب تحزر رقم بين 1 و10 🏆",
]

# ---------- لعبة لغز ----------
@router.message(Command("لغز"))
async def random_puzzle(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)

    puzzle = random.choice(PUZZLES)
    await message.reply(f"{user.first_name}، حل اللغز ده: {puzzle['q']}")

# ---------- لعبة تحدي ممتع ----------
@router.message(Command("تحدي"))
async def fun_challenge(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)

    challenge = random.choice(CHALLENGES)
    await message.reply(f"{user.first_name}, تحديك النهارده: {challenge}")

# ---------- إضافة تفاعل ونقاط على الإجابات ----------
@router.message()
async def track_points(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)

    # تفاعل ذكي: كل رسالة فيها إجابة أو تحدي صح تزيد نقاط
    text = message.text.lower()

    # زيادة نقاط بسيطة لكل مشاركة ذكية
    if any(word in text for word in ["صح", "تمام", "صح جدا", "حلو"]):
        PLAYER_POINTS[user.id] += 20
        await message.reply(f"👍 ممتاز! كسبت 20 نقطة، مجموعك دلوقتي {PLAYER_POINTS[user.id]} نقطة")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
