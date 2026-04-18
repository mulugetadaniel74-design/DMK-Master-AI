import telebot
import google.generativeai as genai
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

# ጄሚኒን ማዘጋጀት
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# ግጭትን ለመከላከል
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ጄሚኒን ማዘዝ
        instruction = "አንተ የዳንኤል ረዳት DMK Master AI ነህ። በአጭር አማርኛ መልስ ስጥ።"
        response = model.generate_content(f"{instruction}\n\nጥያቄ፡ {message.text}")
        
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "እባክህ ቆይተህ ድጋሚ ጠይቀኝ።")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
    
