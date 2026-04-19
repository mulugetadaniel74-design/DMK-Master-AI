import telebot
import google.generativeai as genai
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

# የጄሚኒ ኮንፊገሬሽን - እዚህ ጋር ስሙን አስተካክለነዋል
genai.configure(api_key=GEMINI_API_KEY)
# 'gemini-1.5-flash-latest' በጣም አስተማማኙ ስም ነው
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = telebot.TeleBot(BOT_TOKEN)

# የድሮ ግንኙነትን ማጽዳት
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# የቦቱ መመሪያ
SYSTEM_INSTRUCTION = """
አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ ረዳት ነህ። 
የዳንኤል መርህ 'ሰብአዊነት ይቅደም' ነው። 
በአጭር አማርኛ ብቻ መልስ ስጥ።
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ለጄሚኒ ጥያቄውን መላክ
        response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nጥያቄ፡ {message.text}")
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ መልስ ማመንጨት አልቻልኩም።")
            
    except Exception as e:
        print(f"Error: {e}")
        # ስህተቱ ከቀጠለ ለዳንኤል ይነግረዋል
        bot.reply_to(message, f"የቴክኒክ ስህተት፡ {e}")

if __name__ == "__main__":
    print("DMK Master AI ስራ ጀምሯል...")
    bot.infinity_polling(skip_pending=True)
    
