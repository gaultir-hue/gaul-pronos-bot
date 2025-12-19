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
    with open(ABONNES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            abonnes.add(int(line.strip()))

# ===== SAUVEGARDER UN ABONNÉ =====
def save_abonne(user_id):
    if user_id not in abonnes:
        abonnes.add(user_id)
        with open(ABONNES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{user_id}\n")

# ===== MENU PRINCIPAL =====
async def show_menu(message):
    keyboard = [
        [InlineKeyboardButton("🔐 TOP 3 SAFE", callback_data="safe")],
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

# ===== STATS (ADMIN) =====
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Accès refusé.")
        return

    await update.message.reply_text(
        "📊 STATISTIQUES – GAUL PRONOS\n\n"
        f"👥 Abonnés : {len(abonnes)}\n"
        "🟢 Bot : en ligne"
    )

# ===== NOTIFY (ADMIN) =====
async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    message = (
        "🔔 NOUVEAU TOP 3 SAFE DISPONIBLE 🔔\n\n"
        "🔐 Sélections prudentes du jour\n"
        "🎯 Gestion du risque recommandée\n\n"
        "👉 Ouvre le bot et clique sur « TOP 3 SAFE »"
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

    # ----- TOP 3 SAFE -----
    if query.data == "safe":
        try:
            with open("safe.txt", "r", encoding="utf-8") as f:
                texte = f.read().strip()
        except Exception:
            texte = "⏳ TOP 3 SAFE en cours de mise à jour."

        if not texte:
            texte = "⏳ TOP 3 SAFE non disponible."

        await query.message.reply_text(
            texte,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]]
            )
        )

    # ----- ANALYSES -----
    elif query.data == "analyses":
        try:
            with open("analyses.txt", "r", encoding="utf-8") as f:
                texte = f.read().strip()
        except Exception:
            texte = "⏳ Analyses en cours de mise à jour."

        if not texte:
            texte = "⏳ Analyses vides pour le moment."

        await query.message.reply_text(
            texte,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]]
            )
        )

    # ----- PREMIER LEAGUE -----
    elif query.data == "pl":
        await query.message.reply_text(
            "⚽ PREMIER LEAGUE\n\n"
            "• Over 2.5\n"
            "• BTTS\n"
            "• Victoires à domicile",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]]
            )
        )

    # ----- LA LIGA -----
    elif query.data == "liga":
        await query.message.reply_text(
            "🇪🇸 LA LIGA\n\n"
            "• Over 1.5\n"
            "• Under 3.5\n"
            "• Matchs tactiques",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]]
            )
        )

    # ----- BONUS -----
    elif query.data == "bonus":
        keyboard = [
            [InlineKeyboardButton("🎁 1XBET – Bonus", url="https://bit.ly/4p0ahuw")],
            [InlineKeyboardButton("🎁 COLDBET – Bonus 200%", url="http://coldredir.com/L?tag=d_5024553m_126632c_&site=5024553&ad=126632")],
            [InlineKeyboardButton("🎁 MELBET – Code 4CPR", url="https://refpa3665.com/L?tag=d_3939722m_66335c_&site=3939722&ad=66335")],
            [InlineKeyboardButton("🎁 BETWINNER – Bonus 200%", url="https://betwinner2.com/fr/registration?btag=d_46129m_419562c_bw_KT9AsFLZq3FWBBy768bZMV")],
            [InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]
        ]

        await query.message.reply_text(
            "🎁 BONUS EXCLUSIFS BOOKMAKERS\n\n"
            "💰 Jusqu’à 200% de bonus\n"
            "🎟️ Code promo : 4CPR",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ----- MENU -----
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
