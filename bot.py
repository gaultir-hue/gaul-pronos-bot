from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ===== CONFIG =====
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 2102675933
ABONNES_FILE = "abonnes.txt"

# ===== CHARGER LES ABONNÉS =====
abonnes = set()
if os.path.exists(ABONNES_FILE):
    with open(ABONNES_FILE, "r") as f:
        for line in f:
            abonnes.add(int(line.strip()))

# ===== SAUVEGARDER UN ABONNÉ =====
def save_abonne(user_id):
    if user_id not in abonnes:
        abonnes.add(user_id)
        with open(ABONNES_FILE, "a") as f:
            f.write(f"{user_id}\n")

# ===== MENU PRINCIPAL =====
async def show_menu(message):
    keyboard = [
        [InlineKeyboardButton("📊 Analyses du jour", callback_data="analyses")],
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
    save_abonne(user_id)
    await show_menu(update.message)

# ===== STATS (ADMIN ONLY) =====
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Accès refusé.")
        return

    await update.message.reply_text(
        "📊 STATISTIQUES – GAUL PRONOS\n\n"
        f"👥 Abonnés : {len(abonnes)}\n"
        "🔔 Notifications : activables\n"
        "🟢 Bot : en ligne"
    )

# ===== NOTIFY (ADMIN ONLY) =====
async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    message = (
        "🔔 NOUVELLES ANALYSES DISPONIBLES 🔔\n\n"
        "📊 Les matchs du jour sont en ligne\n"
        "⚽ Sélections claires et rapides\n"
        "🎯 Approche prudente\n\n"
        "👉 Ouvre le bot et clique sur « Analyses du jour »"
    )

    for user_id in abonnes:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except:
            pass

# ===== BOUTONS =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ----- ANALYSES -----
    if query.data == "analyses":
        try:
            with open("analyses.txt", "r", encoding="utf-8") as f:
