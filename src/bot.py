from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Получи токен у @BotFather, вставь сюда
TOKEN = "ВСТАВЬ_ТОКЕН_СЮДА"

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Получено: {text}")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()
