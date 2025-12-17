from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import datetime
import random

router = Router()

# ---------- معلومات المجموعة ----------
@router.message(Command("معلومات_المجموعة"))
async def group_info(message: Message):
    chat = message.chat
    await message.reply(f"📝 اسم المجموعة: {chat.title}\n👥 عدد الأعضاء: {chat.get_members_count()}\n🆔 ايدي المجموعة: {chat.id}")

# ---------- نشر رسالة لجميع الأعضاء ----------
@router.message(Command("اذاعة"))
async def broadcast(message: Message):
    args = message.text.split(" ",1)
    if len(args)<2:
        return await message.reply("اكتب الرسالة اللي تحب تبعتها")
    text = args[1]
    # هنا تحط لوجيك البوت لبث الرسالة لكل الأعضاء أو القروبات
    await message.reply(f"📢 تم ارسال الرسالة: {text}")

# ---------- تغيير اسم البوت ----------
@router.message(Command("تغيير_الاسم"))
async def change_bot_name(message: Message):
    args = message.text.split(" ",1)
    if len(args)<2:
        return await message.reply("اكتب الاسم الجديد للبوت")
    new_name = args[1]
    # هنا تحط كود تغيير الاسم الفعلي لو متاح
    await message.reply(f"🤖 تم تغيير اسم البوت إلى: {new_name}")

# ---------- إرسال صورة عشوائية ----------
@router.message(Command("صورة"))
async def send_random_photo(message: Message):
    photos = [
        "https://picsum.photos/300/200",
        "https://picsum.photos/400/300",
        "https://picsum.photos/500/400"
    ]
    await message.reply_photo(photo=random.choice(photos), caption="📸 صورة عشوائية لك!")

# ---------- إرسال الوقت الحالي ----------
@router.message(Command("الوقت"))
async def current_time(message: Message):
    now = datetime.datetime.now()
    await message.reply(f"⏰ الوقت الحالي: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
