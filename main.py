import telebot
from groq import Groq
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
# እዚህ ጋር 'G' የነበረችውን ወደ 'g' ቀይሬያታለሁ
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# ግጭትን (Conflict) ለመፍታት የቀድሞ ግንኙነትን ማጽዳት
try:
    bot.remove_webhook()
    time.sleep(2)
except:
    pass

SYSTEM_INSTRUCTION = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ ረዳት ነህ። 
የዳንኤል መርህ 'ሰብአዊነት ይቅደም' ነው። 
ሁልጊዜ በአጭር አማርኛ ብቻ መልስ ስጥ።
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
        error_msg = str(e)
        print(f"Error: {error_msg}")
        # ስህተት ካለ ለዳንኤል እንዲነግረው
        bot.reply_to(message, f"ችግር ተፈጥሯል፦ {error_msg}")

if __name__ == "__main__":
    print("DMK Master AI ስራ ጀምሯል...")
    bot.infinity_polling(skip_pending=True)
    
