import telebot
import requests
from groq import Groq
import time

BOT_TOKEN = "8308148615:AAEmQF9X5Em8Kf7nOFPo1oOzJULjCnttmRI"
GROQ_API_KEY = "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"

# 1. ቦቱን ማስነሳት
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# 2. ግጭትን ለመከላከል የድሮ ግንኙነትን ማጽዳት
try:
    bot.remove_webhook()
    print("የድሮ ግንኙነቶች ተጽድተዋል...")
    time.sleep(2)
except:
    pass

SYSTEM_PROMPT = "አንተ 'DMK Master AI' የዳንኤል ረዳት ነህ። በማንኛውም ቋንቋ መልስ ስጥ። ሰብአዊነት ይቅደም!"

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message.text}]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # 3. 'skip_pending=True' የቆዩ መልእክቶችን ችላ እንዲል ያደርጋል
    print("DMK Master AI ስራ ጀምሯል...")
    bot.infinity_polling(skip_pending=True)
    
