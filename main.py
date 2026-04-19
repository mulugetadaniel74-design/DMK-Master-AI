import telebot
from groq import Groq
import time
import os

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GROQ_API_KEY = "Gsk_IB92f00vPOOXJzOcHdw4WGdyb3FYDrMiSLEQoEST6sn8o1bNkmFe"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# 1. ግጭትን (Conflict) ለመፍታት የቀድሞ ግንኙነትን ማጽዳት
print("የድሮ ግንኙነትን በማጽዳት ላይ...")
bot.remove_webhook()
time.sleep(2) # ቦቱ እንዲረጋጋ ትንሽ ሰከንድ መስጠት

# ያንተ ማንነት መመሪያ
SYSTEM_INSTRUCTION = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ ረዳት ነህ። 
የዳንኤል መርህ 'ሰብአዊነት ይቅደም' ነው። 
በአጭር አማርኛ ብቻ መልስ ስጥ።
"""

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
        # በግጭት ምክንያት መልስ ካልመጣ ድጋሚ እንዲሞክር
        pass

if __name__ == "__main__":
    print("DMK Master AI ስራ ጀምሯል...")
    # 2. skip_pending=True የቀድሞ መልእክቶችን እንዳያነብ ያደርጋል
    bot.infinity_polling(skip_pending=True, timeout=60)
    
