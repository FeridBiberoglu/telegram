import aiohttp
from config import config
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def send_telegram_message(chat_id: str, message: str):
    bot_token = config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={'chat_id': chat_id, 'text': message}) as response:
            return await response.json()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Welcome to ProfitSniffer! 🚀\n\n"
        "We're here to help you spot profitable crypto opportunities with ease. Here's what you can do:\n\n"
        "🔎 Set Filters – Customize alerts to match your trading strategy.\n"
        "📊 View Tokens – Check out tokens that meet your criteria.\n"
        "📱 App – Access the full ProfitSniffer experience through our app!\n\n"
        "Ready to get started? Set your filters and let us sniff out profit opportunities for you!"
    )
    await update.message.reply_text(welcome_message)

def setup_telegram_bot():
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    return application

async def run_telegram_bot():
    application = setup_telegram_bot()
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
