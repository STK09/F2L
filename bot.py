import os
import logging
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7646802131:AAHNU9mpzQil2hKRz9hbPggjOoBR7q0aOlU"
CLOUDFLARE_WORKER_URL = "https://drive-cdn.soutick-op.workers.dev/"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Made With ♥️ By Soutick")

async def handle_document(update: Update, context: CallbackContext) -> None:
    file = update.message.document or update.message.video or (update.message.photo[-1] if update.message.photo else None)
    
    if not file:
        await update.message.reply_text("Unsupported file type.")
        return
    
    file_id = file.file_id
    short_hash = base64.b64encode(file_id.encode()).decode()  # Encode file_id

    cdn_link = f"{CLOUDFLARE_WORKER_URL}/{short_hash}"
    await update.message.reply_text(f"✅ Here is your link:\n\n{cdn_link}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    file_filter = filters.Document.ALL | filters.VIDEO | filters.PHOTO
    app.add_handler(MessageHandler(file_filter, handle_document))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
