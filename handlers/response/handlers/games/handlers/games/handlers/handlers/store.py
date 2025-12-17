from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from handlers.points import PLAYER_POINTS

router = Router()

# ---------- رتب البوت ----------
RANKS_STORE = {
    "مميز": 100,
    "ادمن": 200,
    "مدير": 500,
    "منشئ": 1000,
    "مالك": 2000
}

USER_RANKS = {}  # user_id: rank

# ---------- عرض المتجر ----------
@router.message(Command("متجري"))
async def show_store(message: Message):
    text = "🛒 متجر الرتب:\n"
    for rank, price in RANKS_STORE.items():
        text += f"- {rank} : {price} نقطة\n"
    await message.reply(text)

# ---------- شراء رتبة ----------
@router.message(Command("شراء_رتبة"))
async def buy_rank(message: Message):
    try:
        user_id = message.from_user.id
        args = message.text.split(" ", 1)
        if len(args) < 2:
            return await message.reply("اكتب اسم الرتبة بعد الأمر، مثال: شراء_رتبة مميز")
        rank_name = args[1].strip()
        if rank_name not in RANKS_STORE:
            return await message.reply("الرتبة مش موجودة في المتجر 😅")
        price = RANKS_STORE[rank_name]
        PLAYER_POINTS.setdefault(user_id, 0)
        if PLAYER_POINTS[user_id] < price:
            return await message.reply(f"نقاطك مش كفاية 😢 تحتاج {price} نقطة للرتبة دي")
        # خصم النقاط ومنح الرتبة
        PLAYER_POINTS[user_id] -= price
        USER_RANKS[user_id] = rank_name
        await message.reply(f"🎉 ممتاز! اشتريت رتبة {rank_name}\nنقاطك دلوقتي: {PLAYER_POINTS[user_id]}")
    except Exception as e:
        await message.reply(f"حصل خطأ 😢: {e}")

# ---------- عرض رتبة المستخدم ----------
@router.message(Command("رتبتي"))
async def my_rank(message: Message):
    user_id = message.from_user.id
    rank = USER_RANKS.get(user_id, "لا توجد رتبة")
    await message.reply(f"{message.from_user.first_name}، رتبتك دلوقتي: {rank}")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
