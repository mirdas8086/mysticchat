from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================

TOKEN = "8368872106:AAHh3HTQDbcx7CxNAnwDGUa4Sbeha1gsDjU"

ADMIN_ID = 1812185709

# ================= DATABASE =================

users = {}

waiting_girls = []

waiting_boys = []

active_chats = {}

# ================= MENU =================

main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("⚡ Find Partner")],
        [
            KeyboardButton("👧 Find Girls"),
            KeyboardButton("👦 Find Boys"),
        ],
        [
            KeyboardButton("👤 Profile"),
            KeyboardButton("⚙️ Settings"),
        ],
        [KeyboardButton("💎 Premium")],
        [KeyboardButton("🛑 Stop Chat")],
    ],
    resize_keyboard=True,
)

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id

    if user_id not in users:

        users[user_id] = {
            "gender": None,
            "age": None,
            "premium": False,
        }

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👦 Male",
                    callback_data="male",
                ),
                InlineKeyboardButton(
                    "👧 Female",
                    callback_data="female",
                ),
            ]
        ]
    )

    await update.message.reply_text(
        "🔥 Welcome to MysticChat 🔥\n\n"
        "Select your gender:",
        reply_markup=buttons,
    )

# ================= GENDER =================

async def gender_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    user_id = query.message.chat_id

    users[user_id]["gender"] = query.data

    await query.message.reply_text(
        "🎂 Send your age:"
    )

# ================= SAVE AGE =================

async def save_age(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.message.chat_id

    if (
        user_id in users
        and users[user_id]["age"] is None
    ):

        if update.message.text.isdigit():

            users[user_id]["age"] = update.message.text

            await update.message.reply_text(
                "✅ Profile Completed",
                reply_markup=main_menu,
            )

# ================= FIND =================

async def find_partner(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.message.chat_id

    if user_id in active_chats:

        await update.message.reply_text(
            "⚠️ Already connected."
        )

        return

    gender = users[user_id]["gender"]

    # MALE

    if gender == "male":

        if waiting_girls:

            partner = waiting_girls.pop(0)

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

            waiting_boys.append(user_id)

            await update.message.reply_text(
                "⏳ Waiting for girls..."
            )

    # FEMALE

    elif gender == "female":

        if waiting_boys:

            partner = waiting_boys.pop(0)

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

            waiting_girls.append(user_id)

            await update.message.reply_text(
                "⏳ Waiting for boys..."
            )

# ================= STOP =================

async def stop_chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.message.chat_id

    if user_id in active_chats:

        partner = active_chats[user_id]

        del active_chats[user_id]
        del active_chats[partner]

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👍 Like",
                        callback_data="like",
                    ),
                    InlineKeyboardButton(
                        "👎 Dislike",
                        callback_data="dislike",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🚫 Report",
                        callback_data="report",
                    )
                ],
            ]
        )

        await context.bot.send_message(
            user_id,
            "🛑 Chat ended.",
            reply_markup=buttons,
        )

        await context.bot.send_message(
            partner,
            "🛑 Partner disconnected.",
            reply_markup=buttons,
        )

# ================= PROFILE =================

async def profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.message.chat_id

    data = users[user_id]

    premium = "Yes" if data["premium"] else "No"

    await update.message.reply_text(
        f"👤 Profile\n\n"
        f"Gender: {data['gender']}\n"
        f"Age: {data['age']}\n"
        f"Premium: {premium}"
    )

# ================= PREMIUM =================

async def premium(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "💎 Premium Plans\n\n"
        "₹49 Weekly\n"
        "₹99 Monthly\n\n"
        "Benefits:\n"
        "✅ Unlimited Matches\n"
        "✅ Faster Matching\n"
        "✅ Premium Badge"
    )

# ================= SETTINGS =================

async def settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "⚙️ Settings Coming Soon"
    )

# ================= CALLBACKS =================

async def callback_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    if query.data == "report":

        await context.bot.send_message(
            ADMIN_ID,
            f"⚠️ User Reported\n"
            f"User ID: {query.message.chat_id}"
        )

        await query.message.reply_text(
            "✅ Report Submitted"
        )

    elif query.data == "like":

        await query.message.reply_text(
            "👍 Feedback Saved"
        )

    elif query.data == "dislike":

        await query.message.reply_text(
            "👎 Feedback Saved"
        )

# ================= CHAT =================

async def relay_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.message.chat_id

    # SAVE AGE

    if (
        user_id in users
        and users[user_id]["age"] is None
    ):

        await save_age(update, context)

        return

    # RELAY

    if user_id in active_chats:

        partner = active_chats[user_id]

        if update.message.text:

            await context.bot.send_message(
                partner,
                update.message.text,
            )

        elif update.message.photo:

            await context.bot.send_photo(
                partner,
                update.message.photo[-1].file_id,
            )

        elif update.message.video:

            await context.bot.send_video(
                partner,
                update.message.video.file_id,
            )

        elif update.message.voice:

            await context.bot.send_voice(
                partner,
                update.message.voice.file_id,
            )

# ================= MENU BUTTONS =================

async def menu_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = update.message.text

    if text == "⚡ Find Partner":

        await find_partner(update, context)

    elif text == "👤 Profile":

        await profile(update, context)

    elif text == "⚙️ Settings":

        await settings(update, context)

    elif text == "💎 Premium":

        await premium(update, context)

    elif text == "🛑 Stop Chat":

        await stop_chat(update, context)

    elif text == "👧 Find Girls":

        await update.message.reply_text(
            "👧 Matching with girls..."
        )

    elif text == "👦 Find Boys":

        await update.message.reply_text(
            "👦 Matching with boys..."
        )

# ================= BOT =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(
        gender_callback,
        pattern="^(male|female)$",
    )
)

app.add_handler(
    CallbackQueryHandler(
        callback_buttons,
        pattern="^(like|dislike|report)$",
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_buttons,
    )
)

app.add_handler(
    MessageHandler(
        filters.ALL,
        relay_message,
    )
)

print("🔥 MysticChat Professional Running...")

app.run_polling()
