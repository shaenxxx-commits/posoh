import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import whisper

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан. Выполни: export TELEGRAM_BOT_TOKEN=...")

# Загружаем модель один раз при старте
model = whisper.load_model("small")

STREAM_PATH = "/home/shaen/sub0/stream.md"
MEDIA_DIR = "/home/shaen/sub0/media"

os.makedirs(MEDIA_DIR, exist_ok=True)

def append_stream(timestamp: str, source: str, content: str, media: str = None):
    block = f"\n## {timestamp}\n\n**source:** {source}\n"
    if media:
        block += f"**media:** {media}\n"
    block += f"**content:** {content}\n\n---\n"
    with open(STREAM_PATH, "a", encoding="utf-8") as f:
        f.write(block)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = update.message.text or ""
    append_stream(ts, "telegram_text", text)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_dir = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(os.path.join(MEDIA_DIR, date_dir), exist_ok=True)

    voice_file = await update.message.voice.get_file()
    ogg_path = os.path.join(MEDIA_DIR, date_dir, f"voice_{ts.replace(':', '')}.ogg")
    await voice_file.download_to_drive(ogg_path)

    # Транскрипция
    result = model.transcribe(ogg_path, language="ru")
    transcript = result["text"].strip()

    append_stream(ts, "telegram_voice", transcript, media=ogg_path)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_dir = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(os.path.join(MEDIA_DIR, date_dir), exist_ok=True)

    photo = update.message.photo[-1]  # максимальное качество
    photo_file = await photo.get_file()
    jpg_path = os.path.join(MEDIA_DIR, date_dir, f"photo_{ts.replace(':', '')}.jpg")
    await photo_file.download_to_drive(jpg_path)

    append_stream(ts, "telegram_photo", "Получено фото", media=jpg_path)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
