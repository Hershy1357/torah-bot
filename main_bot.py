import telebot
from data import PARSHA_DATA, DAY_NAMES, BOOKS_ORDER

BOT_TOKEN = "8527698073:AAH3ON38Qss8lsZQLso2HVkjneH_l6M2HFI"
bot = telebot.TeleBot(BOT_TOKEN)

WELCOME = """✨ *ברוך הבא!* ✨

דא קענט איר הערן די וועכנטלעכע פרשה
דורכ'ן בארימטן מגיד שיעור
*הר"ר יואל מייזליש שליט"א*

קלויב א חומש און הייב אן! 👇"""

def books_reply_kb():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(telebot.types.KeyboardButton("🏠 היים"))
    kb.add(*[telebot.types.KeyboardButton(f"📖 {b}") for b in BOOKS_ORDER])
    return kb

def parsha_reply_kb(book):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(telebot.types.KeyboardButton("🔙 צוריק צו חומשים"))
    parshiyot = list(PARSHA_DATA[book].keys())
    kb.add(*[telebot.types.KeyboardButton(f"📜 {p}") for p in parshiyot])
    return kb

def days_reply_kb(book, parsha):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.add(telebot.types.KeyboardButton("🔙 צוריק צו פרשיות"))
    kb.add(*[telebot.types.KeyboardButton(f"🎵 {DAY_NAMES[d]}") for d in range(1,8)])
    if PARSHA_DATA[book][parsha].get("_pdf","TODO") != "TODO":
        kb.add(telebot.types.KeyboardButton("📄 PDF"))
    return kb

user_state = {}

@bot.message_handler(commands=['start'])
def start(msg):
    user_state[msg.chat.id] = {}
    bot.send_message(msg.chat.id, WELCOME, parse_mode="Markdown", reply_markup=books_reply_kb())

@bot.message_handler(func=lambda m: m.text == "🏠 היים")
def go_home(msg):
    user_state[msg.chat.id] = {}
    bot.send_message(msg.chat.id, "📚 *קלויב א חומש*", parse_mode="Markdown", reply_markup=books_reply_kb())

@bot.message_handler(func=lambda m: m.text == "🔙 צוריק צו חומשים")
def back_to_books(msg):
    user_state[msg.chat.id] = {}
    bot.send_message(msg.chat.id, "📚 *קלויב א חומש*", parse_mode="Markdown", reply_markup=books_reply_kb())

@bot.message_handler(func=lambda m: m.text == "🔙 צוריק צו פרשיות")
def back_to_parsha(msg):
    state = user_state.get(msg.chat.id, {})
    book = state.get("book")
    if book:
        bot.send_message(msg.chat.id, f"📖 *{book}* – קלויב א פרשה", parse_mode="Markdown", reply_markup=parsha_reply_kb(book))
    else:
        go_home(msg)

@bot.message_handler(func=lambda m: m.text and any(f"📖 {b}" == m.text for b in BOOKS_ORDER))
def pick_book(msg):
    book = msg.text.replace("📖 ", "")
    user_state[msg.chat.id] = {"book": book}
    bot.send_message(msg.chat.id, f"📖 *{book}* – קלויב א פרשה", parse_mode="Markdown", reply_markup=parsha_reply_kb(book))

@bot.message_handler(func=lambda m: m.text and m.text.startswith("📜 "))
def pick_parsha(msg):
    parsha = msg.text.replace("📜 ", "")
    book = None
    for b in BOOKS_ORDER:
        if parsha in PARSHA_DATA[b]:
            book = b
            break
    if not book:
        return
    user_state[msg.chat.id] = {"book": book, "parsha": parsha}
    bot.send_message(msg.chat.id, f"📜 *פרשת {parsha}* – קלויב א טאג", parse_mode="Markdown", reply_markup=days_reply_kb(book, parsha))

@bot.message_handler(func=lambda m: m.text and m.text.startswith("🎵 "))
def pick_day(msg):
    state = user_state.get(msg.chat.id, {})
    book = state.get("book")
    parsha = state.get("parsha")
    if not book or not parsha:
        return
    day_name = msg.text.replace("🎵 ", "")
    day_num = next((k for k, v in DAY_NAMES.items() if v == day_name), None)
    if not day_num:
        return
    fid = PARSHA_DATA[book][parsha].get(day_num, "TODO")
    if fid == "TODO":
        bot.send_message(msg.chat.id, "⏳ נאך נישט אריינגעלייגט")
    elif isinstance(fid, list):
        for i, f in enumerate(fid):
            bot.send_audio(msg.chat.id, f, caption=f"🎵 פרשת *{parsha}* – {day_name} חלק {i+1}", parse_mode="Markdown")
    else:
        bot.send_audio(msg.chat.id, fid, caption=f"🎵 פרשת *{parsha}* – {day_name}", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📄 PDF")
def pick_pdf(msg):
    state = user_state.get(msg.chat.id, {})
    book = state.get("book")
    parsha = state.get("parsha")
    if not book or not parsha:
        return
    fid = PARSHA_DATA[book][parsha].get("_pdf", "TODO")
    if fid == "TODO":
        bot.send_message(msg.chat.id, "⏳ נאך נישט אריינגעלייגט")
    else:
        bot.send_document(msg.chat.id, fid, caption=f"📄 חומש עטרת רש״י – פרשת *{parsha}*", parse_mode="Markdown")

print("Bot running!")
bot.infinity_polling()
