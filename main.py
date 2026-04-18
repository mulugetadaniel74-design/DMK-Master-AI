import telebot
import os
from google import generativeai as genai

# የአንተ ቁልፎች እዚህ ገብተዋል
BOT_TOKEN = "8308148615:AAHQdiHJaHarq5zaM2AiORKh26mh-F_dUTM"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ዳንኤል! የዲኤምኬ Master AI ዝግጁ ነው። ምን ልርዳህ?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ ጌሚኒ መልስ ለመስጠት ተቸግሯል።")

bot.infinity_polling()
