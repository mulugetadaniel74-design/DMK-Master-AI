import telebot
import google.generativeai as genai
import time

# ቁልፎች
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

# Gemini Setup - ሞዴሉን 'gemini-pro' ብንለው ይበልጥ አስተማማኝ ነው
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

bot = telebot.TeleBot(BOT_TOKEN)

# አሮጌ ግንኙነትን ለማጽዳት
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# ማንነትህን የሚገልጽ መመሪያ
SYSTEM_INSTRUCTION = (
    "አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ረዳት ነህ። "
    "ዳንኤል አዲስ አበባ የሚኖር ፈላስፋ እና የሶፍትዌር ደቨሎፐር ነው። "
    "መርሁ 'ሰብአዊነት ይቅደም' (Humanity First) ነው። "
    "ጥያቄ ሲቀርብልህ ሁልጊዜ በአጭር አማርኛ መልስ ስጥ።"
)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        # ለጄሚኒ ጥያቄውን ስንልክ
        response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nተጠቃሚው እንዲህ ብሏል፦ {message.text}")
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ መልስ ማመንጨት አልቻልኩም።")
            
    except Exception as e:
        print(f"Error: {e}")
        # ስህተቱ ምን እንደሆነ ለዳንኤል በቴሌግራም ይነግረዋል
        bot.reply_to(message, f"ችግር ተፈጥሯል፡ {e}")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
    
