from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================

TOKEN = "8368872106:AAHh3HTQDbcx7CxNAnwDGUa4Sbeha1gsDjU"

ADMIN_ID = 1812185709

# ================= DATA =================

waiting_users = []

active_chats = {}

banned_users = []

premium_users = []

user_limits = {}

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id

    if user_id in banned_users:
        return

    await update.message.reply_text(
        "🔥 Welcome to MysticChat 🔥\n\n"
        "🔍 /find - Find Partner\n"
        "⏭ /next - Next Partner\n"
        "🛑 /stop - Stop Chat\n"
        "⚠️ /report - Report User\n"
        "💎 /premium - Premium Info\n"
        "👥 /users - Admin Only"
    )

# ================= FIND =================

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id

    if user_id in banned_users:
        return

    # Daily Limit

    if user_id not in premium_users:

        if user_id not in user_limits:
            user_limits[user_id] = 0

        if user_limits[user_id] >= 200:

            await update.message.reply_text(
                "❌ Daily limit reached.\n"
                "Buy Premium for unlimited finds."
            )

            return

        user_limits[user_id] += 1

    # Already Connected

    if user_id in active_chats:

        await update.message.reply_text(
            "⚠️ Already connected."
        )

        return

    # Match User

    if waiting_users and waiting_users[0] != user_id:

        partner = waiting_users.pop(0)

        active_chats[user_id] = partner
        active_chats[partner] = user_id

        await context.bot.send_message(
            user_id,
            "✅ Connected anonymously."
        )

        await context.bot.send_message(
            partner,
            "✅ Connected anonymously."
        )

    else:

        if user_id not in waiting_users:

            waiting_users.append(user_id)

        await update.message.reply_text(
            "⏳ Waiting for partner..."
        )

# ================= STOP =================

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id

    if user_id in active_chats:

        partner = active_chats[user_id]

        del active_chats[user_id]
        del active_chats[partner]

        await context.bot.send_message(
            user_id,
            "🛑 Chat ended."
        )

        await context.bot.send_message(
            partner,
            "🛑 Partner disconnected."
        )

# ================= NEXT =================

async def next_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await stop(update, context)

    await find(update, context)

# ================= REPORT =================

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id

    if user_id in active_chats:

        partner = active_chats[user_id]

        await context.bot.send_message(
            ADMIN_ID,
            f"⚠️ USER REPORT\n\n"
            f"Reporter ID: {user_id}\n"
            f"Reported ID: {partner}"
        )

        await update.message.reply_text(
            "✅ Report submitted."
        )

# ================= PREMIUM =================

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💎 Premium Plans 💎\n\n"
        "₹49 - Weekly\n"
        "₹99 - Monthly\n\n"
        "Benefits:\n"
        "✅ Unlimited Finds\n"
        "✅ Priority Matching\n"
        "✅ Faster Connections"
    )

# ================= ADMIN USERS =================

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat_id == ADMIN_ID:

        total = len(waiting_users) + len(active_chats)

        await update.message.reply_text(
            f"👥 Total Users: {total}"
        )

# ================= BAN =================

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat_id != ADMIN_ID:
        return

    try:

        uid = int(context.args[0])

        banned_users.append(uid)

        await update.message.reply_text(
            "✅ User banned."
        )

    except:

        await update.message.reply_text(
            "/ban USER_ID"
        )

# ================= MESSAGE =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id

    if user_id in active_chats:

        partner = active_chats[user_id]

        # TEXT

        if update.message.text:

            await context.bot.send_message(
                partner,
                update.message.text
            )

        # PHOTO

        elif update.message.photo:

            await context.bot.send_photo(
                partner,
                update.message.photo[-1].file_id,
                caption=update.message.caption
            )

        # VIDEO

        elif update.message.video:

            await context.bot.send_video(
                partner,
                update.message.video.file_id,
                caption=update.message.caption
            )

        # VOICE

        elif update.message.voice:

            await context.bot.send_voice(
                partner,
                update.message.voice.file_id
            )

# ================= BOT =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("find", find))

app.add_handler(CommandHandler("stop", stop))

app.add_handler(CommandHandler("next", next_chat))

app.add_handler(CommandHandler("report", report))

app.add_handler(CommandHandler("premium", premium))

app.add_handler(CommandHandler("users", users))

app.add_handler(CommandHandler("ban", ban))

app.add_handler(
    MessageHandler(
        filters.TEXT
        | filters.PHOTO
        | filters.VIDEO
        | filters.VOICE,
        handle_message
    )
)

print("🔥 MysticChat Running...")

app.run_polling()
