from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import random

router = Router()

# ---------- قوائم التحشيش ----------
FUN_RESPONSES = [
    "😂 انت جامد موت!",
    "😹 ده مش طبيعي يا عم!",
    "🤣 هههههههههههههه",
    "😎 كدا بقيت ملك التسلية!",
    "😏 فاكر نفسك بطل؟"
]

# ---------- أوامر التحشيش ----------
@router.message(Command("تحشيش"))
async def send_fun(message: Message):
    await message.reply(random.choice(FUN_RESPONSES))

# ---------- أوامر الألعاب الخفيفة ----------
@router.message(Command("كت_تويت"))
async def random_tweet(message: Message):
    tweets = [
        "😂 لو مش حاسس بالسعادة، بص في المرايا!",
        "🤣 الحياة قصيرة، ضحك أكتر!",
        "😅 لما تحاول تذاكر وتلاقي نفسك نايم",
        "😎 القهوة دي اللي هتنقذك من اليوم",
        "😏 انت مش لوحدك اللي متعقد 😹"
    ]
    await message.reply(random.choice(tweets))

@router.message(Command("لو_خيروك"))
async def would_you_rather(message: Message):
    choices = [
        "هل تختار قوة خارقة أم ذكاء فائق؟",
        "هل تختار السفر عبر الزمن أم السفر للفضاء؟",
        "هل تختار المال أم السعادة؟",
        "هل تختار الطعام المفضل لديك أم النوم طوال اليوم؟"
    ]
    await message.reply(random.choice(choices))

# ---------- ألعاب نسب ----------
@router.message(Command("نسبه_حب"))
async def love_percentage(message: Message):
    percent = random.randint(0,100)
    await message.reply(f"❤️ نسبة الحب بينكم: {percent}%")

@router.message(Command("نسبه_غباء"))
async def stupidity_percentage(message: Message):
    percent = random.randint(0,100)
    await message.reply(f"🤪 نسبة الغباء: {percent}%")

@router.message(Command("نسبه_ذكاء"))
async def intelligence_percentage(message: Message):
    percent = random.randint(0,100)
    await message.reply(f"🧠 نسبة الذكاء: {percent}%")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
