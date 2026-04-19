import telebot
from openai import OpenAI
import time

# --- መለያዎች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
DEEPSEEK_API_KEY = "sk-47dd040f7da543df8ff2ff64cdc24d32"

# DeepSeek ዝግጅት
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
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
        
        # DeepSeek ጥሪ
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "አንተ የዳንኤል ረዳት DMK Master AI ነህ። በአጭር አማርኛ መልስ ስጥ።"},
                {"role": "user", "content": message.text},
            ],
            stream=False
        )
        
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        # ስህተቱ ምን እንደሆነ በቴሌግራም ይነግርሃል
        bot.reply_to(message, f"ስህተት፦ {str(e)}")

if __name__ == "__main__":
    print("ቦቱ ስራ ጀምሯል...")
    bot.infinity_polling(skip_pending=True)
    
