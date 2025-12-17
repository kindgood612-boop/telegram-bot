from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# ---------- نقاط كل لاعب ----------
PLAYER_POINTS = {}  # user_id: points

# ---------- إضافة نقاط ----------
@router.message(Command("نقاطي"))
async def show_points(message: Message):
    user_id = message.from_user.id
    points = PLAYER_POINTS.get(user_id, 0)
    await message.reply(f"{message.from_user.first_name}، نقاطك دلوقتي: {points} 🎯")

@router.message(Command("كسب_نقاط"))
async def gain_points(message: Message):
    user_id = message.from_user.id
    PLAYER_POINTS.setdefault(user_id, 0)
    PLAYER_POINTS[user_id] += 50
    await message.reply(f"🎉 ممتاز! كسبت 50 نقطة، مجموعك دلوقتي {PLAYER_POINTS[user_id]} نقطة")

@router.message(Command("خسر_نقاط"))
async def lose_points(message: Message):
    user_id = message.from_user.id
    PLAYER_POINTS.setdefault(user_id, 0)
    PLAYER_POINTS[user_id] = max(PLAYER_POINTS[user_id]-20,0)
    await message.reply(f"😅 خسرت 20 نقطة، مجموعك دلوقتي {PLAYER_POINTS[user_id]} نقطة")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
