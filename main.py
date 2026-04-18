import telebot
import google.generativeai as genai
import time

# --- 1. መለያ ቁጥሮች (Token & Key) ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

# ጄሚኒን ማዘጋጀት
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# ግጭትን ለመከላከል የድሮ ግንኙነትን ማጽዳት
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# ቦቱ እንዲከተለው የምንፈልገው መመሪያ
SYSTEM_INSTRUCTION = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ዲጂታል ረዳት ነህ። 
ዳንኤል አዲስ አበባ የሚኖር ፈላስፋ እና የሶፍትዌር ደቨሎፐር ነው። 
የእሱ ዋና መርህ 'ሰብአዊነት ይቅደም' (Humanity First) ነው።
መመሪያ፦ 
- በደንብ በሚገባ አማርኛ መልስ ስጥ።
- አጭር፣ ግልጽ እና አጋዥ ሁን። 
- የማይገናኙ ቁጥሮችን ወይም ዝባዝንኬ አትጻፍ።
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ለጄሚኒ መመሪያውን እና የሰውየውን ጥያቄ አቀላቅሎ መላክ
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nተጠቃሚው እንዲህ ብሏል፦ {message.text}"
        response = model.generate_content(full_prompt)
        
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "ይቅርታ ዳንኤል፣ ትንሽ ችግር አጋጥሞኛል። ድጋሚ ሞክረኝ።")

if __name__ == "__main__":
    print("DMK Master AI (Gemini) ስራ ጀምሯል!")
    bot.infinity_polling(skip_pending=True)
    
