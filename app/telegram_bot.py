import aiohttp
from app.config import config
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from fastapi import APIRouter, Request

router = APIRouter()

async def send_telegram_message(chat_id: str, message: str):
    application = await setup_telegram_bot()
    await application.bot.send_message(chat_id=chat_id, text=message)

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

async def setup_telegram_bot():
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    
    # Set the webhook URL
    webhook_url = f"{config.BACKEND_URL}/telegram-webhook"
    await application.bot.set_webhook(webhook_url)
    
    return application

@router.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    application = await setup_telegram_bot()
    update = Update.de_json(await request.json(), application.bot)
    await application.process_update(update)
    return {"status": "ok"}

async def run_telegram_bot():
    application = setup_telegram_bot()
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
