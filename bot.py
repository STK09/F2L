import os
import time
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Get bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")
CLOUDFLARE_WORKER_URL = "https://drive-cdn.soutick-op.workers.dev/"

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text("Made With ♥️ By Soutick")

async def handle_document(update: Update, context: CallbackContext) -> None:
    """Handle file uploads and generate a temporary download link."""
    file = update.message.document or update.message.video or (update.message.photo[-1] if update.message.photo else None)
    
    if not file:
        await update.message.reply_text("Unsupported file type.")
        return
    
    file_id = file.file_id
    file_info = await context.bot.get_file(file_id)
    file_path = file_info.file_path

    # Generate a timestamp (current time) to track expiration
    timestamp = int(time.time())  
    cdn_link = f"{CLOUDFLARE_WORKER_URL}?file={file_path}&t={timestamp}"

    await update.message.reply_text(f"✅ Here is your link\n\n{cdn_link}\n\n(valid for 12 hours)")

def main():
    """Start the bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # File handlers (Corrected filter syntax)
    file_filter = filters.Document.ALL | filters.VIDEO | filters.PHOTO
    app.add_handler(MessageHandler(file_filter, handle_document))

    # Print message to VPS terminal
    print("Bot is running...")

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
