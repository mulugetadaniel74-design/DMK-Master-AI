import telebot
import os
from google import generativeai as genai

# ቁልፎቹን ከ Render Environment Variables ላይ ያነባል
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ዳንኤል! አሁን ቦቱ በደህንነት እየሰራ ነው።")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ ጌሚኒን ማግኘት አልቻልኩም።")

bot.infinity_polling()
