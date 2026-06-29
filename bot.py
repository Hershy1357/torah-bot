import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from data import PARSHA_DATA, DAY_NAMES, BOOKS_ORDER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

def make_keyboard(buttons):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data=data) for label, data in row]
        for row in buttons
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_books(update, context)

async def show_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[( f"📖 {book}", f"book|{book}")] for book in BOOKS_ORDER]
    buttons.append([("🏠 היים", "home")])
    kb = make_keyboard(buttons)
    text = "📚 *קלויב א חומש*"
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await show_books(update, context)

    elif data.startswith("book|"):
        book = data.split("|", 1)[1]
        parshiyot = list(PARSHA_DATA[book].keys())
        buttons = [[(f"📜 {p}", f"parsha|{book}|{p}")] for p in parshiyot]
        buttons.append([("🔙 צוריק", "home")])
        await query.edit_message_text(
            f"📖 *{book}* – קלויב א פרשה",
            parse_mode="Markdown",
            reply_markup=make_keyboard(buttons),
        )

    elif data.startswith("parsha|"):
        _, book, parsha = data.split("|", 2)
        day_buttons = [
            [(f"🎵 {DAY_NAMES[d]}", f"day|{book}|{parsha}|{d}") for d in range(1, 4)],
            [(f"🎵 {DAY_NAMES[d]}", f"day|{book}|{parsha}|{d}") for d in range(4, 8)],
        ]
        pdf_id = PARSHA_DATA[book][parsha].get("_pdf", "TODO")
        if pdf_id != "TODO":
            day_buttons.append([("📄 PDF – חומש עטרת רש״י", f"pdf|{book}|{parsha}")])
        day_buttons.append([("🔙 צוריק", f"book|{book}")])
        await query.edit_message_text(
            f"📜 *פרשת {parsha}* – קלויב א טאג",
            parse_mode="Markdown",
            reply_markup=make_keyboard(day_buttons),
        )

    elif data.startswith("day|"):
        _, book, parsha, day_str = data.split("|", 3)
        day = int(day_str)
        file_id = PARSHA_DATA[book][parsha].get(day, "TODO")
        back_cb = f"parsha|{book}|{parsha}"
        if file_id == "TODO":
            await query.edit_message_text(
                f"⏳ דער שיעור פון *{DAY_NAMES[day]}* אין פרשת *{parsha}* איז נאך נישט אריינגעלייגט געווארן.\nקום שפעטער צוריק!",
                parse_mode="Markdown",
                reply_markup=make_keyboard([[(("🔙 צוריק", back_cb))]]),
            )
        else:
            await query.message.reply_audio(
                audio=file_id,
                caption=f"🎵 פרשת *{parsha}* – {DAY_NAMES[day]}",
                parse_mode="Markdown",
            )
            await query.edit_message_reply_markup(
                reply_markup=make_keyboard([[("🔙 צוריק", back_cb)]])
            )

    elif data.startswith("pdf|"):
        _, book, parsha = data.split("|", 2)
        file_id = PARSHA_DATA[book][parsha].get("_pdf", "TODO")
        back_cb = f"parsha|{book}|{parsha}"
        if file_id == "TODO":
            await query.edit_message_text(
                f"⏳ דער PDF פון פרשת *{parsha}* איז נאך נישט אריינגעלייגט.\nקום שפעטער צוריק!",
                parse_mode="Markdown",
                reply_markup=make_keyboard([[("🔙 צוריק", back_cb)]]),
            )
        else:
            await query.message.reply_document(
                document=file_id,
                caption=f"📄 חומש עטרת רש״י – פרשת *{parsha}*",
                parse_mode="Markdown",
            )
            await query.edit_message_reply_markup(
                reply_markup=make_keyboard([[("🔙 צוריק", back_cb)]])
            )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
