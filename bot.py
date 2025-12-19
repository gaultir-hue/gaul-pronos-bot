from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ===== CONFIG =====
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 2102675933

abonnes = set()

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
    abonnes.add(user_id)
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

# ===== NOTIFICATION (ADMIN ONLY) =====
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
        chemin = os.path.join(os.getcwd(), "analyses.txt")

        try:
            with open(chemin, "r", encoding="utf-8") as f:
                texte = f.read().strip()
        except:
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
            [InlineKeyboardButton(
                "🎁 COLDBET – Bonus 200%",
                url="http://coldredir.com/L?tag=d_5024553m_126632c_&site=5024553&ad=126632"
            )],
            [InlineKeyboardButton(
                "🎁 MELBET – Code 4CPR",
                url="https://refpa3665.com/L?tag=d_3939722m_66335c_&site=3939722&ad=66335"
            )],
            [InlineKeyboardButton(
                "🎁 BETWINNER – Bonus 200%",
                url="https://betwinner2.com/fr/registration?btag=d_46129m_419562c_bw_KT9AsFLZq3FWBBy768bZMV"
            )],
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
