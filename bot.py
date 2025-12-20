from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import sqlite3
from datetime import datetime, timedelta

# ===== CONFIG =====
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 2102675933
DB_PATH = "data.db"

# ===== INIT DB =====
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_seen TEXT,
    last_seen TEXT
)
""")
conn.commit()

# ===== USER TRACKING =====
def track_user(user_id: int):
    now = datetime.utcnow().isoformat()

    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "UPDATE users SET last_seen = ? WHERE user_id = ?",
            (now, user_id)
        )
    else:
        cursor.execute(
            "INSERT INTO users (user_id, first_seen, last_seen) VALUES (?, ?, ?)",
            (user_id, now, now)
        )

    conn.commit()

# ===== MENU =====
async def show_menu(message):
    keyboard = [
        [InlineKeyboardButton("📊 Analyses du jour", callback_data="analyses")],
        [InlineKeyboardButton("🔐 TOP 3 SAFE", callback_data="safe")],
        [InlineKeyboardButton("⚽ Premier League", callback_data="pl")],
        [InlineKeyboardButton("🇪🇸 La Liga", callback_data="liga")],
        [InlineKeyboardButton("🎁 Bonus Bookmakers", callback_data="bonus")],
        [InlineKeyboardButton(
            "📢 Rejoindre le canal Telegram",
            url="https://t.me/+YGvGtfdm6xFjMDdk"
        )]
    ]

    await message.reply_text(
        "🏠 MENU PRINCIPAL\n\n👇 Choisis une option :",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    track_user(user_id)
    await show_menu(update.message)

# ===== STATS (ADMIN) =====
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Accès refusé.")
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]

    limit_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE last_seen >= ?",
        (limit_date,)
    )
    mau = cursor.fetchone()[0]

    await update.message.reply_text(
        "📊 STATISTIQUES – GAUL PRONOS\n\n"
        f"👥 Abonnés totaux : {total}\n"
        f"📆 Actifs (30j) : {mau}\n"
        "🟢 Bot : en ligne"
    )

# ===== NOTIFY (ADMIN) =====
async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    message = (
        "🔔 NOUVELLES ANALYSES DISPONIBLES 🔔\n\n"
        "🔐 TOP 3 SAFE du jour en ligne\n"
        "📊 Analyses mises à jour\n\n"
        "👉 Ouvre le bot maintenant"
    )

    for (user_id,) in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except:
            pass

# ===== BUTTONS =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    track_user(query.from_user.id)

    def back():
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]]
        )

    if query.data == "analyses":
        try:
            with open("analyses.txt", "r", encoding="utf-8") as f:
                text = f.read().strip()
        except:
            text = "⏳ Analyses en cours de mise à jour."

        await query.message.reply_text(text, reply_markup=back())

    elif query.data == "safe":
        try:
            with open("safe.txt", "r", encoding="utf-8") as f:
                text = f.read().strip()
        except:
            text = "⏳ TOP 3 SAFE en préparation."

        await query.message.reply_text(text, reply_markup=back())

    elif query.data == "pl":
        await query.message.reply_text(
            "⚽ PREMIER LEAGUE\n\n• Over 2.5\n• BTTS\n• Victoires à domicile",
            reply_markup=back()
        )

    elif query.data == "liga":
        await query.message.reply_text(
            "🇪🇸 LA LIGA\n\n• Over 1.5\n• Under 3.5\n• Matchs tactiques",
            reply_markup=back()
        )

    elif query.data == "bonus":
        keyboard = [
            [InlineKeyboardButton("🎁 1XBET", url="https://bit.ly/4p0ahuw")],
            [InlineKeyboardButton("🎁 MELBET", url="https://refpa3665.com/L?tag=d_3939722m_66335c_&site=3939722&ad=66335")],
            [InlineKeyboardButton("🎁 BETWINNER", url="https://betwinner2.com/fr/registration?btag=d_46129m_419562c_bw_KT9AsFLZq3FWBBy768bZMV")],
            [InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]
        ]
        await query.message.reply_text(
            "🎁 BONUS BOOKMAKERS",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "menu":
        await show_menu(query.message)

# ===== APP =====
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("notify", notify))
app.add_handler(CallbackQueryHandler(buttons))

print("🤖 Bot en ligne...")
app.run_polling()
