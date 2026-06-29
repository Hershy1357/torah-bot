"""
helper_bot.py  –  העבר אליו כל קובץ מהערוץ וקבל את ה file_id
הרץ אותו רק בזמן שאתה ממלא את data.py – אחר כך אפשר להפסיק
"""
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg.audio:
        fid = msg.audio.file_id
        name = msg.audio.file_name or msg.audio.title or "audio"
        await msg.reply_text(f"🎵 *{name}*\n\n`{fid}`", parse_mode="Markdown")
    elif msg.document:
        fid = msg.document.file_id
        name = msg.document.file_name or "document"
        await msg.reply_text(f"📄 *{name}*\n\n`{fid}`", parse_mode="Markdown")
    elif msg.voice:
        fid = msg.voice.file_id
        await msg.reply_text(f"🎤 voice\n\n`{fid}`", parse_mode="Markdown")
    else:
        await msg.reply_text("❌ שלח אודיו או PDF בלבד")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, get_file_id))
    print("Helper bot running – forward files to get their file_id")
    app.run_polling()

if __name__ == "__main__":
    main()
