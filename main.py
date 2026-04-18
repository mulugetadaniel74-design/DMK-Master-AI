import telebot
import os
from google import generativeai as genai

# 1. መታወቂያዎች (Credentials)
BOT_TOKEN = "8308148615:AAHQdiHJaHarq5zaM2AiORKh26mh-F_dUTM"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

# 2. ጌሚኒን ማዘጋጀት
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # ደህንነቱ የተጠበቀ እንዲሆን Settings መጨመር
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
    bot = telebot.TeleBot(BOT_TOKEN)
    print("ቦቱ በተሳካ ሁኔታ ተነስቷል!")
except Exception as e:
    print(f"ማስጀመር አልተቻለም: {e}")

# 3. /start ሲባል የሚመጣ መልስ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "ሰላም ዳንኤል! የዲኤምኬ Master AI (DMK Master AI) ዝግጁ ነው። ማንኛውንም ጥያቄ ጠይቀኝ!"
    bot.reply_to(message, welcome_text)

# 4. ሰዎችን የሚያናግርበት ክፍል
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ለጌሚኒ ጥያቄውን መላክ
        response = model.generate_content(message.text)
        
        # መልሱ ባዶ ካልሆነ ለተጠቃሚው መላክ
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ ጌሚኒ መልስ ማመንጨት አልቻለም። ድጋሚ ሞክር።")
            
    except Exception as e:
        print(f"Error logic: {e}")
        # ለተጠቃሚው የሚሰጥ ግልጽ መልስ
        bot.reply_to(message, "አሁን ጥያቄህን መቀበል አልቻልኩም። ምናልባት ኢንተርኔት ወይም API Key ችግር ሊሆን ይችላል።")

# 5. ቦቱ ሳይቋረጥ እንዲሰራ
if __name__ == "__main__":
    bot.infinity_polling()
    
