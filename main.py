import telebot
import google.generativeai as genai
import time

# --- መለያ ቁጥሮች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

genai.configure(api_key=GEMINI_API_KEY)
# እዚህ ጋር 'gemini-1.5-flash' መጠቀማችንን እናረጋግጥ
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# አሮጌ ግንኙነቶችን ለማጽዳት
bot.remove_webhook()
time.sleep(2)

SYSTEM_PROMPT = "አንተ የዳንኤል ሙሉጌታ ኩምሳ (DMK) ረዳት ነህ። መርህህ 'ሰብአዊነት ይቅደም' ነው። ሁልጊዜ በአጭር አማርኛ መልስ ስጥ። የማይገናኙ ቁጥሮችን አትጻፍ።"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ለጄሚኒ ትክክለኛውን ፎርማት መስጠት
        full_prompt = f"System Instruction: {SYSTEM_PROMPT}\nUser Question: {message.text}"
        response = model.generate_content(full_prompt)
        
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
    
