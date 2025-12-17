from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import datetime
import json
import os

# ====================== إعدادات البوت ======================
TOKEN = "8517776533:AAEgwzqn4EtkIZtAhpi33LU9EMqDk3KHpCc"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ====================== قوائم البوت ======================
banned_users = set()
muted_users = set()
restricted_users = set()
owners = set()
admins = set()
creators = set()
vip_users = set()
welcome_messages = {}
blocked_words = ["رابط", "badword1", "badword2"]  # كلمات محظورة
auto_replies = {"السلام عليكم": "وعليكم السلام"}  # رد تلقائي
logs_file = "bot_logs.json"

# ====================== وظائف مساعدة ======================
def save_logs(data):
    if os.path.exists(logs_file):
        with open(logs_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(data)
    with open(logs_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def user_info(update: Update):
    return f"{update.message.from_user.full_name} ({update.message.from_user.id})"

# ====================== الردود الأساسية ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في عزيزي")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "━━━━━━━━━━━━\nقائمة اوامر الادمنيه\n━━━━━━━━━━━━\n"
    msg += "- اوامر الرفع والتنزيل :\n"
    msg += "• رفع - تنزيل مالك اساسي\n• رفع - تنزيل مالك\n• رفع - تنزيل مشرف\n"
    msg += "• رفع - تنزيل منشئ\n• رفع - تنزيل مدير\n• رفع - تنزيل ادمن\n"
    msg += "• رفع - تنزيل مميز\n• تنزيل الكل - لازاله جميع الرتب اعلاه\n\n"
    msg += "- اوامر المسح :\n"
    msg += "• مسح الكل\n• مسح المنشئين\n• مسح المدراء\n• مسح المالكين\n"
    msg += "• مسح الادمنيه\n• مسح المميزين\n• مسح المحظورين\n• مسح المكتومين\n"
    msg += "• مسح قائمه المنع\n• مسح الردود\n• مسح الاوامر المضافه\n"
    msg += "• مسح + عدد\n• مسح بالرد\n• مسح الايدي\n• مسح الترحيب\n• مسح الرابط\n\n"
    msg += "- اوامر الطرد والحظر :\n"
    msg += "• تقييد + الوقت\n• حظر\n• طرد\n• كتم\n• تقييد\n"
    msg += "• الغاء الحظر\n• الغاء الكتم\n• فك التقييد\n• رفع القيود\n"
    msg += "• منع بالرد\n• الغاء منع بالرد\n• طرد البوتات\n• طرد المحذوفين\n• كشف البوتات\n"
    msg += "━━━━━━━━━━━━"
    await update.message.reply_text(msg)

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"رقمك: {update.message.from_user.id}")

# ====================== أوامر الرفع والتنزيل ======================
async def add_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        owners.add(user_id)
        await update.message.reply_text(f"✅ تم رفع {user_id} كمالك")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def remove_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        owners.discard(user_id)
        await update.message.reply_text(f"✅ تم تنزيل {user_id} من المالكين")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        admins.add(user_id)
        await update.message.reply_text(f"✅ تم رفع {user_id} كادمن")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        admins.discard(user_id)
        await update.message.reply_text(f"✅ تم تنزيل {user_id} من الادمنيه")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def add_creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        creators.add(user_id)
        await update.message.reply_text(f"✅ تم رفع {user_id} كمنشئ")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def remove_creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        creators.discard(user_id)
        await update.message.reply_text(f"✅ تم تنزيل {user_id} من المنشئين")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

# ====================== أوامر الحظر والكتم والطرد ======================
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        banned_users.add(user_id)
        await update.message.reply_text(f"✅ تم حظر {user_id}")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        banned_users.discard(user_id)
        await update.message.reply_text(f"✅ تم رفع الحظر عن {user_id}")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        muted_users.add(user_id)
        await update.message.reply_text(f"✅ تم كتم {user_id}")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        muted_users.discard(user_id)
        await update.message.reply_text(f"✅ تم رفع الكتم عن {user_id}")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ تم طرد المستخدم (مثال)")

async def restrict_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        restricted_users.add(user_id)
        await update.message.reply_text(f"✅ تم تقييد {user_id}")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

async def unrestrict_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        restricted_users.discard(user_id)
        await update.message.reply_text(f"✅ تم رفع التقييد عن {user_id}")
    else:
        await update.message.reply_text("ارُد على رسالة الشخص")

# ====================== الردود التلقائية ======================
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    if user_id in banned_users:
        await update.message.reply_text("❌ أنت محظور من البوت")
        return
    if user_id in muted_users:
        return
    for word in blocked_words:
        if word in text:
            await update.message.reply_text("❌ كلمة محظورة!")
            return
    for key, reply in auto_replies.items():
        if key in text:
            await update.message.reply_text(reply)
            return
    await update.message.reply_text(f"رسالتك: {text}")
    log_entry = {"user": user_id, "text": text, "time": str(datetime.datetime.now())}
    save_logs(log_entry)

# ====================== إشعارات الدخول والخروج ======================
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"أهلاً بك {member.full_name} في الجروب 🎉")

async def left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.message.left_chat_member
    await update.message.reply_text(f"وداعاً {member.full_name} 👋")

# ====================== إعداد التطبيق ======================
app = ApplicationBuilder().token(TOKEN).build()

# أوامر المستخدم
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("id", id_command))

# أوامر الإدارة
app.add_handler(CommandHandler("add_owner", add_owner))
app.add_handler(CommandHandler("remove_owner", remove_owner))
app.add_handler(CommandHandler("add_admin", add_admin))
app.add_handler(CommandHandler("remove_admin", remove_admin))
app.add_handler(CommandHandler("add_creator", add_creator))
app.add_handler(CommandHandler("remove_creator", remove_creator))
app.add_handler(CommandHandler("ban", ban_user))
app.add_handler(CommandHandler("unban", unban_user))
app.add_handler(CommandHandler("mute", mute_user))
app.add_handler(CommandHandler("unmute", unmute_user))
app.add_handler(CommandHandler("kick", kick_user))
app.add_handler(CommandHandler("restrict", restrict_user))
app.add_handler(CommandHandler("unrestrict", unrestrict_user))

# الردود العامة
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))

# إشعارات الدخول والخروج
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member))

print("Bot is ready…")
app.run_polling()
