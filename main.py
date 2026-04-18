import telebot
import requests
from groq import Groq
import time

# ቁልፎች (እንዳይሳሳቱ አረጋግጥ)
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

# ቦቱ እንዲከተለው የምንፈልገው ዋናው መመሪያ
SYSTEM_PROMPT = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ዲጂታል ረዳት ነህ። 
የዳንኤል ዋና መርህ 'ሰብአዊነት ይቅደም' (Humanity First) ነው።
መመሪያዎች፦
1. ሁልጊዜ በአጭሩ፣ በግልጽ እና በታማኝነት መልስ ስጥ።
2. ተጠቃሚው በሚያናግርህ ቋንቋ (አማርኛ፣ ኦሮሚኛ ወይም እንግሊዝኛ) ተጠቀም።
3. ስለ ዳንኤል ከተጠየቅክ እሱ አርቲፊሻል ኢንተለጀንስ የሚያበለጽግ ፈላስፋ መሆኑን ንገር።
4. ዝም ብለህ የማይገናኙ ቃላትን ወይም ቁጥሮችን አትደርድር።
"""

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ለ AI ጥያቄውን መላክ
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7 # መልሱ የተረጋጋ እንዲሆን ያደርጋል
        )
        
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("ቦቱ በአዲስ መመሪያ ስራ ጀምሯል...")
    bot.infinity_polling(skip_pending=True)
    
