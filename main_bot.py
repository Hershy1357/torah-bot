import telebot
from data import PARSHA_DATA, DAY_NAMES, BOOKS_ORDER

BOT_TOKEN = "8527698073:AAH3ON38Qss8lsZQLso2HVkjneH_l6M2HFI"
bot = telebot.TeleBot(BOT_TOKEN)

def books_keyboard():
    kb = telebot.types.InlineKeyboardMarkup()
    for book in BOOKS_ORDER:
        kb.add(telebot.types.InlineKeyboardButton(f"📖 {book}", callback_data=f"book|{book}"))
    return kb

def parsha_keyboard(book):
    kb = telebot.types.InlineKeyboardMarkup()
    for p in PARSHA_DATA[book]:
        kb.add(telebot.types.InlineKeyboardButton(f"📜 {p}", callback_data=f"parsha|{book}|{p}"))
    kb.add(telebot.types.InlineKeyboardButton("🔙 צוריק", callback_data="home"))
    return kb

def days_keyboard(book, parsha):
    kb = telebot.types.InlineKeyboardMarkup(row_width=3)
    btns = [telebot.types.InlineKeyboardButton(f"🎵 {DAY_NAMES[d]}", callback_data=f"day|{book}|{parsha}|{d}") for d in range(1,8)]
    kb.add(*btns)
    if PARSHA_DATA[book][parsha].get("_pdf","TODO") != "TODO":
        kb.add(telebot.types.InlineKeyboardButton("📄 PDF", callback_data=f"pdf|{book}|{parsha}"))
    kb.add(telebot.types.InlineKeyboardButton("🔙 צוריק", callback_data=f"book|{book}"))
    return kb

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "📚 *קלויב א חומש*", parse_mode="Markdown", reply_markup=books_keyboard())

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    d = c.data
    if d == "home":
        bot.edit_message_text("📚 *קלויב א חומש*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=books_keyboard())
    elif d.startswith("book|"):
        book = d.split("|")[1]
        bot.edit_message_text(f"📖 *{book}* – קלויב א פרשה", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=parsha_keyboard(book))
    elif d.startswith("parsha|"):
        _, book, parsha = d.split("|")
        bot.edit_message_text(f"📜 *פרשת {parsha}* – קלויב א טאג", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=days_keyboard(book, parsha))
    elif d.startswith("day|"):
        _, book, parsha, day = d.split("|")
        fid = PARSHA_DATA[book][parsha].get(int(day), "TODO")
        back = telebot.types.InlineKeyboardMarkup()
        back.add(telebot.types.InlineKeyboardButton("🔙 צוריק", callback_data=f"parsha|{book}|{parsha}"))
        if fid == "TODO":
            bot.edit_message_text("⏳ נאך נישט אריינגעלייגט", c.message.chat.id, c.message.message_id, reply_markup=back)
        elif isinstance(fid, list):
            # 2 parts — send both
            for i, f in enumerate(fid):
                bot.send_audio(c.message.chat.id, f, caption=f"🎵 פרשת *{parsha}* – {DAY_NAMES[int(day)]} חלק {i+1}", parse_mode="Markdown")
        else:
            bot.send_audio(c.message.chat.id, fid, caption=f"🎵 פרשת *{parsha}* – {DAY_NAMES[int(day)]}", parse_mode="Markdown")
    elif d.startswith("pdf|"):
        _, book, parsha = d.split("|")
        fid = PARSHA_DATA[book][parsha].get("_pdf","TODO")
        back = telebot.types.InlineKeyboardMarkup()
        back.add(telebot.types.InlineKeyboardButton("🔙 צוריק", callback_data=f"parsha|{book}|{parsha}"))
        if fid == "TODO":
            bot.edit_message_text("⏳ נאך נישט אריינגעלייגט", c.message.chat.id, c.message.message_id, reply_markup=back)
        else:
            bot.send_document(c.message.chat.id, fid, caption=f"📄 פרשת *{parsha}*", parse_mode="Markdown")
    bot.answer_callback_query(c.id)

print("Bot running!")
bot.infinity_polling()
