import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN, TIMEZONE
from database import get_db
from selector import MatchSelector
from reports import ReportBuilder
from datetime import datetime

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                user_id INTEGER PRIMARY KEY,
                active INTEGER DEFAULT 1,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    with get_db() as conn:
        conn.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))

    await update.message.reply_text(
        "👋 Bienvenue sur ton bot de pronostics **MatchBot** !\n\n"
        "Commandes disponibles :\n"
        "/today - Voir les pronostics du jour\n"
        "/help - Afficher l'aide"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **Guide d'utilisation :**\n"
        "/today - Analyse et sélectionne jusqu'à 8 matchs fiables pour aujourd'hui.\n"
        "/help - Affiche ce message d'aide."
    )

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Analyse des matchs en cours... Veuillez patienter.")

    today_str = datetime.now(TIMEZONE).strftime("%Y-%m-%d")

    try:
        selector = MatchSelector()
        result = selector.select_daily_matches(today_str)
        report = ReportBuilder.format_daily_report(today_str, result)
        await update.message.reply_text(report, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Une erreur est survenue : {e}")

def main():
    init_db()
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).read_timeout(45).connect_timeout(45).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("today", today_command))

    print("🤖 Bot démarré avec succès ! En attente de messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
