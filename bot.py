import os
import time
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")  # Get token from environment variables
CLOUDFLARE_WORKER_URL = "https://drive-cdn.soutick-op.workers.dev/"

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the user starts the bot."""
    update.message.reply_text("Made With ♥️ By Soutick")

def handle_document(update: Update, context: CallbackContext) -> None:
    """Handle file uploads and generate a temporary download link."""
    file = update.message.document or update.message.video or update.message.photo[-1] if update.message.photo else None
    
    if not file:
        update.message.reply_text("Unsupported file type.")
        return
    
    file_id = file.file_id
    file_info = context.bot.get_file(file_id)
    file_path = file_info.file_path

    # Generate a timestamp (current time) to track expiration
    timestamp = int(time.time())  
    cdn_link = f"{CLOUDFLARE_WORKER_URL}?file={file_path}&t={timestamp}"

    update.message.reply_text(f"✅ Here is your link\n\n{cdn_link}\n\n(valid for 12 hours):")

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))

    # File handlers
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.photo, handle_document))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
