import telebot
from groq import Groq
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# 1. 'Conflict' ለመፍታት የቆየ ግንኙነትን በሃይል ማጽዳት
print("የቆየ ግንኙነትን በማጽዳት ላይ...")
try:
    bot.remove_webhook()
    time.sleep(3) # ቦቱ እንዲረጋጋ 3 ሰከንድ መስጠት
except:
    pass

SYSTEM_INSTRUCTION = "አንተ 'DMK Master AI' የዳንኤል ረዳት ነህ። በአጭር አማርኛ መልስ ስጥ። ሰብአዊነት ይቅደም!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": message.text},
            ],
            model="llama3-8b-8192",
        )
        bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("DMK Master AI ስራ ጀምሯል...")
    # 2. skip_pending=True የቀድሞ መልእክቶችን እንዳያነብ ያደርጋል
    bot.infinity_polling(skip_pending=True)
    
