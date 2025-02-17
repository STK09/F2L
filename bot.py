import os
import time
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Bot Configuration
TOKEN = "7646802131:AAHNU9mpzQil2hKRz9hbPggjOoBR7q0aOlU"  # ⚠️ Keep this secret!
CLOUDFLARE_WORKER_URL = "https://drive-cdn.soutick-op.workers.dev/"

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text("Made With ♥️ By Soutick")

async def handle_document(update: Update, context: CallbackContext) -> None:
    """Handles file uploads and generates a secure download link."""
    file = update.message.document or update.message.video or (update.message.photo[-1] if update.message.photo else None)

    if not file:
        await update.message.reply_text("Unsupported file type.")
        return

    file_id = file.file_id  # Get Telegram File ID
    timestamp = int(time.time())  # Expiry time tracking

    # Generate Secure Link (Only Using `file_id`)
    cdn_link = f"{CLOUDFLARE_WORKER_URL}?file_id={file_id}&t={timestamp}"

    await update.message.reply_text(f"✅ Here is your secure link:\n\n{cdn_link}\n\n(valid for 12 hours)")

def main():
    """Start the bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # File handlers (Supports documents, videos, and photos)
    file_filter = filters.Document.ALL | filters.VIDEO | filters.PHOTO
    app.add_handler(MessageHandler(file_filter, handle_document))

    # Print message to VPS terminal
    print("Bot is running...")

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
