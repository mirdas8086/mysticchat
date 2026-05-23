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

waiting_male = []

waiting_female = []

active_chats = {}

# ================= MENU =================

main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("⚡ Find Partner")],
        [
            KeyboardButton("👧 Match with Girls"),
            KeyboardButton("👦 Match with Boys"),
        ],
        [
            KeyboardButton("👤 My Profile"),
            KeyboardButton("⚙️ Settings"),
        ],
        [KeyboardButton("💎 Premium")],
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

    gender = query.data

    users[user_id]["gender"] = gender

    await query.message.reply_text(
        "✅ Gender saved.\n\n"
        "Send your age now."
    )

# ================= AGE =================

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
                "✅ Profile setup completed.",
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

    if gender == "male":

        if waiting_female:

            partner = waiting_female.pop(0)

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

            waiting_male.append(user_id)

            await update.message.reply_text(
                "⏳ Waiting for girls..."
            )

    elif gender == "female":

        if waiting_male:

            partner = waiting_male.pop(0)

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

            waiting_female.append(user_id)

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

        rating_buttons = InlineKeyboardMarkup(
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
            reply_markup=rating_buttons,
        )

        await context.bot.send_message(
            partner,
            "🛑 Partner disconnected.",
            reply_markup=rating_buttons,
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
        f"👤 Your Profile\n\n"
        f"Gender: {data['gender']}\n"
        f"Age: {data['age']}\n"
        f"Premium: {premium}"
    )

# ================= PREMIUM =================

async def premium(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💎 Buy Premium",
                    url="https://t.me/",
                )
            ]
        ]
    )

    await update.message.reply_text(
        "💎 Premium Features\n\n"
        "✅ Unlimited Matches\n"
        "✅ Priority Matching\n"
        "✅ Faster Connections\n"
        "✅ Premium Badge",
        reply_markup=buttons,
    )

# ================= SETTINGS =================

async def settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "⚙️ Settings\n\n"
        "More settings coming soon."
    )

# ================= REPORT =================

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
            "✅ Report submitted."
        )

    elif query.data == "like":

        await query.message.reply_text(
            "👍 Feedback saved."
        )

    elif query.data == "dislike":

        await query.message.reply_text(
            "👎 Feedback saved."
        )

# ================= CHAT =================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.message.chat_id

    # Save Age

    if (
        user_id in users
        and users[user_id]["age"] is None
    ):

        await save_age(update, context)

        return

    # Relay Messages

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
                caption=update.message.caption,
            )

        elif update.message.video:

            await context.bot.send_video(
                partner,
                update.message.video.file_id,
                caption=update.message.caption,
            )

        elif update.message.voice:

            await context.bot.send_voice(
                partner,
                update.message.voice.file_id,
            )

# ================= BUTTON HANDLER =================

async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = update.message.text

    if text == "⚡ Find Partner":
        await find_partner(update, context)

    elif text == "👤 My Profile":
        await profile(update, context)

    elif text == "⚙️ Settings":
        await settings(update, context)

    elif text == "💎 Premium":
        await premium(update, context)

    elif text == "👧 Match with Girls":
        await update.message.reply_text(
            "👧 Girl matching enabled."
        )

    elif text == "👦 Match with Boys":
        await update.message.reply_text(
            "👦 Boy matching enabled."
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
        filters.TEXT
        & ~filters.COMMAND,
        menu_handler,
    )
)

app.add_handler(
    MessageHandler(
        filters.ALL,
        handle_message,
    )
)

print("🔥 MysticChat Advanced Running...")

app.run_polling()
