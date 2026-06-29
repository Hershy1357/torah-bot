import telebot
from data import PARSHA_DATA, DAY_NAMES, BOOKS_ORDER

BOT_TOKEN = "8527698073:AAH3ON38Qss8lsZQLso2HVkjneH_l6M2HFI"
bot = telebot.TeleBot(BOT_TOKEN)

WELCOME = """✨ *ברוך הבא!* ✨

דא קענט איר הערן די וועכנטלעכע פרשה
דורכ'ן בארימטן מגיד שיעור
*הר"ר יואל מייזליש שליט"א*

קלויב א חומש און הייב אן! 👇"""

def books_kb():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("ויקרא","שמות","בראשית")
    kb.row("דברים","במדבר")
    kb.row("🏠 היים")
    return kb

def parsha_kb(book):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    parshiyot = list(PARSHA_DATA[book].keys())
    # split into rows of 3, each row reversed
    for i in range(0, len(parshiyot), 3):
        row = parshiyot[i:i+3]
        kb.row(*reversed(row))
    kb.row("🔙 צוריק צו חומשים")
    return kb

def days_kb(book, parsha):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("שלישי","שני","ראשון")
    kb.row("שישי","חמישי","רביעי")
    kb.row("שביעי")
    if PARSHA_DATA[book][parsha].get("_pdf","TODO") != "TODO":
        kb.row("📄 PDF")
    kb.row("🔙 צוריק צו פרשיות")
    return kb

user_state = {}

@bot.message_handler(commands=['start'])
def start(msg):
    user_state[msg.chat.id] = {}
    bot.send_message(msg.chat.id, WELCOME, parse_mode="Markdown", reply_markup=books_kb())

@bot.message_handler(func=lambda m: m.text == "🏠 היים")
def go_home(msg):
    user_state[msg.chat.id] = {}
    bot.send_message(msg.chat.id, "📚 *קלויב א חומש*", parse_mode="Markdown", reply_markup=books_kb())

@bot.message_handler(func=lambda m: m.text == "🔙 צוריק צו חומשים")
def back_books(msg):
    user_state[msg.chat.id] = {}
    bot.send_message(msg.chat.id, "📚 *קלויב א חומש*", parse_mode="Markdown", reply_markup=books_kb())

@bot.message_handler(func=lambda m: m.text == "🔙 צוריק צו פרשיות")
def back_parsha(msg):
    state = user_state.get(msg.chat.id, {})
    book = state.get("book")
    if book:
        bot.send_message(msg.chat.id, f"📖 *{book}* – קלויב א פרשה", parse_mode="Markdown", reply_markup=parsha_kb(book))
    else:
        go_home(msg)

@bot.message_handler(func=lambda m: m.text and m.text in BOOKS_ORDER)
def pick_book(msg):
    user_state[msg.chat.id] = {"book": msg.text}
    bot.send_message(msg.chat.id, f"📖 *{msg.text}* – קלויב א פרשה", parse_mode="Markdown", reply_markup=parsha_kb(msg.text))

@bot.message_handler(func=lambda m: m.text and any(m.text in PARSHA_DATA[b] for b in BOOKS_ORDER))
def pick_parsha(msg):
    parsha = msg.text
    state = user_state.get(msg.chat.id, {})
    book = state.get("book")
    if not book:
        for b in BOOKS_ORDER:
            if parsha in PARSHA_DATA[b]:
                book = b
                break
    user_state[msg.chat.id] = {"book": book, "parsha": parsha}
    bot.send_message(msg.chat.id, f"📜 *פרשת {parsha}* – קלויב א טאג", parse_mode="Markdown", reply_markup=days_kb(book, parsha))

@bot.message_handler(func=lambda m: m.text and m.text in DAY_NAMES.values())
def pick_day(msg):
    state = user_state.get(msg.chat.id, {})
    book = state.get("book")
    parsha = state.get("parsha")
    if not book or not parsha:
        bot.send_message(msg.chat.id, "קלויב ערשט א פרשה", reply_markup=books_kb())
        return
    day_num = next((k for k, v in DAY_NAMES.items() if v == msg.text), None)
    fid = PARSHA_DATA[book][parsha].get(day_num, "TODO")
    if fid == "TODO":
        bot.send_message(msg.chat.id, "⏳ נאך נישט אריינגעלייגט")
    elif isinstance(fid, list):
        for i, f in enumerate(fid):
            bot.send_audio(msg.chat.id, f, caption=f"🎵 פרשת *{parsha}* – {msg.text} חלק {i+1}", parse_mode="Markdown")
    else:
        bot.send_audio(msg.chat.id, fid, caption=f"🎵 פרשת *{parsha}* – {msg.text}", parse_mode="Markdown")

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
