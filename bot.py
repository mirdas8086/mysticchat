from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8368872106:AAHh3HTQDbcx7CxNAnwDGUa4Sbeha1gsDjU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 MysticChat Working!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("🔥 Bot Running...")

app.run_polling()
