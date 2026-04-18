import telebot
import google.generativeai as genai
import time

# ቁልፎች
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GEMINI_API_KEY = "AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# አሮጌ ግንኙነትን ማጽዳት
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# ዋናው መመሪያ (Instruction)
SYSTEM_INSTRUCTION = (
    "አንተ 'DMK Master AI' የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ረዳት ነህ። "
    "ዳንኤል አዲስ አበባ የሚኖር ፈላስፋ እና የሶፍትዌር ደቨሎፐር ነው። "
    "መርሁ 'ሰብአዊነት ይቅደም' (Humanity First) ነው። "
    "ጥያቄ ሲቀርብልህ ሁልጊዜ ዳንኤልን ወክለህ በአጭር አማርኛ መልስ ስጥ።"
)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        # መመሪያውን እና ጥያቄውን አቀላቅሎ መላክ
        full_query = f"{SYSTEM_INSTRUCTION}\n\nተጠቃሚው እንዲህ ብሏል፦ {message.text}"
        response = model.generate_content(full_query)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "እባክህ ድጋሚ ሞክር።")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
    
