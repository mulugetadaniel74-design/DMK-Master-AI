import telebot
import google.generativeai as genai
import time

# --- መለያ ቁጥሮች ---
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

# የቦቱ መመሪያ
SYSTEM_PROMPT = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ዲጂታል ረዳት ነህ። 
ዳንኤል አዲስ አበባ የሚኖር ፈላስፋ እና የሶፍትዌር ደቨሎፐር ነው። 
መርሁ 'ሰብአዊነት ይቅደም' (Humanity First) ነው።
መመሪያ፦ 
- በማንኛውም ቋንቋ (በተለይ በአማርኛ) ግልጽ እና ትክክለኛ መልስ ስጥ። 
- አጭር እና አጋዥ ሁን። 
- ፈጽሞ ዝባዝንኬ ወይም የማይገናኙ ቁጥሮችን አትደርድር።
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ለጄሚኒ ጥያቄውን መላክ
        prompt = f"{SYSTEM_PROMPT}\n\nተጠቃሚው እንዲህ ብሏል፦ {message.text}"
        response = model.generate_content(prompt)
        
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "ይቅርታ፣ ትንሽ ችግር አጋጥሞኛል። እባክህ ቆይተህ ሞክር።")

if __name__ == "__main__":
    print("ቦቱ በጄሚኒ ሞተር ስራ ጀምሯል!")
    bot.infinity_polling(skip_pending=True)
    
