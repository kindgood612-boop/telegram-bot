from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

# ---------- أزرار الإدارة بأسماء الأوامر ----------
admin_buttons = [
    [KeyboardButton("رفع ↢ مشرف"), KeyboardButton("تنزيل ↢ مشرف")],
    [KeyboardButton("حظر"), KeyboardButton("كتم"), KeyboardButton("تقييد")],
    [KeyboardButton("رفع القيود"), KeyboardButton("كشف القيود")]
]

# ---------- أزرار الألعاب بأسماء الأوامر ----------
game_buttons = [
    [KeyboardButton("حجره-ورقه-مقص ← بلاي"), KeyboardButton("لونك المفضل ← الوان")],
    [KeyboardButton("لو خيروك ← التحديات"), KeyboardButton("كت تويت ← التسلية"), KeyboardButton("تحشيش ← التسلية")],
    [KeyboardButton("نسبه الحب"), KeyboardButton("نسبه الذكاء"), KeyboardButton("نسبه الغباء")]
]

# ---------- أزرار الردود والهمسات بأسماء الأوامر ----------
response_buttons = [
    [KeyboardButton("رد السلام ← الردود"), KeyboardButton("همسه ← الهمسات"), KeyboardButton("همسه انلاين ← الهمسات")]
]

# ---------- أزرار القفل والتعطيل بأسماء الأوامر ----------
lock_buttons = [
    [KeyboardButton("قفل الروابط"), KeyboardButton("فتح الروابط"), KeyboardButton("قفل الشات")],
    [KeyboardButton("قفل الصور"), KeyboardButton("فتح الصور"), KeyboardButton("قفل المتحركات")]
]

# ---------- أزرار المتفرقات بأسماء الأوامر ----------
misc_buttons = [
    [KeyboardButton("معلومات القروب ← متفرقات"), KeyboardButton("صورة ← متفرقات"), KeyboardButton("الوقت ← متفرقات")],
    [KeyboardButton("تغيير الاسم ← متفرقات"), KeyboardButton("اذاعة ← متفرقات")]
]

# ---------- زر العودة ----------
back_button = [[KeyboardButton("رجوع")]]

# ---------- دمج كل الأزرار في كيبورد واحد ----------
SMART_NAMED_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=admin_buttons + game_buttons + response_buttons + lock_buttons + misc_buttons + back_button,
    resize_keyboard=True
)

# ---------- أمر إظهار الكيبورد الذكي بالأسماء ----------
@router.message(Command("كيبورد_بالأسماء"))
async def show_named_keyboard(message: Message):
    await message.reply("🌟 استخدم الكيبورد الذكي لأقوى تجربة تفاعلية مع أسماء الأوامر:", reply_markup=SMART_NAMED_KEYBOARD)

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
