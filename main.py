import telebot
import requests
from groq import Groq
import os
import time

# አዲሱ የቴሌግራም ቁልፍ
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ግጭትን ለመከላከል
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

SYSTEM_PROMPT = "አንተ 'DMK Master AI' የዳንኤል ረዳት ነህ። በማንኛውም ቋንቋ መልስ ስጥ። ሰብአዊነት ይቅደም!"

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message.text}]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": [{"type": "text", "text": "ይህንን ፎቶ አብራራ።"}, {"type": "image_url", "image_url": {"url": image_url}}]}]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except:
        bot.reply_to(message, "ፎቶውን ማየት አልቻልኩም።")

if __name__ == "__main__":
    print("ቦቱ ስራ ጀምሯል...")
    bot.infinity_polling(skip_pending=True)
    
