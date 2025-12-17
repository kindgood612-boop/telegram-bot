# handlers/games/smart_fun.py

from aiogram import Router
from aiogram.types import Message, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, Text
import random

router = Router()

# ---------- نقاط اللاعبين ----------
PLAYER_POINTS = {}  # user_id: points

# ---------- الأسئلة المتنوعة ----------
QUESTIONS = [
    {"q": "كم عدد أرجل القطط؟ 🐱", "type": "quiz", "answer": "4"},
    {"q": "ايه لون السما؟ 🌞", "type": "quiz", "answer": "أزرق"},
    {"q": "لو خيروك: تاخد 10000 دلوقتي ولا 50000 بعد سنة؟ 💸", "type": "choice", "options": ["10000 دلوقتي", "50000 بعد سنة"]},
    {"q": "تفضل تعيش في مصر ولا بره؟ 🌍", "type": "choice", "options": ["مصر", "بره"]},
]

# ---------- شعارات ----------
LOGOS = [
    {"img": "assets/logo1.jpg", "options": ["تيك توك","يوتيوب","فيسبوك"], "answer": "تيك توك"},
    {"img": "assets/logo2.jpg", "options": ["فيسبوك","انستغرام","سناب شات"], "answer": "فيسبوك"},
    {"img": "assets/logo3.jpg", "options": ["انستغرام","تيليجرام","تويتر"], "answer": "انستغرام"},
]

# ---------- صور أسئلة ----------
IMAGES = [
    {"img": "assets/img1.jpg", "questions": ["ايه ده في الصورة؟ 🤔","صفلي الصورة بكلمة واحدة 🖼️","تخيل القصة ورا الصورة ✨"]},
    {"img": "assets/img2.jpg", "questions": ["احزر مين في الصورة؟ 😎","ايه الحاجة المميزة هنا؟ 🌟","خمن القصة وراء الصورة"]},
]

# ---------- لعبة أسئلة عشوائية ----------
@router.message(Command("سؤال"))
async def random_question(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)

    question = random.choice(QUESTIONS)
    if question["type"] == "quiz":
        await message.reply(f"{user.first_name}، جاوب السؤال ده: {question['q']}")
    elif question["type"] == "choice":
        options = ", ".join(question["options"])
        await message.reply(f"{user.first_name}، {question['q']}\nاختيارات: {options}")

# ---------- لعبة صورة مع سؤال ----------
@router.message(Command("سؤال_صورة"))
async def question_image(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)

    img_obj = random.choice(IMAGES)
    img = InputFile(img_obj["img"])
    text = random.choice(img_obj["questions"])
    await message.reply_photo(img, caption=f"{user.first_name}، {text}")

# ---------- لعبة شعار ذكي ----------
@router.message(Command("شعار_زكي"))
async def smart_logo_game(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)

    logo = random.choice(LOGOS)
    img = InputFile(logo["img"])

    kb = InlineKeyboardMarkup(row_width=1)
    for idx, option in enumerate(logo["options"], start=1):
        kb.add(InlineKeyboardButton(text=f"{idx} - {option}", callback_data=f"logo_{option}_{user.id}"))
    
    await message.reply_photo(img, caption=f"{user.first_name}، اعرف الشعار ده! ✨", reply_markup=kb)

# ---------- الرد على اختيار الشعار ----------
@router.callback_query(lambda c: c.data.startswith("logo_"))
async def logo_callback(callback_query):
    data = callback_query.data.split("_")
    selected = data[1]
    user_id = int(data[2])

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("دي مش لعبتك 🙄", show_alert=True)
    
    logo = next((l for l in LOGOS if selected in l["options"]), None)
    if not logo:
        return

    if selected == logo["answer"]:
        PLAYER_POINTS[user_id] += 50
        text = f"🎉 صح! الشعار ده {logo['answer']}! \nنقاطك دلوقتي: {PLAYER_POINTS[user_id]}"
    else:
        PLAYER_POINTS[user_id] = max(PLAYER_POINTS[user_id]-10,0)
        text = f"❌ غلط! الشعار الصح: {logo['answer']}\nنقاطك دلوقتي: {PLAYER_POINTS[user_id]}"
    
    await callback_query.message.edit_caption(text)
    await callback_query.answer()

# ---------- لعبة حوار ممتع ----------
@router.message(Command("حوار"))
async def smart_chat(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)
    dialogues = [
        f"{user.first_name}، لو كنت سوبر هيرو، هتعمل ايه اليوم؟ 🦸‍♂️",
        f"{user.first_name}، لو قدرت تغير حاجة في العالم، هتعمل ايه؟ 🌎",
        f"{user.first_name}، قوللي نكتة مضحكة 😂",
        f"{user.first_name}، لو عندك 3 أمنيات، هتطلب ايه؟ ✨",
        f"{user.first_name}، لو حبيت تكسب جائزة كبيرة، هتعمل ايه؟ 🏆"
    ]
    await message.reply(random.choice(dialogues))

# ---------- ألعاب الحظ ----------
@router.message(Command("روليت"))
async def roulette_game(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)
    outcomes = ["خسرت 😢", "كسبت 50 نقطة 💰", "كسبت 100 نقطة 💰", "روليت فاضي 😶"]
    result = random.choice(outcomes)
    if "كسبت" in result:
        points = int(result.split()[1])
        PLAYER_POINTS[user.id] += points
        result += f"، مجموعك دلوقتي {PLAYER_POINTS[user.id]} نقطة"
    await message.reply(f"{user.first_name}: {result}")

@router.message(Command("بنك"))
async def bank_game(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)
    earned = random.randint(10, 100)
    PLAYER_POINTS[user.id] += earned
    await message.reply(f"{user.first_name} كسبت {earned} نقطة 💰، مجموعك دلوقتي {PLAYER_POINTS[user.id]} نقطة")

@router.message(Command("لو_خيروك"))
async def would_you_rather(message: Message):
    user = message.from_user
    PLAYER_POINTS.setdefault(user.id, 0)
    questions = [
        "تفضل تاخد فلوس دلوقتي ولا بعد شهر؟ 💸",
        "تفضل تعيش يوم كامل في البحر ولا في الجبل؟ 🏖️🏔️",
        "تفضل تكون غني بس وحيد ولا فقير مع صحابك؟ 😅"
    ]
    await message.reply(f"{user.first_name}: {random.choice(questions)}")

# ---------- تسجيل الريتر ----------
def register(dp):
    dp.include_router(router)
