import telebot
import os
from google import generativeai as genai

# የእነዚህን ዋጋ ከታች ባለው መመሪያ መሰረት ተካ
BOT_TOKEN = "የቴሌግራም_ቦት_ቶከንህን_እዚህ_ጥቀስ"
GEMINI_API_KEY = "የጌሚኒ_ኤፒአይ_ኪይህን_እዚህ_ጥቀስ"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ዳንኤል! እኔ ያንተ ዲጂታል ትዊን (DMK AI) ነኝ። እንዴት ልረዳህ እችላለሁ?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)

bot.infinity_polling()
