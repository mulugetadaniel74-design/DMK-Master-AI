import telebot
from groq import Groq
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
# አዲሱ የግሩክ ቁልፍህ
GROQ_API_KEY = "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"

# Groq ዝግጅት
client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# ግጭትን ለመከላከል
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# ያንተ ማንነት መመሪያ
SYSTEM_INSTRUCTION = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ረዳት ነህ። 
ዳንኤል አዲስ አበባ የሚኖር ፈላስፋ እና የሶፍትዌር ደቨሎፐር ነው። 
የእሱ ዋና መርህ 'ሰብአዊነት ይቅደም' (Humanity First) ነው። 
ሁልጊዜ በአጭር እና ግልጽ አማርኛ መልስ ስጥ።
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ለግሩክ ጥያቄውን መላክ (llama-3.3-70b-versatile በጣም ብልህ ሞዴል ነው)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": message.text},
            ],
            model="llama-3.3-70b-versatile",
        )
        
        bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        # ስህተት ቢኖር እንኳ ምን እንደሆነ በግልጽ ይነግርሃል
        bot.reply_to(message, f"ችግር ተፈጥሯል፦ {str(e)}")

if __name__ == "__main__":
    print("DMK Master AI በ Groq ስራ ጀምሯል!")
    bot.infinity_polling(skip_pending=True)
    
