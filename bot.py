import os
import logging
import requests
from dotenv import load_dotenv
from fuzzywuzzy import process
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Predefined anime list (expandable)
ANIME_LIST = ["Attack on Titan", "Alya Sometimes Hides Her Feelings in Russian", "Haikyuu", "Naruto Shippuden", "Dan Da Dan"]

# Function to search anime
def search_anime(query):
    best_match = process.extractOne(query, ANIME_LIST)
    if best_match and best_match[1] > 60:  # Confidence threshold
        search_query = best_match[0].replace(" ", "+")
        return f"https://anitown4u.com/search?s_keyword={search_query}", best_match[0]
    return None, None

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is live!\n\nMade With ♥️ By Soutick")

# Handle /anime command
def anime(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("⚠️ Please enter an anime name. Example: /anime naruto")
        return
    
    query = " ".join(context.args)
    update.message.reply_text("🔎 Hold on...")
    
    search_url, anime_name = search_anime(query)
    
    if search_url:
        keyboard = [[InlineKeyboardButton(anime_name, url=search_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"I found {anime_name} 👇", reply_markup=reply_markup)
    else:
        update.message.reply_text("❌ Sorry, this anime isn't available on the website. Admin will upload it soon.")

# Detecting general anime search requests
def detect_search_request(update: Update, context: CallbackContext):
    message = update.message.text.lower()
    user_id = update.message.from_user.id
    
    # Common search patterns
    search_patterns = [
    # English
    "where can i watch", "give me a link to", "is available", "watch", "where to watch", "can i watch",
    "how to watch", "send me link", "where can i find", "watch online", "stream", "download", "any link for",
    "how to stream", "give me website", "where is", "movie link", "series link", "link please", "where i get",
    
    # Hindi (written in English)
    "kaha dekh sakta hu", "kaise dekh sakte hai", "mujhe link do", "dekhne ke liye link", "online dekhna hai",
    "kahaan milega", "watch karna hai", "mujhe movie chahiye", "koi site hai", "download karne ka tarika",
    "link bhejo", "dekhna hai", "movie ka link", "dekhne ka tarika", "kaha milega", "link mil sakta hai",
    
    # Tamil (written in English)
    "enga paakalam", "epdi paakalam", "enna site", "movie link kudunga", "online pakalama", "watch panna solunga",
    "eppudi download", "yenga kidaikum", "watch panna enna website", "movie download panna mudiyuma",
    
    # Telugu (written in English)
    "ekkada chudali", "naku link ivvandi", "chudalani undi", "download cheyyali", "website peru cheppu",
    "watch cheyyali", "ekkada dorikindi", "site yedava", "stream cheyyala", "movie ekkada chudali",
    
    # Bengali (written in English)
    "kothay dekha jabe", "link dao", "ami dekhte chai", "download korbo", "online stream korte chai",
    "movie pabo kothay", "stream korar site", "watch link dao", "download link chao", "kichu pabo",
    
    # Marathi (written in English)
    "kuthe baghuy", "download kasa karaycha", "link dya", "baghayla havi", "movie kuthe milel",
    
    # Gujarati (written in English)
    "kya madse", "watch karvanu", "download link apo", "movie kyathi madse",
    
    # Malayalam (written in English)
    "evide kittum", "watch cheyyan pattumo", "movie link tharan", "site enna",
    
    # Urdu (written in English)
    "kaha dekh sakta hoon", "mujhe ye chahiye", "movie ka link batao", "kahaan milegi",
    
    # General/Informal Slang
    "link plz", "any site for", "any way to watch", "how can i get", "tell me site", "movie site link",
    "series site", "where can i find", "website for streaming", "link do", "how can i download"
]
    
    if any(pattern in message for pattern in search_patterns):
    for pattern in search_patterns:
        message = message.replace(pattern, "")
    
    query = message.strip()

        
        search_url, anime_name = search_anime(query)
        if search_url:
            keyboard = [[InlineKeyboardButton(anime_name, url=search_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f"I found {anime_name} 👇", reply_markup=reply_markup, reply_to_message_id=update.message.message_id)
        else:
            update.message.reply_text("❌ Sorry, this anime isn't available on the website. Admin will upload it soon.", reply_to_message_id=update.message.message_id)

# Main function
if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("anime", anime))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_search_request))
    
    updater.start_polling()
    updater.idle()
