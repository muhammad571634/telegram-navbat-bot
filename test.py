



import os
TOKEN = "8168421097:AAHZk5Uj_F0gPMdQXmR7NYXBxLPzjTKN5aY"

import os
import json
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    
    filters,
)


DATA_FILE = "queue.json"
ADMIN_ID = 877966378  # BU YERGA O‘ZINGNING TELEGRAM ID’ingni YOZ


def load_queue():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_queue():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False)


queue = load_queue()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishlayapti")


async def navbat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(
        "📞 Iltimos, telefon raqamingizni yuboring:",
        reply_markup=reply_markup,
    )


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    name = update.effective_user.first_name
    phone = contact.phone_number

    queue.append(f"{len(queue) + 1}. {name} — {phone}")
    save_queue()

    await update.message.reply_text(
        f"✅ Navbatga qo‘shildingiz!\n"
        f"👤 Ism: {name}\n"
        f"📞 Telefon: {phone}\n"
        f"🔢 Raqamingiz: {len(queue)}"
    )


async def list_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz admin emassiz")
        return

    if not queue:
        await update.message.reply_text("📭 Navbat bo‘sh")
        return

    text = "📋 NAVBAT RO‘YXATI:\n\n" + "\n".join(queue)
    await update.message.reply_text(text)


async def next_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz admin emassiz")
        return

    if not queue:
        await update.message.reply_text("📭 Navbat bo‘sh")
        return

    current = queue.pop(0)
    save_queue()
    await update.message.reply_text(f"➡️ Keyingi mijoz:\n{current}")


async def clear_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz admin emassiz")
        return

    queue.clear()
    save_queue()
    await update.message.reply_text("🧹 Navbat tozalandi")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("navbat", navbat))
app.add_handler(CommandHandler("list", list_queue))
app.add_handler(CommandHandler("next", next_user))
app.add_handler(CommandHandler("clear", clear_queue))
app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

app.run_polling()

