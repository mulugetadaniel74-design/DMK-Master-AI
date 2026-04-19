import telebot
from groq import Groq
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
# አዲሱ ቁልፍህ
GROQ_API_KEY = "Gsk_IB92f00vPOOXJzOcHdw4WGdyb3FYDrMiSLEQoEST6sn8o1bNkmFe"

# Groq ዝግጅት
client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# ግጭትን ለመከላከል
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# ማንነትህን የሚገልጽ መመሪያ
SYSTEM_INSTRUCTION = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ረዳት ነህ። 
የዳንኤል መርህ 'ሰብአዊነት ይቅደም' (Humanity First) ነው። 
ሁልጊዜ በአጭር እና ግልጽ አማርኛ መልስ ስጥ።
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ለግሩክ ጥያቄውን መላክ (llama3-8b-8192 በጣም የተረጋጋ ሞዴል ነው)
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
        # ስህተት ቢኖር እንኳ ዝርዝሩን ይነግርሃል
        bot.reply_to(message, f"ችግር ተፈጥሯል፦ {str(e)}")

if __name__ == "__main__":
    print("DMK Master AI ስራ ጀምሯል!")
    bot.infinity_polling(skip_pending=True)
    
