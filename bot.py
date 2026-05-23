from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8368872106:AAHh3HTQDbcx7CxNAnwDGUa4Sbeha1gsDjU"

ADMIN_ID = 1812185709

users = {}
waiting_male = []
waiting_female = []
active_chats = {}

main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("⚡ Find Partner")],
        [
            KeyboardButton("👧 Find Girls"),
            KeyboardButton("👦 Find Boys"),
        ],
        [
            KeyboardButton("👤 My Profile"),
            KeyboardButton("⚙️ Settings"),
        ],
        [KeyboardButton("💎 Premium")],
        [KeyboardButton("🛑 Stop Chat")],
    ],
    resize_keyboard=True,
)

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

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
        "Choose your gender:",
        reply_markup=buttons,
    )

# ================= GENDER =================

async def gender_select(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    users[user_id]["gender"] = query.data

    await query.message.reply_text(
        "🎂 Send your age:"
    )

# ================= SAVE AGE =================

async def save_age(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.effective_user.id

    if (
        user_id in users
        and users[user_id]["age"] is None
    ):

        if update.message.text.isdigit():

            users[user_id]["age"] = update.message.text

            await update.message.reply_text(
                "✅ Profile Saved",
                reply_markup=main_menu,
            )

# ================= FIND PARTNER =================

async def find_partner(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.effective_user.id

    if user_id in active_chats:

        await update.message.reply_text(
            "⚠️ Already connected."
        )

        return

    gender = users[user_id]["gender"]

    # MALE

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

    # FEMALE

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

    user_id = update.effective_user.id

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
            "🛑 Chat Ended",
            reply_markup=buttons,
        )

        await context.bot.send_message(
            partner,
            "🛑 Partner Left",
            reply_markup=buttons,
        )

# ================= PROFILE =================

async def profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.effective_user.id

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

    await update.message.reply_text(
        "💎 Premium Plans\n\n"
        "₹49 Weekly\n"
        "₹99 Monthly\n\n"
        "Benefits:\n"
        "✅ Unlimited Matching\n"
        "✅ Fast Queue\n"
        "✅ Premium Badge"
    )

# ================= SETTINGS =================

async def settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "⚙️ Settings Panel Coming Soon"
    )

# ================= CALLBACK BUTTONS =================

async def callback_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    if query.data == "like":

        await query.message.reply_text(
            "👍 Feedback Saved"
        )

    elif query.data == "dislike":

        await query.message.reply_text(
            "👎 Feedback Saved"
        )

    elif query.data == "report":

        await context.bot.send_message(
            ADMIN_ID,
            f"🚫 User Reported\n\n"
            f"User ID: {query.from_user.id}"
        )

        await query.message.reply_text(
            "✅ Report Sent"
        )

# ================= CHAT RELAY =================

async def relay(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user_id = update.effective_user.id

    # SAVE AGE

    if (
        user_id in users
        and users[user_id]["age"] is None
    ):

        await save_age(update, context)

        return

    # RELAY CHAT

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

    elif text == "🛑 Stop Chat":

        await stop_chat(update, context)

    elif text == "👧 Find Girls":

        await update.message.reply_text(
            "👧 Finding girls..."
        )

    elif text == "👦 Find Boys":

        await update.message.reply_text(
            "👦 Finding boys..."
        )

# ================= APP =================

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(
        gender_select,
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
        menu_handler,
    )
)

app.add_handler(
    MessageHandler(
        filters.ALL,
        relay,
    )
)

print("🔥 MysticChat Professional Running...")

app.run_polling()
