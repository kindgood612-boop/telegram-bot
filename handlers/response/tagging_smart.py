# handlers/response/tagging_smart.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import random

router = Router()

# ---------- تاكات جاهزة ----------
TAG_MESSAGES = {
    "member": [
        "يا معلم {name} 😎",
        "تفضل شوف يا {name} 😏",
        "فينك يا {name}؟ 🙌",
        "هتعمل ايه يا {name}؟ 😁",
        "يلا بينا يا {name} 🚀"
    ],
    "admin": [
        "يا راعي المجموعة {name} 😎",
        "النهاردة يومك يا {name} 💪",
        "احنا تحت أمرك {name} 😉",
        "تحية خاصة ليك يا {name} 🌟"
    ],
    "owner": [
        "الملك {name} 👑",
        "صاحبنا الكبير {name} 😎",
        "يا باشا {name} الكل بينتظرك 🙌"
    ]
}

EMOJIS = ["😎", "😂", "🔥", "💥", "😉", "🥳", "🤩"]

# ---------- تحديد نوع العضو ----------
def get_user_type(user):
    # Placeholder - ممكن توصلها بالبوت وتحدد على حسب القوائم
    if user.is_bot:
        return "member"
    # هتعدل هنا حسب القوائم: مالك، مشرف، عضو
    return "member"

# ---------- تاك ذكي ----------
@router.message(Command("تاك"))
async def tag_member(message: Message):
    if not message.reply_to_message:
        return await message.reply("اعمل رد على الشخص اللي عايز تعمل له تاك")

    target = message.reply_to_message.from_user
    user_type = get_user_type(target)
    text = random.choice(TAG_MESSAGES[user_type])
    emoji = random.choice(EMOJIS)
    await message.reply(f"{text.format(name=target.first_name)} {emoji}")

# ---------- تاك ايموجي ----------
@router.message(Command("تاك_ايموجي"))
async def tag_emoji(message: Message):
    if not message.reply_to_message:
        return await message.reply("اعمل رد على الشخص اللي عايز تعمله تاك ايموجي")
    
    target = message.reply_to_message.from_user
    emoji_combo = "".join(random.sample(EMOJIS, 3))
    await message.reply(f"{target.first_name} {emoji_combo}")

# ---------- تاك تفاؤلي ----------
@router.message(Command("المتفائل"))
async def tag_optimist(message: Message):
    if not message.reply_to_message:
        return await message.reply("اعمل رد على الشخص اللي عايز تعمله تاك شخصية المتفائل")
    
    target = message.reply_to_message.from_user
    texts = [
        f"{target.first_name} كله خير يا رب! 😇",
        f"{target.first_name} ابتسم 😊",
        f"{target.first_name} يومك حلو إن شاء الله 🌞",
        f"{target.first_name} خليك إيجابي 💪",
        f"{target.first_name} السعادة ليك اليوم 🎉"
    ]
    await message.reply(random.choice(texts))

# ---------- نداء ذكي للمجموعة ----------
@router.message(Command("نداء"))
async def tag_all(message: Message):
    text = message.text.split(maxsplit=1)
    if len(text) < 2:
        return await message.reply("اكتب النص اللي عايز تعمله نداء للكل")

    custom_text = text[1]
    emojis = ["📢", "🎉", "✨", "💥", "🤩"]
    emoji = random.choice(emojis)
    jokes = [
        "يلا نضحك شوية 😎",
        "الكل جاهز؟ 🙌",
        "الفل والوناسة 😁",
        "جاهزين للمرح؟ 🥳"
    ]
    joke = random.choice(jokes)
    await message.reply(f"نداء عام: {custom_text} {emoji} — {joke}")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
