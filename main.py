import telebot
from openai import OpenAI
import os
import time

BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
# ቁልፉን እዚህ ጋር በቀጥታ እናስገባው (ለመሞከር ያህል)
DEEPSEEK_KEY = "sk-47dd040f7da543df8ff2ff64cdc24d32"

client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
bot = telebot.TeleBot(BOT_TOKEN)

try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "አንተ የዳንኤል ረዳት ነህ።"},
                {"role": "user", "content": message.text},
            ],
            stream=False
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        # ስህተቱን በዝርዝር ለዳንኤል ይነግረዋል
        error_msg = f"ዝርዝር ስህተት፦ {str(e)}"
        print(error_msg)
        bot.reply_to(message, error_msg)

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
    
