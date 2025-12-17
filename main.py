from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت
TOKEN = "8517776533:AAEgwzqn4EtkIZtAhpi33LU9EMqDk3KHpCc"

# قائمة الحظر
banned_users = []

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! البوت شغال 🔥")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "أوامر البوت:\n"
    msg += "/ban [رد على رسالة] - حظر عضو\n"
    msg += "/unban [رد على رسالة] - رفع الحظر\n"
    msg += "/id - يظهرلك رقمك\n"
    await update.message.reply_text(msg)

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"رقمك: {user_id}")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("ارُد على رسالة الشخص اللي عايز تحظره")
        return
    user_id = update.message.reply_to_message.from_user.id
    banned_users.append(user_id)
    await update.message.reply_text(f"تم حظر {user_id}")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("ارُد على رسالة الشخص اللي عايز ترفع عنه الحظر")
        return
    user_id = update.message.reply_to_message.from_user.id
    if user_id in banned_users:
        banned_users.remove(user_id)
        await update.message.reply_text(f"تم رفع الحظر عن {user_id}")
    else:
        await update.message.reply_text("الشخص مش محظور أصلاً")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        await update.message.reply_text("أنت محظور من البوت ❌")
        return
    await update.message.reply_text(f"رسالتك: {update.message.text}")

# إنشاء التطبيق
app = ApplicationBuilder().token(TOKEN).build()

# إضافة الأوامر
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("id", id_command))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

print("Bot is running...")
app.run_polling()