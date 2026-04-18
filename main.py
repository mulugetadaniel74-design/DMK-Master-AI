import telebot
import os
from google import generativeai as genai

# የአንተ ትክክለኛ ቁልፎች እዚህ ገብተዋል
BOT_TOKEN = "8308148615:AAHQdiHJaHarq5zaM2AiORKh26mh-F_dUTM"
GEMINI_API_KEY = "AIzaSyCV1PBixf6WIjzRk0smbL8Cw0d5r_LaOE4"

# ጌሚኒን ማዘጋጀት
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ዳንኤል! አዲሱ ቁልፍ (API Key) ገብቷል። አሁን በደንብ መስራት አለበት፣ ሞክረኝ!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ለጌሚኒ ጥያቄውን መላክ
        response = model.generate_content(message.text)
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ጌሚኒ መልስ ማመንጨት አልቻለም። ድጋሚ ሞክር።")
            
    except Exception as e:
        error_info = str(e)
        print(f"ERROR: {error_info}")
        # ለተጠቃሚው የሚሰጥ መልስ
        bot.reply_to(message, f"ስህተት ተፈጥሯል! (API Key ችግር ሊሆን ይችላል)።")

bot.infinity_polling()
