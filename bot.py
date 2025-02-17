import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Set bot token
TOKEN = "7646802131:AAHNU9mpzQil2hKRz9hbPggjOoBR7q0aOlU"
CLOUDFLARE_WORKER_URL = "https://drive-cdn.soutick-op.workers.dev/"

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text("Made With ♥️ By Soutick")

async def handle_document(update: Update, context: CallbackContext) -> None:
    """Handle file uploads and generate a CDN link."""
    file = update.message.document or update.message.video or (update.message.photo[-1] if update.message.photo else None)
    
    if not file:
        await update.message.reply_text("❌ Unsupported file type.")
        return
    
    file_id = file.file_id

    # Generate the CDN link
    cdn_link = f"{CLOUDFLARE_WORKER_URL}/?file_id={file_id}"

    await update.message.reply_text(f"✅ Here is your download link:\n\n{cdn_link}")

def main():
    """Start the bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # File handlers
    file_filter = filters.Document.ALL | filters.VIDEO | filters.PHOTO
    app.add_handler(MessageHandler(file_filter, handle_document))

    # Print message to VPS terminal
    print("🚀 Bot is running...")

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
