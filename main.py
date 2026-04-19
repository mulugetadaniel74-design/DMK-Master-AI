import telebot
from groq import Groq
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
# ቁልፉን በደንብ አረጋግጠህ እዚህ አስገባ
GROQ_API_KEY = "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"

try:
    client = Groq(api_key=GROQ_API_KEY)
    bot = telebot.TeleBot(BOT_TOKEN)
except Exception as e:
    print(f"Setup Error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # 'llama3-8b-8192' ሞዴልን እንጠቀም (ይሄ በሁሉም አካውንት ይሰራል)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "አንተ የዳንኤል ረዳት ነህ።"},
                {"role": "user", "content": message.text},
            ],
            model="llama3-8b-8192",
        )
        
        bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        # ስህተቱ ከምን እንደመጣ በግልጽ ይነግርሃል
        error_text = str(e)
        if "401" in error_text:
            bot.reply_to(message, "ዳንኤል፣ ቁልፉ (API Key) አሁንም አልሰራም። እባክህ Groq ላይ አዲስ ቁልፍ አውጥተህ ሞክር።")
        else:
            bot.reply_to(message, f"ስህተት፦ {error_text}")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
    
